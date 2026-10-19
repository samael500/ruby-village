"""Whole connected-actor packing; original RGBA, one scale, explicit source offsets."""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];O=R/'art/painted-ruta-whole24-v1';O.mkdir(exist_ok=True);S=R/'art/painted-ruta-analysis24-v1/painted-source.png';im=Image.open(S).convert('RGBA');w,h=im.size;alpha=im.getchannel('A');pts={(x,y)for y in range(h)for x in range(w)if alpha.getpixel((x,y))>=16};parts=[]
while pts:
 seed=pts.pop();stack=[seed];part=[seed]
 while stack:
  x,y=stack.pop()
  for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if q in pts:pts.remove(q);stack.append(q);part.append(q)
 if len(part)>=500:
  parts.append({'pixelCountAlpha16':len(part),'bbox':[min(x for x,y in part),min(y for x,y in part),max(x for x,y in part)+1,max(y for x,y in part)+1]})
print('ACTORS',len(parts));assert len(parts)==24,'reject: not24 separate whole actors'
parts.sort(key=lambda p:p['bbox'][1]);ordered=[]
for row in range(4):ordered.extend(sorted(parts[row*6:row*6+6],key=lambda p:p['bbox'][0]))
rows=[];sheet=Image.new('RGBA',(384*6,416*4));pad=[64,48]
for i,part in enumerate(ordered):
 c=i%6;r=i//6;b=part['bbox'];origin=[round(c*w/6),round(r*h/4)];dest=[b[0]-origin[0]+pad[0],b[1]-origin[1]+pad[1]];crop=im.crop(b);frame=Image.new('RGBA',(384,416));assert min(dest)>=0 and dest[0]+crop.width<=384 and dest[1]+crop.height<=416;frame.paste(crop,tuple(dest));frame.save(O/f'frame-{i:02}.png');sheet.paste(frame,(c*384,r*416))
 # Verify extracted rectangular raw pixels exactly; no alpha sanitization or deformation.
 assert frame.crop((dest[0],dest[1],dest[0]+crop.width,dest[1]+crop.height)).tobytes()==crop.tobytes()
 rows.append({'index':i,**part,'sourceNominalCellOriginRounded':origin,'sourceNominalCellOriginExact':[c*w/6,r*h/4],'bboxOffsetFromRoundedOrigin':[b[0]-origin[0],b[1]-origin[1]],'packedBBoxOrigin':dest,'sourceToPackedTranslation':[pad[0]-origin[0],pad[1]-origin[1]],'unverifiedGridRootReference':[pad[0]+c*w/6-origin[0]+128*w/1536,pad[1]+r*h/4-origin[1]+258.42965602874756*h/1280]})
sheet.save(O/'whole24-sheet.png');report={'status':'whole-actor-extraction-only-not-registered','sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'sourceSize':[w,h],'segmentation':'4-connected alpha>=16 components, actor minimum500pixels','actorCount':len(parts),'frameSize':[384,416],'scale':1,'padding':pad,'originalRGBAWithinSourceBBoxPreservedExactly':True,'footAnchor':None,'rootReference':'unverified original nominal grid root retained as metadata only, not anatomical support','frames':rows};(O/'packing.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>Whole painted E24 actors</title><style>body{background:#eee;font:16px sans-serif}canvas{background:repeating-conic-gradient(#ddd 0 25%,#fff 0 50%)0/16px 16px}img{max-width:100%}</style><h1>Whole painted E24 actors — unregistered</h1><p>24 separate connected actors. Original RGBA preserved, fixed source-grid origin plus common padding, scale1. No footAnchor fitting.1666.667ms cycle; right view uses common native body136px scale.</p><button>Pause/play</button><p id="phase"></p><canvas id="big" width="768" height="832"></canvas><canvas id="game" width="280" height="303"></canvas><img src="whole24-sheet.png"><script>let k=0,run=true,frames=[];for(let i=0;i<24;i++){frames[i]=new Image;frames[i].src=`frame-${String(i).padStart(2,'0')}.png`}document.querySelector('button').onclick=()=>run=!run;setInterval(()=>{for(const[id,s]of[['big',2],['game',136/(209.65872262812678*1374/1536)]]){let c=document.getElementById(id),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);if(frames[k].complete)x.drawImage(frames[k],0,0,384*s,416*s)}document.getElementById('phase').textContent=`frame ${k}`;if(run)k=(k+1)%24},1666.666667/24)</script>''')
