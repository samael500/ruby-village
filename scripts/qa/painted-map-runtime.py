"""Real production map with saved-progress fixtures; no renderer/module injection."""
import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/evidence/painted-map-runtime';out.mkdir(parents=True,exist_ok=True);checks=[]
ids=['gate','garden','well','bakery','stream','mill','post','forest']
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(1920,1080),(844,390),(740,360),(1024,768)]:
  for state,completed,patches in [('new',[],0),('partial',ids[:2],1),('complete',ids,7)]:
   q=b.new_page(viewport={'width':w,'height':h});errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
   if completed:q.add_init_script(f"localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'layoutVersion':1,'completed':completed,'introSeen':completed})}))")
   q.goto(os.environ.get('RUBY_QA_URL','http://127.0.0.1:5286/ruby-village/'));q.locator('#choose-level').click();q.locator('#map-background').evaluate('(i)=>i.decode()');q.locator('#map-wide').evaluate('(i)=>i.decode()');q.wait_for_load_state('networkidle')
   assert q.locator('#map-background').get_attribute('src').endswith('chapter-map-v2/map-base.webp');assert q.locator('[data-painted-progress]').count()==patches
   assert q.locator('#map-roads path,#map-roads polygon,#map-roads ellipse').count()==0
   coverage=q.evaluate('''()=>{const a=document.querySelector('.map-landscape').getBoundingClientRect(),w=document.querySelector('#map-wide').getBoundingClientRect(),c=document.querySelector('#map-world').getBoundingClientRect(),fit=c.width/1000;return {covers:w.left<=a.left+2&&w.top<=a.top+2&&w.right>=a.right-2&&w.bottom>=a.bottom-2,coreOffsetError:Math.max(Math.abs(c.left-w.left-200*fit),Math.abs(c.top-w.top-200*fit)),natural:[document.querySelector('#map-wide').naturalWidth,document.querySelector('#map-wide').naturalHeight]}}''');assert coverage['covers'] and coverage['coreOffsetError']<.1 and coverage['natural']==[1400,800],coverage
   targets=q.locator('.level-card').evaluate_all('(ns)=>ns.map(n=>{const r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,disabled:n.disabled}})');labels=q.locator('.map-label').evaluate_all('(ns)=>ns.map(n=>{const r=n.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})');assert len(targets)==8 and len(labels)==8
   assert all(t['w']>=44 and t['h']>=44 and t['x']>=0 and t['y']>=0 and t['x']+t['w']<=w+1 and t['y']+t['h']<=h+1 for t in targets)
   assert all(x>=0 and y>=0 and x+ww<=w+1 and y+hh<=h+1 for x,y,ww,hh in labels)
   assert sum(not t['disabled'] for t in targets)==min(8,len(completed)+1)
   q.screenshot(path=str(out/f'{state}-{w}x{h}.jpg'),type='jpeg',quality=88);assert not errors and not bad
   checks.append({'viewport':[w,h],'state':state,'savedProgressFixture':completed,'paintedProgressImages':patches,'vectorRoadShapes':0,'all8Targets44pxAndLabelsInside':True,'unlocked':sum(not t['disabled'] for t in targets),'pageErrors':errors,'httpErrors':bad,'wideCoverageAndRegistration':coverage,'scope':'native painted map + garden paving repair + registered painted landscape; no art injection'});q.close()
 b.close()
(out/'report.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS15 actual map states across5 viewports; native painted paving, progress, labels and targets')
