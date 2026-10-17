"""Real Chromium input and motion evidence for the isolated review bench, not game QA."""
import asyncio,json,argparse
from pathlib import Path
from playwright.async_api import async_playwright
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:5193/ruby-village/docs/chapter-1-rc/painted-motion/full-preview.html');args=parser.parse_args();out=root/'docs/chapter-1-rc/painted-motion';out.mkdir(exist_ok=True,parents=True)
async def run():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True);context=await browser.new_context(viewport={'width':1280,'height':720},record_video_dir='/tmp/ruta-v2-full-video',record_video_size={'width':1280,'height':720});page=await context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  await page.goto(args.url);await page.wait_for_function('window.motionReady');await page.click('#play');seen={};states=[]
  for _ in range(84):
   await page.wait_for_timeout(250);s=await page.evaluate('window.motionFullState');states.append(s)
   if s['state']=='walk' and s['direction'] not in seen:
    seen[s['direction']]=s;await page.screenshot(path=str(out/f'v2-route-{s["direction"]}.png'))
  assert set(seen)=={'e','se','sw','w','nw','ne'},seen
  final=states[-1];assert final['completions']==1 and not final['playing'] and final['state']=='idle',final
  await page.click('#play');await page.wait_for_timeout(4100);await page.click('#pause');await page.wait_for_timeout(50);a=await page.evaluate('window.motionFullState');await page.wait_for_timeout(500);b=await page.evaluate('window.motionFullState');assert a['phaseMs']==b['phaseMs'] and a['position']==b['position'];await page.click('#pause')
  await context.close();await page.video.save_as(str(out/'v2-full-route.webm'))
  mobile=await browser.new_context(viewport={'width':844,'height':390});small=await mobile.new_page();await small.goto(args.url);await small.wait_for_function('window.motionReady');await small.select_option('#scene','post');await small.wait_for_timeout(800);await small.click('#play');await small.wait_for_timeout(4200);post=await small.evaluate('window.motionFullState');assert 'calibrated-1-' in post['frameFile'];await small.screenshot(path=str(out/'v2-post-landscape.png'))
  await small.set_viewport_size({'width':390,'height':844});await small.wait_for_timeout(100);portraitA=await small.evaluate('window.motionFullState');await small.wait_for_timeout(500);portraitB=await small.evaluate('window.motionFullState');assert portraitA['position']==portraitB['position'] and portraitB['paused'];await small.screenshot(path=str(out/'v2-portrait-paused.png'))
  await small.set_viewport_size({'width':844,'height':390});await small.check('#reduced');await small.wait_for_timeout(100);reduced=await small.evaluate('window.motionFullState');assert not reduced['playing'] and reduced['state']=='idle' and reduced['completions']==1,reduced
  assert not errors,errors;await browser.close();(out/'v2-browser-audit.json').write_text(json.dumps({'result':'passed','actualInput':['replay button','pause/resume button','scene selector post','portrait viewport','reduced-motion checkbox'],'directions':seen,'completeRoute':final,'paused':b,'calibratedPost':post,'reducedMotion':reduced,'browserErrors':errors,'physicalPhone':'not-run','familyTest':'not-run','scope':'isolated actual CharacterPlayer/CharacterRoute review bench; game integration separate'},indent=2)+'\n');print('Browser assertions passed: six directions, one completion, pause, scene camera, portrait and reduced motion')
asyncio.run(run())
