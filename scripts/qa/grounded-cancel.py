"""Real release/cancel and persistence checks. No layout injection."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/grounded-cancel';OUT.mkdir(parents=True,exist_ok=True)
report=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for touch in [False,True]:
  c=b.new_context(viewport={'width':844 if touch else 1280,'height':390 if touch else 720},is_mobile=touch,has_touch=touch);q=c.new_page();q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').click();q.locator('#prologue-skip').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.locator('#tray [data-piece="gate-1"]').click();q.locator('[data-cell="3,2"] polygon').first.click(force=True);q.locator('#place').click()
  baseline=q.evaluate('JSON.stringify(localStorage)');q.locator('#tray [data-piece="gate-2"]').click();q.locator('[data-cell="0,0"] polygon').first.click(force=True);assert q.locator('#place').is_disabled();q.locator('#right').click();assert q.locator('#placement-preview[data-preview="invalid"]').count()
  q.locator('#other').click();assert q.locator('#placement-preview').count()==0;assert q.locator('[data-owner="gate-1"]').count()==1
  # Reposition a committed piece, cancel -> exact confirmed origin.
  q.locator('[data-cell="3,2"] polygon').first.click(force=True);q.locator('[data-cell="0,0"] polygon').first.click(force=True);assert q.locator('#placement-preview[data-preview="invalid"]').count();q.locator('#other').click();assert q.locator('[data-cell="3,2"][data-owner="gate-1"]').count()==1
  # Invalid preview -> pause -> portrait -> landscape -> reload leaves confirmed placement only.
  q.locator('#tray [data-piece="gate-2"]').click();q.locator('[data-cell="0,0"] polygon').first.click(force=True);q.locator('#settings-open').click();q.locator('#pause-continue').click();q.set_viewport_size({'width':390,'height':844});q.wait_for_timeout(100);q.set_viewport_size({'width':844 if touch else 1280,'height':390 if touch else 720});q.wait_for_timeout(100);q.reload();q.locator('#continue-game').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  assert q.locator('[data-cell="3,2"][data-owner="gate-1"]').count()==1;assert q.locator('[data-owner="gate-2"]').count()==0;assert not q.locator('#placement-preview').count()
  q.screenshot(path=str(OUT/('touch-reloaded.jpg' if touch else 'mouse-reloaded.jpg')))
  report.append({'touchEmulated':touch,'confirmModeInvalidPlaceDisabled':True,'cancelNewPreview':True,'cancelMovedConfirmedRestoresOrigin':True,'pausePortraitReloadOnlyConfirmed':True})
  c.close()
 b.close()
(OUT/'report.json').write_text(json.dumps({'commit':'6637b8c','checks':report},indent=2)+'\n');print(report)
