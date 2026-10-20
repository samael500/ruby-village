from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import urllib.request,json,hashlib,io
O=Path(__file__).resolve().parent;u='http://localhost:5311/art/ruta-native-contact-transition-pilot-v1/review.html';base=u.rsplit('/',1)[0]+'/';html=urllib.request.urlopen(u).read();raw=urllib.request.urlopen(base+'proof-manifest.json').read();assert hashlib.sha256(html).hexdigest()=='ddd293fd7fe9447affd89fdf1065b63c20b37b254d3be36d505c893458180308';assert hashlib.sha256(raw).hexdigest()=='43cc5c7ee2e2af7b66a21b06d0251b4faa4bccced6149cf877d3221d8a081e3c';m=json.loads(raw);assert len(m['frames'])==80;files={f['file']for f in m['frames']};assert len(files)==73;pngs=[]
for file in sorted(files):
 b=urllib.request.urlopen(base+file).read();im=Image.open(io.BytesIO(b));assert im.size==(256,320);pngs.append({'file':file,'sha256':hashlib.sha256(b).hexdigest(),'size':list(im.size)})
r={'url':u,'author':'2ef9366','HTMLSHA256':hashlib.sha256(html).hexdigest(),'manifestSHA256':hashlib.sha256(raw).hexdigest(),'PNG73HashDecode':pngs,'runs':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch()
 for name,w,h,dpr,touch in [('desktop',1280,800,1,False),('landscape-touch',844,390,2,True)]:
  out=O/name;out.mkdir(exist_ok=True);ctx=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=dpr,record_video_dir=str(out/'video'),record_video_size={'width':w,'height':h});ctx.add_init_script('''window.__draws={};let first=null;const origM=CanvasRenderingContext2D.prototype.moveTo,origB=CanvasRenderingContext2D.prototype.beginPath,origD=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.beginPath=function(...a){first=null;return origB.apply(this,a)};CanvasRenderingContext2D.prototype.moveTo=function(...a){if(first===null)first=a;return origM.apply(this,a)};CanvasRenderingContext2D.prototype.drawImage=function(...a){const f=document.querySelector('#seek'),m=document.querySelector('#mode');if(this.canvas.id==='stage'&&f&&m){window.__draws[m.value+':'+(window.__phaseTag??f.value)]={file:a[0].src,args:a.slice(1),firstGroundMove:first,transform:[this.getTransform().a,this.getTransform().d]}}return origD.apply(this,a)}''');page=ctx.new_page();errors=[];http=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda q:errors.append([q.url,q.failure]));page.on('response',lambda q:http.append([q.url,q.status])if q.status>=400 else None)
  if touch:ctx.new_cdp_session(page).send('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':5})
  page.goto(u,wait_until='networkidle');page.wait_for_function('window.reviewReady');states=[]
  for mode in ['fixed','route']:
   page.evaluate('(m)=>{delete window.__phaseTag;reviewSetMode(m)}',mode);page.locator('#replay').click();page.wait_for_timeout(m['durationMs']+350);assert page.evaluate('reviewState.frame')==79 and not page.evaluate('reviewState.playing');page.screenshot(path=str(out/f'{mode}-end79.png'));states.append(page.evaluate('reviewState'))
   for i in [3,4,15,16,63,64,75,76]:
    page.evaluate('(i)=>reviewSeek(i)',i);page.wait_for_timeout(30);page.screenshot(path=str(out/f'{mode}-{i:02}.png'))
  # Deterministic timestamp seeking proves every timeline entry even if display cadence skipped a short phase.
  for mode in ['fixed','route']:
   page.evaluate('(m)=>reviewSetMode(m)',mode)
   for i in range(80):page.evaluate('(i)=>{window.__phaseTag=i;reviewSeek(i)}',i)
  run={'name':name,'endStates':states,'actualDraws':page.evaluate('__draws'),'errors':errors,'httpFailures':http,'touchEmulated':touch,'geometry':page.evaluate('''()=>({viewport:[innerWidth,innerHeight],scroll:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],canvas:{backing:[stage.width,stage.height],rect:stage.getBoundingClientRect().toJSON()},state:reviewState})'''),'video':str(page.video.path())};ctx.close();r['runs'].append(run)
 browser.close()
(O/'raw-report.json').write_text(json.dumps(r,indent=2)+'\n')
for run in r['runs']:
 for mode in ['fixed','route']:
  for f in m['frames']:
   d=run['actualDraws'][mode+':'+str(f['index'])];dx,dy=f['rootProjectedDeltaPx'];bx=170 if mode=='route'else 384;origin=m['rootProjectionOriginPx'];expected=[bx-origin[0]+(dx if mode=='route'else 0),16+(dy if mode=='route'else 0),256,320];assert max(abs(a-b)for a,b in zip(d['args'],expected))<1e-8;ground=m['groundGridProjectedPx'][0][0];expectedGround=[ground[0]+bx-origin[0]-(dx if mode=='fixed'else 0),ground[1]+16-(dy if mode=='fixed'else 0)];assert max(abs(a-b)for a,b in zip(d['firstGroundMove'],expectedGround))<1e-8
(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');(O/'proof-manifest.json').write_bytes(raw)
