import ast,json,time,base64,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parent
src=Path('/tmp/ruby-final-rc/docs/chapter-1-rc/qa/bridge-floor-v4-6f6fcbe/av-demo.py')
AUDIO=next(ast.literal_eval(n.value) for n in ast.parse(src.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='AUDIO' for t in n.targets))
states=json.loads((O.parent/'desktop/1280/states-live.json').read_text());reports=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for sid,reduced in [('gate',False),('stream',False),('mill',False),('gate',True)]:
  name=sid+('-reduced' if reduced else '');d=O/name;d.mkdir(exist_ok=True)
  earned=next(s['save'] for s in states if s['scene']==sid and s['label']=='reload-solved')
  c=b.new_context(viewport={'width':1280,'height':720},reduced_motion='no-preference',record_video_dir=str(d/'raw'),storage_state={'cookies':[],'origins':[{'origin':'http://127.0.0.1:5390','localStorage':[{'name':'ruby-village:chapter-1:v1','value':json.dumps(earned)}]}]})
  c.add_init_script(AUDIO);created=time.monotonic();q=c.new_page();errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
  q.goto('http://127.0.0.1:5390/ruby-village/');offset=time.monotonic()-created-q.evaluate('performance.now()')/1000;q.locator('#continue-game').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.wait_for_selector('#app[data-motion="ready"]')
  if reduced:
   q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#reduced-motion').check();q.locator('#settings-close').click()
  q.evaluate('window.samples=[];window.sampling=setInterval(()=>{let m=document.querySelector("#ruta-marker"),f=m?.querySelector("[data-motion-frame]");if(m&&f)samples.push({t:performance.now(),gait:m.dataset.gaitState,direction:m.dataset.direction,route:m.dataset.routeMs,rect:f.getAttribute("viewBox"),x:f.getAttribute("x"),y:f.getAttribute("y")})},25)')
  q.locator('#check').click();pause=None
  if sid=='gate' and not reduced:
   q.wait_for_function('document.querySelector("#ruta-marker")?.dataset.gaitState==="walk"');q.locator('#settings-open').click();q.wait_for_timeout(100)
   snap=lambda:q.locator('#ruta-marker').get_attribute('data-route-ms')
   before=snap();q.wait_for_timeout(500);after=snap();assert before==after,(before,after);pause={'before':before,'after':after,'durationMs':500};q.screenshot(path=str(d/'paused.jpg'));q.locator('#pause-continue').click()
  q.wait_for_selector('#story[open]',timeout=90000)
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.wait_for_selector('#completion-panel[open]');q.screenshot(path=str(d/'victory.jpg'));q.wait_for_timeout(700)
  samples=q.evaluate('clearInterval(sampling);samples');(d/'samples.json').write_text(json.dumps(samples))
  info=q.evaluate('qaContexts.map(c=>({startedAt:c.startedAt,stateEvents:c.stateEvents}))');assert len(info)==1,info
  encoded=q.evaluate('''async()=>{let c=qaContexts[0];await new Promise(r=>{c.recorder.onstop=r;c.recorder.stop()});return await new Promise(r=>{let f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(new Blob(c.chunks,{type:'audio/webm'}))})}''');(d/'audio.webm').write_bytes(base64.b64decode(encoded.split(',')[1]));v=q.video;c.close();v.save_as(str(d/'silent.webm'))
  delay=max(0,offset+info[0]['startedAt']/1000)
  subprocess.run(['ffmpeg','-y','-i',str(d/'silent.webm'),'-itsoffset',str(delay),'-i',str(d/'audio.webm'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','28','-threads','2','-c:a','aac',str(d/'actual-audio.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  assert not errors and not bad,(errors,bad)
  reports.append({'scene':sid,'reduced':reduced,'earnedSave':'desktop reload-solved actual UI','pause':pause,'errors':errors,'httpErrors':bad,'audioContexts':info,'estimatedAudioDelaySec':delay,'rectCount':len(set(s['rect'] for s in samples)),'gaits':sorted(set(s['gait'] for s in samples)),'directions':sorted(set(s['direction'] for s in samples))});(O/'report.json').write_text(json.dumps(reports,indent=2));print('PASS',name,flush=True)
 b.close()
