from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import urllib.request,json,hashlib
O=Path(__file__).resolve().parent;u='http://localhost:5311/art/ruta-native-volume-front-proof-v1/review.html';base=u.rsplit('/',1)[0]+'/';raw=urllib.request.urlopen(base+'source-contract.json').read();m=json.loads(raw);assert m['renderedFrameCount']==48;assert m['sourceSha256']=='09acadc1f01d1abb940723c80b8fdbd357553aa9cf8be09f7e7d225ea4b1715d';frames=m['cameraVariants']['front-proof']['directions']['front-proof']['clips']['walk']['frames'];assert len(frames)==48
proof=[]
for f in frames:
 b=urllib.request.urlopen(base+f['file']).read();assert hashlib.sha256(b).hexdigest()==f['sha256'];import io
 im=Image.open(io.BytesIO(b));assert im.size==(512,640);proof.append({'index':f['index'],'sha256':f['sha256'],'anchor':f['worldOriginAnchorPx']})
r={'url':u,'htmlSha256':hashlib.sha256(urllib.request.urlopen(u).read()).hexdigest(),'contractSha256':hashlib.sha256(raw).hexdigest(),'sourceSHA256':m['sourceSha256'],'PNGAllHashDecode':proof,'runs':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch()
 for name,w,h,dpr,touch in [('desktop-dpr1',1280,800,1,False),('desktop-dpr2',1280,800,2,False),('landscape-touch',844,390,2,True)]:
  out=O/name;out.mkdir(exist_ok=True);ctx=browser.new_context(viewport={'width':w,'height':h},device_scale_factor=dpr,record_video_dir=str(out/'video'),record_video_size={'width':w,'height':h});ctx.add_init_script('''window.__draws={};const old=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(...a){if(this.canvas.id==='actor'){window.__draws[a[0].src]={args:a.slice(1),transform:[this.getTransform().a,this.getTransform().d]}}return old.apply(this,a)}''');page=ctx.new_page();errors=[];http=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda q:errors.append([q.url,q.failure]));page.on('response',lambda q:http.append([q.url,q.status])if q.status>=400 else None)
  if touch:ctx.new_cdp_session(page).send('Emulation.setTouchEmulationEnabled',{'enabled':True,'maxTouchPoints':5})
  page.goto(u,wait_until='networkidle');page.wait_for_function('window.reviewState?.index>=0');page.wait_for_timeout(4200);page.screenshot(path=str(out/'playing.png'));run={'name':name,'state':page.evaluate('reviewState'),'actualDraws':page.evaluate('__draws'),'geometry':page.evaluate('''()=>({dpr:devicePixelRatio,viewport:[innerWidth,innerHeight],scroll:[document.documentElement.scrollWidth,document.documentElement.scrollHeight],canvas:{backing:[actor.width,actor.height],rect:actor.getBoundingClientRect().toJSON(),smoothing:actor.getContext('2d').imageSmoothingEnabled,quality:actor.getContext('2d').imageSmoothingQuality}})''')};page.locator('#pause').click()
  for phase in [0,7,8,15,16,23,24,31,32,39,40,47]:
   page.locator('#phase').fill(str(phase));page.locator('#phase').dispatch_event('input');page.wait_for_function(f'reviewState.index==={phase}');page.screenshot(path=str(out/f'phase-{phase:02}.png'))
  run.update(errors=errors,httpFailures=http,video=str(page.video.path()),touchEmulated=touch);ctx.close();r['runs'].append(run)
 browser.close()
for run in r['runs']:
 assert len(run['actualDraws'])==48
 for draw in run['actualDraws'].values():assert draw['args']==[0,0,512,640,0,0,256,320]
(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');(O/'source-contract.json').write_bytes(raw)
