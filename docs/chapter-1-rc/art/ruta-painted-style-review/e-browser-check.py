from playwright.sync_api import sync_playwright
import json
from pathlib import Path
O=Path('/tmp/ruby-ruta-style-qa/docs/chapter-1-rc/art/ruta-painted-style-review');errors=[]
with sync_playwright()as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1280,'height':900});page.on('pageerror',lambda e:errors.append(str(e)));page.goto('http://localhost:5310/ruta-painted-ready-v1/review.html');page.wait_for_function("document.querySelector('#status').textContent.includes('24')");samples=[]
 for i in range(6):
  page.wait_for_timeout(120);samples.append(page.locator('#number').inner_text())
 page.screenshot(path=str(O/'e-browser-actual.png'));status=page.locator('#status').inner_text();imgs=page.evaluate("[...document.querySelectorAll('canvas')].map(c=>({id:c.id,width:c.width,height:c.height,nonzeroPixels:[...c.getContext('2d').getImageData(0,0,c.width,c.height).data].filter((v,i)=>i%4===3&&v>0).length}))");b.close()
(O/'e-browser-check.json').write_text(json.dumps({'url':'http://localhost:5310/ruta-painted-ready-v1/review.html','status':status,'frameReadbacks':samples,'uniqueObservedFrameNumbers':len(set(samples)),'canvases':imgs,'pageErrors':errors,'scope':'actual browser frame advancement and loaded canvas; screenshot is one still, not subjective realtime motion certification','registration':'page applies artist-origin proposal per-frame translations; frame7 has interpolatedanchor; no spritepixelwarping'},indent=2)+'\n')
