"""Regression scenarios from PR #28: pan, deselect and live drag selection."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_images import screenshot
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/screenshots/ui-v7';OUT.mkdir(parents=True,exist_ok=True)
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/'
KEY='ruby-village:chapter-1:v1'
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels))"],cwd=ROOT,text=True))
def setup(page,id):
 page.goto(URL);page.evaluate('(v)=>localStorage.setItem(v.k,JSON.stringify({version:2,completed:v.ids,introSeen:v.ids}))',{'k':KEY,'ids':[l['id'] for l in LEVELS]});page.reload();page.locator('#choose-level').click();page.locator(f'[data-level="{id}"]').click()
def mode(page,value):
 page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#mode').select_option(value);page.locator('#settings-close').click()
def saved_layout(page):return page.evaluate('(k)=>JSON.parse(localStorage.getItem(k)).session.layout',KEY)
def finger(cdp,kind,x=None,y=None):
 cdp.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if x is None else [{'x':x,'y':y}]})
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':740,'height':360},has_touch=True,reduced_motion='reduce');errors=[];page.on('pageerror',lambda e:errors.append(str(e)));setup(page,'gate');cdp=page.context.new_cdp_session(page)
 for value in ['select','drag']:
  mode(page,value);tray=page.locator('#tray');tray.evaluate('(el)=>el.scrollLeft=0');box=tray.bounding_box();x=box['x']+box['width']-30;y=box['y']+box['height']/2
  assert page.evaluate('p=>!!document.elementFromPoint(p.x,p.y).closest("[data-piece]")',{'x':x,'y':y})
  before=saved_layout(page);finger(cdp,'touchStart',x,y)
  for i in range(1,11):finger(cdp,'touchMove',x-i*18,y)
  finger(cdp,'touchEnd');page.wait_for_function('document.getElementById("tray").scrollLeft>0');assert saved_layout(page)==before
  assert page.evaluate('window.scrollX===0&&window.scrollY===0')
  last=page.locator('[data-piece="gate-7"]').bounding_box();assert last['x']+last['width']<=box['x']+box['width']+1
  print(f'{value}: swipe begins on a stone, reaches last piece, no layout/page changes: PASS',flush=True)
 # Drag the last, previously clipped tile: retain the actual source SVG until release.
 tile=page.locator('[data-piece="gate-7"]');original=tile.locator(':scope > svg').element_handle();box=tile.bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
 anchor=LEVELS[0]['solution']['gate-7']['anchor'];cell_selector='[data-cell="%s,%s"] > polygon'%(anchor['q'],anchor['r'])
 cell=page.locator(cell_selector).bounding_box();tx=cell['x']+cell['width']/2;ty=cell['y']+cell['height']/2+max(42,cell['height']*.8)
 finger(cdp,'touchStart',x,y);expect(tile).to_have_attribute('aria-pressed','true');assert original.evaluate('(el)=>el.isConnected');finger(cdp,'touchMove',x,y-25)
 for i in range(1,11):finger(cdp,'touchMove',x+(tx-x)*i/10,y-25+(ty-y+25)*i/10)
 expect(page.locator('#placement-preview')).to_have_attribute('data-preview','valid');assert original.evaluate('(el)=>el.isConnected');screenshot(page,OUT/'drag-selected-last-740x360.png');finger(cdp,'touchEnd');expect(page.locator('[data-owner="gate-7"]')).to_have_count(1)
 # Move the placed instance and cancel; ownership and layout survive.
 before=saved_layout(page);box=page.locator(cell_selector).bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
 finger(cdp,'touchStart',x,y);expect(tile).to_have_attribute('aria-pressed','true');finger(cdp,'touchMove',x+40,y-30);finger(cdp,'touchCancel');assert saved_layout(page)==before;expect(page.locator('[data-owner="gate-7"]')).to_have_count(1)
 page.locator('#undo').tap();expect(page.locator('[data-owner="gate-7"]')).to_have_count(0);print('Last piece drag, live selection, stable SVG, placed-piece cancel and undo: PASS',flush=True)
 page.close()
 for w,h in [(1280,720),(844,390)]:
  page=b.new_page(viewport={'width':w,'height':h},has_touch=True,reduced_motion='reduce');page.on('pageerror',lambda e:errors.append(str(e)));setup(page,'garden')
  for id,v in LEVELS[1]['solution'].items():
   page.locator(f'[data-piece="{id}"]').tap()
   for _ in range(v['turns']):page.locator('#right').tap()
   page.locator('[data-cell="%s,%s"] > polygon'%(v['anchor']['q'],v['anchor']['r'])).tap();page.locator('#place').tap()
  before=saved_layout(page)
  for value in ['select','drag']:
   mode(page,value);spare=page.locator('[data-piece="garden-c"]');spare.tap();expect(spare).to_have_attribute('aria-pressed','true');expect(page.locator('#check')).to_be_disabled();spare.tap();expect(spare).to_have_attribute('aria-pressed','false');expect(page.locator('#check')).to_be_enabled();assert saved_layout(page)==before
  screenshot(page,OUT/f'spare-deselected-{w}x{h}.png');page.locator('#check').tap();expect(page.locator('#story')).to_be_visible();print(f'{w}x{h}: tap selected spare to deselect in both modes, unchanged road wins: PASS',flush=True);page.close()
 assert not errors,errors;b.close()
