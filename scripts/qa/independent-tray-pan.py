import json
from pathlib import Path
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parents[2]/'docs/chapter-1-rc/qa/runtime-extra'
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':740,'height':360},has_touch=True,is_mobile=True);q=c.new_page();q.goto('http://127.0.0.1:5183/ruby-village/');q.locator('#continue-game').tap();q.locator('#prologue-skip').tap()
 while q.locator('#story[open]').count():q.locator('#story-action').tap()
 # Native horizontal tray gesture, intentionally no vertical lift.
 tray=q.locator('#tray');box=tray.bounding_box();client=c.new_cdp_session(q);x=box['x']+box['width']-25;y=box['y']+box['height']/2;before=tray.evaluate('(e)=>e.scrollLeft');client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
 for i in range(1,13):client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x-i*22,'y':y}]})
 client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});q.wait_for_timeout(300);after=tray.evaluate('(e)=>e.scrollLeft');last=tray.locator('[data-piece]').last;last.tap();selected=last.get_attribute('aria-pressed')=='true';assert selected;assert after>before,(before,after);q.screenshot(path=str(OUT/'last-tray-piece.jpg'),type='jpeg');report={'viewport':'740x360','nativeHorizontalPanScrollBefore':before,'nativeHorizontalPanScrollAfter':after,'lastPieceSelected':selected,'lastPiece':last.get_attribute('data-piece')};(OUT/'tray-pan.json').write_text(json.dumps(report,indent=2)+'\n');print(report);b.close()
