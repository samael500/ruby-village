import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
async def main():
 async with async_playwright()as p:
  b=await p.chromium.launch(headless=True);page=await b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto('http://localhost:5322/head-pivot-cadence-study/review.html');await page.wait_for_function('window.reviewState?.ready');await page.locator('#play').click();await page.locator('#frame').focus();await page.keyboard.press('End');states=[]
  for stride in ['1','2','3','1']:
   await page.locator('#cadence').select_option(stride);s=await page.evaluate('JSON.parse(JSON.stringify(reviewState))');assert s['clockPhase']==47;assert s['sourcePhase']==47//int(stride)*int(stride);assert s['uniquePhaseCount']==48/int(stride);assert s['cycleSeconds']==40/24;states.append(s)
  assert not errors;await b.close();Path(__file__).with_name('smoke.json').write_text(json.dumps({'scope':'author actual UI smoke only, NOT video or perceptual cadence acceptance','states':states,'pageErrors':errors},indent=2)+'\n')
asyncio.run(main())
