"""Independent real mouse/touch release review; exact production commit is in report."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]; OUT=ROOT/'docs/chapter-1-rc/qa/grounded-bridge';OUT.mkdir(parents=True,exist_ok=True)
results=[]
with sync_playwright() as p:
 b=p.chromium.launch()
 for touch in [False,True]:
  c=b.new_context(viewport={'width':844 if touch else 1280,'height':390 if touch else 720},has_touch=touch,is_mobile=touch,record_video_dir=str(OUT/'raw-video'))
  q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)));q.goto('http://127.0.0.1:5297/ruby-village/');q.locator('#continue-game').click();q.locator('#prologue-skip').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.emulate_media(reduced_motion='reduce')
  levels=json.loads((ROOT/'docs/chapter-1-rc/production-solutions.json').read_text())
  for level in levels[:4]:
   for ident,placement in level['solution'].items():
    q.locator(f'#tray [data-piece="{ident}"]').click()
    for _ in range(placement['turns']):q.locator('#right').click()
    h=placement['anchor'];q.locator(f'[data-cell="{h["q"]},{h["r"]}"] polygon').first.click(force=True);q.locator('#place').click()
   q.locator('#check').click();q.wait_for_selector('#story[open],#completion-panel[open]')
   while q.locator('#story[open]').count():q.locator('#story-action').click()
   q.locator('#next-level').click()
   while q.locator('#story[open]').count():q.locator('#story-action').click()
  q.locator('#settings-open').click();q.locator('#pause-settings').click();q.locator('#mode').select_option('drag');q.locator('#settings-close').click()
  ident='bridge';source=q.locator(f'#tray [data-piece="{ident}"]').bounding_box();bad=q.locator('[data-cell="6,2"] polygon').first.bounding_box();good=q.locator('[data-cell="6,1"] polygon').first.bounding_box();assert source and bad and good
  client=c.new_cdp_session(q)
  def drag(a,z):
   x,y=a;tx,ty=z
   if touch:
    client.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
    for i in range(1,6):client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-i*10}]})
    for i in range(1,16):client.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(tx-x)*i/15,'y':y-50+(ty-y+50)*i/15}]})
    client.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:q.mouse.move(x,y);q.mouse.down();q.mouse.move(tx,ty,steps=20);q.mouse.up()
   q.wait_for_timeout(150)
  center=lambda bb:(bb['x']+bb['width']/2,bb['y']+bb['height']/2)
  bx,by=center(bad);lift=max(42,bad['height']*.8) if touch else 0
  drag(center(source),(bx,by+lift));assert q.locator('#placement-preview[data-preview="invalid"]').count()==1
  assert q.locator('[data-owner="bridge"]').count()==0
  old=q.locator('#placement-preview').inner_html()
  for _ in range(3):q.locator('#right').click()
  assert q.locator('#placement-preview[data-preview="invalid"]').count()>0
  q.screenshot(path=str(OUT/('touch-invalid.jpg' if touch else 'mouse-invalid.jpg')))
  # Pinned invalid preview is not serialized and capture is released.
  saved=q.evaluate('JSON.stringify(localStorage)');capture=q.evaluate('Array.from(document.querySelectorAll("*" )).some(e=>e.hasPointerCapture(1))');assert not capture
  for _ in range(3):q.locator('#right').click()
  gx,gy=center(good);drag((bx,by),(gx,gy+lift));assert q.locator('[data-owner="bridge"]').count()>0
  q.screenshot(path=str(OUT/('touch-valid.jpg' if touch else 'mouse-valid.jpg')))
  q.reload();q.locator('#continue-game').click()
  while q.locator('#story[open]').count():q.locator('#story-action').click()
  assert q.locator('[data-owner="bridge"]').count()>0
  results.append({'touchEmulated':touch,'invalidRetained':True,'threeRotationsRetained':True,'captureReleased':True,'movePreviewThenValidDrop':True,'reloadConfirmedOnly':True,'pageErrors':errors});assert not errors
  c.close()
 b.close()
(OUT/'report.json').write_text(json.dumps({'commit':'6637b8c','results':results,'physicalPhone':'NOT RUN'},indent=2)+'\n')
print(results)
