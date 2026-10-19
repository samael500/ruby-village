"""Read-only source analysis; global canvas resize only, never pose fitting."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];O=R/'art/painted-ruta-analysis-v1';O.mkdir(exist_ok=True)
S=Path('/home/mskorokhod/life/ruby-village-36-painted-ready/art/ruta-painted-ready-v1/painted-e8-v1.png')
shutil.copy2(S,O/'painted-source.png');im=Image.open(S).convert('RGBA');w,h=im.size
norm=im.resize((1536,960),Image.Resampling.LANCZOS);norm.save(O/'global-normalized.png')
guide=Image.open(R/'art/painted-ruta-guides-v1/walk-e8-key-guide.png').convert('RGBA');markers=json.loads((R/'art/painted-ruta-guides-v1/pose-markers-e8.json').read_text())
diag=Image.new('RGB',(1536,1920),'#dddddd');d=ImageDraw.Draw(diag);rows=[]
def bbox(a,threshold=16):return a.getchannel('A').point(lambda v:255 if v>=threshold else 0).getbbox()
def feet(a):
 # Component bounds in low band: visual foot candidates, not anatomical landmarks.
 b=bbox(a);y0=max(0,b[3]-95);mask=a.getchannel('A');pts={(x,y)for y in range(y0,b[3])for x in range(a.width)if mask.getpixel((x,y))>=128};out=[]
 while pts:
  seed=pts.pop();stack=[seed];comp=[seed]
  while stack:
   x,y=stack.pop()
   for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
    if q in pts:pts.remove(q);stack.append(q);comp.append(q)
  if len(comp)>=20:out.append({'bbox':[min(x for x,y in comp),min(y for x,y in comp),max(x for x,y in comp)+1,max(y for x,y in comp)+1],'pixels':len(comp)})
 return sorted(out,key=lambda v:v['pixels'],reverse=True)
for i in range(8):
 col=i%4;row=i//4;native=(round(col*w/4),round(row*h/2),round((col+1)*w/4),round((row+1)*h/2));im.crop(native).save(O/f'native-{i:02}.png')
 rect=(col*384,row*480,(col+1)*384,(row+1)*480);p=norm.crop(rect);g=guide.crop(rect);p.save(O/f'frame-{i:02}.png');g.save(O/f'guide-{i:02}.png');pb=bbox(p);gb=bbox(g);fc=feet(p)
 rows.append({'slot':i,'walkFrameIndex':i*3,'nativeCellXYXY':native,'paintedAlpha16BBox':pb,'paintedAnyAlphaBBox':bbox(p,1),'guideAlpha16BBox':gb,'heightRatio':(pb[3]-pb[1])/(gb[3]-gb[1]),'bottomDifferencePx':pb[3]-gb[3],'low95pxComponentsNotAnkleLandmarks':fc,'guideAnkleLandmarks':{k:v['keyGuideLocalPx']for k,v in markers['frames'][i]['markers'].items()if 'ankle' in k.lower()}})
 for kind,a,bb,oy in [('painted',p,pb,row*960),('guide',g,gb,row*960+480)]:
  ox=col*384;diag.paste(a,(ox,oy),a);d.rectangle((ox+bb[0],oy+bb[1],ox+bb[2],oy+bb[3]),outline='blue');rx=ox+192;ry=oy+387.644484;d.line((rx-10,ry,rx+10,ry),fill='red',width=2);d.line((rx,ry-10,rx,ry+10),fill='red',width=2);d.text((ox+8,oy+8),f'{kind} frame {i*3}',fill='black')
 for f in fc:
  b=f['bbox'];d.rectangle((col*384+b[0],row*960+b[1],col*384+b[2],row*960+b[3]),outline='green')
diag.save(O/'registration-diagnosis.png')
report={'status':'candidate-only-not-runtime-approved','sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'sourceSize':[w,h],'globalCanvasResize':{'size':[1536,960],'scaleX':1536/w,'scaleY':960/h,'note':'one whole-sheet resize; no per-cell pose scale, crop, translation, warp or foot correction; original retained'},'rootReference':[192,387.64448404312134],'paintedAnkleLandmarks':'Not inferred: low-alpha components are foot candidates only; anatomical ankle requires visual annotation. Guide ankles are native skeletal projections.','frames':rows}
(O/'analysis.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Painted E8 original registration analysis</title><style>body{background:#eee;font:16px sans-serif}canvas{background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%) 0/24px 24px}img{max-width:100%}</style><h1>Candidate E8 — global canvas resize only</h1><p>8 phases held208.333ms each;1666.667ms cycle. No interpolation or pose correction. Red cross=fixed native root reference; blue=guide ghost. Painted anatomy/foot registration remains unaccepted.</p><button id="pause">Pause/play</button><label><input id="ghost" type="checkbox">Guide ghost</label><canvas width="384" height="480"></canvas><span id="phase"></span><h2>Painted / guide registration</h2><img src="registration-diagnosis.png"><script>const c=document.querySelector('canvas'),ctx=c.getContext('2d'),p=[],g=[];for(let i=0;i<8;i++){p[i]=new Image;p[i].src=`frame-${String(i).padStart(2,'0')}.png`;g[i]=new Image;g[i].src=`guide-${String(i).padStart(2,'0')}.png`}let run=true,k=0;document.querySelector('#pause').onclick=()=>run=!run;setInterval(()=>{ctx.clearRect(0,0,384,480);if(p[k].complete)ctx.drawImage(p[k],0,0);if(document.querySelector('#ghost').checked&&g[k].complete){ctx.globalAlpha=.35;ctx.drawImage(g[k],0,0);ctx.globalAlpha=1}ctx.strokeStyle='red';ctx.beginPath();ctx.moveTo(182,387.644484);ctx.lineTo(202,387.644484);ctx.moveTo(192,377.644484);ctx.lineTo(192,397.644484);ctx.stroke();document.querySelector('#phase').textContent=`Walk frame ${k*3}`;if(run)k=(k+1)%8},1666.666667/8)</script>''')
print(json.dumps([{k:f[k]for k in ['walkFrameIndex','heightRatio','bottomDifferencePx','paintedAlpha16BBox']}for f in rows],indent=2))
