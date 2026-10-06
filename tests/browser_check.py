"""Optional browser checks: pip install playwright && playwright install chromium.
Start npm run dev, then python tests/browser_check.py [base URL].
"""
import sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/'

def center(page, selector):
    b=page.locator(selector).bounding_box()
    assert b, selector
    return (b['x']+b['width']/2,b['y']+b['height']/2)

def cell(q,r): return f'[data-cell="{q},{r}"]'
def click_cell(page,q,r):
    x,y=center(page,cell(q,r)); page.mouse.click(x,y)
def place(page,piece,q,r):
    page.locator(f'[data-piece="{piece}"]').click()
    click_cell(page,q,r)
    assert page.locator('[data-preview="valid"]').count()==1
    preview=page.locator('[data-preview]').inner_html()
    # A person moves across the board to reach the confirmation button.
    page.mouse.move(*center(page,'#place'),steps=30)
    assert page.locator('[data-preview]').inner_html()==preview, 'Clicked destination moved while reaching for Place'
    assert page.locator('#place').is_enabled()
    page.locator('#place').click()
    assert page.locator(f'[data-piece="{piece}"].placed').count()==1
    assert piece_name(piece) in page.locator(cell(q,r)).get_attribute('aria-label')

def piece_name(piece):
    return {'line':'Три в ряд','bend':'Уголок','cluster':'Четвёрка','one-a':'Камешек 1','one-b':'Камешек 2'}[piece]

def drag_to(page,source,target):
    x,y=center(page,source); a,b=center(page,target)
    page.mouse.move(x,y);page.mouse.down();page.mouse.move(a,b,steps=12);page.mouse.up()

def setting(page, selector, value=None):
    page.locator('#settings-open').click()
    if value is None:
        page.locator(selector).click()
    else:
        page.locator(selector).select_option(value)
    page.locator('#settings-close').click()

def check_layout(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth && document.documentElement.scrollHeight <= innerHeight')
    assert page.locator('button:visible, select:visible').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().height>=48 && e.getBoundingClientRect().width>=48)')
    assert page.locator('#board [data-cell] polygon').evaluate_all('''els=>els.every(e=>{const b=e.getBoundingClientRect(); const p=document.querySelector('#field').getBoundingClientRect();return b.x>=p.x&&b.y>=p.y&&b.right<=p.right&&b.bottom<=p.bottom})''')
    assert page.locator('button:visible, select:visible, #status').evaluate_all('''els=>els.every(e=>{const r=e.getBoundingClientRect();return r.x>=0&&r.y>=0&&r.right<=innerWidth&&r.bottom<=innerHeight})''')

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1280,'height':720})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(URL)
    for width,height in [(640,360),(800,450),(960,540),(1280,720),(915,412),(740,360)]:
        page.set_viewport_size({'width':width,'height':height})
        for size,count in [('7,5',35),('9,6',54),('11,7',77)]:
            setting(page,'#size',size)
            page.wait_for_timeout(100)
            assert page.locator('[data-cell]').count()==count
            check_layout(page)
            print(f'Layout {width}x{height}, {size}: {page.locator("#metric").text_content()}')
        setting(page,'#size','9,6')
        page.screenshot(path=f'/tmp/ruby-village-{width}.png')
    # Settings must close without losing a pending placement, including Escape.
    page.set_viewport_size({'width':640,'height':360})
    page.locator('[data-piece="line"]').click();click_cell(page,1,1)
    pending=page.locator('[data-preview]').inner_html()
    page.locator('#settings-open').click()
    page.keyboard.press('Escape')
    assert not page.locator('#settings-panel').is_visible()
    assert page.locator('[data-preview]').inner_html()==pending
    page.locator('#other').click()
    assert page.locator('#tray').is_visible()
    # Hover previews before the first click; a subsequent click changes the pinned cell.
    for width,height in [(640,360),(800,450),(960,540),(1280,720),(915,412),(740,360)]:
        page.set_viewport_size({'width':width,'height':height})
        field_before=page.locator('#field').bounding_box()
        page.locator('[data-piece="one-a"]').click()
        check_layout(page)
        assert page.locator('#field').bounding_box()==field_before, 'Choosing a piece must not resize the field'
        assert page.locator('#tray').is_hidden()
        assert page.locator('#selection-actions').is_visible()
        page.mouse.move(*center(page,cell(1,1)),steps=10)
        hover_preview=page.locator('[data-preview]').inner_html()
        page.mouse.move(*center(page,cell(2,1)),steps=10)
        assert page.locator('[data-preview]').inner_html()!=hover_preview
        click_cell(page,2,1)
        pinned_preview=page.locator('[data-preview]').inner_html()
        page.mouse.move(*center(page,cell(3,1)),steps=10)
        assert page.locator('[data-preview]').inner_html()==pinned_preview
        click_cell(page,3,1)
        assert page.locator('[data-preview]').inner_html()!=pinned_preview
        page.mouse.move(*center(page,'#place'),steps=30)
        assert page.locator('#place').is_enabled()
        page.locator('#place').click()
        assert 'Камешек 1' in page.locator(cell(3,1)).get_attribute('aria-label')
        setting(page,'#clear')
        place(page,'line',0,1)
        setting(page,'#clear')
    page.set_viewport_size({'width':915,'height':412})
    place(page,'line',0,1)
    # Own cells can be selected and edited, then undo restores the position.
    click_cell(page,0,1)
    original_preview=page.locator('[data-preview]').inner_html()
    page.mouse.move(*center(page,'#right'),steps=30)
    assert page.locator('[data-preview]').inner_html()==original_preview
    page.locator('#right').click();page.locator('#place').click()
    page.locator('#undo').click()
    assert 'Три в ряд' in page.locator(cell(2,1)).get_attribute('aria-label')
    # Overlap and outside bounds are visibly invalid.
    page.locator('[data-piece="bend"]').click();click_cell(page,1,2)
    page.locator('#left').click()
    click_cell(page,8,0)
    assert page.locator('[data-preview="invalid"]').count()==1
    assert page.locator('#place').is_disabled()
    page.keyboard.press('Escape')
    click_cell(page,0,1);page.locator('#return').click()
    assert page.locator('.piece.placed').count()==0
    page.locator('#undo').click();assert page.locator('.piece.placed').count()==1
    setting(page,'#clear');assert page.locator('.piece.placed').count()==0
    page.locator('#undo').click();assert page.locator('.piece.placed').count()==1
    setting(page,'#mode','drag')
    drag_to(page,'[data-piece="one-a"]',cell(3,2))
    assert page.locator('[data-piece="one-a"].placed').count()==1
    drag_to(page,cell(3,2),cell(4,2))
    assert 'Камешек 1' in page.locator(cell(4,2)).get_attribute('aria-label')
    # Invalid drag returns to committed state.
    drag_to(page,cell(4,2),cell(0,1))
    assert 'Камешек 1' in page.locator(cell(4,2)).get_attribute('aria-label')
    page.locator('#undo').click()
    assert 'Камешек 1' in page.locator(cell(3,2)).get_attribute('aria-label')
    # Pointer cancellation does not remove the original instance.
    x,y=center(page,cell(3,2));a,b=center(page,cell(4,3))
    page.mouse.move(x,y);page.mouse.down();page.mouse.move(a,b,steps=5)
    page.locator('#app').dispatch_event('pointercancel',{'pointerId':1,'isPrimary':True,'pointerType':'mouse'})
    page.mouse.up()
    assert 'Камешек 1' in page.locator(cell(3,2)).get_attribute('aria-label')
    before=page.locator('.piece.placed').count()
    page.set_viewport_size({'width':412,'height':915});page.wait_for_timeout(100)
    check_layout(page);assert page.locator('.portrait').is_visible()
    assert page.locator('.piece.placed').count()==before
    page.set_viewport_size({'width':915,'height':412});page.wait_for_timeout(100)
    assert page.locator('.piece.placed').count()==before
    setting(page,'#size','7,5')
    assert page.locator('.piece.placed').count()==0
    assert page.locator('#undo').is_disabled()
    setting(page,'#mode','select')
    page.locator('#check').click();assert 'Пока дорога не соединена' in page.locator('#status').inner_text()
    # Middle row r=2 has q=-1..5. Endpoints alone plus 5 paved cells suffice.
    place(page,'line',0,2);place(page,'one-a',3,2);place(page,'one-b',4,2)
    page.locator('#check').click();assert 'Дорога готова!' in page.locator('#status').inner_text()
    assert page.locator('.cell.path').count()==7
    assert page.locator('.piece.placed').count()==3
    assert not errors, errors
    print('Mouse selection, edit, rotation, return, drag, invalid drop, cancel, undo, clear, resize, path: PASS')
    # Real browser touch events, including the target lifted above the finger.
    context=browser.new_context(viewport={'width':640,'height':360},has_touch=True,is_mobile=True)
    touch=context.new_page();touch.goto(URL)
    touch.locator('[data-piece="one-a"]').tap();touch.locator(cell(2,2)).tap();touch.locator('#place').tap()
    assert touch.locator('.piece.placed').count()==1
    setting(touch,'#mode','drag')
    session=context.new_cdp_session(touch)
    x,y=center(touch,'[data-piece="line"]');a,b=center(touch,cell(1,1))
    radius=touch.locator(cell(1,1)).bounding_box()['height']/2
    lift=max(42,radius*1.6)
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':a,'y':b+lift}]})
    assert touch.locator('[data-preview="valid"]').count()==1
    session.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    assert touch.locator('[data-piece="line"].placed').count()==1
    assert 'Три в ряд' in touch.locator(cell(1,1)).get_attribute('aria-label')
    x,y=center(touch,cell(1,1))
    session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':a+50,'y':b+lift}]})
    session.send('Input.dispatchTouchEvent',{'type':'touchCancel','touchPoints':[]})
    assert touch.locator('[data-piece="line"].placed').count()==1
    assert 'Три в ряд' in touch.locator(cell(1,1)).get_attribute('aria-label')
    assert touch.evaluate('scrollX===0 && scrollY===0')
    print('Touch select, drag offset and touchCancel: PASS')
    browser.close()
