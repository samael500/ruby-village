from pathlib import Path
import asyncio,json
from playwright.async_api import async_playwright
O=Path(__file__).resolve().parent;URL='http://127.0.0.1:5365/art/ruta-native-painted-production-v1/e-quarter0/packing/review.html'
async def main():
 rows=[]
 async with async_playwright()as p:
  b=await p.chromium.launch(headless=True)
  for dpr in[1,2]:
   c=await b.new_context(viewport={'width':1000,'height':1000},device_scale_factor=dpr);page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto(URL);await page.wait_for_function('window.reviewState?.ready');initial=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert initial['frame']==0 and not initial['playing'];assert initial['loop']is False;await page.wait_for_timeout(150);assert await page.evaluate('reviewState.frame')==0;await page.screenshot(path=str(O/f'dpr{dpr}-phase00.png'),full_page=True)
   sizes=await page.evaluate('''()=>[...document.querySelectorAll('canvas')].map(c=>{const p=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let y0=c.height,y1=-1;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(p[(y*c.width+x)*4+3]>128){y0=Math.min(y0,y);y1=Math.max(y1,y)}return{backing:[c.width,c.height],alpha128Height:y1-y0+1}})''');assert all(x['backing']==[320*dpr,400*dpr]for x in sizes);assert abs(sizes[0]['alpha128Height']-sizes[1]['alpha128Height'])<=2
   await page.locator('#play').click();await page.wait_for_function('reviewState.completed===true');end=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert end['frame']==11 and not end['playing'];await page.wait_for_timeout(600);assert await page.evaluate('reviewState.frame')==11;await page.locator('#frame').focus();await page.keyboard.press('Home');assert await page.evaluate('reviewState.frame')==0;assert not await page.evaluate('reviewState.playing');assert not errors;rows.append({'dpr':dpr,'initialState':initial,'phase0ActualRasterHeights':sizes,'endState':end,'forwardThenStopNoLoopObserved':True,'scrubPaused':True,'pageErrors':errors});await c.close()
  await b.close()
 (O/'browser-smoke.json').write_text(json.dumps({'status':'AUTHOR-QUARTER-PACKING-DISPLAY-SMOKE-NOT-FULL-WALK-ACCEPTANCE','rows':rows},indent=2)+'\n')
asyncio.run(main())
