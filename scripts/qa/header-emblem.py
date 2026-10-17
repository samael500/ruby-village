"""Real level-header art/readability check, saved progress fixtures only."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/ui-header';OUT.mkdir(parents=True,exist_ok=True)
ids=['gate','garden','well','bakery','stream','mill','post','forest'];results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h,dpr in [(1280,720,1),(844,390,2),(740,360,2)]:
  for index,sid in enumerate(ids):
   q=b.new_page(viewport={'width':w,'height':h},device_scale_factor=dpr);errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
   q.add_init_script(f"localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':ids[:index],'introSeen':ids})}))")
   q.goto(os.environ.get('RUBY_QA_URL','http://127.0.0.1:5286/ruby-village/'));q.locator('#continue-game').click();q.wait_for_load_state('networkidle')
   metrics=q.locator('h1').evaluate('''n=>{const r=n.getBoundingClientRect(),s=getComputedStyle(n),range=document.createRange();range.selectNodeContents(n);return {title:n.firstChild.textContent,box:[r.x,r.y,r.width,r.height],font:s.fontSize,borderImage:s.borderImageSource,textRects:[...range.getClientRects()].map(t=>[t.left,t.top,t.right,t.bottom]),scroll:n.scrollWidth,client:n.clientWidth}}''')
   assert 'ui/v8/level-header-v1.webp' in metrics['borderImage'];assert metrics['scroll']<=metrics['client']+1
   x,y,ww,hh=metrics['box'];assert x>=0 and y>=0 and x+ww<=w and y+hh<=h
   assert all(a>=x and bb>=y and c<=x+ww+1 and d<=y+hh+1 for a,bb,c,d in metrics['textRects'])
   for button in ['#scene-back','#scene-help','#settings-open']:
    r=q.locator(button).bounding_box()
    if r:assert min(x+ww,r['x']+r['width'])<=max(x,r['x']) or min(y+hh,r['y']+r['height'])<=max(y,r['y']), (sid,button,metrics,r)
   q.screenshot(path=str(OUT/f'{sid}-{w}-dpr{dpr}.jpg'),type='jpeg',quality=90);q.locator('.brand').screenshot(path=str(OUT/f'{sid}-title-{w}-dpr{dpr}.png'))
   assert not errors and not bad;results.append({'scene':sid,'viewport':[w,h],'dpr':dpr,'metrics':metrics,'pageErrors':errors,'httpErrors':bad});q.close()
 b.close()
(OUT/'report.json').write_text(json.dumps({'scope':'actual game UI; title remains live text, painted lossless raster nine-slice; progress fixtures only; no physical phone','checks':results},ensure_ascii=False,indent=2)+'\n');print('PASS24 actual headers:8scenes×3desktop/landscape/DPR configurations')
