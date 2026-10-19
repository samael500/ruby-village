from pathlib import Path
import json,hashlib,urllib.request,urllib.parse,subprocess
from playwright.sync_api import sync_playwright
O=Path(__file__).resolve().parent;url='http://localhost:5322/semantic-pivot-trial/review.html';join=lambda s:urllib.parse.urljoin(url,s);fetch=lambda s:urllib.request.urlopen(s,timeout=15).read();sha=lambda b:hashlib.sha256(b).hexdigest();mb=fetch(join('manifest.json'));html=fetch(url);m=json.loads(mb);assert sha(mb)=='e55516008f2f0f9c2fe1cc2fa3e9f917d398a37a8917e45675582d2280b0e20d';assert sha(html)=='cc5c567735817990ab8741b375e7842150eb7dff97dbdb33ef97e9bf12304953';assert m['estimatedOccludedPhases']==[14,15,16,17,32];assert m['fixedScale']==1.1631563024644236
for k in ['paintedAtlas','nativeAtlas','reference']:assert sha(fetch(join(m[k]['path'])))==m[k]['sha256']
report={'url':url,'authorCommit':'50d40743bd57efbe28c25370085721c57fc69fd2','manifestSha256':sha(mb),'htmlSha256':sha(html),'manifest':m,'cases':[],'scope':'semanticfullceltranslationtrialNOTnoSlipartgameacceptance'}
with sync_playwright()as p:
 b=p.chromium.launch()
 for label,vp in [('desktop',{'width':1280,'height':800}),('landscape',{'width':844,'height':390})]:
  D=O/label;D.mkdir(exist_ok=True);errors=[];failed=[];http=[];ctx=b.new_context(viewport=vp,record_video_dir=str(D/'video'),record_video_size=vp);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:failed.append({'url':r.url,'error':r.failure}));page.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  page.add_init_script("""window.qaCalls=[];window.qaPhases=[];const old=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(...a){if(['painted','native'].includes(this.canvas.id))qaCalls.push({canvas:this.canvas.id,mode:document.querySelector('#mode')?.value,args:a.slice(1),t:performance.now()});return old.apply(this,a)};function tick(t){const s=window.reviewState;if(s?.ready&&(qaPhases.at(-1)?.frame!==s.frame||qaPhases.at(-1)?.mode!==s.mode))qaPhases.push({frame:s.frame,mode:s.mode,t});requestAnimationFrame(tick)}requestAnimationFrame(tick)""")
  page.goto(url,wait_until='networkidle');page.wait_for_function('window.reviewState?.ready');modeResults={}
  for mode in ['baseline','candidate']:
   page.locator('#mode').select_option(mode);page.wait_for_timeout(3500);page.screenshot(path=str(D/f'{mode}-loop.png'));page.locator('#play').click();assert page.evaluate('reviewState.playing')is False;pause=page.evaluate('reviewState.frame');page.wait_for_timeout(140);assert page.evaluate('reviewState.frame')==pause
   for i in [0,7,8,13,14,15,16,17,18,23,24,31,32,33,38,39,40,41,46,47]:
    page.locator('#frame').focus();page.keyboard.press('Home')
    for k in range(i):page.keyboard.press('ArrowRight')
    page.wait_for_function(f'reviewState.frame==={i}');page.screenshot(path=str(D/f'{mode}-{i:02}.png'))
    state=page.evaluate('reviewState');assert bool(state['estimated'])==(i in [14,15,16,17,32])
    if i in [14,15,16,17,32]:assert 'неизвестна' in page.locator('#pivot').inner_text()
   modeResults[mode]={'pauseStableFrame':pause,'inputs':'actualkeyboardHomeArrowRight','estimatedLabelsChecked':[14,15,16,17,32]};page.locator('#play').click();page.wait_for_function('reviewState.playing');page.wait_for_timeout(250)
  page.locator('#mode').select_option('overlay');page.locator('#markers').check();page.wait_for_timeout(120);page.screenshot(path=str(D/'overlay-markers.png'));page.locator('#markers').uncheck();page.locator('#mode').select_option('candidate')
  data=page.evaluate("""()=>({calls:qaCalls,phases:qaPhases,rects:[...document.querySelectorAll('canvas')].map(c=>({id:c.id,rect:c.getBoundingClientRect().toJSON()})),scrollWidth:document.documentElement.scrollWidth,innerWidth:innerWidth})""");checks=[];unique=[]
  for mode in ['baseline','candidate']:
   for cid in ['painted','native']:
    calls=[x for x in data['calls']if x['mode']==mode and x['canvas']==cid];src={tuple(x['args'][:4])for x in calls};assert len(src)==48;seen={}
    for call in calls:
     args=call['args'];row=next(f for f in m['frames']if f['paintedRect'if cid=='painted'else'nativeRect']==args[:4]);dest=args[4:];i=row['phase']if 'phase'in row else m['frames'].index(row)
     if cid=='native':expected=[0,0,256,320]
     else:
      x,y=m['baselineDisplayOrigin'];dx,dy=row['translationNativeComparisonPx']if mode=='candidate'else[0,0];expected=[x+dx,y+dy,row['paintedRect'][2]*m['fixedScale'],row['paintedRect'][3]*m['fixedScale']]
     assert max(abs(a-b)for a,b in zip(dest,expected))<1e-8
     seen.setdefault(i,call)
    checks.append({'mode':mode,'canvas':cid,'actualCalls':len(calls),'uniquePhases':len(src),'everyDestinationMatchesDeclaredFullFrameTranslationFixedScale':True});unique.extend(seen.values())
   assert any(a['frame']==47 and z['frame']==0 and a['mode']==z['mode']==mode for a,z in zip(data['phases'],data['phases'][1:]))
  assert not errors and not failed and not http;video=page.video.path();ctx.close();data.pop('calls');report['cases'].append({'viewport':vp,'errors':errors,'failedRequests':failed,'httpFailures':http,'modeResults':modeResults,'checks':checks,'uniqueObservedActualDrawCalls':unique,'data':data,'silentVideoPath':str(video),'videoSha256':sha(Path(video).read_bytes())})
 b.close()
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('SEMANTIC_PIVOT_BROWSER_COMPLETE')
