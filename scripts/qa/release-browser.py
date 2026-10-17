import os
"""All routes via real UI against pruned production export; not physical-device QA."""
import json,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/release/current-export';out.mkdir(parents=True,exist_ok=True);levels=json.loads((root/'docs/chapter-1-rc/production-solutions.json').read_text());results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});errors=[];bad=[];failed=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append({'url':r.url,'status':r.status}) if r.status>=400 else None);q.on('requestfailed',lambda r:failed.append({'url':r.url,'failure':r.failure}));q.goto(os.environ.get('RUBY_QA_URL','http://127.0.0.1:5180/ruby-village/'));q.locator('#main-settings').click();q.locator('#reduced-motion').check();q.locator('#settings-close').click();q.locator('#continue-game').click()
  for _ in range(6):q.wait_for_selector('#prologue-canvas[data-ready=true]');q.locator('#prologue-next').click()
  def dismiss():
   while q.locator('#story[open]').count():q.locator('#story-action').click()
  scenes=[]
  for i,level in enumerate(levels):
   dismiss()
   for ident,placement in level['solution'].items():
    q.locator(f'[data-piece="{ident}"]').click()
    for _ in range(placement['turns']):q.locator('#right').click()
    a=placement['anchor'];q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
   q.locator('#check').click();q.wait_for_selector('#story[open]');dismiss();q.wait_for_selector('#completion-panel[open]');q.wait_for_load_state('networkidle');scenes.append({'scene':level['id'],'residents':q.locator('#completion-scene [data-resident]').count()})
   if i<7:q.locator('#next-level').click()
   else:q.locator('#completion-map').click()
  q.wait_for_load_state('networkidle');q.screenshot(path=str(out/f'map-{w}x{h}.jpg'),type='jpeg',quality=88);assert not errors and not bad and not failed,(errors,bad,failed)
  results.append({'viewport':[w,h],'scenes':scenes,'prologueFrames':6,'input':'real UI, no seeded progress/layout','reducedMotion':'enabled explicitly through settings; resource coverage, not gait acceptance','httpErrors':bad,'requestFailures':failed,'pageErrors':errors});q.close()
 b.close()
report={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'scope':'layout1 pruned export; final layout2/gait/map must repeat; author verification','results':results};(out/'browser-report.json').write_text(json.dumps(report,indent=2)+'\n');(out/'export-assets.json').write_text((root/'dist/export-assets.json').read_text());print('PASS16 actual routes,12 prologue frames,2 maps, zero failed resources')
