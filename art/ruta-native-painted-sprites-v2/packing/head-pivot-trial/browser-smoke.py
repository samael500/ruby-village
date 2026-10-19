from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
O=Path(__file__).resolve().parent
async def main():
 rows=[]
 async with async_playwright()as p:
  b=await p.chromium.launch(headless=True)
  for name,args in [('desktop',{'viewport':{'width':1280,'height':900}}),('landscape-emulated',{'viewport':{'width':844,'height':390},'is_mobile':True,'has_touch':True})]:
   c=await b.new_context(**args);page=await c.new_page();err=[];page.on('pageerror',lambda e:err.append(str(e)));await page.goto('http://localhost:5322/head-pivot-trial/review.html');await page.wait_for_function('window.reviewState?.ready');await page.locator('#play').tap()if name.startswith('landscape')else await page.locator('#play').click();await page.locator('#frame').focus();await page.keyboard.press('End');await page.keyboard.press('ArrowLeft');states=[]
   for mode in ['head','clasp','baseline','head']:
    await page.locator('#mode').select_option(mode);s=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert s['frame']==46 and s['mode']==mode;states.append(s)
   assert states[0]['lastDraw']['displayOrigin']!=states[1]['lastDraw']['displayOrigin'];assert not err;await page.screenshot(path=str(O/(name+'-frame46.png')));rows.append({'context':name,'actualControls':True,'samePhaseAcrossModes':True,'modeStates':states,'pageErrors':err,'physicalPhone':'NOT RUN'});await c.close()
  await b.close()
 (O/'browser-smoke.json').write_text(json.dumps({'status':'AUTHOR-UI-SMOKE-ONLY-NOT-MOTION-ACCEPTANCE','rows':rows},indent=2)+'\n')
asyncio.run(main())
