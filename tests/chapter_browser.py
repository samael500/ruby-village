"""Eight puzzles through public UI, story/progress migration, touch and fixed layouts."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4173/ruby-village/'
SHOTS=Path(sys.argv[2]) if len(sys.argv)>2 else Path('/tmp/ruby-chapter-shots')
SHOTS.mkdir(parents=True,exist_ok=True)
ROOT=Path(__file__).resolve().parents[1]
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels));"],cwd=ROOT,text=True))
KEY='ruby-village:chapter-1:v1'
def center(page,selector):
 b=page.locator(selector).bounding_box();assert b,selector
 return b['x']+b['width']/2,b['y']+b['height']/2
def click(page,selector,touch=False):
 page.locator(selector).tap() if touch else page.locator(selector).click()
def skip(page,touch=False):
 if page.locator('#story').is_visible():click(page,'#story-skip',touch)
def enter(page,id,touch=False):
 click(page,f'[data-level="{id}"]',touch)
 if page.locator('#story').is_visible():
  fit(page)
  if id=='stream':
   click(page,'#story-action',touch);click(page,'#story-action',touch)
   assert page.locator('#bridge-guide').is_visible();fit(page)
 skip(page,touch)
def settings(page,selector,value=None,touch=False):
 click(page,'#settings-open',touch)
 if value is None:click(page,selector,touch)
 else:page.locator(selector).select_option(value)
 if page.locator('#settings-panel').is_visible():click(page,'#settings-close',touch)
def place(page,id,p,touch=False):
 click(page,f'[data-piece="{id}"]',touch)
 for _ in range(p['turns']):click(page,'#right',touch)
 q,r=p['anchor']['q'],p['anchor']['r'];a,b=center(page,f'[data-cell="{q},{r}"] > polygon')
 page.touchscreen.tap(a,b) if touch else page.mouse.click(a,b)
 expect(page.locator('[data-preview="valid"]')).to_have_count(1)
 click(page,'#place',touch)
 assert page.locator(f'[data-piece="{id}"].placed').count()==1

def solve(page,level,touch=False,first=True,resize_walk=False):
 click(page,'#check',touch);assert not page.locator('#story').is_visible()
 assert 'Пока дорога' in page.locator('#status').inner_text()
 for id,p in level['solution'].items():place(page,id,p,touch)
 if level['id']=='post':assert page.locator('[data-piece="post-extra"]:visible').count()==1
 if first:
  size=page.viewport_size;page.screenshot(path=str(SHOTS/f'road-{level["id"]}-{size["width"]}x{size["height"]}.png'))
 click(page,'#check',touch)
 if resize_walk:
  expect(page.locator('#ruta-marker')).to_be_visible()
  assert page.locator('#board #ruta-idle').count()==0
  owners=page.locator('[data-owner]:not([data-owner=""])').count()
  for w,h in [(390,844),(915,412)]:
   page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(80)
   assert page.locator('#board #ruta-idle,#board #ruta-marker').count()==1
   assert page.locator('[data-owner]:not([data-owner=""])').count()==owners
   fit(page)
 page.locator('#check').evaluate('el=>{el.dispatchEvent(new MouseEvent("click"));el.dispatchEvent(new MouseEvent("click"));}')
 expect(page.locator('#story')).to_be_visible(timeout=15000)
 assert page.locator('.cell.path').count()>1
 assert page.locator('[data-victory-event]').count()==1;fit(page)
 assert page.locator('#board #ruta-idle,#board #ruta-marker').count()==1
 if first:assert page.locator('#story-text').inner_text()==level['outro'].split('\n')[0].split(': ',1)[1]
 if level['id']=='mill':
  assert page.locator('[data-wheel="running"]').count()==1
  if page.evaluate('matchMedia("(prefers-reduced-motion:reduce)").matches'):
   assert page.locator('[data-wheel="running"]').evaluate('el=>getComputedStyle(el).animationName')=='none'
 skip(page,touch)
 if first and level['id']=='forest':
  expect(page.locator('#story-title')).to_have_text('Глава «За калитку» пройдена')
  page.screenshot(path=str(SHOTS/'chapter-ending.png'));click(page,'#story-action',touch)
  assert 'Письма через лес' in page.locator('#story-text').inner_text()
  page.screenshot(path=str(SHOTS/'next-chapter-announcement.png'));skip(page,touch)
 expect(page.locator('#chapter-map')).to_be_visible()

def fit(page):
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight')
 selector='#story button:visible' if page.locator('#story').is_visible() else 'button:visible'
 bad=page.locator(selector).evaluate_all('''els=>els.filter(e=>{const r=e.getBoundingClientRect();return r.width<47.9||r.height<47.9||r.left<-.1||r.top<-.1||r.right>innerWidth+.1||r.bottom>innerHeight+.1}).map(e=>({id:e.id,text:e.innerText,rect:e.getBoundingClientRect().toJSON()}))''')
 assert not bad,bad
 if page.locator('#field').is_visible():
  panels=page.locator('#scene-event:visible,[data-prototype]:visible').evaluate_all('els=>els.map(e=>e.getBoundingClientRect().toJSON())')
  assert page.locator('[data-cell] > polygon').evaluate_all('''(els,panels)=>els.every(e=>{const r=e.getBoundingClientRect();return panels.every(a=>a.right<=r.left||a.left>=r.right||a.bottom<=r.top||a.top>=r.bottom)})''',panels)
  assert page.locator('[data-cell] > polygon').evaluate_all('''els=>els.every(e=>{const r=e.getBoundingClientRect(),p=document.querySelector('#field').getBoundingClientRect();return r.left>=p.left-.1&&r.right<=p.right+.1&&r.top>=p.top-.1&&r.bottom<=p.bottom+.1})''')

with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 page=b.new_page(viewport={'width':740,'height':360},reduced_motion='reduce')
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);fit(page);page.screenshot(path=str(SHOTS/'map-new-740x360.png'));assert page.locator('[data-level]').count()==8
 for index,level in enumerate(LEVELS):
  enter(page,level['id']);fit(page);solve(page,level)
  assert page.locator('[data-road][data-complete="true"]').count()==index+1
  page.reload();assert page.locator('[data-road][data-complete="true"]').count()==index+1
  if index<7:assert page.locator(f'[data-level="{LEVELS[index+1]["id"]}"]').is_enabled()
 print('Eight levels, first outcomes, sequential unlock and reload: PASS',flush=True)
 assert page.locator('#chapter-ending').is_visible();assert page.locator('#letter-open').is_visible()
 page.locator('#letter-open').click();assert 'Чашек хватит всем' in page.locator('#story-text').inner_text();skip(page)
 for w,h in [(1280,720),(915,412),(740,360),(844,390),(390,844)]:
  page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(100);fit(page)
  page.screenshot(path=str(SHOTS/f'map-{w}x{h}.png'))
  for level in LEVELS:
   enter(page,level['id']);page.wait_for_timeout(70);fit(page)
   assert not page.locator('#story').is_visible() # before is not automatic on replay
   if level['id'] in ['gate','stream','forest'] or w==1280:page.screenshot(path=str(SHOTS/f'{level["id"]}-{w}x{h}.png'))
   if level['id']=='stream':
    place(page,'bridge',level['solution']['bridge']);fit(page)
    page.screenshot(path=str(SHOTS/f'bridge-{w}x{h}.png'))
   page.locator('#scene-back').click()
 print('Map/all puzzles and bridge on five viewport sizes: PASS',flush=True)
 # Replay does not duplicate progress or play after-dialogue again.
 before=json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))
 enter(page,'gate');solve(page,LEVELS[0],first=False)
 assert json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))==before
 for level in LEVELS:
  page.locator(f'[aria-label="Реплики: {level["name"]}"]').click()
  while page.locator('#story-action').inner_text()!='Закрыть':
   fit(page);page.locator('#story-action').click()
  fit(page);skip(page)
 page.locator('#sandbox-open').click();settings(page,'#size','11,7');assert page.locator('[data-cell]').count()==77
 settings(page,'#map-return');assert json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))==before
 page.locator('#reset-open').click();page.locator('#reset-cancel').click();assert page.locator('[data-road][data-complete="true"]').count()==8
 page.locator('#reset-open').click();page.locator('#reset-confirm').click();page.reload()
 assert page.locator('[data-road][data-complete="true"]').count()==0;assert page.locator('[data-level="garden"]').is_disabled()
 page.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({version:1,completed:["gate","garden","mill"]}))',KEY);page.reload()
 assert page.locator('[data-level="well"]').is_enabled();assert page.locator('[data-level="mill"]').is_enabled()
 assert page.locator('[data-level="bakery"]').is_disabled();assert page.locator('[data-level="post"]').is_disabled()
 enter(page,'well');settings(page,'#map-return');page.reload()
 assert json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['completed']==['gate','garden','mill']
 page.evaluate('(k)=>localStorage.setItem(k,"broken{")',KEY);page.reload();assert page.locator('[data-level="gate"]').is_enabled()
 print('Replay/story archive/letter, reset, sandbox, legacy migration and corrupt save: PASS',flush=True)
 # Touch first-play through all eight also exercises rotated compound pieces.
 ctx=b.new_context(viewport={'width':915,'height':412},has_touch=True,is_mobile=True,reduced_motion='reduce')
 touch=ctx.new_page();touch.on('pageerror',lambda e:errors.append(str(e)));touch.goto(URL)
 for level in LEVELS:enter(touch,level['id'],True);solve(touch,level,True)
 enter(touch,'stream',True);settings(touch,'#mode','drag',True)
 session=ctx.new_cdp_session(touch)
 def drag(id,q,r,cancel=False,source=None):
  x,y=center(touch,source or f'[data-piece="{id}"]');a,bottom=center(touch,f'[data-cell="{q},{r}"] > polygon')
  radius=touch.locator(f'[data-cell="{q},{r}"] > polygon').bounding_box()['height']/2
  session.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
  for step in range(1,11):
   session.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(a-x)*step/10,'y':y+(bottom+max(42,radius*1.6)-y)*step/10}]});touch.wait_for_timeout(20)
  session.send('Input.dispatchTouchEvent',{'type':'touchCancel' if cancel else 'touchEnd','touchPoints':[]});touch.wait_for_timeout(80)
 drag('bridge',4,3,True);assert touch.locator('[data-owner="bridge"]').count()==0
 touch.locator('#other').tap();drag('bridge',4,3);assert touch.locator('[data-owner="bridge"]').count()==3
 drag('bridge',1,1,source='[data-cell="4,3"] > polygon');assert touch.locator('[data-owner="bridge"]').count()==3
 drag('bridge',4,2,True,source='[data-cell="4,3"] > polygon');assert touch.locator('[data-cell="4,3"]').get_attribute('data-owner')=='bridge'
 touch.locator('#undo').tap();assert touch.locator('[data-owner="bridge"]').count()==0
 drag('stream-a',4,3);assert touch.locator('[data-owner="stream-a"]').count()==0
 touch.locator('#other').tap();touch.locator('#scene-back').tap();enter(touch,'forest',True)
 drag('forest-a',1,3);assert touch.locator('[data-owner="forest-a"]').count()==4
 print('Touch eight puzzles, large pieces, bridge drag/cancel/invalid return, water rejection, undo: PASS',flush=True)
 denied=b.new_context(viewport={'width':740,'height':360},reduced_motion='reduce')
 denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('denied')}})")
 offline=denied.new_page();offline.goto(URL);enter(offline,'gate');solve(offline,LEVELS[0])
 assert offline.locator('[data-level="garden"]').is_enabled();assert 'только' in offline.locator('#save-status').inner_text()
 offline.reload();assert offline.locator('[data-level="garden"]').is_disabled()
 normal=b.new_context(viewport={'width':740,'height':360})
 normal.add_init_script('const raf=requestAnimationFrame.bind(window);window.requestAnimationFrame=cb=>raf(ts=>cb(ts-50));')
 walking=normal.new_page();walking.on('pageerror',lambda e:errors.append(str(e)));walking.goto(URL)
 walking.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({version:2,completed:["gate"]}))',KEY);walking.reload()
 enter(walking,'garden');solve(walking,LEVELS[1],resize_walk=True)
 print('Normal walking animation, duplicate-check guard and early frame timestamp: PASS',flush=True)
 assert not errors,errors
 print('Denied storage session play: PASS; no browser errors.',flush=True);b.close()
