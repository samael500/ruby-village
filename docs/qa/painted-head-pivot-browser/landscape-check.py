from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,urllib.request
O=Path(__file__).resolve().parent/'landscape';O.mkdir(exist_ok=True)
u='http://localhost:5311/art/ruta-native-painted-sprites-v2/packing/head-pivot-trial/review.html';h=urllib.request.urlopen(u).read();assert hashlib.sha256(h).hexdigest()=='a384ba2f9c6044e2567c163d198bbe0386595f928d3c9966eda1780b5efa6221'
r={'url':u,'htmlSha':hashlib.sha256(h).hexdigest(),'scope':'CDP touch emulation, not physical phone','errors':[],'httpFailures':[]}
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':844,'height':390},record_video_dir=str(O/'video'),record_video_size={'width':844,'height':390});page=c.new_page();cdp=c.new_cdp_session(page);cdp.send('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':5});page.on('pageerror',lambda e:r['errors'].append(str(e)));page.on('response',lambda q:r['httpFailures'].append([q.url,q.status]) if q.status>=400 else None);page.on('requestfailed',lambda q:r['errors'].append([q.url,q.failure]));page.goto(u,wait_until='networkidle');page.wait_for_function('window.reviewState?.ready');page.locator('#mode').select_option('head');page.wait_for_timeout(4200);page.screenshot(path=str(O/'playing.png'));r['state']=page.evaluate('reviewState');r['geometry']=page.evaluate('''() => ({viewport:[innerWidth,innerHeight],scroll:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],canvases:[...document.querySelectorAll('canvas')].map(c=>({id:c.id,rect:c.getBoundingClientRect().toJSON(),backing:[c.width,c.height]}))})''');page.locator('#play').click()
 for i in [39,40,47,0]:
  page.locator('#frame').focus();page.keyboard.press('Home')
  for j in range(i):page.keyboard.press('ArrowRight')
  page.wait_for_function(f'reviewState.frame==={i}');page.screenshot(path=str(O/f'frame-{i:02}.png'))
 r['video']=str(page.video.path());c.close();b.close()
(O/'report.json').write_text(json.dumps(r,indent=2)+'\n')
