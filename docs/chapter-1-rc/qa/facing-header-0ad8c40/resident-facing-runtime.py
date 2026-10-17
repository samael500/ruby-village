"""Event-driven resident views/anchors in real game. No renderer injection."""
import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'docs/chapter-1-rc/qa/facing-header-0ad8c40/states';OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text());manifest=json.loads((ROOT/'public/assets/characters-facing-v1/residents-facing-manifest.json').read_text())['characters'];reports=[]
scenes={'garden':['rabbit'],'well':['teacher'],'stream':['squirrel'],'mill':['miller','squirrel'],'post':['hedgehog'],'bakery':['baker']}
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  for index,l in enumerate(levels):
   sid=l['id']
   if sid not in scenes:continue
   q=b.new_page(viewport={'width':w,'height':h});errors=[];bad=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
   prior=[x['id'] for x in levels[:index]];q.add_init_script(f"if(!localStorage.getItem('ruby-village:chapter-1:v1'))localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({json.dumps({'version':2,'completed':prior,'introSeen':prior})}))")
   q.goto(os.environ.get('RUBY_QA_URL','http://127.0.0.1:5286/ruby-village/'));q.locator('#continue-game').click();q.wait_for_load_state('networkidle')
   def actors():return q.locator('#board [data-resident]').evaluate_all('(ns)=>ns.map(n=>({id:n.dataset.resident,view:n.dataset.view,reason:n.dataset.facingReason,anchor:n.getAttribute("transform"),href:n.querySelector("image").getAttribute("href")}))')
   initial=actors();assert sorted(a['id'] for a in initial)==sorted(scenes[sid])
   for a in initial:
    expected='conversation-left' if 'conversation-left' in manifest.get(a['id'],{}).get('frames',{}) else 'idle'
    assert a['view']==expected and a['reason']=='encounter',(sid,a,expected)
   q.screenshot(path=str(OUT/f'{sid}-meeting-{w}.jpg'),type='jpeg',quality=90)
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   waiting=actors();assert all(a['reason']=='activity' for a in waiting);assert [a['anchor'] for a in waiting]==[a['anchor'] for a in initial]
   q.screenshot(path=str(OUT/f'{sid}-activity-{w}.jpg'),type='jpeg',quality=90)
   q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#story-replay').click()
   replay=actors();assert [(a['view'],a['anchor']) for a in replay]==[(a['view'],a['anchor']) for a in initial]
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.reload();q.locator('#continue-game').click();q.wait_for_load_state('networkidle');reloaded=actors();assert [a['anchor'] for a in reloaded]==[a['anchor'] for a in initial];assert all(a['reason']=='activity' for a in reloaded)
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#reduced-motion').check();q.locator('#settings-close').click()
   for ident,placement in l['solution'].items():
    q.locator(f'[data-piece="{ident}"]').click()
    for _ in range(placement['turns']):q.locator('#right').click()
    a=placement['anchor'];q.locator(f'[data-cell="{a["q"]},{a["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
   q.locator('#check').click();q.wait_for_selector('#story[open]');arrival=actors();assert [a['anchor'] for a in arrival]==[a['anchor'] for a in initial]
   for a in arrival:
    wanted='conversation-front' if sid=='well' or (sid=='mill' and a['id']=='squirrel') else 'conversation-left'
    expected=wanted if wanted in manifest.get(a['id'],{}).get('frames',{}) else 'idle'
    assert a['view']==expected,(sid,a,expected)
   rutaFeet=q.evaluate('''()=>{let f=document.querySelector('#ruta-marker [data-motion-frame]'),l=document.querySelector('#board [data-scene-residents]').transform.baseVal.consolidate().matrix;return {x:(+f.getAttribute('x')+(+f.getAttribute('width'))*72/144-l.e)/l.a,y:(+f.getAttribute('y')+(+f.getAttribute('height'))*192/216-l.f)/l.d}}''');rutaDirection=q.locator('#ruta-marker').get_attribute('data-direction');assert rutaDirection in ['e','ne','nw','w','sw','se']
   q.screenshot(path=str(OUT/f'{sid}-arrival-{w}.jpg'),type='jpeg',quality=90)
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.wait_for_selector('#completion-panel[open]');assert q.locator('#completion-scene [data-resident]').count()==len(initial)
   assert not errors and not bad;reports.append({'scene':sid,'viewport':[w,h],'intro':initial,'activity':waiting,'replay':replay,'reload':reloaded,'arrival':arrival,'rutaArrivalDirection':rutaDirection,'rutaActualArrivalFeet':rutaFeet,'anchorsStable':True,'resourceErrors':bad,'pageErrors':errors,'motion':'reduced via real settings for view/state check; not gait quality acceptance'});q.close()
 b.close()
(OUT/'report.json').write_text(json.dumps({'scope':'actual UI; known authored views are asserted, missing unfinished resident views remain explicit fallbackidle; physical phone NOT RUN','checks':reports},ensure_ascii=False,indent=2)+'\n');print('PASS12 actual resident facing/state runs')
