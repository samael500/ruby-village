from pathlib import Path
from playwright.sync_api import sync_playwright
import json,urllib.request,hashlib
O=Path(__file__).resolve().parent;url='http://localhost:5322/head-pivot-trial/review.html';h=urllib.request.urlopen(url).read();m=urllib.request.urlopen('http://localhost:5322/head-pivot-trial/manifest.json').read();assert hashlib.sha256(h).hexdigest()=='a384ba2f9c6044e2567c163d198bbe0386595f928d3c9966eda1780b5efa6221';assert hashlib.sha256(m).hexdigest()=='a3d51c711ee2bd2178b38ab535828a48e3731ca327463f44a0100a96f025919d';report={'url':url,'htmlSha':hashlib.sha256(h).hexdigest(),'manifestSha':hashlib.sha256(m).hexdigest(),'modes':[]};errors=[]
with sync_playwright()as p:
 b=p.chromium.launch();ctx=b.new_context(viewport={'width':1280,'height':800},record_video_dir=str(O/'video'),record_video_size={'width':1280,'height':800});page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(url,wait_until='networkidle');page.wait_for_function('window.reviewState?.ready')
 for mode in ['baseline','clasp','head']:
  page.locator('#mode').select_option(mode);page.wait_for_timeout(4200);page.screenshot(path=str(O/f'{mode}-loop.png'));page.locator('#play').click()
  for i in [7,8,15,16,23,24,31,32,37,38,39,40,47,0]:
   page.locator('#frame').focus();page.keyboard.press('Home')
   for j in range(i):page.keyboard.press('ArrowRight')
   page.wait_for_function(f'reviewState.frame==={i}');page.screenshot(path=str(O/f'{mode}-{i:02}.png'))
  report['modes'].append({'mode':mode,'state':page.evaluate('reviewState')});page.locator('#play').click()
 report['errors']=errors;report['videoPath']=str(page.video.path());ctx.close();b.close();(O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
