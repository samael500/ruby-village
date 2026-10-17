"""Real input/evidence for the arbitrary native-ground planner; not a production bridge test."""
import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
out=Path(__file__).resolve().parents[1]/'docs/chapter-1-rc/painted-motion'
async def run():
 async with async_playwright() as p:
  b=await p.chromium.launch(headless=True);c=await b.new_context(viewport={'width':1280,'height':720},record_video_dir='/tmp/ruta-ground-goal',record_video_size={'width':1280,'height':720});page=await c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));await page.goto('http://127.0.0.1:5193/ruby-village/docs/chapter-1-rc/painted-motion/full-preview.html');await page.wait_for_function('window.motionReady');results={}
  for scene in ['gate','post']:
   if scene=='post':await page.select_option('#scene',scene);await page.wait_for_timeout(700)
   await page.click('#goal');await page.wait_for_function('window.motionFullState?.goal');await page.wait_for_timeout(1400);await page.click('#pause');await page.wait_for_timeout(50);a=await page.evaluate('window.motionFullState');await page.wait_for_timeout(400);z=await page.evaluate('window.motionFullState');assert a['position']==z['position'] and a['phaseMs']==z['phaseMs'];await page.click('#pause');await page.wait_for_function('window.motionFullState?.goal && !window.motionFullState.playing',timeout=20000);s=await page.evaluate('window.motionFullState');assert s['goal']['inside'] and s['completions']==1 and s['state']=='idle',s;assert s['position']==s['goal']['endpoint'];assert s['goal']['residualPixels']<=11.3;assert s['goal']['residualPixels']>.01;assert s['contacts']==round(s['goal']['worldLength']/.36)+1,s;results[scene]=s;await page.screenshot(path=str(out/f'v2-ground-goal-{scene}.png'))
  assert not errors,errors;await c.close();await page.video.save_as(str(out/'v2-ground-goal-route.webm'));await b.close();(out/'v2-ground-goal-browser.json').write_text(json.dumps({'result':'passed','scope':'actual arbitrary-length motion bench with goal polygon, not production bridge gameplay','scenes':results,'errors':errors,'physicalPhone':'not-run','familyTest':'not-run'},indent=2)+'\n');print('PASS: gate/post arbitrary routes finish physically on goal ground, residual <11.3px, no center slide, actual pause/input')
asyncio.run(run())
