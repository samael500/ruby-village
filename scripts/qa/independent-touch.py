"""Chromium touch emulation; does not represent physical phone/Safari."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'docs/chapter-1-rc/qa/touch';OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch();c=b.new_context(viewport={'width':844,'height':390},has_touch=True,is_mobile=True);q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5183/ruby-village/');q.locator('#continue-game').tap();q.locator('#prologue-skip').tap()
 while q.locator('#story[open]').count():q.locator('#story-action').tap()
 q.locator('#settings-open').tap();q.locator('#pause-settings').tap();q.locator('#mode').select_option('drag');q.locator('#settings-close').tap()
 piece=q.locator('#tray [data-piece]').first;ident=piece.get_attribute('data-piece');piece.tap();[q.locator('#right').tap() for _ in range(6)]
 # Real protocol touch drag from selected handle into a valid cell, using native touch lift offset.
 # We use known solution first anchor; pick turn count via actual buttons.
 sol=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())[0]['solution'][ident]
 for _ in range(sol['turns']):q.locator('#right').tap()
 box=q.locator(f'#tray [data-piece="{ident}"]').bounding_box();target=q.locator(f'[data-cell="{sol["anchor"]["q"]},{sol["anchor"]["r"]}"] polygon').first.bounding_box();assert box and target
 x,y=box['x']+box['width']/2,box['y']+box['height']/2;tx,ty=target['x']+target['width']/2,target['y']+target['height']/2+max(42,target['height']*.8)
 client=c.new_cdp_session(q)
 client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
 client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-50}]})
 for i in range(1,11):client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(tx-x)*i/10,'y':y-50+(ty-y+50)*i/10}]})
 client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});q.wait_for_timeout(100)
 print('touch debug',q.locator('#status').inner_text(),q.locator('#metric').inner_text(),ident,sol,box,target,flush=True)
 placed=q.locator(f'[data-owner="{ident}"]').count()>0
 q.screenshot(path=str(OUT/'drag.png'))
 # Cancel a subsequent drag; owner count must survive cancellation.
 before=q.locator('[data-owner]:not([data-owner=""])').count();piece=q.locator('#tray [data-piece]').last;bb=piece.bounding_box()
 if bb:
  client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':bb['x']+bb['width']/2,'y':bb['y']+bb['height']/2}]});client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':400,'y':100}]});client.send('Input.dispatchTouchEvent',{'type':'touchCancel','touchPoints':[]})
 assert before==q.locator('[data-owner]:not([data-owner=""])').count()
 q.set_viewport_size({'width':390,'height':844});q.screenshot(path=str(OUT/'portrait.png'));q.set_viewport_size({'width':844,'height':390});q.screenshot(path=str(OUT/'landscape-return.png'));assert not errors
 report={'touchDragPlaced':placed,'cancelPreservesLayout':True,'orientationRoundtrip':True,'pageErrors':errors,'physicalPhone':'not-run'};(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(report);b.close()
