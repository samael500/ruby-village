"""Illustrated scene regression. Run against `npm run preview` to check production base URLs."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4173/ruby-village/'
SHOTS=Path(sys.argv[2]) if len(sys.argv)>2 else Path('/tmp/ruby-art-shots')
SHOTS.mkdir(parents=True,exist_ok=True)
def center(page,selector):
    b=page.locator(selector).bounding_box()
    return b['x']+b['width']/2,b['y']+b['height']/2
with sync_playwright() as p:
    browser=p.chromium.launch();errors=[]
    for width,height in [(1280,720),(844,390),(390,844),(915,412),(740,360)]:
        page=browser.new_page(viewport={'width':width,'height':height},has_touch=True)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL);page.locator('[data-level="gate"]').tap();page.locator('#story-action').tap()
        assert page.evaluate('document.documentElement.scrollWidth===innerWidth && document.documentElement.scrollHeight===innerHeight')
        # Every cell centre still hits its cell, including cells behind the character.
        assert page.locator('[data-cell]').evaluate_all('els=>els.every(el=>{const b=el.getBoundingClientRect();return document.elementFromPoint(b.x+b.width/2,b.y+b.height/2)?.closest("[data-cell]")===el;})')
        for asset in ['meadow','ruta-house','garden-gate','ruta-idle']:
            assert page.request.get(URL+'assets/level-1/'+asset+'.png').ok
        page.evaluate('()=>Promise.all([...document.querySelectorAll("#board image")].map(el=>new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=reject;img.src=el.getAttribute("href");})))')
        grid=page.locator('[data-cell]').evaluate_all('els=>{const b=els.map(e=>e.getBoundingClientRect());return {l:Math.min(...b.map(x=>x.left)),r:Math.max(...b.map(x=>x.right)),t:Math.min(...b.map(x=>x.top)),b:Math.max(...b.map(x=>x.bottom))};}')
        for box in page.locator('[data-decoration]').evaluate_all('els=>els.map(e=>{const b=e.getBoundingClientRect();return {l:b.left,r:b.right,t:b.top,b:b.bottom};})'):
            assert box['r']<=grid['l'] or box['l']>=grid['r'] or box['b']<=grid['t'] or box['t']>=grid['b']
        page.screenshot(path=str(SHOTS/f'gate-{width}x{height}.png'))
        # Drag on the decorated board uses the same finger offset and hit geometry.
        page.locator('#settings-open').tap();page.locator('#mode').select_option('drag');page.locator('#settings-close').tap()
        session=page.context.new_cdp_session(page)
        x,y=center(page,'[data-piece="pair"]');a,b=center(page,'[data-cell="1,2"]')
        radius=page.locator('[data-cell="1,2"]').bounding_box()['height']/2
        session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
        for step in range(1,11):
            session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(a-x)*step/10,'y':y+(b+max(42,radius*1.6)-y)*step/10}]})
            page.wait_for_timeout(20)
        page.wait_for_timeout(100)
        session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
        page.evaluate('()=>new Promise(requestAnimationFrame)')
        assert page.locator('[data-piece="pair"].placed').count()==1
        page.locator('#undo').tap()
        assert page.locator('.piece.placed').count()==0
        page.locator('#settings-open').tap();page.locator('#mode').select_option('select');page.locator('#settings-close').tap()
        idle=page.locator('#ruta-idle').get_attribute('x'),page.locator('#ruta-idle').get_attribute('y')
        for piece,q in [('pair',1),('single',3)]:
            page.locator(f'[data-piece="{piece}"]').tap()
            page.locator('#left').tap();page.locator('#right').tap()
            page.touchscreen.tap(*center(page,f'[data-cell="{q},2"]'));page.locator('#place').tap()
        page.screenshot(path=str(SHOTS/f'road-{width}x{height}.png'))
        page.locator('#check').tap();expect(page.locator('#story')).to_be_visible()
        assert page.locator('#story-title').inner_text()=='Дорога готова!'
        assert page.locator('#ruta-marker').count()==0
        assert idle==(page.locator('#ruta-idle').get_attribute('x'),page.locator('#ruta-idle').get_attribute('y'))
        page.locator('#story-action').tap();page.reload()
        assert page.locator('[data-level="garden"]').is_enabled()
        page.locator('[data-level="garden"]').tap()
        assert page.locator('svg.ruta-portrait').is_visible()
        assert not page.locator('#story-ruta').is_visible()
        page.close()
    assert not errors,errors
    browser.close()
    print('Production assets, cell hit targets, decoration bounds, touch placement/rotation, static victory, progress and portrait restoration: PASS')
