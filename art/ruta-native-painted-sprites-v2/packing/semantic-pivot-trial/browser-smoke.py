"""Author controls smoke only. Independent actual loop/video QA is separate."""
from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
P=Path(__file__).resolve().parent
async def main():
 rows=[]
 async with async_playwright()as pw:
  b=await pw.chromium.launch(headless=True)
  for name,size,touch in [('desktop',{'width':1280,'height':900},False),('landscape-emulated',{'width':844,'height':390},True)]:
   c=await b.new_context(viewport=size,has_touch=touch,is_mobile=touch);p=await c.new_page();errs=[];p.on('pageerror',lambda e:errs.append(str(e)));await p.goto('http://127.0.0.1:5322/semantic-pivot-trial/review.html');await p.wait_for_function('window.reviewState?.ready');await p.wait_for_timeout(100)
   if touch:await p.locator('#play').tap()
   else:await p.locator('#play').click()
   await p.locator('#frame').focus();await p.keyboard.press('End')
   for _ in range(8):await p.keyboard.press('ArrowLeft')
   state=await p.evaluate('({...window.reviewState})');assert state['frame']==39 and state['mode']=='candidate' and not state['playing'];await p.screenshot(path=str(P/f'{name}-candidate39.png'),full_page=True)
   await p.locator('#mode').select_option('baseline');base=await p.evaluate('({...window.reviewState})');assert base['frame']==39 and base['lastDraw']['displayOrigin']!=state['lastDraw']['displayOrigin'];await p.locator('#mode').select_option('overlay');assert await p.evaluate('window.reviewState.frame')==39;await p.locator('#mode').select_option('candidate');await p.locator('#frame').focus();await p.keyboard.press('Home')
   for _ in range(14):await p.keyboard.press('ArrowRight')
   occluded=await p.evaluate('({...window.reviewState})');assert occluded['frame']==14 and occluded['estimated'];await p.screenshot(path=str(P/f'{name}-estimated14.png'),full_page=True);assert not errs;rows.append({'context':name,'viewport':size,'mouseOrNativeCdpTouchPause':True,'actualKeyboardSeek39And14':True,'togglePreservesPhase':True,'baselineAndCandidateDestinationsDiffer':True,'occlusion14ExplicitlyEstimated':True,'pageErrors':errs,'physicalPhone':'NOT RUN'});await c.close()
  await b.close()
 (P/'browser-smoke.json').write_text(json.dumps({'status':'AUTHOR-UI-SMOKE-NOT-INDEPENDENT-MOTION-ACCEPTANCE','rows':rows},indent=2)+'\n')
asyncio.run(main())
