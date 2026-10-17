"""Candidate layer in the actual map; preserves the accepted background and nodes."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parents[2]/'docs/chapter-1-rc/evidence/map-trails'
out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();checks=[]
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
  q.goto('http://127.0.0.1:5181/ruby-village/');q.locator('#choose-level').click();q.locator('#map-background').evaluate('(i)=>i.decode()')
  for state,ids in [('new',[]),('partial',['garden','well']),('complete',['garden','well','bakery','stream','mill','post','forest'])]:
   q.evaluate('''async ids=>{const {renderMapTrails}=await import('/ruby-village/src/map-trails.ts');renderMapTrails(document.querySelector('#map-roads'),new Set(ids));}''',ids)
   q.wait_for_load_state('networkidle')
   assert q.locator('[data-map-trail]').count()==7
   assert q.locator('[data-map-trail][data-complete="true"]').count()==len(ids)
   assert q.locator('#map-roads path[stroke-width="5"]').count()==0
   assert q.locator('.level-card').count()==8
   q.screenshot(path=str(out/f'{state}-{w}x{h}.jpg'),type='jpeg',quality=90)
   checks.append({'viewport':[w,h],'state':state,'restored':ids,'errors':errors.copy(),'scope':'actual map, candidate module injection; progress unchanged'})
  assert not errors; q.close()
 b.close();(out/'report.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS six actual map captures, seven landscape trails, progress layer states')
