"""Actual runtime resident checks. Seed progress only; solve by real UI input."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2];out=root/'docs/chapter-1-rc/evidence/residents-runtime';out.mkdir(parents=True,exist_ok=True)
levels=json.loads((root/'docs/chapter-1-rc/production-solutions.json').read_text());expected={'garden':['rabbit'],'well':['teacher'],'bakery':['baker'],'stream':['squirrel'],'mill':['miller','squirrel'],'post':['hedgehog']};reports=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  for index,level in enumerate(levels):
   sid=level['id']
   if sid not in expected:continue
   q=b.new_page(viewport={'width':w,'height':h});errors=[];q.on('pageerror',lambda e:errors.append(str(e)));prior=[l['id'] for l in levels[:index]]
   q.add_init_script(f"localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':prior,'introSeen':prior})}));localStorage.setItem('ruby-village:settings:v1',JSON.stringify({{reducedMotion:true}}))")
   q.goto('http://127.0.0.1:5180/ruby-village/');q.locator('#continue-game').click()
   for stage in ['dialog','puzzle']:
    if stage=='puzzle':
     while q.locator('#story[open]').count():q.locator('#story-action').click()
    q.wait_for_load_state('networkidle');ids=q.locator('#board [data-resident]').evaluate_all('(ns)=>ns.map(n=>n.dataset.resident)');assert sorted(ids)==sorted(expected[sid]),(sid,stage,ids)
    assert q.locator('#board [data-scene-residents]').is_visible();q.screenshot(path=str(out/f'{sid}-{stage}-{w}x{h}.jpg'),type='jpeg',quality=88)
   q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#story-replay').click()
   assert q.locator('#story[open]').count()
   assert q.locator('#board [data-resident]').count()==len(expected[sid])
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.reload();q.locator('#continue-game').click()
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   assert q.locator('#board [data-resident]').count()==len(expected[sid])
   q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#reduced-motion').check();q.locator('#settings-close').click()
   for ident,placement in level['solution'].items():
    q.locator(f'[data-piece="{ident}"]').click()
    for _ in range(placement['turns']):q.locator('#right').click()
    a=placement['anchor'];q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
   q.locator('#check').click();q.wait_for_selector('#story[open]')
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.wait_for_selector('#completion-panel[open]');assert q.locator('#completion-scene [data-resident]').count()==len(expected[sid]);q.screenshot(path=str(out/f'{sid}-result-{w}x{h}.jpg'),type='jpeg',quality=88)
   reports.append({'scene':sid,'viewport':[w,h],'residents':ids,'dialog':True,'puzzle':True,'reload':True,'replay':True,'result':True,'input':'actual tray/rotate/cell/place/check; progress only seeded','reducedMotion':'enabled for focused resident state checks','pageErrors':errors});assert not errors;q.close()
 b.close()
(out/'report.json').write_text(json.dumps(reports,indent=2)+'\n');print('PASS',len(reports),'scene/viewport runs')
