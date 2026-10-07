"""Landscape gate, saved layout/dialogs and real animation pause, without reload."""
import json,subprocess,sys
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4173/ruby-village/'
SHOTS=Path(sys.argv[2]) if len(sys.argv)>2 else Path('/tmp/ruby-orientation-shots');SHOTS.mkdir(parents=True,exist_ok=True)
ROOT=Path(__file__).resolve().parents[1]
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels));"],cwd=ROOT,text=True))
KEY='ruby-village:chapter-1:v1'
def cell(page,q,r):
 b=page.locator(f'[data-cell="{q},{r}"] > polygon').bounding_box();return b['x']+b['width']/2,b['y']+b['height']/2
def place(page,id,placement):
 page.locator(f'[data-piece="{id}"]').click()
 for _ in range(placement['turns']):page.locator('#right').click()
 page.mouse.click(*cell(page,placement['anchor']['q'],placement['anchor']['r']));page.locator('#place').click()
def turn(page,w,h):page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(120)
with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 for w,h in [(390,844),(768,1024),(500,900)]:
  page=b.new_page(viewport={'width':w,'height':h});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL)
  expect(page.locator('#orientation-screen')).to_be_visible();assert page.locator('#app').evaluate('el=>el.inert&&el.hidden')
  assert 'Поверни устройство' in page.locator('#orientation-screen').inner_text();assert 'Расширь окно' in page.locator('#orientation-screen').inner_text()
  assert page.locator('[data-level="gate"]').is_hidden()
  page.screenshot(path=str(SHOTS/f'rotate-{w}x{h}.png'))
  page.evaluate('window.sessionIdentity=42');turn(page,1280,720)
  assert page.evaluate('window.sessionIdentity')==42;assert page.locator('#orientation-screen').is_hidden()
  page.locator('[data-level="gate"]').click();expect(page.locator('#story')).to_be_visible()
  text=page.locator('#story-text').inner_text();turn(page,w,h)
  assert page.locator('#story').is_hidden();expect(page.locator('#orientation-screen')).to_be_visible()
  turn(page,915,412);expect(page.locator('#story')).to_be_visible();assert page.locator('#story-text').inner_text()==text
  page.locator('#story-skip').click();place(page,'gate-1',LEVELS[0]['solution']['gate-1'])
  page.locator('[data-piece="gate-2"]').click();page.mouse.click(*cell(page,2,1));assert page.locator('#place').is_enabled()
  saved=page.evaluate('(k)=>localStorage.getItem(k)',KEY);turn(page,w,h)
  page.locator('#check').evaluate('el=>el.click()');assert page.evaluate('(k)=>localStorage.getItem(k)',KEY)==saved
  turn(page,915,412);assert page.locator('[data-owner="gate-1"]').count()==1;assert page.locator('#place').is_enabled()
  page.locator('#place').click();assert page.locator('[data-cell="2,1"]').get_attribute('data-owner')=='gate-2'
  page.screenshot(path=str(SHOTS/f'resumed-{w}x{h}.png'));page.close()
 print('Phone/tablet/window: overlay, inert, no reload, dialogue and pending/placed state: PASS',flush=True)
 for reduced in ['no-preference','reduce']:
  page=b.new_page(viewport={'width':915,'height':412},reduced_motion=reduced);page.goto(URL)
  page.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({version:2,completed:["gate"]}))',KEY);page.reload()
  page.locator('[data-level="garden"]').click();page.locator('#story-skip').click()
  for id,placement in LEVELS[1]['solution'].items():place(page,id,placement)
  page.locator('#check').click()
  if reduced=='no-preference':
   page.wait_for_timeout(250);turn(page,390,844)
   marker=page.locator('#ruta-marker').get_attribute('transform');saved=page.evaluate('(k)=>localStorage.getItem(k)',KEY)
   page.wait_for_timeout(3000);assert page.locator('#ruta-marker').get_attribute('transform')==marker
   assert not page.locator('#story').is_visible();assert page.evaluate('(k)=>localStorage.getItem(k)',KEY)==saved
   turn(page,915,412);page.wait_for_timeout(200);assert page.locator('#ruta-marker').get_attribute('transform')!=marker
  expect(page.locator('#story')).to_be_visible(timeout=15000)
  assert page.locator('#board #ruta-idle,#board #ruta-marker').count()==1
  page.locator('#story-skip').click();assert page.locator('[data-level="well"]').is_enabled();page.close()
 # Rotation interrupts a live pointer drag without losing or moving the instance.
 page=b.new_page(viewport={'width':915,'height':412});page.goto(URL);page.locator('#sandbox-open').click()
 page.locator('#settings-open').click();page.locator('#mode').select_option('drag');page.locator('#settings-close').click()
 box=page.locator('[data-piece="one-a"]').bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();page.mouse.move(*cell(page,2,2),steps=8)
 turn(page,390,844);page.mouse.up();turn(page,915,412)
 assert page.locator('[data-owner="one-a"]').count()==0
 page.locator('#other').click();box=page.locator('[data-piece="one-a"]').bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();page.mouse.move(*cell(page,2,2),steps=8);page.mouse.up()
 assert page.locator('[data-cell="2,2"]').get_attribute('data-owner')=='one-a'
 page.mouse.move(*cell(page,2,2));page.mouse.down();page.mouse.move(*cell(page,3,2),steps=8);turn(page,390,844);page.mouse.up();turn(page,915,412)
 assert page.locator('[data-cell="2,2"]').get_attribute('data-owner')=='one-a'
 print('Resize cancels active tray/board pointer drags without loss: PASS',flush=True)
 print('Ruta pauses for 3s and resumes without jumping/duplicate completion; reduced motion: PASS',flush=True)
 assert not errors,errors;b.close()
