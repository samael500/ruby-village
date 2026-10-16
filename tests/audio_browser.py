"""Real Chromium/WebAudio module smoke. Isolated harness, not production gameplay acceptance."""
import base64,json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/chapter-1-rc/audio-effects';OUT.mkdir(parents=True,exist_ok=True)
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5190/ruby-village/'
with sync_playwright() as p:
 browser=p.chromium.launch();page=browser.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/assets/audio/music/manifest.json',lambda route:route.fulfill(json={'version':1,'cues':{'water':{'file':'../sfx/water.ogg','gain':.5,'loop':True}}}));page.goto(URL)
 page.evaluate('''async()=>{
  const Native=window.AudioContext;
  window.AudioContext=class extends Native {constructor(){super();window.startOffsets=[];const create=this.createBufferSource.bind(this);this.createBufferSource=()=>{const source=create(),start=source.start.bind(source);source.start=(when=0,offset=0)=>{startOffsets.push(offset);start(when,offset);};return source;};const capture=this.createMediaStreamDestination();const gain=this.createGain.bind(this);this.createGain=()=>{const node=gain(),connect=node.connect.bind(node);node.connect=(target,...args)=>{if(target===this.destination)connect(capture);return connect(target,...args);};return node;};window.chunks=[];window.recorder=new MediaRecorder(capture.stream);recorder.ondataavailable=e=>chunks.push(e.data);recorder.start();}};
  const {createGameAudio}=await import('./src/audio.ts');window.audio=createGameAudio('/ruby-village/',localStorage);
  document.body.innerHTML='<button id="unlock">Enable audio smoke</button>';
  document.querySelector('button').onclick=async()=>{await audio.unlock();audio.setScene('stream');audio.setMusic('water');await audio.play('tile-place');};
 }''')
 assert page.evaluate('audio.metrics.contextState')=='not-created';page.click('#unlock');page.wait_for_timeout(600)
 assert page.evaluate('audio.metrics.unlocked');assert page.evaluate('audio.metrics.loadErrors')==0
 page.evaluate("audio.play('path-connected')");page.wait_for_timeout(1200)
 for scene in ['gate','garden','well','bakery','stream','mill','post','forest']:
  page.evaluate('(scene)=>audio.setScene(scene)',scene);page.wait_for_timeout(100)
 page.wait_for_timeout(800);assert page.evaluate('audio.metrics.activeVoices')<=2
 page.evaluate('audio.setPaused(true)');assert page.evaluate('audio.unlock().then(value=>!value)');assert page.evaluate('audio.metrics.activeVoices')==0
 page.evaluate('audio.setPaused(false)');page.wait_for_timeout(300);assert page.evaluate('startOffsets.slice(-2).every(offset=>offset>0)')
 page.evaluate("audio.setPreferences({muted:true,music:.2,sfx:.4})")
 assert json.loads(page.evaluate("localStorage.getItem('ruby-village:audio:v1')"))=={'muted':True,'music':.2,'sfx':.4}
 page.evaluate('audio.setScene(null);audio.setMusic(null)');page.wait_for_timeout(500);assert page.evaluate('audio.metrics.activeVoices')==0
 metrics=page.evaluate('audio.metrics');assert metrics['loadErrors']==0
 data=page.evaluate('''async()=>{await new Promise(resolve=>{recorder.onstop=resolve;recorder.stop();});const bytes=new Uint8Array(await new Blob(chunks).arrayBuffer());let text='';for(const b of bytes)text+=String.fromCharCode(b);return btoa(text);}''')
 (OUT/'chromium-module-smoke.webm').write_bytes(base64.b64decode(data));page.evaluate('audio.dispose()');assert not errors,errors
 (OUT/'browser-smoke.json').write_text(json.dumps({'scope':'isolated real WebAudio module, not gameplay','browser':browser.version,'metrics':metrics,'pageErrors':errors,'checks':['gesture gate','real Ogg decode','all eight scene changes','bounded loops','pause/resume','preference persistence','null scene stop','recording MediaStreamDestination','music/ambience resume offsets (water fixture cue)','unlock does not bypass pause']},indent=2)+'\n');browser.close()
 print('Chromium audio module smoke pass; actual WebAudio capture saved (not gameplay)')
