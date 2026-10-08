"""Narrative flow, isolated saves, exact six frames and real screenshots."""
import json,sys,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
from browser_images import ready_images
ROOT=Path(__file__).resolve().parents[1]
URL=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:5180/ruby-village/'
KEY='ruby-village:chapter-1:v1';INTRO='ruby-village:prologue:v1'
OUT=ROOT/'docs/screenshots/prologue';OUT.mkdir(parents=True,exist_ok=True)
LEVELS=json.loads(subprocess.check_output(['node','--experimental-strip-types','--input-type=module','-e',"import {levels} from './src/levels.ts';console.log(JSON.stringify(levels))"],cwd=ROOT,text=True))
IDS=[l['id'] for l in LEVELS]
def screenshot(page,path):
 ready_images(page)
 page.screenshot(path=str(path),quality=90)
def state(page,key=KEY):return page.evaluate('(k)=>localStorage.getItem(k)',key)
def bounds(page):
 ready_images(page)
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth&&document.documentElement.scrollHeight<=innerHeight')
 for selector in ['#prologue-next','#prologue-back','#prologue-skip','#prologue-text']:
  box=page.locator(selector).bounding_box();assert box and box['x']>=0 and box['y']>=0 and box['x']+box['width']<=page.viewport_size['width']+1 and box['y']+box['height']<=page.viewport_size['height']+1,(selector,box)
  if selector!='#prologue-text':assert box['height']>=44
 assert page.locator('#prologue-text').evaluate('(e)=>e.scrollHeight<=e.clientHeight')
 bg=page.locator('#prologue-background').bounding_box();assert abs(bg['width']/bg['height']-1672/941)<.01
with sync_playwright() as p:
 b=p.chromium.launch();errors=[]
 for w,h in [(1440,900),(844,390),(740,360)]:
  ctx=b.new_context(viewport={'width':w,'height':h},has_touch=True,reduced_motion='reduce');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.goto(URL)
  before=state(page);page.locator('#continue-game').tap();expect(page.locator('#prologue-panel')).to_be_visible();assert page.locator('#tray').is_visible()==False
  for i in range(6):
   assert page.locator('#prologue-panel').get_attribute('data-frame')==str(i);bounds(page)
   if w!=740:screenshot(page,OUT/f'frame-{i+1}-{w}x{h}.jpg')
   assert state(page)==before
   if i==2:
    page.locator('#prologue-back').tap();assert page.locator('#prologue-panel').get_attribute('data-frame')=='1';page.locator('#prologue-next').tap()
    page.reload();expect(page.locator('#continue-game')).to_have_text('Продолжить');page.locator('#continue-game').tap();assert page.locator('#prologue-panel').get_attribute('data-frame')=='2'
    page.set_viewport_size({'width':h,'height':w});expect(page.locator('#orientation-screen')).to_be_visible();assert page.locator('#app').evaluate('(e)=>e.inert')
    page.set_viewport_size({'width':w,'height':h});expect(page.locator('#prologue-panel')).to_be_visible();assert page.locator('#prologue-panel').get_attribute('data-frame')=='2'
   if i==5:expect(page.locator('#prologue-next')).to_have_text('К калитке →')
   page.locator('#prologue-next').tap()
  expect(page.locator('#story')).to_be_visible();assert json.loads(state(page,INTRO))['seen'];assert not json.loads(state(page))['completed']
  page.locator('#story-action').tap();assert 'Поставить' in page.locator('#story-text').inner_text();page.locator('#story-skip').tap()
  # Place a real stone, replay from pause, cancel replay and retain exact storage and board.
  solution=LEVELS[0]['solution']['gate-1'];page.locator('[data-piece="gate-1"]').tap();anchor=solution['anchor'];page.locator('[data-cell="%s,%s"] > polygon'%(anchor['q'],anchor['r'])).tap();page.locator('#place').tap()
  old=state(page);old_intro=state(page,INTRO);page.locator('#settings-open').tap();page.locator('#pause-prologue').tap();page.locator('#prologue-next').tap();page.locator('#prologue-skip').tap()
  assert state(page)==old and state(page,INTRO)==old_intro;assert page.locator('[data-owner="gate-1"]').count()==1
  page.reload();page.locator('#continue-game').tap();expect(page.locator('#prologue-panel')).to_be_hidden();assert page.locator('[data-owner="gate-1"]').count()==1
  page.locator('#scene-back').tap();page.locator('#home-menu').tap();old=state(page);page.locator('#prologue-replay').tap()
  for _ in range(5):page.locator('#prologue-next').tap()
  expect(page.locator('#prologue-next')).to_have_text('Вернуться в меню');page.locator('#prologue-next').tap();assert state(page)==old;expect(page.locator('#main-menu')).to_be_visible()
  # Existing session wins even over an unfinished prologue save.
  page.evaluate('(k)=>localStorage.setItem(k,JSON.stringify({version:1,seen:false,active:true,frame:3}))',INTRO);page.reload();page.locator('#continue-game').tap();expect(page.locator('#prologue-panel')).to_be_hidden();assert page.locator('[data-owner="gate-1"]').count()==1
  # First introductions keep narrator and correct character portraits; all text is DOM.
  page.evaluate('(v)=>localStorage.setItem(v.k,JSON.stringify({version:2,completed:v.ids,introSeen:[]}))',{'k':KEY,'ids':IDS});page.reload();page.locator('#choose-level').tap()
  for id,name in [('stream','Бельчонок'),('post','Ёж')]:
   # Completed levels skip intro; use the book to read it without changing progress.
   page.locator(f'[aria-label="Реплики: {LEVELS[IDS.index(id)]["name"]}"]').tap()
   expect(page.locator('#story-ruta')).to_be_hidden();assert page.locator('#story .eyebrow').inner_text()=='Рассказчик'
   if w!=740:screenshot(page,OUT/f'{id}-introduction-{w}x{h}.jpg')
   page.locator('#story-action').tap();expect(page.locator('#story-ruta')).to_be_visible();assert page.locator('#story-ruta').get_attribute('alt')==name
   if w!=740:screenshot(page,OUT/f'{id}-speaker-{w}x{h}.jpg')
   page.locator('#story-skip').tap()
  ctx.close();print(f'{w}x{h}: six frames, back/reload/rotation, replay isolation, old save and character introductions: PASS',flush=True)
 # Skip remains separate from completion, and denied storage still allows the entire flow.
 ctx=b.new_context(viewport={'width':844,'height':390});page=ctx.new_page();page.goto(URL);page.locator('#continue-game').click();page.locator('#prologue-skip').click();assert json.loads(state(page,INTRO))['seen'];assert not json.loads(state(page))['completed'];ctx.close()
 ctx=b.new_context(viewport={'width':844,'height':390});ctx.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('denied')}})");page=ctx.new_page();page.goto(URL);page.locator('#continue-game').click()
 for _ in range(6):page.locator('#prologue-next').click()
 expect(page.locator('#story')).to_be_visible();page.locator('#story-skip').click();page.locator('#scene-back').click();page.locator('#home-menu').click();page.locator('#prologue-replay').click();page.locator('#prologue-skip').click();expect(page.locator('#main-menu')).to_be_visible();ctx.close()
 # A replay opened while Ruta is walking pauses the existing journey, including a turn.
 ctx=b.new_context(viewport={'width':844,'height':390},reduced_motion='no-preference');page=ctx.new_page();page.goto(URL)
 page.evaluate('(v)=>localStorage.setItem(v.k,JSON.stringify({version:2,completed:["gate"],introSeen:["garden"],session:{levelId:"garden",cols:11,rows:7,layout:v.solution,mode:"select",reducedMotion:false}}))',{'k':KEY,'solution':LEVELS[1]['solution']});page.reload();page.locator('#continue-game').click();page.locator('#check').click();page.wait_for_timeout(100);page.locator('#settings-open').click();page.locator('#pause-prologue').click()
 marker=page.locator('#ruta-marker').get_attribute('transform');page.wait_for_timeout(700);assert marker==page.locator('#ruta-marker').get_attribute('transform')
 page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(200);page.set_viewport_size({'width':844,'height':390});expect(page.locator('#prologue-panel')).to_be_visible();assert marker==page.locator('#ruta-marker').get_attribute('transform')
 page.locator('#prologue-skip').click();expect(page.locator('#story')).to_be_visible(timeout=15000);ctx.close()
 assert not errors,errors;b.close();print('Skip, in-memory flow without localStorage, walking pause during replay/rotation: PASS')
