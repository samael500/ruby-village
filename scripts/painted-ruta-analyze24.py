"""Fixed rational-cell E24 analysis: no per-frame registration or scale correction."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'art/painted-ruta-analysis24-v1';O.mkdir(exist_ok=True);S=Path('/home/mskorokhod/life/ruby-village-36-painted-ready/art/ruta-painted-ready-v1/painted-e24-v1.png');shutil.copy2(S,O/'painted-source.png');im=Image.open(S).convert('RGBA');w,h=im.size
# One common sheet transform, then fixed cells; native rational cells also retained.
norm=im.resize((1536,1280),Image.Resampling.LANCZOS);norm.save(O/'global-normalized.png');guide=Image.open(R/'art/painted-ruta-guides-v1/walk-e24-guide.png').convert('RGBA');diag=Image.new('RGB',(1536,2560),'#ddd');d=ImageDraw.Draw(diag);rows=[]
def mainbbox(a):
 mask=a.getchannel('A');pts={(x,y)for y in range(a.height)for x in range(a.width)if mask.getpixel((x,y))>=16};best=[]
 while pts:
  q=pts.pop();stack=[q];part=[q]
  while stack:
   x,y=stack.pop()
   for v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
    if v in pts:pts.remove(v);stack.append(v);part.append(v)
  if len(part)>len(best):best=part
 return [min(x for x,y in best),min(y for x,y in best),max(x for x,y in best)+1,max(y for x,y in best)+1]
def bbox(a,t):return a.getchannel('A').point(lambda v:255 if v>=t else 0).getbbox()
for i in range(24):
 c=i%6;r=i//6;native=[round(c*w/6),round(r*h/4),round((c+1)*w/6),round((r+1)*h/4)];im.crop(native).save(O/f'native-{i:02}.png');rect=[c*256,r*320,(c+1)*256,(r+1)*320];p=norm.crop(rect);g=guide.crop(rect);p.save(O/f'frame-{i:02}.png');g.save(O/f'guide-{i:02}.png');pb=bbox(p,16);gb=bbox(g,16)
 rows.append({'index':i,'sourceFrame':40*i/24,'nativeCellXYXY':native,'paintedAlpha16BBox':pb,'paintedLargestAlpha16ComponentBBox':mainbbox(p),'paintedAnyAlphaBBox':bbox(p,1),'guideAlpha16BBox':gb,'heightRatio':(pb[3]-pb[1])/(gb[3]-gb[1]),'bottomDeltaPx':pb[3]-gb[3],'topDeltaPx':pb[1]-gb[1],'alpha16TouchesCellBoundary':pb[0]==0 or pb[1]==0 or pb[2]==256 or pb[3]==320})
 for label,a,b,y in [('painted',p,pb,r*640),('guide',g,gb,r*640+320)]:
  x=c*256;diag.paste(a,(x,y),a);d.rectangle((x+b[0],y+b[1],x+b[2],y+b[3]),outline='blue');rx=x+128;ry=y+258.429656;d.line((rx-8,ry,rx+8,ry),fill='red');d.line((rx,ry-8,rx,ry+8),fill='red');d.text((x+4,y+4),f'{label} {i}',fill='black')
diag.save(O/'registration-diagnosis.png')
report={'status':'unregistered-candidate-not-runtime','sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'sourceSize':[w,h],'globalSheetResize':[1536,1280],'globalScale':[1536/w,1280/h],'individualPoseCorrection':False,'cycleDurationMs':1666.6666666666667,'frameSize':[256,320],'rootReference':[128,258.42965602874756],'display136Scale':136/209.65872262812678,'displayScaleExplanation':'same scale as native bodyReference209.6587; painted body not individually normalized to136','visibleThreshold':16,'frames':rows}
(O/'analysis.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Unregistered painted E24</title><style>body{font:16px sans-serif;background:#eee}canvas{background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%)0/16px 16px}img{max-width:100%}</style><h1>Unregistered painted E24</h1><p>1666.667ms cycle; fixed global canvas transform only. Red cross=native root reference, no anchor correction. Game view uses native body reference scale136/209.6587; painted height drift remains visible.</p><button id="pause">Pause/play</button><label><input type="checkbox" id="ghost">Native guide ghost</label><label><input type="checkbox" id="native">Show native guide instead</label><p id="phase"></p><canvas id="large" width="512" height="640"></canvas><canvas id="game" width="166" height="208"></canvas><h2>Each painted row followed by guide row</h2><img src="registration-diagnosis.png"><script>let run=true,k=0;const p=[],g=[],scale=136/209.65872262812678;for(let i=0;i<24;i++){p[i]=new Image;p[i].src=`frame-${String(i).padStart(2,'0')}.png`;g[i]=new Image;g[i].src=`guide-${String(i).padStart(2,'0')}.png`}document.querySelector('#pause').onclick=()=>run=!run;function draw(id,s){let c=document.querySelector(id),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);let a=document.querySelector('#native').checked?g[k]:p[k];if(a.complete)x.drawImage(a,0,0,256*s,320*s);if(document.querySelector('#ghost').checked&&g[k].complete){x.globalAlpha=.35;x.drawImage(g[k],0,0,256*s,320*s);x.globalAlpha=1}x.strokeStyle='red';x.beginPath();x.moveTo(120*s,258.429656*s);x.lineTo(136*s,258.429656*s);x.moveTo(128*s,250.429656*s);x.lineTo(128*s,266.429656*s);x.stroke()}setInterval(()=>{draw('#large',2);draw('#game',scale);document.querySelector('#phase').textContent=`frame ${k}`;if(run)k=(k+1)%24},1666.666667/24)</script>''')
print('height ratios',min(f['heightRatio']for f in rows),max(f['heightRatio']for f in rows));print('bottom deltas',min(f['bottomDeltaPx']for f in rows),max(f['bottomDeltaPx']for f in rows));print('edge contacts',[f['index']for f in rows if f['alpha16TouchesCellBoundary']])
