from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,urllib.request
O=Path(__file__).resolve().parent;u='http://localhost:5311/art/ruta-native-painted-sprites-v2/packing/render-sampling-study/review.html';r={'url':u,'htmlSha':hashlib.sha256(urllib.request.urlopen(u).read()).hexdigest(),'runs':[]}
with sync_playwright() as p:
 b=p.chromium.launch()
 for dpr in [1,2]:
  out=O/f'dpr-{dpr}';out.mkdir(exist_ok=True);c=b.new_context(viewport={'width':1280,'height':900},device_scale_factor=dpr,record_video_dir=str(out/'video'),record_video_size={'width':1280,'height':900});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(u,wait_until='networkidle');page.wait_for_function('window.reviewState?.ready');page.wait_for_timeout(4200);page.locator('#play').click();run={'dpr':dpr,'state':page.evaluate('reviewState'),'errors':errors}
  for i in [0,40]:
   page.locator('#frame').fill(str(i));page.locator('#frame').dispatch_event('input');page.wait_for_function(f'reviewState.frame==={i}');page.screenshot(path=str(out/f'frame-{i:02}.png'));page.locator('#baseline').screenshot(path=str(out/f'baseline-{i:02}.png'));page.locator('#direct').screenshot(path=str(out/f'direct-{i:02}.png'))
  run['video']=str(page.video.path());c.close();r['runs'].append(run)
 b.close()
(O/'report.json').write_text(json.dumps(r,indent=2)+'\n')
