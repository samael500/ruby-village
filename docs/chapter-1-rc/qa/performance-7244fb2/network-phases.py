"""Extra network-only cold sample: phase tagged before actual UI actions."""
import json,time
from pathlib import Path
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parent;reports=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for touch,w,h in [(False,1280,720),(True,844,390)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch);p=c.new_page();cdp=c.new_cdp_session(p);cdp.send('Network.enable');cdp.send('Network.clearBrowserCache');cdp.send('Network.setCacheDisabled',{'cacheDisabled':True});phase='menu';frame=None;rows={};markers=[]
  def sent(e):rows.setdefault(e['requestId'],{}).update(url=e['request']['url'],requestPhase=phase,requestFrame=frame,cdpTimestamp=e['timestamp'])
  def response(e):r=e['response'];rows.setdefault(e['requestId'],{}).update(status=r['status'],mime=r['mimeType'],responsePhase=phase,fromDiskCache=r.get('fromDiskCache',False),fromServiceWorker=r.get('fromServiceWorker',False))
  def finish(e):rows.setdefault(e['requestId'],{}).update(encodedBytes=e['encodedDataLength'],finishPhase=phase)
  cdp.on('Network.requestWillBeSent',sent);cdp.on('Network.responseReceived',response);cdp.on('Network.loadingFinished',finish)
  def mark(label):markers.append({'label':label,'performanceMs':p.evaluate('performance.now()')})
  def tap(n):
   n.scroll_into_view_if_needed();r=n.bounding_box();x,y=r['x']+r['width']/2,r['y']+r['height']/2
   if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:p.mouse.click(x,y)
  p.goto('http://127.0.0.1:5298/ruby-village/');mark('menu-goto-load-return');phase='prologue';frame=0;tap(p.locator('#continue-game'))
  while p.locator('#prologue-panel[open]').count():
   p.wait_for_function("document.querySelector('#prologue-canvas').dataset.ready==='true'");frame=int(p.locator('#prologue-panel').get_attribute('data-frame'));mark('prologue-frame-'+str(frame)+'-ready')
   if frame==5:phase='gate-entry';mark('before-last-prologue-next')
   else:frame+=1
   tap(p.locator('#prologue-next'))
  p.wait_for_selector('#app[data-motion="ready"]');mark('gate-motion-ready');p.wait_for_load_state('networkidle');mark('gate-network-idle');out={'source':'7244fb2','viewport':[w,h],'phaseDefinition':'requestPhase set before actual user action; responsePhase/finishPhase can differ because prior downloads finish later','cache':'fresh context, cache cleared/disabled','markers':markers,'requests':list(rows.values()),'scope':'network-only extra sample; timings include automated actual UI progression, no bandwidth/CPU throttling'}
  (O/f'network-phases-{w}.json').write_text(json.dumps(out,indent=2)+'\n');reports.append(out);c.close();print('PHASES',w,len(out['requests']),flush=True)
 b.close()
