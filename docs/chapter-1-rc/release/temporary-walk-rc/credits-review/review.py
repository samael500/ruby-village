from pathlib import Path
import asyncio,json,hashlib,zipfile,urllib.request,subprocess
from playwright.async_api import async_playwright
root=Path('/tmp/ruby-final-rc');out=Path(__file__).parent;base='http://127.0.0.1:5390/ruby-village/'
sha=lambda b:hashlib.sha256(b).hexdigest()
async def main():
 report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'base':base,'archive':[],'contexts':[],'http':[]}
 with zipfile.ZipFile(root/'public/licenses/music-source.zip') as z:
  for n in z.namelist():
   b=z.read(n);same=b==(root/n).read_bytes();assert same;report['archive'].append({'file':n,'bytes':len(b),'sha256':sha(b),'repoByteEqual':same})
  assert len(z.namelist())==11 and len([n for n in z.namelist() if n.endswith('.mid')])==5
  assert not any(n.lower().endswith(('.flac','.wav','.blend','.fbx')) for n in z.namelist())
 for name in ['credits.html','licenses/music-GPL-2.txt','licenses/music-notices.txt','licenses/music-source.zip','licenses/sound-notices.txt']:
  with urllib.request.urlopen(base+name) as r:b=r.read();report['http'].append({'url':r.url,'status':r.status,'sha256':sha(b),'distByteEqual':b==(root/'dist'/name).read_bytes()});assert report['http'][-1]['distByteEqual']
 async with async_playwright() as p:
  browser=await p.chromium.launch()
  for w,h in [(1280,720),(844,390)]:
   c=await browser.new_context(viewport={'width':w,'height':h});page=await c.new_page();req=[];err=[];page.on('request',lambda r:req.append(r.url));page.on('pageerror',lambda e:err.append(str(e)))
   await page.goto(base);await page.locator('#game-credits').wait_for(state='visible');await page.wait_for_timeout(500)
   before=list(req);a=page.locator('#game-credits');props=await a.evaluate('(e)=>({href:e.href,target:e.target,rel:e.rel,rect:e.getBoundingClientRect().toJSON()})');assert props['target']=='_blank' and 'noopener' in props['rel']
   async with page.expect_popup() as pop:await a.click()
   credit=await pop.value;await credit.wait_for_load_state();assert await credit.locator('h2').count()==3
   await credit.screenshot(path=str(out/f'credits-{w}.png'),full_page=True)
   assert not await credit.evaluate('document.documentElement.scrollWidth>innerWidth')
   await credit.close();assert await page.locator('#continue-game').is_visible();await page.locator('#continue-game').click();await page.wait_for_timeout(500)
   assert await page.locator('#prologue-panel').is_visible();await page.locator('#prologue-skip').click();await page.wait_for_timeout(500);assert not await page.locator('#main-menu').is_visible();await page.screenshot(path=str(out/f'play-after-credits-{w}.png'))
   auto=[u for u in req if 'music-source.zip' in u];assert not auto;assert not err
   report['contexts'].append({'viewport':[w,h],'anchor':props,'popupUrl':base+'credits.html','gameRemainedAvailable':True,'startButtonEnteredGame':True,'sourceZipAutoloads':auto,'pageErrors':err,'initialRequests':before})
   await c.close()
  await browser.close()
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: two viewports, popup/play, five HTTP files, 11 exact archive files, no autoload')
asyncio.run(main())
