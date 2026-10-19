"""Observed local cold load and actual-input RAF cadence, not device benchmark."""
import json,time,hashlib,statistics,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;URL='http://127.0.0.1:5298/ruby-village/';solutions=json.loads((R/'src/art-solutions.json').read_text());earned=json.loads((R/'docs/chapter-1-rc/qa/full8-production/1280/report.json').read_text())['states'][-1]['save'];reports=[]
INIT="""window.__qaLong=[];new PerformanceObserver(l=>{for(const e of l.getEntries())window.__qaLong.push({start:e.startTime,duration:e.duration,name:e.name})}).observe({type:'longtask',buffered:true});window.__qaRAF=[];window.__qaPhase=null;function qaf(t){if(window.__qaPhase)window.__qaRAF.push({phase:window.__qaPhase,t});requestAnimationFrame(qaf)}requestAnimationFrame(qaf);"""
def summary(nums):
 nums=sorted(nums)
 return {'count':len(nums),'p50Ms':statistics.median(nums)if nums else None,'p95Ms':nums[min(len(nums)-1,int(len(nums)*.95))]if nums else None,'maxMs':max(nums)if nums else None,'over50ms':sum(x>50 for x in nums),'over100ms':sum(x>100 for x in nums)}
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for sid in ['gate','mill']:
  for touch,w,h in [(False,1280,720),(True,844,390)]:
   ident=f'{sid}-{w}';dest=O/ident;dest.mkdir(exist_ok=True);opts=dict(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,reduced_motion='no-preference')
   if sid=='mill':opts['storage_state']={'cookies':[],'origins':[{'origin':'http://127.0.0.1:5298','localStorage':[{'name':'ruby-village:chapter-1:v1','value':json.dumps(earned)}]}]}
   c=b.new_context(**opts);c.add_init_script(INIT);p=c.new_page();cdp=c.new_cdp_session(p);cdp.send('Network.enable');cdp.send('Network.clearBrowserCache');cdp.send('Network.setCacheDisabled',{'cacheDisabled':True});requests={};errors=[]
   def response(e):
    r=e['response'];requests.setdefault(e['requestId'],{}).update(url=r['url'],status=r['status'],mime=r['mimeType'],fromDiskCache=r.get('fromDiskCache',False),fromServiceWorker=r.get('fromServiceWorker',False),responseEncodedBytes=r.get('encodedDataLength',0))
   def finish(e):requests.setdefault(e['requestId'],{}).update(encodedBytes=e['encodedDataLength'],finishedAt=time.monotonic())
   cdp.on('Network.responseReceived',response);cdp.on('Network.loadingFinished',finish);cdp.on('Network.loadingFailed',lambda e:errors.append(e));p.on('pageerror',lambda e:errors.append(str(e)))
   def center(n):n.scroll_into_view_if_needed();z=n.bounding_box();return(z['x']+z['width']/2,z['y']+z['height']/2)
   def tap(n):
    x,y=center(n)
    if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    else:p.mouse.click(x,y)
   def cell(q,r):return p.locator(f'#board [data-cell="{q},{r}"]>polygon.cell')
   def phase(name):p.evaluate('n=>window.__qaPhase=n',name)
   def setting(mode):
    tap(p.locator('#settings-open'));tap(p.locator('#pause-settings'));tap(p.locator('#mode'));p.keyboard.press('Home'if mode=='select'else'End');p.keyboard.press('Enter');assert p.locator('#mode').input_value()==mode;tap(p.locator('#settings-close'))
   start=time.monotonic();p.goto(URL);menuMs=(time.monotonic()-start)*1000;menuBytes=sum(v.get('encodedBytes',0)for v in requests.values());menuCount=len(requests)
   if sid=='gate':
    tap(p.locator('#continue-game'))
    while p.locator('#prologue-panel[open]').count():p.wait_for_function("document.querySelector('#prologue-canvas').dataset.ready==='true'");tap(p.locator('#prologue-next'))
   else:tap(p.locator('#choose-level'));tap(p.locator('button[data-level="mill"]'))
   entering=time.monotonic();p.wait_for_selector('#app[data-motion="ready"]');readyMs=(time.monotonic()-start)*1000;readyAfterInput=(time.monotonic()-entering)*1000;p.wait_for_load_state('networkidle');coldEnd=time.monotonic();cold=[dict(v)for v in requests.values()];resource=p.evaluate("performance.getEntriesByType('resource').map(e=>({name:e.name,start:e.startTime,duration:e.duration,transferSize:e.transferSize,encodedBodySize:e.encodedBodySize,decodedBodySize:e.decodedBodySize,initiatorType:e.initiatorType}))")
   p.screenshot(path=str(dest/'cold-ready.jpg'));cdp.send('Network.setCacheDisabled',{'cacheDisabled':False})
   while p.locator('#story[open]').count():tap(p.locator('#story-action'))
   # Probe currently visible raster dimensions after cold metrics are frozen.
   images=p.evaluate("""async()=>{let nodes=[...document.querySelectorAll('img,image')].filter(n=>{let r=n.getBoundingClientRect();return r.width&&r.height&&r.right>0&&r.bottom>0&&r.left<innerWidth&&r.top<innerHeight&&getComputedStyle(n).visibility!=='hidden'&&getComputedStyle(n).display!=='none'});let urls=[...new Set(nodes.map(n=>n.currentSrc||n.src?.baseVal||n.src||n.getAttribute('href')).filter(Boolean))];return await Promise.all(urls.map(async u=>{let i=new Image();i.src=u;try{await i.decode();return{url:i.src,width:i.naturalWidth,height:i.naturalHeight,rgbaPixelEstimate:i.naturalWidth*i.naturalHeight*4}}catch(e){return{url:String(u),decodeError:String(e)}}}))}""")
   setting('drag');piece='gate-1'if sid=='gate'else'mill-v6-a';phase('drag')
   for repeat in range(3):
    chip=p.locator(f'#tray [data-piece="{piece}"]');x,y=center(chip);tx,ty=center(cell(0,0));z=cell(0,0).bounding_box();ty+=max(42,z['height']*.8)if touch else 0
    if touch:
     cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]})
     for k in range(1,4):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-60*k/3,'id':1}]})
     for k in range(1,13):cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+(tx-x)*k/12,'y':y-60+(ty-y+60)*k/12,'id':1}]})
     cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    else:p.mouse.move(x,y);p.mouse.down();p.mouse.move(tx,ty,steps=15);p.mouse.up()
    p.wait_for_timeout(200);tap(p.locator('#other'))
   p.wait_for_timeout(250);phase(None);p.screenshot(path=str(dest/'after-drag.jpg'));setting('select')
   for piece,placement in solutions[sid].items():
    tap(p.locator(f'#tray [data-piece="{piece}"]'))
    for _ in range(placement['turns']):tap(p.locator('#right'))
    a=placement['anchor'];tap(cell(a['q'],a['r']));tap(p.locator('#place'))
   phase('walk');tap(p.locator('#check'));p.wait_for_selector('#story[open]',timeout=120000);phase(None);p.screenshot(path=str(dest/'after-walk.jpg'))
   sample=p.evaluate('({frames:window.__qaRAF,longTasks:window.__qaLong,clock:performance.now()})');phases={}
   for name in ['drag','walk']:
    frames=[v['t']for v in sample['frames']if v['phase']==name];phases[name]={'rafIntervals':summary([b-a for a,b in zip(frames,frames[1:])]),'firstTimestamp':frames[0]if frames else None,'lastTimestamp':frames[-1]if frames else None}
    lo,hi=phases[name]['firstTimestamp'],phases[name]['lastTimestamp'];tasks=[e['duration']for e in sample['longTasks']if lo is not None and lo<=e['start']<=hi];phases[name]['longTasks']=summary(tasks)
   result={'source':'7244fb2','servedBundle':'index-Booi3P-Q.js','scene':sid,'viewport':[w,h],'input':'native CDP touch + native settings select keyboard navigation'if touch else'mouse','cache':'fresh context; browser cache cleared and disabled through cold-ready snapshot; restored before interaction','network':'local localhost server, no network/CPU throttling','browser':b.version,'menuGotoReturnMs':menuMs,'menuRequestCountAtGotoReturn':menuCount,'menuEncodedBytesAtGotoReturn':menuBytes,'navToMotionReadyMs':readyMs,'afterFinalEntryInputToMotionReadyMs':readyAfterInput,'coldReadyNetworkIdleMs':(coldEnd-start)*1000,'coldRequestCount':len(cold),'coldEncodedBytes':sum(v.get('encodedBytes',0)for v in cold),'coldRequests':cold,'resourceTimings':resource,'visibleRasterDecodeProbeAfterColdSnapshot':images,'estimatedVisibleRgbaPixelBytes':sum(i.get('rgbaPixelEstimate',0)for i in images),'phases':phases,'rawFramesAndLongTasks':sample,'errors':errors,'physicalPhone':'NOT RUN','scope':'single observed local sample per scene/viewport; RAF timestamps measure scheduling cadence, not GPU presentation or universal device FPS'}
   (dest/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');reports.append(result);c.close();print('COMPLETE PERF',ident,result['coldEncodedBytes'],phases,flush=True)
 b.close()
(O/'report.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
