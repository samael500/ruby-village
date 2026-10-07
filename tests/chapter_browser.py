"""Run with Vite serving, Node 22.18+ on PATH, and Python Playwright installed."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/'
ROOT=Path(__file__).resolve().parents[1]
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts'; console.log(JSON.stringify(levels));"],cwd=ROOT,text=True))
KEY='ruby-village:chapter-1:v1'

def center(page,selector):
    b=page.locator(selector).bounding_box();assert b,selector
    return b['x']+b['width']/2,b['y']+b['height']/2

def enter(page,id,touch=False):
    target=page.locator(f'[data-level="{id}"]')
    target.tap() if touch else target.click()
    expect(page.locator('#story')).to_be_visible()
    page.locator('#story-action').tap() if touch else page.locator('#story-action').click()

def settings(page,selector,value=None,touch=False):
    page.touchscreen.tap(*center(page,'#settings-open')) if touch else page.locator('#settings-open').click()
    if value is None:page.touchscreen.tap(*center(page,selector)) if touch else page.locator(selector).click()
    else:page.locator(selector).select_option(value)
    if page.locator('#settings-panel').is_visible():page.touchscreen.tap(*center(page,'#settings-close')) if touch else page.locator('#settings-close').click()

def solve(page,level,touch=False):
    for id,p in level['solution'].items():
        button=page.locator(f'[data-piece="{id}"]')
        button.tap() if touch else button.click()
        for _ in range(p['turns']):page.locator('#right').tap() if touch else page.locator('#right').click()
        q,r=p['anchor']['q'],p['anchor']['r'];target=page.locator(f'[data-cell="{q},{r}"]')
        target.tap() if touch else page.mouse.click(*center(page,f'[data-cell="{q},{r}"]'))
        expect(page.locator('[data-preview="valid"]')).to_have_count(1)
        if not touch:page.mouse.move(*center(page,'#place'),steps=15)
        page.locator('#place').tap() if touch else page.locator('#place').click()
        assert page.locator(f'[data-piece="{id}"].placed').count()==1
    print('Checking',level['id'],'touch',touch,flush=True)
    page.locator('#check').tap() if touch else page.locator('#check').click()
    page.locator('#check').evaluate('(el)=>{el.dispatchEvent(new MouseEvent("click"));el.dispatchEvent(new MouseEvent("click"));}')
    expect(page.locator('#story')).to_be_visible(timeout=15000)
    assert page.locator('#story-text').inner_text()==level['outro']
    assert page.locator('.cell.path').count()>1
    if level['id']=='mill':
        assert page.locator('[data-wheel="running"]').count()==1
        if page.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches'):
            assert page.locator('[data-wheel="running"]').evaluate('(el)=>getComputedStyle(el).animationName')=='none'
    page.locator('#story-action').tap() if touch else page.locator('#story-action').click()

def fit(page):
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth && document.documentElement.scrollHeight<=innerHeight')
    assert page.locator('button:visible, select:visible').evaluate_all('''els=>els.every(e=>{let r=e.getBoundingClientRect();return r.width>=48&&r.height>=48&&r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight})''')
    if page.locator('#field').is_visible():
        assert page.locator('[data-cell] > polygon').evaluate_all('''els=>els.every(e=>{let r=e.getBoundingClientRect(),p=document.querySelector('#field').getBoundingClientRect();return r.left>=p.left&&r.right<=p.right&&r.top>=p.top&&r.bottom<=p.bottom})''')

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':740,'height':360})
    errors=[];page.on('pageerror',lambda error:(errors.append(str(error)),print('Browser error:',error,flush=True)))
    page.goto(URL);fit(page)
    assert page.locator('[data-level="garden"]').is_disabled()
    assert page.locator('[data-level="mill"]').is_disabled()
    for index,level in enumerate(LEVELS):
        enter(page,level['id']);solve(page,level)
        assert page.locator('[data-road][data-complete="true"]').count()==index+1
        page.reload()
        assert page.locator('[data-road][data-complete="true"]').count()==index+1
        if index<2:assert page.locator(f'[data-level="{LEVELS[index+1]["id"]}"]').is_enabled()
    print('All three levels through real controls, outcomes, wheel, sequential unlock and reload: PASS')
    for width,height in [(1280,720),(915,412),(740,360),(640,360)]:
        page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(80);fit(page)
        page.screenshot(path=f'/tmp/ruby-chapter-map-{width}.png')
        for level in LEVELS:
            enter(page,level['id']);page.wait_for_timeout(80);fit(page)
            if width==640:page.screenshot(path=f'/tmp/ruby-chapter-{level["id"]}-640.png')
            settings(page,'#map-return')
    enter(page,'gate');settings(page,'#clear');settings(page,'#map-return')
    assert page.locator('[data-road][data-complete="true"]').count()==3
    # Sandbox cannot change chapter progress.
    before=page.evaluate('(key)=>localStorage.getItem(key)',KEY)
    page.locator('#sandbox-open').click();settings(page,'#size','11,7')
    assert page.locator('[data-cell]').count()==77
    settings(page,'#map-return');assert page.evaluate('(key)=>localStorage.getItem(key)',KEY)==before
    page.locator('#reset-open').click();page.locator('#reset-cancel').click()
    assert page.locator('[data-road][data-complete="true"]').count()==3
    page.locator('#reset-open').click();page.locator('#reset-confirm').click();page.reload()
    assert page.locator('[data-road][data-complete="true"]').count()==0
    assert page.locator('[data-level="garden"]').is_disabled()
    # Corrupt and denied storage recover to an open first puzzle.
    page.evaluate('(key)=>localStorage.setItem(key,"broken{")',KEY);page.reload()
    assert page.locator('[data-level="gate"]').is_enabled()
    assert page.locator('[data-level="garden"]').is_disabled()
    print('Responsive map/levels, replay/restart, sandbox isolation, confirmed reset, corrupt save: PASS')
    # Touch solves include rotated large pieces; reduced motion skips walking animation.
    context=browser.new_context(viewport={'width':640,'height':360},has_touch=True,is_mobile=True,reduced_motion='reduce')
    touch=context.new_page();touch.on('pageerror',lambda error:(errors.append(str(error)),print('Browser error:',error,flush=True)));touch.goto(URL)
    for level in LEVELS:enter(touch,level['id'],True);solve(touch,level,True)
    enter(touch,'mill',True);settings(touch,'#mode','drag',touch=True)
    session=context.new_cdp_session(touch)
    def touch_drag(id,q,r,cancel=False,selected=False,source=None):
        x,y=center(touch,source or ('#selected-drag' if selected else f'[data-piece="{id}"]'));a,b=center(touch,f'[data-cell="{q},{r}"]')
        radius=touch.locator(f'[data-cell="{q},{r}"]').bounding_box()['height']/2
        session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
        # Model a finger travelling across the screen, not a zero-time fling.
        for step in range(1,11):
            session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(a-x)*step/10,'y':y+(b+max(42,radius*1.6)-y)*step/10}]})
            touch.wait_for_timeout(20)
        touch.wait_for_timeout(100)
        session.send('Input.dispatchTouchEvent',{'type':'touchCancel' if cancel else 'touchEnd','touchPoints':[]})
        touch.evaluate('()=>new Promise(requestAnimationFrame)')
    touch_drag('bridge',5,1,True)
    assert touch.locator('.piece.placed').count()==0
    touch.locator('#other').tap()
    touch.locator('[data-piece="bridge"]').tap();touch.locator('#left').tap();touch.locator('#right').tap()
    fit(touch)
    touch_drag('bridge',5,1,selected=True)
    assert touch.locator('[data-piece="bridge"].placed').count()==1
    touch_drag('mill-a',2,0)
    assert touch.locator('[data-piece="mill-a"].placed').count()==1
    touch.locator('[data-piece="mill-b"]').tap()
    for _ in range(3):touch.locator('#right').tap()
    touch_drag('mill-b',8,2,selected=True)
    assert touch.locator('[data-piece="mill-b"].placed').count()==1
    touch_drag('bridge',5,3,source='[data-cell="5,1"]')
    assert 'Мост' in touch.locator('[data-cell="5,1"]').get_attribute('aria-label')
    touch_drag('bridge',5,3,cancel=True,source='[data-cell="5,1"]')
    assert 'Мост' in touch.locator('[data-cell="5,1"]').get_attribute('aria-label')
    settings(touch,'#map-return',touch=True);enter(touch,'mill',True)
    touch_drag('mill-extra',5,1) # Ordinary stones cannot cover water.
    assert touch.locator('.piece.placed').count()==0
    print('Touch large figures/rotations, bridge drag/cancel, water rejection, reduced motion: PASS')
    denied=browser.new_context(viewport={'width':740,'height':360},reduced_motion='reduce')
    denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('denied')}})")
    offline=denied.new_page();offline.goto(URL);enter(offline,'gate');solve(offline,LEVELS[0])
    assert offline.locator('[data-level="garden"]').is_enabled()
    assert 'только' in offline.locator('#save-status').inner_text()
    offline.reload();assert offline.locator('[data-level="garden"]').is_disabled()
    delayed=browser.new_context(viewport={'width':740,'height':360})
    delayed.add_init_script('const raf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=(cb)=>raf(ts=>cb(ts-50));')
    animation=delayed.new_page();animation.on('pageerror',lambda error:errors.append(str(error)));animation.goto(URL)
    enter(animation,'gate');solve(animation,LEVELS[0])
    enter(animation,'garden');solve(animation,LEVELS[1])
    print('Animation tolerates an initial frame timestamp before the click handler: PASS')
    assert not errors,errors
    print('Storage denied: play and session unlock work. No browser errors.')
    browser.close()
