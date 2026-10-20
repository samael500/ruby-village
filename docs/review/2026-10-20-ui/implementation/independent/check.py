import json
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path('/tmp/ui79-independent'); results=[]
levels=['gate','garden','well','bakery','stream','mill','post','forest']
with sync_playwright() as p:
 b=p.chromium.launch(headless=True)
 for w,h in [(1440,900),(844,390),(740,360)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000,device_scale_factor=1)
  pg=c.new_page(); errors=[];pg.on('pageerror',lambda e:errors.append(str(e)))
  pg.goto('http://localhost:5392/ruby-village/');pg.evaluate('(v)=>localStorage.setItem("ruby-village:chapter-1:v1",JSON.stringify({version:2,completed:v,introSeen:v}))',levels);pg.reload();pg.locator('#choose-level').click()
  def press(s):
   if w<1000: pg.locator(s).tap()
   else:pg.locator(s).click()
  for i,l in enumerate(levels):
   press('[data-level="'+l+'"]');pg.wait_for_timeout(250)
   if pg.locator('#story[open]').count():press('#story-skip')
   pg.wait_for_timeout(150)
   info=pg.locator('h1 small').evaluate('(e)=>({text:e.textContent,rect:e.getBoundingClientRect().toJSON(),color:getComputedStyle(e).color,bg:getComputedStyle(e).backgroundColor,scroll:e.scrollWidth,width:e.clientWidth})')
   assert info['text']==f'Уровень {i+1} из 8',info
   assert info['rect']['x']>=0 and info['rect']['right']<=w and info['rect']['bottom']<=h,info
   assert info['scroll']<=info['width']+1,info
   assert pg.locator('#scene-event svg[data-painted-miniature="'+l+'"]').is_visible()
   pg.screenshot(path=str(out/f'{w}-{l}.png'))
   results.append({'viewport':[w,h],'level':l,'progress':info})
   press('#scene-back')
  press('#map-more');assert pg.locator('#sandbox-open').count()==0
  assert pg.locator('#chapter-ending').is_visible() and pg.locator('#letter-open').is_visible()
  pg.screenshot(path=str(out/f'{w}-adventure.png'))
  press('#letter-open');assert 'приглашение' in pg.locator('#story-title').inner_text().lower();press('#story-skip')
  press('#map-more');press('#chapter-ending');assert pg.locator('#story[open]').count()==1;press('#story-skip')
  pg.reload();assert '8 из 8' in pg.locator('#menu-progress').inner_text()
  results.append({'viewport':[w,h],'dialogs':'letter+ending real input PASS','reload':'8/8 retained','pageErrors':errors})
  c.close()
 b.close()
(out/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('PASS',len(results),'cases')
