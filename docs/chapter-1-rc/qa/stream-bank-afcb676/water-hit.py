from pathlib import Path
from playwright.sync_api import sync_playwright
import json
O=Path(__file__).resolve().parent;reports=[]
with sync_playwright()as p:
 b=p.chromium.launch()
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);q=c.new_page();cdp=c.new_cdp_session(q)
  def tap(loc):
   box=loc.bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
   if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:q.mouse.click(x,y)
  q.goto('http://127.0.0.1:5306/ruby-village/');tap(q.locator('#continue-game'))
  while q.locator('#story[open]').count():tap(q.locator('#story-action'))
  q.wait_for_load_state('networkidle');before=q.evaluate('localStorage.getItem("ruby-village:chapter-1:v1")');attrs=q.locator('#board [data-terrain="water"]>polygon.cell').evaluate_all('ns=>ns.map(n=>({cell:n.parentElement.dataset.cell,opacity:getComputedStyle(n).opacity,pointerEvents:getComputedStyle(n).pointerEvents,fill:n.getAttribute("fill")}))');assert len(attrs)==7 and all(n['opacity']=='0' and n['pointerEvents']=='all'for n in attrs);assert q.locator('#board [data-puzzle-landmarks] text').evaluate_all('ns=>ns.every(n=>n.textContent!=="≈")')
  results=[]
  for row in attrs:
   tap(q.locator('#tray [data-piece="stream-v6-a"]'));tap(q.locator('#board [data-cell="'+row['cell']+'"]>polygon.cell'));assert q.locator('#placement-preview[data-preview="invalid"]').count();assert q.evaluate('localStorage.getItem("ruby-village:chapter-1:v1")')==before;results.append({'cell':row['cell'],'actualPointerTapProducesInvalidLandPreview':True,'saveUnchanged':True});tap(q.locator('#other'))
  q.screenshot(path=str(O/(('touch844'if touch else'mouse1280')+'-water-no-presentation-overrides.png')))
  reports.append({'nativeTouch':touch,'attributes':attrs,'waterTapResults':results,'presentationCssInjected':False});c.close()
 b.close()
(O/'water-hit.json').write_text(json.dumps(reports,indent=2)+'\n');print('PASS 14 native pointer watercell taps, hidden fill still interactive')
