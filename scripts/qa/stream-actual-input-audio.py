# Coordinator verification derived from the independent14b1f6f real-input harness.
# Author rerun, not a substitute for independent adaptive-bank review.
# Record one uninterrupted document so real WebAudio survives the whole clip.
import json,base64,time,subprocess,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/road/stream-pilot/actual-input-audio-afcb676';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'art/chapter-1-v9/layers/water/stream-pilot/manifest.json').read_text());geometry=json.loads((ROOT/manifest['geometry']).read_text());solution=[p for p in manifest['solution'] if p['placement']];reports=[]
AUDIO='''const Native=window.AudioContext,connect=AudioNode.prototype.connect;window.qaContexts=[];AudioNode.prototype.connect=function(destination,...args){const r=connect.call(this,destination,...args);if(destination===this.context.destination&&this.context.captureNode)connect.call(this,this.context.captureNode);return r};window.AudioContext=new Proxy(Native,{construct(Target,args){let c=new Target(...args);c.captureNode=c.createMediaStreamDestination();let chunks=[],recorder=new MediaRecorder(c.captureNode.stream,{mimeType:'audio/webm;codecs=opus'});recorder.ondataavailable=e=>chunks.push(e.data);recorder.start();window.qaContexts.push({recorder,chunks,startedAt:performance.now()});return c}});'''
with sync_playwright() as p:
 b=p.chromium.launch()
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  prefix='touch844' if touch else 'mouse1280';c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,reduced_motion='no-preference',record_video_dir=str(OUT/'raw-video'),record_video_size={'width':w,'height':h});c.add_init_script(AUDIO);created=time.monotonic();q=c.new_page();errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url) if r.status>=400 else None);client=c.new_cdp_session(q)
  def center(loc):
   r=loc.bounding_box();assert r;return {'x':r['x']+r['width']/2,'y':r['y']+r['height']/2}
  def tap(loc):
   z=center(loc)
   if touch:client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{**z,'id':1}]});client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:q.mouse.click(**z)
  def cell(a):return q.locator(f'#board [data-cell="{a["q"]},{a["r"]}"] > polygon.cell')
  def saved():return q.evaluate("localStorage.getItem('ruby-village:chapter-1:v1')")
  q.goto('http://127.0.0.1:5306/ruby-village/');navigationOffset=time.monotonic()-created-q.evaluate('performance.now()')/1000;tap(q.locator('#continue-game'))
  while q.locator('#story[open]').count():tap(q.locator('#story-action'))
  q.wait_for_load_state('networkidle');q.wait_for_selector('#app[data-motion="ready"]');states=[]
  def check(label):
   state=q.evaluate('''()=>({owners:[...document.querySelectorAll('#board [data-cell]')].filter(n=>n.dataset.owner).map(n=>({cell:n.dataset.cell,id:n.dataset.owner})),road:document.querySelector('#board [data-connected-road]')?.dataset.confirmedRoadCells,clip:[...document.querySelectorAll('#board [data-connected-road] clipPath polygon')].map(n=>n.getAttribute('points')),outline:[...document.querySelectorAll('#board [data-instance-outlines]')].map(n=>n.getAttribute('d')),edge:document.querySelector('#board [data-road-outer-edge]')?.getAttribute('d'),bridge:document.querySelector('#board [data-painted-bridge]')?.outerHTML})''')
   expect={n['cell'] for n in state['owners'] if n['id']!='bridge'}|{'1,3','9,1'};actual=set(state['road'].split(';'));assert actual==expect,(label,expect,actual);assert len(state['clip'])==len(expect)
   # Each clip polygon equals the exact input polygon of its confirmed cell;
   # labels alone cannot falsely certify a different rendered clip.
   board=q.locator('#board [data-cell]').evaluate_all('ns=>Object.fromEntries(ns.map(n=>[n.dataset.cell,n.querySelector("polygon.cell").getAttribute("points")]))')
   def norm(s):return sorted((round(float(a),5),round(float(b),5)) for a,b in (pair.split(',') for pair in s.split()))
   assert sorted(map(norm,state['clip']))==sorted(norm(board[k]) for k in expect)
   state['label']=label;state['expectedRoad']=sorted(expect);states.append(state);return state
  check('empty-fixed-endpoints')
  for piece in solution:
   tap(q.locator(f'#tray [data-piece="{piece["id"]}"]'))
   for _ in range(piece['placement']['turns']):tap(q.locator('#right'))
   tap(cell(piece['placement']['anchor']));tap(q.locator('#place'));check('placed-'+piece['id'])
  baseline=check('solved');baselineSave=saved();q.screenshot(path=str(OUT/f'{prefix}-solved-technical.jpg'))
  # Runtime itself now renders clean painted water; no style hiding.
  q.screenshot(path=str(OUT/f'{prefix}-solved-clean.jpg'))
  water=[v for v in geometry['cells'] if v['terrain']=='water']
  q.evaluate('''cells=>{const ns='http://www.w3.org/2000/svg',svg=document.querySelector('#board'),g=document.createElementNS(ns,'g');g.id='qa-water-overlay';g.setAttribute('transform',document.querySelector('[data-painted-world]').getAttribute('transform'));g.setAttribute('pointer-events','none');for(const cell of cells){let p=document.createElementNS(ns,'polygon');p.setAttribute('points',cell.polygon.map(p=>p.x+','+p.y).join(' '));p.setAttribute('fill','#19d5ff33');p.setAttribute('stroke','#ff247a');p.setAttribute('stroke-width','2');g.append(p)}svg.append(g)}''',water)
  q.screenshot(path=str(OUT/f'{prefix}-solved-water-overlay.jpg'));q.locator('#qa-water-overlay').evaluate('n=>n.remove()')
  # Whole-instance select, preview rotation and invalid move must leave surface/save.
  chosen=next(v for v in solution if v['id']=='stream-v6-a');tap(cell(chosen['placement']['anchor']));selected=check('reselect-whole');assert selected['outline'] and len([o for o in selected['owners'] if o['id']==chosen['id']])==3
  tap(q.locator('#right'));rotated=check('pending-rotation');assert rotated['road']==baseline['road'] and saved()==baselineSave
  tap(cell({'q':0,'r':0}));assert q.locator('#placement-preview[data-preview="invalid"]').count();invalid=check('pending-invalid');assert invalid['road']==baseline['road'] and saved()==baselineSave;q.screenshot(path=str(OUT/f'{prefix}-invalid-preview.jpg'));tap(q.locator('#other'))
  # Move confirmed composite through real UI to valid free ground, undo it.
  tap(cell(chosen['placement']['anchor']));
  for _ in range(4):tap(q.locator('#right'))
  tap(cell({'q':0,'r':3}));tap(q.locator('#place'));moved=check('moved-composite');assert moved['road']!=baseline['road'];tap(q.locator('#undo'));assert check('undo-move')['road']==baseline['road']
  tap(cell(chosen['placement']['anchor']));tap(q.locator('#return'));returned=check('returned-composite');assert len([o for o in returned['owners'] if o['id']==chosen['id']])==0;tap(q.locator('#undo'));assert check('undo-return')['road']==baseline['road']
  tap(q.locator('#check'));q.wait_for_selector('#story[open]',timeout=90000)
  while q.locator('#story[open]').count():tap(q.locator('#story-action'))
  q.wait_for_selector('#completion-panel[open]');q.screenshot(path=str(OUT/f'{prefix}-result.jpg'))
  assert not errors and not bad
  audioInfo=q.evaluate('window.qaContexts.map(c=>({startedAt:c.startedAt,state:c.recorder.state}))');assert len(audioInfo)==1,audioInfo
  encoded=q.evaluate('''async()=>{let c=window.qaContexts[0];await new Promise(r=>{c.recorder.onstop=r;c.recorder.stop()});return await new Promise(r=>{let f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(new Blob(c.chunks,{type:'audio/webm'}))})}''');audio=OUT/f'{prefix}-actual-audio.webm';audio.write_bytes(base64.b64decode(encoded.split(',')[1]));video=q.video;c.close();videoPath=OUT/f'{prefix}-actual-input-silent.webm';video.save_as(str(videoPath));delay=max(0,navigationOffset+audioInfo[0]['startedAt']/1000)
  subprocess.run(['ffmpeg','-y','-i',str(videoPath),'-itsoffset',str(delay),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','28','-threads','2','-c:a','aac',str(OUT/f'{prefix}-actual-input-audio.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  reports.append({'input':'native CDP touch' if touch else 'mouse','viewport':[w,h],'states':states,'pageErrors':errors,'httpErrors':bad,'audioContexts':audioInfo,'estimatedAudioDelaySec':delay,'audioAlignment':'estimated from page creation monotonic / navigation performance.now; MediaRecorder start. Not hardware-sync calibrated. Original streams retained.','physicalPhone':'NOT RUN'})
 b.close()
(OUT/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n');print('PASS2 actual accepted stream solves,road union/clip/preview/select/move/return/undo,actual browseraudio captured')
