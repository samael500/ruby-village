import json,pathlib
from playwright.sync_api import sync_playwright
O=pathlib.Path(__file__).resolve().parent;requests=[];restore=False
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox']);c=b.new_context(viewport={'width':1280,'height':720});c.add_init_script("localStorage.setItem('ruby-village:chapter-1:v1',JSON.stringify({version:2,completed:[],introSeen:['gate']}))");q=c.new_page()
 def route(r):
  requests.append({'url':r.request.url,'networkRestored':restore})
  if restore:r.continue_()
  else:r.abort()
 q.route('**/characters-walk-v1/animated-v3/*.webp',route)
 q.goto('http://127.0.0.1:5298/ruby-village/');q.locator('#continue-game').click();q.wait_for_selector('#app[data-motion="load-failed"]');before=q.locator('#app').get_attribute('data-motion');q.screenshot(path=str(O/'game-first-failure.jpg'))
 restore=True;q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#map-return').click();q.locator('button[data-level="gate"]').click();q.wait_for_selector('#app[data-motion="ready"]');q.wait_for_load_state('networkidle');q.screenshot(path=str(O/'game-reentry-recovered.jpg'));after=q.locator('#app').get_attribute('data-motion')
 (O/'game-reentry-41f8c8c.json').write_text(json.dumps({'source':'41f8c8c','productionLayoutVersion':1,'bundle':'index-BC1WQ_hQ.js','before':before,'after':after,'requests':requests,'scope':'real mouse UI level entry -> failed atlases -> network restored -> settings -> map -> same gate; progress-only introSeen fixture, no layout injection'},indent=2)+'\n');b.close()
