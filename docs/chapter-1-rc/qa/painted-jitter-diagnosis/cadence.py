import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
async def main():
 rows=[]
 async with async_playwright()as p:
  b=await p.chromium.launch(headless=True)
  for name,args in [('desktop',{'viewport':{'width':1280,'height':900}}),('landscape-emulated',{'viewport':{'width':844,'height':390},'is_mobile':True,'has_touch':True,'device_scale_factor':1})]:
   c=await b.new_context(**args);page=await c.new_page();await page.goto('http://localhost:5322/semantic-pivot-trial/review.html');await page.wait_for_function('window.reviewState?.ready');samples=await page.evaluate('''()=>new Promise(resolve=>{let a=[],start=performance.now();function tick(t){a.push({t,phase:reviewState.frame});if(t-start<9000)requestAnimationFrame(tick);else resolve(a)}requestAnimationFrame(tick)})''');trans=[samples[i]for i in range(1,len(samples))if samples[i]['phase']!=samples[i-1]['phase']];skips=[{'from':samples[i-1]['phase'],'to':samples[i]['phase'],'dt':samples[i]['t']-samples[i-1]['t']}for i in range(1,len(samples))if(samples[i]['phase']-samples[i-1]['phase'])%48>1];rows.append({'context':name,'samples':samples,'phaseChangeIntervalsMs':[trans[i]['t']-trans[i-1]['t']for i in range(1,len(trans))],'skippedTransitions':skips,'physicalPhone':'NOT RUN'});await c.close()
  await b.close()
 Path(__file__).with_name('cadence.json').write_text(json.dumps(rows,indent=2)+'\n')
asyncio.run(main())
