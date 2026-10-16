from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path('/home/mskorokhod/life/ruby-village/docs/chapter-1-rc/evidence/map-runtime');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();checks=[]
 for w,h in [(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080)]:
  page=b.new_page(viewport={'width':w,'height':h});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://127.0.0.1:5180/ruby-village/');page.locator('#choose-level').click();page.locator('#map-background').evaluate('(image)=>image.decode()');page.screenshot(path=str(out/f'map-new-{w}x{h}.jpg'),type='jpeg',quality=85)
  boxes=page.locator('.level-card, .map-label').evaluate_all('(nodes)=>nodes.map(n=>{const r=n.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})');assert len(boxes)==16
  assert all(x>=0 and y>=0 and x+ww<=w+1 and y+hh<=h+1  for x,y,ww,hh in boxes),(w,h,boxes)
  assert page.locator('.level-card:enabled').count()==1
  assert not errors;checks.append({'viewport':[w,h],'eightTargetsInside':True,'labelsInside':True,'targetsAtLeast44px':page.locator('.level-card').evaluate_all('(ns)=>ns.every(n=>{const r=n.getBoundingClientRect();return r.width>=44&&r.height>=44})'),'errors':errors});page.close()
 (out/'report.json').write_text(json.dumps(checks,indent=2)+'\n');b.close();print(checks)
