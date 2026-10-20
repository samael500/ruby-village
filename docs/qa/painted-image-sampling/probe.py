from pathlib import Path
from playwright.sync_api import sync_playwright
import json
O=Path(__file__).resolve().parent
u='http://localhost:5311/art/ruta-native-painted-sprites-v2/packing/head-pivot-trial/review.html'
r=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for dpr in [1,2]:
  c=b.new_context(viewport={'width':1280,'height':800},device_scale_factor=dpr);page=c.new_page();page.goto(u);page.wait_for_function('window.reviewState?.ready');page.locator('#play').click();r.append(page.evaluate('''()=>({dpr:devicePixelRatio,viewport:[innerWidth,innerHeight],state:reviewState,canvases:[...document.querySelectorAll('canvas')].map(c=>({id:c.id,backing:[c.width,c.height],rect:c.getBoundingClientRect().toJSON(),smoothing:c.getContext('2d').imageSmoothingEnabled,quality:c.getContext('2d').imageSmoothingQuality,cssImageRendering:getComputedStyle(c).imageRendering}))})'''));page.screenshot(path=str(O/f'dpr-{dpr}.png'));c.close()
 b.close()
(O/'probe.json').write_text(json.dumps(r,indent=2)+'\n')
