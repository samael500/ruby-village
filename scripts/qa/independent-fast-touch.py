"""Independent #61 rapid native touch test, no persisted layout/progress injection."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/touch-release-063/independent';OUT.mkdir(parents=True,exist_ok=True)
levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text());results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for trial in range(8):
  c=b.new_context(viewport={'width':844,'height':390},has_touch=True,is_mobile=True,reduced_motion='reduce',record_video_dir=str(OUT/'raw-video'));q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').tap();q.locator('#prologue-skip').tap()
  def dismiss():
   while q.locator('#story[open]').count():q.locator('#story-action').tap()
  dismiss()
  for ident,placement in levels[0]['solution'].items():
   q.locator(f'#tray [data-piece="{ident}"]').tap();h=placement['anchor'];q.locator(f'[data-cell="{h["q"]},{h["r"]}"] polygon').first.tap(force=True);q.locator('#place').tap()
  q.locator('#check').tap();q.wait_for_selector('#story[open],#completion-panel[open]');dismiss();q.locator('#next-level').tap();dismiss()
  q.locator('#settings-open').tap();q.locator('#pause-settings').tap();q.locator('#mode').select_option('select' if trial>=6 else 'drag');q.locator('#settings-close').tap()
  client=c.new_cdp_session(q)
  def center(locator):
   bb=locator.bounding_box();assert bb;return {'x':bb['x']+bb['width']/2,'y':bb['y']+bb['height']/2}
  def emit(kind,pos=None):client.send('Input.dispatchTouchEvent',{'type':kind,'touchPoints':[] if pos is None else [{**pos,'id':1,'radiusX':4,'radiusY':4}]})
  def tap(locator):
   pos=center(locator);emit('touchStart',pos);emit('touchEnd')
  def drag(a,z):
   emit('touchStart',a);lift={**a,'y':a['y']-35};emit('touchMove',lift)
   for i in range(1,13):emit('touchMove',{'x':lift['x']+(z['x']-lift['x'])*i/12,'y':lift['y']+(z['y']-lift['y'])*i/12})
   emit('touchEnd')
  def cell(h):return q.locator(f'[data-cell="{h["q"]},{h["r"]}"] > polygon.cell')
  bad=cell({'q':0,'r':0});badpos=center(bad);lift=max(42,bad.bounding_box()['height']*.8)
  button=q.locator('[data-piece="garden-a"]')
  if trial>=6:tap(button);tap(bad)
  else:drag(center(button),{**badpos,'y':badpos['y']+lift})
  assert q.locator('#placement-preview[data-preview="invalid"]').count()
  icons=[]
  # No deliberate gap or hold between five rotate taps. Every native release must activate once.
  for turn in range(1,6):
   tap(q.locator('#right'));icon=button.get_attribute('data-icon');icons.append(icon);assert f':{turn}:' in icon,(trial,turn,icon)
  assert q.locator('#placement-preview[data-preview="invalid"]').count()
  action='cancel' if trial%2 else 'confirm-place' if trial>=6 else 'valid-drop'
  if action=='cancel':tap(q.locator('#other'));assert not q.locator('#placement-preview').count();assert not q.locator('[data-owner="garden-a"]').count()
  elif trial>=6:
   good=cell(levels[1]['solution']['garden-a']['anchor']);tap(good);tap(q.locator('#place'));q.wait_for_function('document.querySelectorAll("#board [data-owner=garden-a]").length===3');assert not q.locator('#placement-preview').count()
  else:
   good=cell(levels[1]['solution']['garden-a']['anchor']);goodpos=center(good);drag(badpos,{**goodpos,'y':goodpos['y']+max(42,good.bounding_box()['height']*.8)});q.screenshot(path=str(OUT/f'trial-{trial+1}-drop.jpg'))
   state=q.evaluate('({preview:document.querySelector("#placement-preview")?.outerHTML,status:document.querySelector("#status").textContent,icon:document.querySelector("[data-piece=garden-a]")?.dataset.icon,owners:[...document.querySelectorAll("[data-owner=garden-a]")].map(e=>e.dataset.cell)})');(OUT/f'trial-{trial+1}-drop.json').write_text(json.dumps(state,indent=2));assert q.locator('[data-owner="garden-a"]').count()==3
  # Touch is immediately followed by native mouse, Enter and Space on rotate.
  q.locator('[data-piece="garden-b"]').click();q.locator('#right').click();q.locator('#right').focus();q.keyboard.press('Enter');q.keyboard.press('Space');assert ':3:' in q.locator('[data-piece="garden-b"]').get_attribute('data-icon')
  q.screenshot(path=str(OUT/f'trial-{trial+1}-{action}.jpg'));assert not errors
  results.append({'trial':trial+1,'nativeTouchRotations':icons,'explicitInterTapDelayMs':0,'mode':'select' if trial>=6 else 'drag','afterInvalidRelease':action,'mouseEnterSpaceAfterTouch':'PASS','pageErrors':errors});c.close()
 b.close()
(OUT/'report.json').write_text(json.dumps({'baseline':'063bb19','ownBuildMerge':'c9a6b2b (baseline with prior QA-only additions)','input':'native CDP touch + native mouse and keyboard; gate completed through actual UI','results':results,'physicalPhone':'NOT RUN'},indent=2)+'\n');print('PASS8/8')
