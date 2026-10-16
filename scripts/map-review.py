"""Real browser evidence for isolated candidate map, not production acceptance."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'docs/chapter-1-rc/ui-map';url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5191/ruby-village/scripts/map-review.html'
checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 for w,h in [(1440,900),(844,390),(740,360)]:
  page=browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url)
  page.locator('.map>img').evaluate('(image)=>image.decode()')
  for state in ['new','partial','complete']:
   page.click(f'[data-state={state}]');assert page.locator('.node').count()==8
   assert page.locator('.node:enabled').count()=={'new':1,'partial':5,'complete':8}[state]
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight')
   for label in page.locator('.label').all():
    box=label.bounding_box();assert box and box['x']>=0 and box['y']>=0 and box['x']+box['width']<=w and box['y']+box['height']<=h,(w,h,state,box)
   page.screenshot(path=str(out/f'map-{state}-{w}x{h}.jpg'),quality=88)
  page.click('[data-state=new]');page.locator('.node:enabled').first.focus();page.keyboard.press('Enter');assert 'Выбрано' in page.locator('.status').text_content();assert not errors,errors
  checks.append({'viewport':[w,h],'states':['new','partial','complete'],'labelBounds':True,'nodeCount':8,'keyboardActivation':True,'pageErrors':errors});page.close()
 (out/'browser-review.json').write_text(json.dumps({'scope':'isolated real browser review of unaccepted visual candidate, not production','browser':browser.version,'checks':checks},indent=2)+'\n');browser.close()
print('Map review browser states/bounds/keyboard pass')
