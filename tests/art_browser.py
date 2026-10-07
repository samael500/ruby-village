"""Courtyard regression; pass a Vite/production base URL and optional screenshot directory."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4173/ruby-village/'
SHOTS=Path(sys.argv[2]) if len(sys.argv)>2 else Path('/tmp/ruby-art-shots')
SHOTS.mkdir(parents=True,exist_ok=True)
ROOT=Path(__file__).resolve().parents[1]
LEVEL=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels[0]));"],cwd=ROOT,text=True))
KEY='ruby-village:chapter-1:v1'
def center(page,selector):
    b=page.locator(selector).bounding_box();assert b,selector
    return b['x']+b['width']/2,b['y']+b['height']/2

def anchors(page):
    # Use actual image source anchors and SVG screen transform, not a DOM data claim.
    return page.evaluate('''()=>{
      const feet=document.querySelector('#ruta-idle'),point=new DOMPoint(+feet.getAttribute('x')+.55*feet.width.baseVal.value,+feet.getAttribute('y')+.965*feet.height.baseVal.value).matrixTransform(feet.getScreenCTM());
      const cell=document.querySelector('[data-cell="0,1"] > polygon').getBoundingClientRect();
      return Math.hypot(point.x-cell.x-cell.width/2,point.y-cell.y-cell.height/2)<.1;
    }''')
def fit(page):
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight')
    assert page.locator('button:visible').evaluate_all('els=>els.every(e=>{const b=e.getBoundingClientRect();return b.width>=48&&b.height>=48&&b.left>=0&&b.right<=innerWidth&&b.top>=0&&b.bottom<=innerHeight;})')
    assert anchors(page)
    assert page.evaluate('''()=>{
      const bg=document.querySelector('#court-background'),r=bg.getBoundingClientRect(),board=document.querySelector('#board').getBoundingClientRect();
      const artRatio=bg.width.baseVal.value/bg.height.baseVal.value;
      return Math.abs(r.width/r.height-artRatio)<1e-6 && r.left>=board.left-.1&&r.right<=board.right+.1&&r.top>=board.top-.1&&r.bottom<=board.bottom+.1 && !document.querySelector('#scene-house,#scene-gate,[data-environment]');
    }''')
    assert page.locator('[data-grid] path').count()==2
    assert page.locator('[data-approach]').count()==0

def settings(page,value):
    page.get_by_role('button',name='Настройки',exact=True).tap();page.locator('#mode').select_option(value);page.locator('#settings-close').tap()
with sync_playwright() as p:
    browser=p.chromium.launch();errors=[]
    for width,height in [(1280,720),(844,390),(390,844),(915,412),(740,360)]:
        page=browser.new_page(viewport={'width':width,'height':height},has_touch=True)
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(URL)
        # Legacy completion data has no coordinates and must survive this redesign.
        old=json.dumps({'version':1,'completed':['gate','garden','mill']})
        page.evaluate('([key,value])=>localStorage.setItem(key,value)',[KEY,old]);page.reload()
        page.locator('[data-level="gate"]').tap();page.locator('#story-action').tap()
        fit(page)
        assert page.locator('[data-cell][data-terrain="ground"]').evaluate_all('els=>els.every(el=>{const b=el.querySelector("polygon").getBoundingClientRect();return document.elementFromPoint(b.x+b.width/2,b.y+b.height/2)?.closest("[data-cell]")===el;})')
        for asset in ['courtyard-landscape','courtyard-portrait','charoite-texture','ruta-idle']:assert page.request.get(URL+'assets/level-1/v4/'+asset+'.png').ok
        page.evaluate('()=>Promise.all([...document.querySelectorAll("#board image")].map(el=>new Promise((resolve,reject)=>{const img=new Image();img.onload=resolve;img.onerror=reject;img.src=el.getAttribute("href");})))')
        page.screenshot(path=str(SHOTS/f'gate-{width}x{height}.png'))
        assert page.locator('#board .landmark').count()==0
        page.locator('#check').tap();expect(page.locator('#status')).to_have_class('feedback')
        assert page.locator('#status').bounding_box()['height']>20
        page.locator('#scene-help').tap();page.locator('#help-close').tap()
        # Hidden visual labels must not turn the header settings into an unnamed button.
        settings_button=page.get_by_role('button',name='Настройки',exact=True)
        expect(settings_button).to_be_visible()
        settings_button.focus();page.keyboard.press('Enter')
        expect(page.locator('#settings-panel')).to_be_visible()
        page.keyboard.press('Escape');expect(page.locator('#settings-panel')).not_to_be_visible()
        # Recover from an invalid drop by clicking/tapping a valid cell under the toast.
        for touch in [False,True]:
            page.locator('[data-piece="gate-a"]').tap() if touch else page.locator('[data-piece="gate-a"]').click()
            action=page.touchscreen.tap if touch else page.mouse.click
            action(*center(page,'[data-cell="4,4"] > polygon'))
            expect(page.locator('[data-preview]')).to_have_attribute('data-preview','invalid')
            expect(page.locator('#place')).to_be_disabled()
            expect(page.locator('#status')).to_have_class('feedback')
            action(*center(page,'[data-cell="3,0"] > polygon'))
            expect(page.locator('[data-preview]')).to_have_attribute('data-preview','valid')
            expect(page.locator('#place')).to_be_enabled()
            page.locator('#place').tap() if touch else page.locator('#place').click()
            assert page.locator('[data-cell="3,0"]').get_attribute('data-owner')=='gate-a'
            page.locator('#undo').tap() if touch else page.locator('#undo').click()
            assert page.locator('[data-owner="gate-a"]').count()==0
        # The start remains clickable while Ruta is anchored to it.

        page.locator('[data-piece="single"]').tap();fit(page)
        page.touchscreen.tap(*center(page,'[data-cell="0,1"] > polygon'));page.locator('#place').tap()
        assert page.locator('#tray .piece:visible').count()==2
        page.set_viewport_size({'width':height,'height':width});page.wait_for_timeout(100)
        assert anchors(page);assert page.locator('[data-cell="0,1"]').get_attribute('data-owner')=='single'
        page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(100)
        page.touchscreen.tap(*center(page,'[data-cell="0,1"] > polygon'));page.locator('#return').tap()
        assert page.locator('#tray .piece:visible').count()==3
        settings(page,'drag')
        session=page.context.new_cdp_session(page)
        def drag(cancel=False):
            x,y=center(page,'[data-piece="gate-a"]');a,b=center(page,'[data-cell="1,1"] > polygon')
            radius=page.locator('[data-cell="1,1"] > polygon').bounding_box()['height']/2
            session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
            for step in range(1,11):
                session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(a-x)*step/10,'y':y+(b+max(42,radius*1.6)-y)*step/10}]});page.wait_for_timeout(20)
            page.wait_for_timeout(100)
            session.send('Input.dispatchTouchEvent',{'type':'touchCancel' if cancel else 'touchEnd','touchPoints':[]})
            page.evaluate('()=>new Promise(requestAnimationFrame)')
        drag(True);assert page.locator('[data-owner="gate-a"]').count()==0
        page.locator('#other').tap();drag()
        assert page.locator('[data-owner="gate-a"]').count()==3
        page.locator('#undo').tap();assert page.locator('[data-owner="gate-a"]').count()==0
        settings(page,'select')
        idle=page.locator('#ruta-idle').get_attribute('x'),page.locator('#ruta-idle').get_attribute('y')
        for id,placement in LEVEL['solution'].items():
            page.locator(f'[data-piece="{id}"]').tap()
            page.locator('#left').tap();page.locator('#right').tap()
            q,r=placement['anchor']['q'],placement['anchor']['r']
            page.touchscreen.tap(*center(page,f'[data-cell="{q},{r}"] > polygon'));page.locator('#place').tap()
        page.screenshot(path=str(SHOTS/f'road-{width}x{height}.png'))
        page.locator('#check').tap();expect(page.locator('#story')).to_be_visible()
        assert page.locator('#story-title').inner_text()=='Дорога готова!'
        assert page.locator('#ruta-marker').count()==0
        assert idle==(page.locator('#ruta-idle').get_attribute('x'),page.locator('#ruta-idle').get_attribute('y'))
        page.locator('#story-action').tap();page.reload()
        assert json.loads(page.evaluate('(key)=>localStorage.getItem(key)',KEY))==json.loads(old)
        page.locator('[data-level="garden"]').tap();assert page.locator('svg.ruta-portrait').is_visible()
        page.close()
    page=browser.new_page(viewport={'width':844,'height':390});page.goto(URL);page.locator('#sandbox-open').click()
    page.locator('#settings-open').click();page.locator('#size').select_option('11,7');page.locator('#settings-close').click()
    assert page.locator('[data-cell]').count()==77
    page.screenshot(path=str(SHOTS/'sandbox-11x7-844x390.png'))
    assert not errors,errors
    browser.close()
    print('Design v4: anchors, visible ground cells, original progress, touch/drag/cancel/rotate/undo, resize, victory and sandbox: PASS')
