"""Real Chromium source-resource viewports; explicitly not integrated gameplay."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/chapter-1-rc/art/garden-well/browser';OUT.mkdir(parents=True,exist_ok=True)
rows=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for scene in ['garden','well']:
        for w,h in [(1280,720),(1920,1080),(2560,1080),(844,390),(932,430),(1024,600)]:
            page=browser.new_page(viewport={'width':w,'height':h});errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            page.goto(f'http://127.0.0.1:5297/docs/chapter-1-rc/art/garden-well/preview.html?scene={scene}')
            page.wait_for_function('window.previewReady===true')
            bounds=page.locator('#wide').bounding_box()
            assert bounds
            coverage=bounds['x']<=1 and bounds['y']<=1 and bounds['x']+bounds['width']>=w-1 and bounds['y']+bounds['height']>=h-1
            assert coverage and not errors,(scene,w,h,bounds,errors)
            page.screenshot(path=str(OUT/f'{scene}-{w}x{h}.png'))
            rows.append({'scene':scene,'viewport':[w,h],'paintedCoverage':coverage,'pageErrors':errors,'fit':page.evaluate('previewFit')});page.close()
    browser.close()
(OUT/'checks.json').write_text(json.dumps({'scope':'standalone real Chromium source-art registration, not actual game or physical phone','cases':rows},indent=2)+'\n')
print('12 standalone Chromium art viewports PASS')
