"""UI v7: loaded screenshots, permanent stock, speakers and HUD collision checks."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_images import screenshot,ready_images
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/screenshots/ui-v7';OUT.mkdir(parents=True,exist_ok=True)
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/'
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels))"],cwd=ROOT,text=True));IDS=[l['id'] for l in LEVELS];KEY='ruby-village:chapter-1:v1'
def seed(page,completed=None,intro=None):
 page.evaluate('(v)=>localStorage.setItem(v.k,JSON.stringify(v.data))',{'k':KEY,'data':{'version':2,'completed':IDS if completed is None else completed,'introSeen':IDS if intro is None else intro}});page.reload();page.locator('#choose-level').click()
def enter(page,id):page.locator('[data-level="'+id+'"]').click()
def skip(page):
 if page.locator("#prologue-panel").is_visible():page.locator("#prologue-skip").click()
 if page.locator('#story').is_visible():page.locator('#story-skip').click()
def place(page,id,v):
 page.locator(f'[data-piece="{id}"]').click()
 for _ in range(v['turns']):page.locator('#right').click()
 page.locator('[data-cell="%s,%s"] > polygon'%(v['anchor']['q'],v['anchor']['r'])).click();page.locator('#place').click()
def scene(page,id):
 if page.locator('#completion-panel').is_visible():page.locator('#completion-map').click();skip(page)
 elif page.locator('#field').is_visible():page.locator('#scene-back').click()
 enter(page,id)
with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 for w,h in [(1280,720),(844,390)]:
  page=b.new_page(viewport={'width':w,'height':h},has_touch=True,reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL)
  def shot(name):screenshot(page,OUT/f'{name}-{w}x{h}.png')
  shot('menu-new');page.locator('#continue-game').click();page.locator('#prologue-skip').click();shot('dialogue-ruta');expect(page.locator('#story-ruta')).to_be_visible();skip(page);shot('gate-tray')
  assert page.locator('[data-piece]').count()==len(LEVELS[0]['pieces'])
  place(page,'gate-1',LEVELS[0]['solution']['gate-1']);page.reload();shot('menu-saved')
  seed(page);shot('map');enter(page,'garden');page.locator('[data-piece="garden-a"]').click();shot('garden-selected')
  expect(page.locator('#tray')).to_be_visible();expect(page.locator('#check')).to_be_visible()
  page.locator('[data-piece="garden-a"]').focus();before=page.locator('#tray').evaluate('(el)=>el.scrollLeft');page.locator('#right').focus();page.keyboard.press('Enter');assert page.locator('#tray').evaluate('(el)=>el.scrollLeft')==before;assert page.locator('#right').evaluate('(el)=>el===document.activeElement');shot('garden-rotated')
  page.locator('[data-piece="garden-b"]').click();assert page.locator('[data-piece="garden-b"]').get_attribute('aria-pressed')=='true'
  page.locator('#settings-open').click();shot('pause');page.locator('#pause-settings').click();shot('settings');page.locator('#settings-close').click()
  page.locator('#settings-open').click();page.locator('#pause-restart').click();shot('restart-confirm');page.locator('#restart-cancel').click()
  page.locator('#scene-back').click();seed(page,IDS[:4],IDS[:4]);enter(page,'stream')
  for _ in range(20):
   if 'Бельчонок' in page.locator('#story .eyebrow').inner_text():break
   page.locator('#story-action').click()
  assert page.locator('#story .eyebrow').inner_text()=='Бельчонок';expect(page.locator('#story-ruta')).to_be_visible();assert page.locator('#story-ruta').get_attribute('alt')=='Бельчонок';shot('dialogue-belchonok');skip(page)
  scene(page,'stream');skip(page);page.locator('[data-piece="bridge"]').click();shot('stream-bridge')
  page.locator('#scene-back').click();seed(page);enter(page,'forest');skip(page);page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#mode').select_option('drag');page.locator('#settings-close').click()
  source=page.locator('[data-piece="forest-a"]').bounding_box();v=LEVELS[7]['solution']['forest-a'];target=page.locator('[data-cell="%s,%s"] > polygon'%(v['anchor']['q'],v['anchor']['r'])).bounding_box()
  page.mouse.move(source['x']+source['width']/2,source['y']+source['height']/2);page.mouse.down();page.mouse.move(target['x']+target['width']/2,target['y']+target['height']/2,steps=8);shot('compound-drag');page.mouse.up()
  page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#mode').select_option('select');page.locator('#settings-close').click();page.locator('#undo').click()
  for id,v in LEVELS[7]['solution'].items():place(page,id,v)
  page.locator('#check').click();expect(page.locator('#story')).to_be_visible();skip(page);shot('chapter-finish');page.locator('#completion-map').click();skip(page)
  enter(page,'gate');skip(page)
  for id,v in LEVELS[0]['solution'].items():place(page,id,v)
  expect(page.locator('.tray-note')).to_be_visible();page.locator('#check').click();expect(page.locator('#story')).to_be_visible();skip(page);shot('gate-completion');page.locator('#completion-map').click()
  # Failed road is visibly explained; no reliance on SR status only.
  enter(page,'garden');skip(page);page.locator('#check').click();expect(page.locator('#status.feedback')).to_be_visible();shot('road-feedback')
  page.close();print(f'{w}x{h}: fourteen UI states, permanent stock, rotation focus/scroll, correct speakers: PASS',flush=True)
 # Every available cell must stay clear of actionable HUD buttons/title.
 for w,h in [(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080)]:
  page=b.new_page(viewport={'width':w,'height':h},reduced_motion='reduce',has_touch=True);page.goto(URL);seed(page)
  for id in IDS:
   enter(page,id);ready_images(page)
   overlaps=page.evaluate('''()=>{const hud=[...document.querySelectorAll('header button,header .brand')].filter(el=>el.getBoundingClientRect().width).map(el=>el.getBoundingClientRect());return [...document.querySelectorAll('[data-cell]')].filter(el=>!['tree','house','flower','rock','water'].includes(el.dataset.terrain)).filter(el=>{const r=el.querySelector('polygon').getBoundingClientRect();return hud.some(h=>r.left<h.right&&r.right>h.left&&r.top<h.bottom&&r.bottom>h.top)}).map(el=>el.dataset.cell)}''')
   assert not overlaps,(w,h,id,overlaps)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight')
   page.locator('#scene-back').click()
  print(f'{w}x{h}: all eight scenes clear of HUD, no page overflow: PASS',flush=True)
  if w==740:
   enter(page,'gate');tray=page.locator('#tray');assert tray.evaluate('(el)=>el.scrollWidth>el.clientWidth')
   rect=tray.bounding_box();x=rect['x']+rect['width']-15;y=rect['y']+rect['height']/2;cdp=page.context.new_cdp_session(page)
   cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
   for i in range(1,11):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-i*15,'y':y}]})
   cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});page.wait_for_function('document.getElementById("tray").scrollLeft>0')
   assert page.evaluate('window.scrollX===0&&window.scrollY===0');page.locator('#scene-back').click()
  if w==844:
   enter(page,'gate');place(page,'gate-1',LEVELS[0]['solution']['gate-1']);page.set_viewport_size({'width':390,'height':844});expect(page.locator('#orientation-screen')).to_be_visible();screenshot(page,OUT/'orientation-390x844.png');page.set_viewport_size({'width':844,'height':390});expect(page.locator('#orientation-screen')).to_be_hidden();assert page.locator('[data-owner="gate-1"]').count()==1
  page.close()
 assert not errors,errors;b.close()
