"""Focused real-input bridge/render check. Only progress is seeded to open stream."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/evidence/bridge-three-hex';out.mkdir(parents=True,exist_ok=True)
levels=json.loads((root/'docs/chapter-1-rc/production-solutions.json').read_text())
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for index,level in enumerate(levels):
  if level['id'] not in ['stream','mill']:continue
  for w,h in [(1280,720),(844,390)]:
   q=b.new_page(viewport={'width':w,'height':h});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
   prior=[l['id'] for l in levels[:index]];q.add_init_script(f"localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':prior,'introSeen':prior})}))")
   q.goto('http://127.0.0.1:5180/ruby-village/');q.locator('#continue-game').click()
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   for ident,placement in level['solution'].items():
    q.locator(f'[data-piece="{ident}"]').click()
    for _ in range(placement['turns']):q.locator('#right').click()
    a=placement['anchor'];q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
   q.wait_for_load_state('networkidle');assert q.locator('#board [data-painted-bridge]').count()==1
   assert q.locator('#board .bridge-cell').evaluate_all('(ns)=>ns.length===3&&ns.every(n=>n.getAttribute("opacity")==="0"&&n.getAttribute("pointer-events")==="all")')
   q.screenshot(path=str(out/f'{level["id"]}-mask-{w}x{h}.jpg'),type='jpeg',quality=90)
   q.locator('#board [data-cell][data-terrain=water] .cell').evaluate_all('(ns)=>ns.forEach(n=>n.style.opacity="0")');q.locator('#board [data-puzzle-landmarks]').evaluate_all('(ns)=>ns.forEach(n=>n.style.visibility="hidden")')
   q.screenshot(path=str(out/f'{level["id"]}-art-{w}x{h}.jpg'),type='jpeg',quality=90)
   q.locator('#board [data-cell][data-terrain=water] .cell').evaluate_all('(ns)=>ns.forEach(n=>n.style.removeProperty("opacity"))');q.locator('#board [data-puzzle-landmarks]').evaluate_all('(ns)=>ns.forEach(n=>n.style.removeProperty("visibility"))')
   q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#reduced-motion').check();q.locator('#settings-close').click();q.locator('#check').click()
   q.wait_for_selector('#story[open]');
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.wait_for_selector('#completion-panel[open]')
   assert q.locator('#completion-scene .bridge-cell').evaluate_all('(ns)=>ns.length===3&&ns.every(n=>n.getAttribute("opacity")==="0")')
   assert q.locator('#game-controls').evaluate('(n)=>getComputedStyle(n).display')=='none'
   assert q.locator('#board [data-grid]').evaluate_all('(ns)=>ns.every(n=>getComputedStyle(n).display==="none")')
   q.screenshot(path=str(out/f'{level["id"]}-result-{w}x{h}.jpg'),type='jpeg',quality=90)
   assert not errors;checks.append({'scene':level['id'],'viewport':[w,h],'realInput':True,'seed':'progress only; placement through UI','threeInvisibleInteractiveHitCells':True,'paintedDeck':1,'resultHitCellsInvisible':True,'resultTechnicalLayersHidden':True,'reducedMotion':'enabled only for this focused rendering check; normal movement independently tested','scope':'legacy layout1; final v9 banks not certified; water overlay hidden only for paired art capture','pageErrors':errors});q.close()
 b.close()
(out/'report.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS both three-hex bridges, overlay/art pairs and restored results on desktop and landscape')
