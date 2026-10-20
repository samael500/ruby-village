import asyncio,json,sys,pathlib
from playwright.async_api import async_playwright
BASE=sys.argv[1];OUT=pathlib.Path(sys.argv[2]);AFTER='--after' in sys.argv;OUT.mkdir(parents=True,exist_ok=True)
IDS=['gate','garden','well','bakery','stream','mill','post','forest']
async def run():
 report=[]
 async with async_playwright() as p:
  b=await p.chromium.launch()
  for w,h in [(1280,720),(844,390),(740,360)]:
   c=await b.new_context(viewport={'width':w,'height':h},has_touch=w<1000,is_mobile=w<1000,device_scale_factor=1)
   page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   await page.add_init_script("""if(!localStorage.getItem('ruby-village:chapter-1:v1'))localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:['gate','garden','well','bakery','stream','mill','post','forest'],introSeen:['gate','garden','well','bakery','stream','mill','post','forest']}));""")
   await page.goto(BASE);await page.locator('#choose-level').click();await page.locator('#map-more').click()
   await page.screenshot(path=str(OUT/f'{w}-adventure.png'))
   if AFTER:
    assert await page.get_by_text('Песочница',exact=True).count()==0
    assert await page.locator('#chapter-ending [data-painted-miniature]').count()==1
    await page.locator('#letter-open').click();await page.locator('#story[open]').wait_for();assert 'приглашение' in (await page.locator('#story-title').inner_text()).lower();await page.locator('#story-skip').click()
    await page.locator('#map-more').click();await page.locator('#chapter-ending').click();await page.locator('#story[open]').wait_for();await page.locator('#story-skip').click()
    if await page.locator('#choose-level').is_visible():await page.locator('#choose-level').click()
   else:await page.locator('#map-extra-close').click()
   for i,id in enumerate(IDS):
    if not await page.locator('#chapter-map').is_visible():
     await page.locator('#scene-back').click()
    await page.locator(f'.level-card[data-level="{id}"]').click();await page.locator('#board').wait_for();await page.wait_for_timeout(400)
    if await page.locator('#story[open]').count():await page.locator('#story-skip').click()
    await page.screenshot(path=str(OUT/f'{w}-{id}.png'))
    metrics=await page.locator('h1 small').evaluate('(e)=>({text:e.textContent,display:getComputedStyle(e).display,font:getComputedStyle(e).fontSize,rect:e.getBoundingClientRect().toJSON(),color:getComputedStyle(e).color,background:getComputedStyle(e).backgroundColor})')
    if AFTER:
     assert metrics['text']==f'Уровень {i+1} из 8',metrics
     assert metrics['display']!='none' and float(metrics['font'][:-2])>=11,metrics
     assert await page.locator('#scene-event image').count()==1
     assert metrics['rect']['right']<w and metrics['rect']['top']>=0,metrics
    report.append({'viewport':[w,h],'level':id,'progress':metrics})
   if AFTER:
    await page.reload();await page.locator('#continue-game').click();await page.wait_for_timeout(200)
    saved=await page.evaluate("JSON.parse(localStorage.getItem('ruby-village:chapter-1:v1'))")
    assert saved['completed']==IDS
    assert saved['session']['levelId']=='forest'
   assert not errors,errors
   await c.close()
  await b.close()
 (OUT/'report.json').write_text(json.dumps({'checks':report,'after':AFTER,'scope':'Real browser desktop and touch-capable landscape emulation; screenshots of restored replays. Not physical phone. Progress fixture is preloaded, no claim of full solves.'},ensure_ascii=False,indent=2))
asyncio.run(run())
