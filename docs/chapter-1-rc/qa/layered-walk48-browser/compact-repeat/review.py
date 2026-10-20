"""Run only after coordinator confirms actual pack exists. No runtime/source mutations."""
from pathlib import Path
import argparse,json,hashlib,urllib.request,urllib.parse,io,subprocess
from PIL import Image
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://localhost:5311/art/ruta-native-layered-walk48-v2/review.html');p.add_argument('--expected-source-sha',default='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706');args=p.parse_args();O=Path(__file__).resolve().parent;O.mkdir(exist_ok=True);join=lambda x:urllib.parse.urljoin(args.url,x);sha=lambda b:hashlib.sha256(b).hexdigest()
def fetch(url):
 with urllib.request.urlopen(url,timeout=15)as r:return r.read()
raw=fetch(join('manifest.json'));manifest=json.loads(raw);assert manifest['sourceSha256']==args.expected_source_sha;assert manifest['packedFrameCount']==48;assert manifest['frameSize']==[256,320];assert manifest['deliveryTransform']['wholeCanvasUniformScale']==.5
source=Path(manifest['sourceBlend']);sourcecheck={'path':str(source),'exists':source.exists()}
if source.exists():sourcecheck['sha256']=sha(source.read_bytes());assert sourcecheck['sha256']==args.expected_source_sha
assets=[]
for variant,v in manifest['cameraVariants'].items():
 for direction,spec in v['directions'].items():
  for name,clip in spec['clips'].items():
   assert len(clip['frames'])==48;assert abs(clip['durationSeconds']-40/24)<1e-9;ab=fetch(join(clip['atlas']));af=next(x for x in manifest['files']if x['path']==clip['atlas']);assert sha(ab)==af['sha256'];atlas=Image.open(io.BytesIO(ab)).convert('RGBA');rows=[]
   for f in clip['frames']:
    pb=fetch(join(f['sourcePng']));assert sha(pb)==f['sourcePngSha256'];im=Image.open(io.BytesIO(pb)).convert('RGBA');assert im.size==(512,640);whole=im.resize((256,320),Image.Resampling.LANCZOS);x,y,w,h=f['rect'];tile=atlas.crop((x,y,x+w,y+h));assert tile.tobytes()==whole.tobytes();rows.append({'index':f['index'],'sourcePngSha256':sha(pb),'wholeHalfResizeRGBAExact':True,'sourceFrame':f['sourceFrame']})
   
   contact=Image.new('RGBA',(8*192,6*240),'#e6e2d6')
   for f in clip['frames']:
    x,y,w,h=f['rect'];tile=atlas.crop((x,y,x+w,y+h)).resize((192,240),Image.Resampling.LANCZOS);contact.alpha_composite(tile,((f['index']%8)*192,(f['index']//8)*240))
   contact.convert('RGB').save(O/f'{variant}-{direction}-{name}-all48-contact.jpg',quality=96)
   assets.append({'variant':variant,'direction':direction,'clip':name,'atlasSha256':sha(ab),'atlasSize':atlas.size,'nativeHeightPx':spec['nativeHeightPx'],'anchor':spec['footAnchor'],'frames':rows})
report={'url':args.url,'manifestSha256':sha(raw),'expectedSourceSha256':args.expected_source_sha,'sourceCheck':sourcecheck,'assets':assets,'cases':[],'scope':'standalone sprite review page, not actual game or physical phone'}
with sync_playwright()as pw:
 browser=pw.chromium.launch()
 for label,size in [('desktop',{'width':1280,'height':800}),('landscape',{'width':844,'height':390})]:
  D=O/label;D.mkdir(exist_ok=True);errors=[];fails=[];http=[];ctx=browser.new_context(viewport=size,record_video_dir=str(D/'video'),record_video_size=size);page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:fails.append({'url':r.url,'error':r.failure}));page.on('response',lambda r:http.append({'url':r.url,'status':r.status})if r.status>=400 else None)
  page.add_init_script("""window.__qaFrames=[];window.__qaDraws=[];const old=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(...a){if(this.canvas.id==='actor'){window.__qaDraws.push({image:a[0].currentSrc||a[0].src,args:a.slice(1)});if(window.__qaDraws.length>3000)window.__qaDraws.shift()}return old.apply(this,a)};function qa(){const r=window.rutaSpriteReview;if(r&&window.__qaFrames.at(-1)?.index!==r.index)window.__qaFrames.push({index:r.index,t:performance.now()});requestAnimationFrame(qa)}requestAnimationFrame(qa);""")
  page.goto(args.url,wait_until='networkidle');page.wait_for_function('window.rutaSpriteReview&&document.querySelector("#phase").max==="47"');assert page.locator('#error').inner_text()=='';page.screenshot(path=str(D/'top.png'));page.locator('#actor').scroll_into_view_if_needed();page.wait_for_timeout(3500);page.screenshot(path=str(D/'loop.png'));page.locator('#play').click();assert page.evaluate('window.rutaSpriteReview.playing')is False;paused=page.evaluate('window.rutaSpriteReview.index');page.wait_for_timeout(180);assert page.evaluate('window.rutaSpriteReview.index')==paused
  # Actual keyboard input to range: Home/ArrowRight/End rather than injected frame state.
  page.locator('#phase').focus();page.keyboard.press('Home');page.wait_for_function('window.rutaSpriteReview.index===0');page.locator('#actor').scroll_into_view_if_needed();page.screenshot(path=str(D/'frame00.png'));page.locator('#phase').focus();page.keyboard.press('End');page.wait_for_function('window.rutaSpriteReview.index===47');page.locator('#actor').scroll_into_view_if_needed();page.screenshot(path=str(D/'frame47.png'));page.locator('#play').click();page.wait_for_function('window.rutaSpriteReview.playing');page.wait_for_function('window.__qaFrames.some((r,i,a)=>i&&a[i-1].index===47&&r.index===0)',timeout=5000);page.wait_for_timeout(500);page.locator('#actor').scroll_into_view_if_needed();page.screenshot(path=str(D/'resumed.png'))
  data=page.evaluate("""()=>({frames:window.__qaFrames,draws:window.__qaDraws,status:document.querySelector('#status').textContent,live:window.rutaSpriteReview,actorRect:document.querySelector('#actor').getBoundingClientRect().toJSON(),canvasTransform:[...Object.values(document.querySelector('#actor').getContext('2d').getTransform().toJSON())],scrollWidth:document.documentElement.scrollWidth,innerWidth:innerWidth})""");draws=data['draws'];assert draws;srcRects={tuple(x['args'][:4])for x in draws};assert len(srcRects)==48,('not all48 actual source rectangles drawn',len(srcRects));assert abs(data['actorRect']['width']/data['actorRect']['height']-.8)<1e-6;dest={tuple(x['args'][4:])for x in draws};assert len(dest)==1;spec=next(iter(next(iter(manifest['cameraVariants'].values()))['directions'].values()));scale=420/spec['nativeHeightPx'];anchor=spec['footAnchor'];expected=[256-anchor[0]*scale,560-anchor[1]*scale,256*scale,320*scale];actual=list(next(iter(dest)));assert max(abs(a-b)for a,b in zip(expected,actual))<1e-7;assert data['live']['sourceSha256']==args.expected_source_sha
  case={'viewport':size,'errors':errors,'requestFailures':fails,'httpFailures':http,'pauseStableFrame':paused,'rangeHomeEndAndResumePass':True,'actualFrame47To0Observed':True,'uniqueObservedFrames':len(set(x['index']for x in data['frames'])),'uniqueActualAtlasSourceRectangles':len(srcRects),'canvasCssAspectRatio':data['actorRect']['width']/data['actorRect']['height'],'fixedDestinationDrawArgs':actual,'expectedDestinationDrawArgs':expected,'scale':scale,'referenceScale':420/512,'actual':data,'video':'silent actual Playwright browser capture, no audio track expected'};assert not errors and not fails and not http;report['cases'].append(case);vp=page.video.path();ctx.close();case['videoPath']=str(vp)
 browser.close()
(O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('BROWSER_SPRITE_REVIEW_DONE',len(report['cases']))
