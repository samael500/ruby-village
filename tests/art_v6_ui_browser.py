"""Live menu/session/modals and all eight levels through sequential public UI."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5173/ruby-village/'
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels))"],cwd=ROOT,text=True))
KEY='ruby-village:chapter-1:v1';SHOTS=ROOT/'docs/screenshots/art-v6'
def skip(page):
 if page.locator('#story').is_visible():page.locator('#story-skip').click()
def place(page,id,v,touch=False):
 page.locator(f'[data-piece="{id}"]').click()
 for _ in range(v['turns']):page.locator('#right').click()
 cell=page.locator('[data-cell="%s,%s"] > polygon'%(v['anchor']['q'],v['anchor']['r']))
 cell.tap() if touch else cell.click()
 expect(page.locator('#place')).to_be_enabled();page.locator('#place').click()
with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 page=b.new_page(viewport={'width':844,'height':390},reduced_motion='reduce',has_touch=True);page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL)
 expect(page.locator('#continue-game')).to_have_text('Начать приключение');page.screenshot(path=str(SHOTS/'menu-844x390.png'))
 page.locator('#continue-game').click();skip(page)
 place(page,'gate-1',LEVELS[0]['solution']['gate-1'],True)
 page.locator('#settings-open').click();page.screenshot(path=str(SHOTS/'pause-844x390.png'));page.keyboard.press('Escape');assert page.locator('[data-owner="gate-1"]').count()==1
 page.reload();expect(page.locator('#continue-game')).to_have_text('Продолжить');page.locator('#continue-game').click();assert page.locator('[data-owner="gate-1"]').count()==1
 page.set_viewport_size({'width':390,'height':844});expect(page.locator('#orientation-screen')).to_be_visible();page.set_viewport_size({'width':844,'height':390});assert page.locator('[data-owner="gate-1"]').count()==1
 page.locator('#settings-open').click();page.locator('#pause-restart').click();page.locator('#restart-cancel').click();assert page.locator('[data-owner="gate-1"]').count()==1
 page.locator('#settings-open').click();page.locator('#pause-restart').click();page.locator('#restart-confirm').click();assert page.locator('[data-owner="gate-1"]').count()==0
 for i,l in enumerate(LEVELS):
  if i:skip(page)
  for id,v in l['solution'].items():place(page,id,v,True)
  page.locator('#check').click();expect(page.locator('#story')).to_be_visible();page.screenshot(path=str(SHOTS/f'dialogue-{i+1}-844x390.png'));skip(page)
  expect(page.locator('#completion-panel')).to_be_visible();assert len(json.loads(page.evaluate('(k)=>localStorage.getItem(k)',KEY))['completed'])==i+1
  if i==7:expect(page.locator('#next-level')).to_be_hidden();page.locator('#completion-map').click();skip(page)
  else:page.locator('#next-level').click()
 page.screenshot(path=str(SHOTS/'map-complete-844x390.png'));page.locator('#reset-open').click();page.locator('#reset-confirm').click();page.reload();page.locator('#choose-level').click();expect(page.locator('[data-level="garden"]')).to_be_disabled()
 page.locator('#sandbox-open').click();page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#size').select_option('11,7');page.locator('#mode').select_option('drag');page.locator('#settings-close').click();assert page.locator('[data-cell]').count()==77
 # Real mouse drag, undo and persisted control mode.
 poly=page.locator('[data-cell="2,2"] > polygon').bounding_box();tray=page.locator('[data-piece="one-a"]').bounding_box();page.mouse.move(tray['x']+tray['width']/2,tray['y']+tray['height']/2);page.mouse.down();page.mouse.move(poly['x']+poly['width']/2,poly['y']+poly['height']/2,steps=8);page.mouse.up();assert page.locator('[data-owner="one-a"]').count()==1
 page.locator('#undo').click();assert page.locator('[data-owner="one-a"]').count()==0;page.reload();page.locator('#continue-game').click();assert page.locator('#mode').input_value()=='drag';assert page.locator('[data-cell]').count()==77
 # Modal walking pause with overlapping portrait blocker.
 page.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({version:2,completed:["gate"],introSeen:["garden"]}))',KEY);page.reload();page.locator('#choose-level').click();page.locator('[data-level="garden"]').click();page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#mode').select_option('select');page.locator('#settings-close').click();page.emulate_media(reduced_motion='no-preference')
 for id,v in LEVELS[1]['solution'].items():place(page,id,v)
 page.locator('#check').click();page.wait_for_timeout(200);page.locator('#settings-open').click();marker=page.locator('#ruta-marker').get_attribute('transform');page.wait_for_timeout(700);assert marker==page.locator('#ruta-marker').get_attribute('transform')
 page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(700);page.set_viewport_size({'width':844,'height':390});expect(page.locator('#pause-panel')).to_be_visible();assert marker==page.locator('#ruta-marker').get_attribute('transform');page.locator('#pause-continue').click();expect(page.locator('#story')).to_be_visible(timeout=15000)
 # Touch bridge and large-piece drag use the projected radius, including cancel/invalid drops.
 ctx=b.new_context(viewport={'width':915,'height':412},has_touch=True,is_mobile=True,reduced_motion='reduce');t=ctx.new_page();t.goto(URL)
 t.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({version:2,completed:["gate","garden","well","bakery","stream","mill","post","forest"],introSeen:["stream","forest"]}))',KEY);t.reload();t.locator('#choose-level').click();t.locator('[data-level="stream"]').click();t.locator('#settings-open').click();t.locator('#pause-settings').click();t.locator('#mode').select_option('drag');t.locator('#settings-close').click()
 cdp=ctx.new_cdp_session(t)
 def drag(id,placement,cancel=False,source=None):
  box=t.locator(source or f'[data-piece="{id}"]').bounding_box();x,y=box['x']+box['width']/2,box['y']+box['height']/2
  h=placement['anchor'];cell=t.locator('[data-cell="%s,%s"] > polygon'%(h['q'],h['r'])).bounding_box();tx,ty=cell['x']+cell['width']/2,cell['y']+cell['height']/2+max(42,cell['height']*.8)
  cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
  for step in range(1,11):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(tx-x)*step/10,'y':y+(ty-y)*step/10}]})
  cdp.send('Input.dispatchTouchEvent',{'type':'touchCancel' if cancel else 'touchEnd','touchPoints':[]});t.wait_for_timeout(100)
 bridge=LEVELS[4]['solution']['bridge'];drag('bridge',bridge,True);assert t.locator('[data-owner="bridge"]').count()==0;t.locator('#other').tap();drag('bridge',bridge);assert t.locator('[data-owner="bridge"]').count()==3
 h=bridge['anchor'];source='[data-cell="%s,%s"] > polygon'%(h['q'],h['r']);drag('bridge',{'anchor':{'q':1,'r':1}},source=source);assert t.locator('[data-owner="bridge"]').count()==3;t.locator('#undo').tap();assert t.locator('[data-owner="bridge"]').count()==0
 t.locator('#scene-back').tap();t.locator('[data-level="forest"]').tap();drag('forest-a',LEVELS[7]['solution']['forest-a']);assert t.locator('[data-owner="forest-a"]').count()==4
 ctx.close()
 denied=b.new_context(viewport={'width':740,'height':360},reduced_motion='reduce');denied.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('denied')}})");d=denied.new_page();d.goto(URL);assert 'Не удалось сохранить' in d.locator('#menu-save-status').inner_text();d.locator('#continue-game').click();skip(d)
 for id,v in LEVELS[0]['solution'].items():place(d,id,v)
 d.locator('#check').click();expect(d.locator('#story')).to_be_visible();skip(d);d.locator('#next-level').click();skip(d);assert d.locator('[data-cell]').count()==77;d.reload();expect(d.locator('#continue-game')).to_have_text('Начать приключение');denied.close()
 assert not errors,errors
 print('Menu, session reload, restart confirmation, eight sequential victories, next/map/finale, reset, sandbox drag/undo, modal + orientation pause: PASS')
 b.close()
