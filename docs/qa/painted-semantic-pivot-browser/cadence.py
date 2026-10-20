from pathlib import Path
from playwright.sync_api import sync_playwright
import json,statistics
O=Path(__file__).resolve().parent;out={}
with sync_playwright()as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1280,'height':800});page.goto('http://localhost:5322/semantic-pivot-trial/review.html');page.wait_for_function('window.reviewState?.ready')
 for mode in ['baseline','candidate']:
  page.locator('#mode').select_option(mode);rows=page.evaluate("""()=>new Promise(resolve=>{const rows=[];const start=performance.now();function tick(t){const s=reviewState;if(rows.at(-1)?.index!==s.frame)rows.push({index:s.frame,t,playing:s.playing});if(t-start<4200)requestAnimationFrame(tick);else resolve(rows)}requestAnimationFrame(tick)})""");dt=[y['t']-x['t']for x,y in zip(rows,rows[1:])];skips=[{'from':x['index'],'to':y['index'],'dt':y['t']-x['t']}for x,y in zip(rows,rows[1:])if(y['index']-x['index'])%48!=1];out[mode]={'samples':rows,'intervalCount':len(dt),'minMs':min(dt),'maxMs':max(dt),'medianMs':statistics.median(dt),'meanMs':statistics.mean(dt),'skippedPhases':skips,'scope':'uninterrupted4.2second desktoprequestAnimationFramereadback, nointeractions/screenshots/recorderduringwindow'}
 b.close()
(O/'cadence.json').write_text(json.dumps(out,indent=2)+'\n');print({k:{q:v[q]for q in ['minMs','maxMs','meanMs','skippedPhases']}for k,v in out.items()})
