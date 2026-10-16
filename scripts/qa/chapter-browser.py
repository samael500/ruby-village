"""Real input smoke/playthrough; browser emulation is not a physical phone test."""
import json, os, base64, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/chapter-1-rc/evidence'; OUT.mkdir(parents=True,exist_ok=True)
URL=os.environ.get('RUBY_QA_URL','http://127.0.0.1:5178/ruby-village/')

def dismiss(page):
 for _ in range(60):
  if page.locator('#story[open]').count(): page.locator('#story-action').click()
  elif page.locator('#completion-panel[open]').count():return
  else:return
 raise AssertionError('Dialog never ended')

with sync_playwright() as p:
 browser=p.chromium.launch()
 context=browser.new_context(viewport={'width':1280,'height':720},record_video_dir=str(OUT/'video'),record_video_size={'width':1280,'height':720})
 context.add_init_script("""
 const Native=window.AudioContext, connect=AudioNode.prototype.connect;
 AudioNode.prototype.connect=function(destination,...args){
  const result=connect.call(this,destination,...args);
  if(destination===this.context.destination&&this.context.captureNode)connect.call(this,this.context.captureNode);
  return result;
 };
 window.AudioContext=new Proxy(Native,{construct(Target,args){
  const context=new Target(...args);context.captureNode=context.createMediaStreamDestination();
  const chunks=[],recorder=new MediaRecorder(context.captureNode.stream,{mimeType:'audio/webm;codecs=opus'});
  recorder.ondataavailable=e=>chunks.push(e.data);recorder.start();
  window.audioCapture={recorder,chunks,startedAt:performance.now()};return context;
 }});
 """)
 page=context.new_page(); errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.locator('#continue-game').click()
 frames=[]
 for i in range(6):
  page.locator('#prologue-panel[open]').wait_for()
  page.screenshot(path=str(OUT/f'prologue-{i+1}.png'))
  frames.append(page.locator('#prologue-text').inner_text())
  page.locator('#prologue-next').click()
 dismiss(page)
 levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())
 for index,level in enumerate(levels):
  dismiss(page)
  for ident,placement in level['solution'].items():
   page.locator(f'#tray [data-piece="{ident}"]').click()
   for _ in range(placement['turns']):page.locator('#right').click()
   q,r=placement['anchor']['q'],placement['anchor']['r']
   page.locator(f'[data-cell="{q},{r}"] polygon').first.click(force=True)
   page.locator('#place').click()
   assert page.locator(f'[data-owner="{ident}"]').count()>0,(level['id'],ident)
  page.screenshot(path=str(OUT/f"{level['id']}-solved.png"))
  page.locator('#check').click()
  page.wait_for_function("document.querySelector('#story[open]') || document.querySelector('#completion-panel[open]')",timeout=10000)
  dismiss(page)
  page.locator('#completion-panel[open]').wait_for()
  page.screenshot(path=str(OUT/f"{level['id']}-complete.png"))
  if index<7:page.locator('#next-level').click()
  else:page.locator('#completion-map').click()
 assert not errors,errors
 report={'url':URL,'input':'mouse clicks on tray, rotate, cells, placement and check; no layout injection','levels':len(levels),'prologueFrames':frames,'pageErrors':errors,'physicalPhone':'not-run','familyPlaytest':'not-run'}
 (OUT/'browser-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 if page.evaluate('!!window.audioCapture'):
  encoded=page.evaluate("""async()=>{const c=window.audioCapture;await new Promise(r=>{c.recorder.onstop=r;c.recorder.stop()});return await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(new Blob(c.chunks,{type:'audio/webm'}))})}""")
  (OUT/'game-audio.webm').write_bytes(base64.b64decode(encoded.split(',')[1]))
 video=page.video.path()
 context.close();browser.close()
 if (OUT/'game-audio.webm').exists():
  subprocess.run(['ffmpeg','-y','-i',str(video),'-i',str(OUT/'game-audio.webm'),'-c:v','libx264','-preset','veryfast','-threads','2','-crf','28','-c:a','aac','-shortest',str(OUT/'chapter-playthrough-with-audio.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 print(json.dumps(report,ensure_ascii=False))
