"""Actual Chromium wide perimeter review, preserving production fitScene formula."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1];O=R/'docs/chapter-1-rc/art/map-match-post-forest';results=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True)
 for name in ['post','forest']:
  for w,h in [(1280,720),(1920,1080),(2560,1080),(844,390),(932,430),(1024,600)]:
   page=b.new_page(viewport={'width':w,'height':h});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:5201/docs/chapter-1-rc/art/map-match-post-forest/preview.html?scene={name}');page.wait_for_function('window.previewReady===true');page.screenshot(path=str(O/f'{name}-{w}x{h}.png'));assert not errors;results.append({'scene':name,'viewport':[w,h],'fit':page.evaluate('previewFit'),'pageErrors':errors});page.close()
 b.close()
(O/'browser-checks.json').write_text(json.dumps({'scope':'actual Chromium standalone fitScene-art preview, not production gameplay or physical phone','cases':results},indent=2)+'\n')
