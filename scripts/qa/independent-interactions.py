"""Independent production behavior checks. Browser emulation only."""
import json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/interactions';OUT.mkdir(parents=True,exist_ok=True)
URL='http://127.0.0.1:5183/ruby-village/';KEY='ruby-village:chapter-1:v1';results=[]
def dismiss(page):
 for _ in range(40):
  if page.locator('#story[open]').count():page.locator('#story-action').click()
  else:return
 raise AssertionError('dialog loop')
def start(page):
 page.goto(URL);page.locator('#continue-game').click()
 if page.locator('#prologue-panel[open]').count():page.locator('#prologue-skip').click()
 dismiss(page)
def record(name,fn):
 try:fn();results.append({'check':name,'status':'pass'})
 except Exception as e:results.append({'check':name,'status':'fail','error':str(e)})
with sync_playwright() as p:
 browser=p.chromium.launch();context=browser.new_context(viewport={'width':1280,'height':720});page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));start(page)
 solution=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())[0];ident,placement=next(iter(solution['solution'].items()))
 def place():
  page.locator(f'#tray [data-piece="{ident}"]').click()
  for _ in range(placement['turns']):page.locator('#right').click()
  page.locator(f'[data-cell="{placement["anchor"]["q"]},{placement["anchor"]["r"]}"] polygon').first.click(force=True);page.locator('#place').click()
  assert page.locator(f'[data-owner="{ident}"]').count()>0
 record('real placement',place)
 def reload():
  page.reload();page.locator('#continue-game').click();dismiss(page);assert page.locator(f'[data-owner="{ident}"]').count()>0
 record('partial save reload',reload)
 def undo():
  # Undo history deliberately does not persist; test an actual new move.
  page.locator(f'[data-owner="{ident}"] polygon').first.click(force=True);page.locator('#return').click();assert not page.locator(f'[data-owner="{ident}"]').count();page.locator('#undo').click();assert page.locator(f'[data-owner="{ident}"]').count()>0
 record('return and undo',undo)
 def settings():
  page.locator('#settings-open').click();page.locator('#pause-settings').click();page.locator('#audio-muted').check();page.locator('#audio-music').fill('0.15');page.locator('#audio-music').dispatch_event('input');page.locator('#audio-sfx').fill('0.25');page.locator('#audio-sfx').dispatch_event('input');page.locator('#reduced-motion').check();page.locator('#settings-close').click();page.reload();saved=json.loads(page.evaluate("localStorage.getItem('ruby-village:audio:v1')"));assert saved=={'muted':True,'music':.15,'sfx':.25};page.locator('#continue-game').click();dismiss(page)
 record('audio preferences persisted',settings)
 for width,height in [(1280,720),(844,390),(740,360),(915,412),(1024,768),(1920,1080),(390,844)]:
  def viewport(w=width,h=height):
   page.set_viewport_size({'width':w,'height':h});page.wait_for_timeout(200);page.screenshot(path=str(OUT/f'gate-{w}x{h}.png'));assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   if w>h:
    assert page.locator('#tray').is_visible();assert page.locator('#check').is_visible()
  record(f'viewport {width}x{height}',viewport)
 context.close()
 for name,script in [('denied-storage',"Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Denied','SecurityError')}})"),('corrupt-storage',f"localStorage.setItem('{KEY}','broken')"),('v1-migration',f"localStorage.setItem('{KEY}',JSON.stringify({{version:1,completed:['gate','garden','mill']}}))")]:
  def storage_case(script=script,name=name):
   c=browser.new_context(viewport={'width':1280,'height':720});c.add_init_script(script);q=c.new_page();q.on('pageerror',lambda e:errors.append(str(e)));q.goto(URL)
   if name=='v1-migration':
    q.locator('#choose-level').click();assert q.locator('[data-level="mill"]').inner_text().find('Пройден')>=0;assert not q.locator('[data-level="well"]').is_disabled();assert q.locator('[data-level="bakery"]').is_disabled()
   else:start(q);assert q.locator('#tray').is_visible()
   q.screenshot(path=str(OUT/f'{name}.png'));c.close()
  record(name,storage_case)
 browser.close()
report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'results':results,'pageErrors':errors,'physicalPhone':'not-run','familyPlaytest':'not-run'}
(OUT/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
