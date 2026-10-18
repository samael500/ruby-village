from pathlib import Path
import json
from playwright.sync_api import sync_playwright
r=Path(__file__).resolve().parents[2];o=r/'docs/chapter-1-rc/road/stream-pilot';o.mkdir(parents=True,exist_ok=True)
sol=json.loads((r/'art/chapter-1-v9/layers/water/stream-pilot/manifest.json').read_text())['solution']
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});err=[];q.on('pageerror',lambda e:err.append(str(e)));q.goto('http://127.0.0.1:5306/ruby-village/');q.locator('#continue-game').click();q.wait_for_load_state('networkidle')
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.screenshot(path=str(o/f'empty-{w}.jpg'))
  for row in sol:
   a=row['placement']
   if not a:continue
   q.locator(f'[data-piece="{row["id"]}"]').click()
   for _ in range(a['turns']):q.locator('#right').click()
   q.locator(f'[data-cell="{a["anchor"]["q"]},{a["anchor"]["r"]}"] > polygon.cell').click(force=True);q.locator('#place').click()
  q.wait_for_load_state('networkidle');q.screenshot(path=str(o/f'solved-{w}.jpg'));print(w,err,q.locator('[data-confirmed-road-cells]').get_attribute('data-confirmed-road-cells'));q.close()
 b.close()
