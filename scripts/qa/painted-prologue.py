from pathlib import Path
from playwright.sync_api import sync_playwright
import json
out=Path('/home/mskorokhod/life/ruby-village/docs/chapter-1-rc/evidence/painted-prologue');out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();checks=[]
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5180/ruby-village/');q.locator('#continue-game').click()
  for i in range(6):
   q.wait_for_selector('#prologue-canvas[data-ready="true"]');q.wait_for_load_state('networkidle');q.screenshot(path=str(out/f'frame-{i+1}-{w}x{h}.jpg'),type='jpeg',quality=90)
   checks.append({'frame':i,'viewport':[w,h],'actors':q.locator('[data-story-actor]').evaluate_all('(ns)=>ns.map(n=>n.getAttribute("data-story-actor"))'),'road':q.locator('[data-story-road]').count()})
   q.locator('#prologue-next').click()
  assert not errors,errors;q.close()
 b.close();(out/'report.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');print(checks)
