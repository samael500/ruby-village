import json
from pathlib import Path
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
 b=p.chromium.launch();q=b.new_page(viewport={'width':844,'height':390},has_touch=True,is_mobile=True)
 q.add_init_script("localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:['gate'],introSeen:['gate','garden']}))")
 q.goto('http://127.0.0.1:5180/ruby-village/');q.locator('#continue-game').tap();q.locator('[data-piece="garden-a"]').tap()
 q.evaluate("window.rotateEvents=[];for(const type of ['pointerdown','pointerup','click'])document.querySelector('#right').addEventListener(type,e=>window.rotateEvents.push({type,time:performance.now()}))")
 c=q.context.new_cdp_session(q);results=[]
 for gap in [100,150,250,500]:
  before=q.locator('[data-piece="garden-a"]').get_attribute('data-icon');box=q.locator('#right').bounding_box()
  for i in range(12):
   c.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':box['x']+box['width']/2,'y':box['y']+box['height']/2,'id':1}]});q.wait_for_timeout(50)
   c.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});q.wait_for_timeout(gap)
  after=q.locator('[data-piece="garden-a"]').get_attribute('data-icon');events=q.evaluate('window.rotateEvents.splice(0)');clicks=sum(e['type']=='click' for e in events)
  results.append({'gapMs':gap,'holdMs':50,'taps':12,'clicks':clicks,'before':before,'after':after,'events':events})
  assert clicks==12,(gap,events);assert after==before,(gap,before,after)
 q.locator('#right').focus();q.keyboard.press('Enter');q.keyboard.press('Space');q.locator('#right').click()
 assert q.locator('[data-piece="garden-a"]').get_attribute('data-icon')=='garden:3:true:false'
 output=Path(__file__).resolve().parents[2]/'docs/chapter-1-rc/evidence/fast-touch-buttons';output.mkdir(parents=True,exist_ok=True)
 (output/'report.json').write_text(json.dumps({'touch':results,'mouseEnterSpaceAfterTouch':'pass','scope':'actual native Chromium CDP input; no physical phone claimed'},indent=2)+'\n')
 print('PASS 48 native touch taps at100/150/250/500ms gaps, followed by Enter, Space and mouse click');b.close()
