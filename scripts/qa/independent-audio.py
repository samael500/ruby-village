"""Observe native WebAudio lifecycle in production; no exported game API injection."""
import json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/final-smoke';OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1280,'height':720});c.add_init_script('''window.observedAudio={contexts:[],active:0,starts:0};const Native=window.AudioContext;window.AudioContext=new Proxy(Native,{construct(T,a){const c=new T(...a);window.observedAudio.contexts.push(c);const create=c.createBufferSource.bind(c);c.createBufferSource=()=>{const s=create(),start=s.start.bind(s),stop=s.stop.bind(s);let active=false;s.addEventListener('ended',()=>{if(active){active=false;window.observedAudio.active--}});s.start=(...a)=>{start(...a);active=true;window.observedAudio.active++;window.observedAudio.starts++};s.stop=(...a)=>{stop(...a);if(active){active=false;window.observedAudio.active--}};return s};return c}});''');q=c.new_page();errors=[];requests=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:requests.append({'url':r.url,'status':r.status}) if '/audio/' in r.url else None);q.goto('http://127.0.0.1:5183/ruby-village/');assert q.evaluate('observedAudio.contexts.length')==0;q.locator('#continue-game').click();q.wait_for_timeout(1200)
 prologue=[]
 for i in range(6):
  q.screenshot(path=str(OUT/f'prologue-{i+1}.jpg'),type='jpeg',quality=80);prologue.append(q.locator('#prologue-text').inner_text());q.locator('#prologue-next').click()
 while q.locator('#story[open]').count():q.locator('#story-action').click()
 q.wait_for_timeout(1200);assert q.evaluate('observedAudio.contexts.length')==1;running=q.evaluate('observedAudio.active');assert running>=2
 q.locator('#settings-open').click();q.wait_for_timeout(100);paused=q.evaluate('observedAudio.active');assert paused==0;q.locator('#pause-continue').click();q.wait_for_timeout(900);resumed=q.evaluate('observedAudio.active');assert resumed>=2
 q.set_viewport_size({'width':390,'height':844});q.wait_for_timeout(100);portrait=q.evaluate('observedAudio.active');assert portrait==0;q.set_viewport_size({'width':1280,'height':720});q.wait_for_timeout(900);assert q.evaluate('observedAudio.active')>=2
 # CDP background state varies in headless; explicitly untested rather than simulated document.hidden.
 assert not errors;assert not [r for r in requests if r['status']>=400]
 q.screenshot(path=str(OUT/'gate-approved-ruta.jpg'),type='jpeg',quality=85)
 report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'autoplayNoContextBeforeGesture':True,'contexts':1,'activeRunning':running,'activePaused':paused,'activeResumed':resumed,'activePortrait':portrait,'responses':requests,'pageErrors':errors,'prologueFrames':len(prologue),'backgroundTab':'not-run','humanListening':'not-run'};(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False));b.close()
