"""Real viewport rotation during actual gameplay walking, not real hardware."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/grounded-walk-portrait';OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':844,'height':390},has_touch=True,is_mobile=True);q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').tap();q.locator('#prologue-skip').tap()
 def dismiss():
  while q.locator('#story[open]').count():q.locator('#story-action').tap()
 dismiss();level=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())[0]
 for ident,placement in level['solution'].items():
  q.locator(f'#tray [data-piece="{ident}"]').tap();h=placement['anchor'];q.locator(f'[data-cell="{h["q"]},{h["r"]}"] polygon').first.tap(force=True);q.locator('#place').tap()
 q.locator('#check').tap();q.wait_for_timeout(2100);assert q.locator('#app').get_attribute('data-motion')=='walking';q.screenshot(path=str(OUT/'walking-before.jpg'))
 q.set_viewport_size({'width':390,'height':844});q.wait_for_timeout(100);before=q.locator('#ruta-marker').get_attribute('data-route-ms');q.wait_for_timeout(1500);after=q.locator('#ruta-marker').get_attribute('data-route-ms');assert before==after,(before,after);q.screenshot(path=str(OUT/'portrait-blocked.jpg'))
 q.set_viewport_size({'width':844,'height':390});q.wait_for_timeout(300);resumed=q.locator('#ruta-marker').get_attribute('data-route-ms');assert int(resumed)>int(after);q.screenshot(path=str(OUT/'walking-resumed.jpg'))
 q.wait_for_selector('#story[open],#completion-panel[open]',timeout=90000);dismiss();q.locator('#completion-panel[open]').wait_for();q.screenshot(path=str(OUT/'finished.jpg'));assert not errors
 (OUT/'report.json').write_text(json.dumps({'baseline':'5dc2036 (tracked tree 237162a)','clockBeforeWait':before,'clockAfter1500msPortrait':after,'clockAfterReturn300ms':resumed,'finished':True,'pageErrors':errors,'physicalPhone':'NOT RUN'},indent=2)+'\n');c.close();b.close()
