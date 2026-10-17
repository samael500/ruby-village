"""Actual narrative stone scale and technical-layer visibility, desktop/landscape."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
out=Path(__file__).resolve().parents[2]/'docs/chapter-1-rc/evidence/prologue-stones';out.mkdir(parents=True,exist_ok=True)
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for w,h in [(1280,720),(844,390)]:
  q=b.new_page(viewport={'width':w,'height':h});q.goto('http://127.0.0.1:5181/ruby-village/');q.locator('#continue-game').click()
  for frame in range(5):
   q.wait_for_selector('#prologue-canvas[data-ready="true"]');q.wait_for_load_state('networkidle')
   assert q.locator('#prologue-canvas [data-cell],#prologue-canvas [data-grid],#prologue-canvas #placement-preview').count()==0
   if frame in [3,4]:
    sizes=q.locator('[data-story-loose-stone]').evaluate_all('(ns)=>ns.map(n=>{const r=n.getBoundingClientRect();return {width:r.width,height:r.height}})')
    assert len(sizes)==(3 if frame==3 else 1)
    assert all(s['width']>=35 for s in sizes),sizes
    q.screenshot(path=str(out/f'frame-{frame+1}-{w}x{h}.jpg'),type='jpeg',quality=90)
    checks.append({'viewport':[w,h],'frame':frame,'stoneBounds':sizes,'technicalLayers':0,'scope':'actual prologue on dev integration; final scene art still pending'})
   q.locator('#prologue-next').click()
  q.close()
 b.close()
(out/'report.json').write_text(json.dumps(checks,indent=2)+'\n');print('PASS real narrative stones, no technical layers, two viewports')
