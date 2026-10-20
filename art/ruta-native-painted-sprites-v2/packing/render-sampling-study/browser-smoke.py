from pathlib import Path
import asyncio,json,hashlib
from playwright.async_api import async_playwright
O=Path(__file__).resolve().parent;URL='http://127.0.0.1:5364/'
async def frame40(page):
 await page.wait_for_function('window.reviewState?.ready');await page.locator('#play').click();await page.locator('#frame').focus();await page.keyboard.press('End')
 for _ in range(7):await page.keyboard.press('ArrowLeft')
 assert await page.evaluate('reviewState.frame')==40
async def main():
 rows=[]
 async with async_playwright()as p:
  browser=await p.chromium.launch(headless=True)
  for dpr in [1,2]:
   context=await browser.new_context(viewport={'width':1000,'height':1000},device_scale_factor=dpr);page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto(URL+'render-sampling-study/review.html');await frame40(page);s=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert s['baseline']['backing']==[256,320];assert s['direct']['backing']==[320*dpr,400*dpr];assert s['baseline']['size']==s['direct']['size'];assert s['baseline']['origin']==s['direct']['origin'];before=await page.locator('#baseline').evaluate('(c)=>c.toDataURL()');await page.screenshot(path=str(O/f'dpr{dpr}-frame40.png'),full_page=True)
   # Exact old baseline pixels at identical source phase/pivot.
   original=await context.new_page();await original.goto(URL+'head-pivot-trial/review.html');await frame40(original);old=await original.locator('#painted').evaluate('(c)=>c.toDataURL()');assert before==old;await original.close()
   await page.locator('#snap').check();sn=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert sn['direct']['size']==s['direct']['size'];assert all(abs(x-round(x))<1e-8 for x in sn['direct']['physicalOrigin']);assert sn['baseline']==s['baseline'];count=sn['drawCount'];await page.wait_for_timeout(180);assert await page.evaluate('reviewState.drawCount')==count,'ResizeObserver feedback while paused';assert not errors
   rows.append({'dpr':dpr,'state':s,'snappedState':sn,'oldBaselineCanvasPixelsExact':True,'sameCSSActorSize':True,'snapPhysicalOriginInteger':True,'noPausedResizeObserverLoop':True,'pageErrors':errors});await context.close()
  await browser.close()
 (O/'browser-smoke.json').write_text(json.dumps({'status':'AUTHOR-RENDERER-SMOKE-NOT-SHIMMER-FIX-OR-ART-ACCEPTANCE','rows':rows},indent=2)+'\n')
asyncio.run(main())
