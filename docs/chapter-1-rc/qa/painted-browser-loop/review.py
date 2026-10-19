"""Independent actual browser UI capture; no source, image, or registration edits."""
import json,hashlib,time
from pathlib import Path
from playwright.sync_api import sync_playwright
S=Path('/home/mskorokhod/life/ruby-village-36-painted-ready');O=Path(__file__).resolve().parent;URL='http://localhost:5310/ruta-painted-ready-v1/review.html'
files=['art/ruta-painted-ready-v1/review.html','art/painted-ruta-artist-origin24-v1/artist-origin-proposal.json']+[f'art/painted-ruta-whole24-v1/frame-{i:02}.png'for i in range(24)]+[f'art/painted-ruta-analysis24-v1/guide-{i:02}.png'for i in range(24)]
hashes={p:hashlib.sha256((S/p).read_bytes()).hexdigest()for p in files};data=json.loads((S/files[1]).read_text());reports=[]
MEASURE="""()=>{let out={};for(const id of ['painted','native']){let c=document.querySelector('#'+id),a=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let x0=c.width,y0=c.height,x1=-1,y1=-1,count=0,edge=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(a[(y*c.width+x)*4+3]>=16){count++;x0=Math.min(x0,x);y0=Math.min(y0,y);x1=Math.max(x1,x);y1=Math.max(y1,y);if(x<2||y<2||x>=c.width-2||y>=c.height-2)edge++}out[id]={backing:[c.width,c.height],cssBox:c.getBoundingClientRect().toJSON(),alpha16BBox:[x0,y0,x1+1,y1+1],alphaPixelCount:count,alphaIn2PxEdge:edge,png:c.toDataURL()};}return{phase:Number(document.querySelector('#number').textContent),slider:document.querySelector('#frame').value,button:document.querySelector('#play').textContent,canvases:out,scroll:[scrollX,scrollY],viewport:[innerWidth,innerHeight],pageScrollWidth:document.documentElement.scrollWidth}}"""
with sync_playwright()as pw:
 b=pw.chromium.launch(headless=True,args=['--no-sandbox'])
 for touch,w,h in [(False,1280,800),(True,844,390)]:
  dest=O/str(w);dest.mkdir(exist_ok=True);c=b.new_context(viewport={'width':w,'height':h},has_touch=touch,is_mobile=touch,record_video_dir=str(dest/'raw'),record_video_size={'width':w,'height':h});p=c.new_page();cdp=c.new_cdp_session(p);errors=[];http=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  def tap(n):
   n.scroll_into_view_if_needed();z=n.bounding_box();x,y=z['x']+z['width']/2,z['y']+z['height']/2
   if touch:cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   else:p.mouse.click(x,y)
  p.goto(URL);p.wait_for_function("document.querySelector('#status').textContent.startsWith('24 кадра')");p.wait_for_load_state('networkidle');assert p.locator('#painted').get_attribute('width')=='360';tap(p.locator('#play'));assert p.locator('#play').inner_text()=='Играть';p.locator('#frame').focus();p.keyboard.press('Home');p.wait_for_function("document.querySelector('#number').textContent==='0'");states=[]
  for i in range(24):
   if i:p.locator('#frame').focus();p.keyboard.press('ArrowRight')
   p.wait_for_function('i=>Number(document.querySelector("#number").textContent)===i',arg=i);p.locator('#painted').scroll_into_view_if_needed();p.wait_for_timeout(40);m=p.evaluate(MEASURE)
   for name,v in m['canvases'].items():
    import base64
    raw=base64.b64decode(v.pop('png').split(',')[1]);(dest/f'{i:02}-{name}-actual-canvas.png').write_bytes(raw);v['pngSha256']=hashlib.sha256(raw).hexdigest()
   assert m['phase']==i and m['slider']==str(i);assert m['canvases']['painted']['alphaIn2PxEdge']==0 and m['canvases']['native']['alphaIn2PxEdge']==0,m
   p.screenshot(path=str(dest/f'{i:02}-actual-viewport.jpg'));states.append(m)
  paused=p.evaluate(MEASURE);p.wait_for_timeout(300);still=p.evaluate(MEASURE);assert paused['phase']==still['phase'] and paused['canvases']['painted']['png']==still['canvases']['painted']['png'],'pause is not stable'
  # Read-only observer records actual visible phase transitions, including wrap.
  p.evaluate("""()=>{window.__qaTransitions=[];let last=null;new MutationObserver(()=>{let k=Number(document.querySelector('#number').textContent);if(k!==last){window.__qaTransitions.push({phase:k,ms:performance.now()});last=k}}).observe(document.querySelector('#number'),{childList:true,characterData:true,subtree:true})}""")
  tap(p.locator('#play'));assert p.locator('#play').inner_text()=='Пауза';p.locator('#painted').scroll_into_view_if_needed();p.wait_for_timeout(8700);timeline=p.evaluate('window.__qaTransitions');tap(p.locator('#play'));p.locator('#painted').scroll_into_view_if_needed();p.screenshot(path=str(dest/'actual-loop-end.jpg'));seen=sorted(set(x['phase']for x in timeline));wraps=sum(a['phase']==23 and z['phase']==0 for a,z in zip(timeline,timeline[1:]));assert seen==list(range(24))and wraps>=4,(seen,wraps);assert not errors and not http
  report={'sourceHashes':hashes,'viewport':[w,h],'input':'native CDP touch buttons + real range keyboard navigation'if touch else'mouse buttons + real range keyboard navigation','states':states,'pauseStable300ms':True,'loopTimeline':timeline,'observedWraps23to0':wraps,'all24ActualPhasesObserved':True,'pageErrors':errors,'httpErrors':http,'physicalPhone':'NOT RUN','scope':'2D browser presentation of whole painted E actor, not actual game route/physical no-slip/source-rig acceptance','artistOriginIsPhysicalSupport':False,'browser':b.version};(dest/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');reports.append(report);video=p.video;c.close();video.save_as(str(dest/'actual-phase-controls-and-loop-silent.webm'))
  for f in(dest/'raw').glob('*'):f.unlink()
  (dest/'raw').rmdir();print('PASS actualpaintedloop',w,'wraps',wraps,flush=True)
 b.close()
after={p:hashlib.sha256((S/p).read_bytes()).hexdigest()for p in files};assert hashes==after,'source changed during review';(O/'source-hashes.json').write_text(json.dumps({'sourceRoot':str(S),'before':hashes,'after':after,'unchanged':hashes==after,'noSourceEdits':True,'presentationBackingCanvas':[360,360]},indent=2)+'\n')
