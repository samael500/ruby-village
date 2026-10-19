from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib
O=Path('/tmp/ruby-painted-native48-qa/docs/qa/painted-head-pivot-browser/cadence-study');O.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1280,'height':800},record_video_dir=str(O/'video'));page=c.new_page();page.goto('http://localhost:5311/art/ruta-native-painted-sprites-v2/packing/head-pivot-cadence-study/review.html');page.wait_for_function('window.reviewState?.ready');r=[]
 for stride in ['1','2','3']:
  page.locator('#cadence').select_option(stride);page.wait_for_timeout(4200);page.screenshot(path=str(O/f'cadence-{stride}.png'));r.append(page.evaluate('reviewState'))
 (O/'results.json').write_text(json.dumps({'states':r,'htmlSha':hashlib.sha256(page.content().encode()).hexdigest(),'video':str(page.video.path())},indent=2));c.close();b.close()
