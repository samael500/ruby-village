"""844x390 native Chromium touch, reduced-motion scene review, not a physical device."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/grounded-phone-scenes';OUT.mkdir(parents=True,exist_ok=True)
report=[]
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':844,'height':390},is_mobile=True,has_touch=True,reduced_motion='reduce');q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').tap();q.locator('#prologue-skip').tap()
 def dismiss():
  while q.locator('#story[open]').count():q.locator('#story-action').tap()
 levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())
 for index,level in enumerate(levels):
  if q.locator('#story[open]').count():
   q.wait_for_timeout(150)
   display=q.locator('#ground-plane').evaluate('(e)=>getComputedStyle(e).display')
   if display!='none':
    q.screenshot(path=str(OUT/'story-display-failure.jpg'));(OUT/'story-display-failure.json').write_text(json.dumps(q.evaluate('({classes:document.querySelector("#app").className,dialogs:[...document.querySelectorAll("dialog[open]")].map(e=>e.id),ground:getComputedStyle(document.querySelector("#ground-plane")).display,controls:getComputedStyle(document.querySelector("#game-controls")).display})')))
   assert display=='none'
   assert q.locator('#game-controls').evaluate('(e)=>getComputedStyle(e).display')=='none'
   q.screenshot(path=str(OUT/f'{level["id"]}-story.jpg'))
  dismiss()
  for ident,placement in level['solution'].items():
   q.locator(f'#tray [data-piece="{ident}"]').tap()
   for _ in range(placement['turns']):q.locator('#right').tap()
   h=placement['anchor'];q.locator(f'[data-cell="{h["q"]},{h["r"]}"] polygon').first.tap(force=True);q.locator('#place').tap()
  q.screenshot(path=str(OUT/f'{level["id"]}-solved.jpg'));q.locator('#check').tap();q.wait_for_selector('#story[open],#completion-panel[open]');dismiss();q.locator('#completion-panel[open]').wait_for();q.screenshot(path=str(OUT/f'{level["id"]}-result.jpg'))
  assert q.locator('[data-result-scene]').get_attribute('data-result-scene')==level['name']
  assert q.locator('#game-controls').evaluate('(e)=>getComputedStyle(e).display')=='none'
  assert all(x=='none' for x in q.locator('#board [data-grid]').evaluate_all('(a)=>a.map(e=>getComputedStyle(e).display)'))
  report.append({'id':level['id'],'storyPuzzleDisplayNone':True,'resultCurrentScene':True,'touchInput':True})
  if index<7:q.locator('#next-level').tap()
 q.locator('#completion-map').tap();dismiss()
 # End of chapter may show a book/ending dialog; use its actual controls.
 if q.locator('#ending-panel[open]').count():q.locator('#ending-close').tap()
 q.screenshot(path=str(OUT/'map-complete.jpg'))
 (OUT/'report.json').write_text(json.dumps({'commit':'5dc2036 (local identical tracked tree: 237162a)','viewport':[844,390],'reducedMotion':True,'levels':report,'errors':errors,'physicalPhone':'NOT RUN'},indent=2));assert not errors
 c.close();b.close()
