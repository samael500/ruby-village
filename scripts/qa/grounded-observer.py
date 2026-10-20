"""Observe real browser motion, narrative and audio without replacing game state."""
import json,time
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/grounded-observer';OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':1280,'height':720});q=c.new_page();errors=[];requests=[];q.on('pageerror',lambda e:errors.append(str(e)));q.on('response',lambda r:requests.append(r.url) if '/audio/' in r.url else None)
 q.add_init_script('''window.qaMotion=[];setInterval(()=>{const m=document.querySelector('#ruta-marker');if(m)window.qaMotion.push({t:performance.now(),state:m.dataset.gaitState,direction:m.dataset.direction,ms:m.dataset.routeMs,images:[...m.querySelectorAll('image')].map(i=>({href:i.getAttribute('href'),x:i.getAttribute('x'),transform:i.getAttribute('transform')}))})},60);''')
 q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').click();q.locator('#prologue-skip').click()
 def dismiss():
  while q.locator('#story[open]').count():q.locator('#story-action').click()
 dismiss();observations=[]
 levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())
 for index,level in enumerate(levels):
  dismiss()
  # Enter-story DOM layer measurement is done before dismissal in later followup.
  for ident,placement in level['solution'].items():
   q.locator(f'#tray [data-piece="{ident}"]').click()
   for _ in range(placement['turns']):q.locator('#right').click()
   h=placement['anchor'];q.locator(f'[data-cell="{h["q"]},{h["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
  begin=q.evaluate('window.qaMotion.length');q.locator('#check').click();q.wait_for_timeout(1800)
  motion=q.locator('#app').get_attribute('data-motion')
  if index==0:
   q.locator('#settings-open').click();q.wait_for_timeout(80);before=q.locator('#ruta-marker').get_attribute('data-route-ms');q.wait_for_timeout(800);after=q.locator('#ruta-marker').get_attribute('data-route-ms');assert before==after,(before,after)
   q.locator('#pause-continue').click();q.wait_for_timeout(250)
  for tick in range(50):
   if q.locator('#story[open],#completion-panel[open]').count():break
   q.wait_for_timeout(2000)
   (OUT/'live.json').write_text(json.dumps(q.evaluate('({ms:document.querySelector("#ruta-marker")?.dataset.routeMs,samples:window.qaMotion.slice(-3),dialogs:[...document.querySelectorAll("dialog[open]")].map(e=>e.id),hidden:document.hidden})')))
  else:raise AssertionError('Motion did not finish within 100seconds')
  if q.locator('#story[open]').count():
   hidden=q.locator('#ground-plane').evaluate('(e)=>getComputedStyle(e).display');grid=q.locator('[data-grid]').first.evaluate('(e)=>getComputedStyle(e).display') if q.locator('[data-grid]').count() else 'absent'
  else:hidden=grid='no-story'
  dismiss();q.locator('#completion-panel[open]').wait_for();samples=q.evaluate('(n)=>window.qaMotion.slice(n)',begin)
  scene=q.locator('[data-result-scene]').get_attribute('data-result-scene');assert scene==level['name'],scene
  q.screenshot(path=str(OUT/f'{level["id"]}-result.jpg'))
  observations.append({'level':level['id'],'motion':motion,'samples':samples,'resultScene':scene,'storyGroundDisplay':hidden,'storyGridDisplay':grid})
  (OUT/'partial.json').write_text(json.dumps(observations,ensure_ascii=False,indent=2))
  if index<7:q.locator('#next-level').click()
 (OUT/'report.json').write_text(json.dumps({'commit':'6637b8c','observations':observations,'audioRequests':requests,'pageErrors':errors},ensure_ascii=False,indent=2));assert not errors
 c.close();b.close()
