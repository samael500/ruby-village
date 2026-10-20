"""Author smoke of generic preview controls; not independent art/game acceptance."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parent
async def main():
 rows=[]
 async with async_playwright()as pw:
  b=await pw.chromium.launch(headless=True)
  for name,size,touch in [('desktop',{'width':1280,'height':900},False),('landscape-emulated',{'width':844,'height':390},True)]:
   c=await b.new_context(viewport=size,has_touch=touch,is_mobile=touch);page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto('http://127.0.0.1:5322/full48/review.html');await page.wait_for_function('window.reviewState?.ready');await page.wait_for_timeout(250);first=await page.evaluate('({...window.reviewState})');await page.wait_for_timeout(120);second=await page.evaluate('({...window.reviewState})');assert first['frameCount']==48 and second['drawCount']>first['drawCount'],(first,second,errors)
   if touch:await page.locator('#play').tap()
   else:await page.locator('#play').click()
   assert not(await page.evaluate('window.reviewState.playing'));await page.locator('#frame').focus();await page.keyboard.press('End');await page.wait_for_timeout(30);state=await page.evaluate('({...window.reviewState})');assert state['frame']==state['nativePhaseIndex']==47;assert await page.locator('#reference').evaluate('(e)=>e.tagName')=='CANVAS';ref=state['referenceDraw'];assert abs(ref['height']-186.55436028830434)<1e-9 and abs(ref['x']+ref['width']/2-128)<1e-9 and abs(ref['y']+ref['height']-258.42965602874756)<1e-9;assert first['referenceDraw']==state['referenceDraw'];await page.screenshot(path=str(P/f'full48/{name}-frame47.png'),full_page=True);assert not errors;rows.append({'context':name,'viewport':size,'touchEmulated':touch,'playClockAdvances':True,'pauseMouseOrTouchActual':True,'actualKeyboardSliderEndFrame':state['frame'],'sameNativePhase':state['nativePhaseIndex'],'referenceTag':'CANVAS','referenceDraw':ref,'referenceConstantAcrossSampledFrames':True,'pageErrors':errors,'physicalPhone':'NOT RUN'});await c.close()
  await b.close()
 (P/'full48/browser-smoke.json').write_text(json.dumps({'status':'AUTHOR-CONTROL-SMOKE-NOT-INDEPENDENT-LOOP-OR-ART-ACCEPTANCE','rows':rows},indent=2)+'\n')
asyncio.run(main())
