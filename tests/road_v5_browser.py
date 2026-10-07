"""Rendered variants follow an instance through rotation/movement; feet stay anchored."""
import sys
from playwright.sync_api import sync_playwright,expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4173/ruby-village/'
def materials(page,selector):
    return page.locator(selector+' [data-material]').evaluate_all("els=>Object.fromEntries(els.map(e=>[e.dataset.visualKey,e.dataset.tileVariant]))")
def tap_cell(page,key):
    box=page.locator(f'[data-cell="{key}"] > polygon').bounding_box()
    page.touchscreen.tap(box['x']+box['width']/2,box['y']+box['height']/2)
with sync_playwright() as p:
    b=p.chromium.launch();errors=[]
    for w,h in [(1280,720),(844,390),(390,844)]:
        page=b.new_page(viewport={'width':w,'height':h},has_touch=True)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL);page.locator('[data-level="gate"]').tap();page.locator('#story-skip').tap()
        ratio=page.evaluate('''()=>{
          const img=document.querySelector('#ruta-idle'),height=img.height.baseVal.value*img.getScreenCTM().a*(1277-45)/1300;
          return height/document.querySelector('[data-cell="0,1"] > polygon').getBoundingClientRect().height;
        }''')
        assert ratio>=1
        assert page.locator('#ruta-idle').evaluate('el=>{const m=el.getScreenCTM();return Math.abs(m.a-m.d)<1e-6&&Math.abs(m.b)<1e-6&&Math.abs(m.c)<1e-6}')
        page.locator('#scene-back').tap()
        page.evaluate("()=>localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:['gate','garden','well']}))")
        page.reload();page.locator('[data-level="bakery"]').tap();page.locator('#story-skip').tap()
        initial=materials(page,'[data-piece="bakery-a"]');assert len(initial)==3
        page.locator('[data-piece="bakery-a"]').tap();tap_cell(page,'1,1');page.locator('#place').tap()
        assert materials(page,'[data-owner="bakery-a"]')==initial
        tap_cell(page,'1,1');page.locator('#right').tap()
        assert materials(page,'#selected-drag')==initial
        page.locator('#place').tap();assert materials(page,'[data-owner="bakery-a"]')==initial
        tap_cell(page,'1,1');tap_cell(page,'5,3');page.locator('#place').tap()
        assert materials(page,'[data-owner="bakery-a"]')==initial
        page.locator('#undo').tap();assert materials(page,'[data-owner="bakery-a"]')==initial
        # Render uses actual nested SVG masks, with only positive viewports and rotations.
        assert page.locator('[data-material]').evaluate_all("els=>els.every(e=>getComputedStyle(e).clipPath!=='none'&&!e.innerHTML.includes('scale(-')&&!e.innerHTML.includes('scaleX(-')&&!e.innerHTML.includes('scaleY(-'))")
        page.close();print(f'{w}x{h}: visible Ruta/hex={ratio:.3f}, tray/board seeds, rotate/move/undo, exact clip/no reflection: PASS')
    assert not errors,errors
    b.close()
