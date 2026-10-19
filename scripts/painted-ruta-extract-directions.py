"""Whole-actor extraction, five source directions; no individual transforms or anchors."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image
R=Path(__file__).resolve().parents[1];SOURCE=Path('/home/mskorokhod/life/ruby-village-36-painted-ready/art/ruta-painted-ready-v1');OUT=R/'art/painted-ruta-whole-directions-v1';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();allrows=[]
for direction in ['se','sw','w','nw','ne']:
 O=OUT/direction;O.mkdir(exist_ok=True);src=SOURCE/f'painted-base-{direction}24-v1.png';shutil.copy2(src,O/'source.png');im=Image.open(src).convert('RGBA');w,h=im.size;a=im.getchannel('A');pts={(x,y)for y in range(h)for x in range(w)if a.getpixel((x,y))>=16};parts=[];small=[]
 while pts:
  seed=pts.pop();stack=[seed];part=[seed]
  while stack:
   x,y=stack.pop()
   for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
    q=(x+dx,y+dy)
    if q in pts:pts.remove(q);stack.append(q);part.append(q)
  if len(part)>=500:parts.append({'pixels':part,'pixelCountAlpha16':len(part),'bbox':[min(x for x,y in part),min(y for x,y in part),max(x for x,y in part)+1,max(y for x,y in part)+1]})
  else:small.append(len(part))
 assert len(parts)==24,(direction,'REJECT componentcount',len(parts));parts.sort(key=lambda p:p['bbox'][1]);ordered=[]
 for row in range(4):ordered.extend(sorted(parts[row*6:row*6+6],key=lambda p:p['bbox'][0]))
 rows=[];sheet=Image.new('RGBA',(512*6,512*4))
 for i,p in enumerate(ordered):
  b=p['bbox'];c=i%6;r=i//6;origin=[round(c*w/6),round(r*h/4)];dest=[b[0]-origin[0]+128,b[1]-origin[1]+96];crop=im.crop(b)
  # Raw bbox may contain low-alpha decoration; never include visible pixels of another actor.
  for j,other in enumerate(ordered):
   if i!=j:assert not any(b[0]<=x<b[2] and b[1]<=y<b[3]for x,y in other['pixels']),(direction,i,'other actor in bbox',j)
  assert min(dest)>=0 and dest[0]+crop.width<=512 and dest[1]+crop.height<=512
  f=Image.new('RGBA',(512,512));f.paste(crop,tuple(dest));path=O/f'frame-{i:02}.png';f.save(path);assert f.crop((dest[0],dest[1],dest[0]+crop.width,dest[1]+crop.height)).tobytes()==crop.tobytes();sheet.paste(f,(c*512,r*512))
  rows.append({'index':i,'pixelCountAlpha16':p['pixelCountAlpha16'],'sourceBBoxXYXY':b,'sourceCellOriginRounded':origin,'sourceCellOriginExact':[c*w/6,r*h/4],'bboxOffsetFromCell':[b[0]-origin[0],b[1]-origin[1]],'packedBBoxOrigin':dest,'sourceToPackedTranslation':[128-origin[0],96-origin[1]],'sourceCropRawRGBASha256':hashlib.sha256(crop.tobytes()).hexdigest(),'framePngSha256':sha(path),'exactCropRGBAEquality':True})
 sheet.save(O/'whole24-sheet.png');report={'status':'unregistered-whole-actor-candidate-not-runtime','direction':direction,'sourceFile':src.name,'sourceSha256':sha(src),'sourceSize':[w,h],'componentMethod':'8-connected alpha>=16, actor>=500pixels','actorCount':24,'ignoredSmallComponentSizes':small,'otherActorWithinEachBBox':False,'frameSize':[512,512],'scale':1,'commonPaddingFromSourceCellOrigin':[128,96],'footAnchor':None,'cycleDurationMs':1666.6666666666667,'frames':rows};(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
 (O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Unregistered DIR whole Walk24</title><style>body{background:#eee;font:16px sans-serif}canvas{background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%)0/16px 16px}img{max-width:100%}</style><h1>DIR —24 whole actors, unregistered candidate</h1><p>Original source pixels scale1, common padded origin.1666.667ms cycle. No physical anchor or per-frame fitting.</p><button>Pause/play</button><span></span><br><canvas width="512" height="512"></canvas><img src="whole24-sheet.png"><script>let k=0,run=true,im=[];for(let i=0;i<24;i++){im[i]=new Image;im[i].src=`frame-${String(i).padStart(2,'0')}.png`}document.querySelector('button').onclick=()=>run=!run;setInterval(()=>{let x=document.querySelector('canvas').getContext('2d');x.clearRect(0,0,512,512);if(im[k].complete)x.drawImage(im[k],0,0);document.querySelector('span').textContent=`frame ${k}`;if(run)k=(k+1)%24},1666.666667/24)</script>'''.replace('DIR',direction.upper()))
 allrows.append({'direction':direction,'manifest':direction+'/manifest.json','loop':direction+'/index.html','actorCount':24,'sourceSha256':sha(src)});print('WHOLE_DIRECTION_OK',direction,flush=True)
(OUT/'manifest.json').write_text(json.dumps({'status':'source-only-unregistered-all-six','directions':[{'direction':'e','manifest':'../painted-ruta-whole24-v1/packing.json','loop':'../painted-ruta-whole24-v1/index.html','frameSize':[384,416]},*allrows],'newDirectionsCommonFrameSize':[512,512],'newDirectionsScale':1,'footAnchorsNotAssigned':True},indent=2)+'\n')
