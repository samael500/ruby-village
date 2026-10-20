"""Focused real-input bridge/render check. Only progress is seeded to open stream."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/evidence/painted-bridge';out.mkdir(parents=True,exist_ok=True)
solution=next(l for l in json.loads((root/'docs/chapter-1-rc/production-solutions.json').read_text()) if l['id']=='stream')['solution']
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
  q.add_init_script("localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:['gate','garden','well','bakery'],introSeen:['gate','garden','well','bakery']}))")
  q.goto('http://127.0.0.1:5180/ruby-village/');q.locator('#continue-game').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  for ident,placement in solution.items():
   q.locator(f'[data-piece="{ident}"]').click()
   for _ in range(placement['turns']):q.locator('#right').click()
   a=placement['anchor'];q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
  q.wait_for_load_state('networkidle');assert q.locator('#board [data-painted-bridge]').count()==1
  assert q.locator('#board .bridge-cell').evaluate_all('(ns)=>ns.length===3&&ns.every(n=>n.getAttribute("opacity")==="0"&&n.getAttribute("pointer-events")==="all")')
  q.screenshot(path=str(out/f'stream-installed-{w}x{h}.jpg'),type='jpeg',quality=90)
  q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#reduced-motion').check();q.locator('#settings-close').click();q.locator('#check').click()
  q.wait_for_selector('#story[open]');
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.wait_for_selector('#completion-panel[open]')
  assert q.locator('#completion-scene .bridge-cell').evaluate_all('(ns)=>ns.length===3&&ns.every(n=>n.getAttribute("opacity")==="0")')
  assert q.locator('#game-controls').evaluate('(n)=>getComputedStyle(n).display')=='none'
  assert q.locator('#board [data-grid]').evaluate_all('(ns)=>ns.every(n=>getComputedStyle(n).display==="none")')
  q.screenshot(path=str(out/f'stream-result-{w}x{h}.jpg'),type='jpeg',quality=90)
  assert not errors;checks.append({'viewport':[w,h],'realInput':True,'seed':'progress only; placement through UI','threeInvisibleInteractiveHitCells':True,'paintedDeck':1,'resultHitCellsInvisible':True,'resultTechnicalLayersHidden':True,'reducedMotion':'enabled only for this focused rendering check; normal movement independently tested','scope':'legacy stream/layout1; final v9 banks not certified','pageErrors':errors});q.close()
 b.close()
(out/'report.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS painted bridge and restored result on desktop and landscape')
