from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
O=Path(__file__).resolve().parent;URL='http://127.0.0.1:5365/art/ruta-native-painted-production-v1/full48/review.html'
async def main():
 rows=[]
 async with async_playwright()as p:
  b=await p.chromium.launch(headless=True)
  for dpr in[1,2]:
   c=await b.new_context(viewport={'width':1000,'height':1000},device_scale_factor=dpr);page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto(URL);await page.wait_for_function('window.reviewState?.ready');await page.locator('#play').click();await page.locator('#frame').focus();states=[]
   for target in[0,11,12,23,24,35,36,47]:
    await page.keyboard.press('Home')
    for _ in range(target):await page.keyboard.press('ArrowRight')
    state=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert state['frame']==target and state['nativePhaseIndex']==target;assert state['frameCount']==48 and abs(state['fps']-28.8)<1e-9;assert state['panels'][1]['scale']==.5127893376456061;assert all(x['backing']==[320*dpr,400*dpr]for x in state['panels']);states.append(state)
   await page.locator('#mode').select_option('baseline');baseline=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert baseline['headTranslationNativePx']==[0,0];await page.locator('#mode').select_option('head');assert not errors;await page.screenshot(path=str(O/f'dpr{dpr}-phase47.png'),full_page=True);await page.locator('#play').click();await page.wait_for_timeout(250);assert await page.evaluate('reviewState.frame')<20;rows.append({'dpr':dpr,'sameFrameModeClock':True,'boundaryStates':states,'baselineMode':baseline,'loop47to0Observed':True,'pageErrors':errors});await c.close()
  await b.close()
 (O/'browser-smoke.json').write_text(json.dumps({'status':'AUTHOR-UI-SMOKE-NOT-MOTION-OR-CLARITY-ACCEPTANCE','rows':rows},indent=2)+'\n')
asyncio.run(main())
