"""Whole-pose stance registration and measured source-space timing; never deform limbs."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
root=Path(__file__).resolve().parents[1];p=root/'art/characters-walk-v1/calm-east-v5';out=p/'stance-corrected';out.mkdir(exist_ok=True)
names=['key-0-tight.png','between-1-raw.png','phase-2-guide-only-painted.png','between-3-fixed.png','key-2-raw.png','between-5-contact-cleanup.png','phase-6-guide-only-painted.png','phase-7-guide-only-painted.png'];scale=.188;nativeheight=224;sceneheight=136

def waist(im):
 pixels=im.load();remaining=set()
 for y in range(600,660):
  for x in range(785,850):
   r,g,b,a=pixels[x,y]
   if a>128 and r>145 and g>75 and b<110 and r>g*1.2 and g>b*1.5:remaining.add((x,y))
 components=[]
 while remaining:
  first=remaining.pop();todo=[first];c=[first]
  while todo:
   x,y=todo.pop()
   for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if q in remaining:remaining.remove(q);todo.append(q);c.append(q)
  xs=[q[0]for q in c];ys=[q[1]for q in c];box=[min(xs),min(ys),max(xs),max(ys)]
  if box[3]-box[1]>=20 and box[2]-box[0]>=10:components.append((len(c),box))
 assert components,'waist buckle not found';_,box=max(components);return[(box[0]+box[2])/2,(box[1]+box[3])/2],box

def point(im,foot,phase):
 # Toe-front silhouette is observable independently from waist registration. Select corresponding forefoot pad70source px behind toe.
 manual=(phase==0 and foot=='far')or(phase==7 and foot=='far')
 if manual:x=740 if phase==0 else 820;toe=None
 else:
  ranges={('near',0):(800,1150),('near',1):(710,1100),('near',2):(640,1000),('near',3):(480,820),('near',4):(450,790),('far',4):(800,1150),('far',5):(700,1120),('far',6):(850,1050)};left,right=ranges[(foot,phase)];valid=[]
  for x in range(left,right):
   count=sum(im.getpixel((x,y))[3]>180 for y in range(1050,1230))
   if count>=5:valid.append(x)
  toe=max(valid);assert toe<right-1,(phase,foot,'toe truncated');x=toe-70
 ys=[y for y in range(1050,1230)if any(im.getpixel((xx,y))[3]>180 for xx in range(x-2,x+3))];assert ys,(phase,foot);return{'raw':[x,max(ys)],'toeFrontX':toe,'method':'manual visible forefoot pad; toe partially occluded'if manual else'observed toe-front silhouette minus70source px, outsole alpha boundary','manualUncertaintySourcePixels':8 if manual else 4}

frames=[];sources=[]
for i,name in enumerate(names):
 im=Image.open(p/name).convert('RGBA');assert im.size==(1254,1254);r,b=waist(im);points={}
 for foot in ['near','far']:
  if(foot=='near'and i<=4)or(foot=='far'and(i==0 or i>=4)):points[foot]=point(im,foot,i)
 planted='near'if i<4 else'far';plant=points[planted]['raw'];offset=[160-r[0]*scale,256-plant[1]*scale];packed=im.transform((320,320),Image.Transform.AFFINE,(1/scale,0,-offset[0]/scale,0,1/scale,-offset[1]/scale),Image.Resampling.BICUBIC);packed.save(out/f'{i:02}.png')
 for foot,item in points.items():item['native']=[item['raw'][0]*scale+offset[0],item['raw'][1]*scale+offset[1]]
 frames.append({'index':i,'source':name,'file':f'{i:02}.png','rawWaistRoot':r,'rawBuckleBounds':b,'wholeFrameTranslation':offset,'nativeWaistRoot':[160,r[1]*scale+offset[1]],'planted':planted,'points':points});sources.append(im)
# Each interval uses ONLY the actual support foot. Swinging foot is never required to be stationary.
deltas=[]
for i in range(8):
 foot=frames[i]['planted'];a=frames[i]['points'][foot]['native'][0];b=frames[(i+1)%8]['points'][foot]['native'][0];deltas.append(a-b)
assert all(d>0 for d in deltas),('nonmonotonic planted source',deltas)
stride=sum(deltas);duration=720;elapsed=0;advance=0;world_audit={'near':[],'far':[]}
for i,f in enumerate(frames):
 f['durationMs']=duration*deltas[i]/stride;f['startMs']=elapsed;f['rootAdvanceNative']=advance;f['rootAdvanceScene']=advance*sceneheight/nativeheight;f['intervalSourceRootDistancePixels']=deltas[i]/scale;f['intervalNativeRootDistancePixels']=deltas[i];f['contact']='near'if i==0 else'far'if i==4 else None
 for foot in ['near','far']:
  if foot==f['planted']:world_audit[foot].append({'frame':i,'worldX':advance+f['points'][foot]['native'][0],'worldY':f['points'][foot]['native'][1]})
 elapsed+=f['durationMs'];advance+=deltas[i]
assert abs(elapsed-720)<1e-8
for foot,items in world_audit.items():
 xs=[q['worldX']for q in items];ys=[q['worldY']for q in items];assert max(xs)-min(xs)<1e-8;assert max(ys)-min(ys)<1e-8
report={'status':'source-boundary-calibrated-needs-independent-moving-loop-review','productionEnabled':False,'cycleDurationMs':720,'sourceCanvas':[1254,1254],'frameSize':[320,320],'uniformRawToNativeScale':scale,'nativeHeight':nativeheight,'sceneHeight':sceneheight,'footAnchor':[160,256],'sourceStridePixels':stride/scale,'nativeStridePixels':stride,'sceneStridePixels':stride*sceneheight/nativeheight,'frameDurationsMs':[f['durationMs']for f in frames],'contactTimesMs':{'near':0,'far':frames[4]['startMs']},'calibration':'positive measured support displacement sets each duration; Y registered by actual support outsole; no Xoffset beyond visible waist registration, no perframe scaling','landmarkDefinition':'toe-front alpha silhouette minus70source pixels, visible forefoot pad; partly occluded far pads0/7 manually inspected','landmarkUncertaintySourcePixels':8,'sourceBoundaryWorldSupport':world_audit,'importantLimits':['Zero boundary residual follows the measured calibration and is not independent proof','Held whole PNGs with continuous root movement can drift between source boundaries; recording must be reviewed','Far pads0/7 are manually corresponded, uncertainty and boot rolling remain','This is E loop only; no new idle/start/stop/turn or other directions'],'maximumHeldFrameTravelScenePixels':max(deltas)*sceneheight/nativeheight,'nativeWaistYRange':[min(f['nativeWaistRoot'][1]for f in frames),max(f['nativeWaistRoot'][1]for f in frames)],'frames':frames}
(out/'manifest.json').write_text(json.dumps(report,indent=2)+'\n')
# Native strip and raw annotation are reviewable, not just a numerical fit.
sheet=Image.new('RGB',(1280,690),'#eee5d3');draw=ImageDraw.Draw(sheet)
for i,(f,im)in enumerate(zip(frames,sources)):
 packed=Image.open(out/f'{i:02}.png');x=i%4*320;y=i//4*345;sheet.paste(packed,(x,y),packed);draw.text((x+8,y+323),f'{i}/8 {f["durationMs"]:.1f}ms support:{f["planted"]}',fill='#333');mark=im.copy();d=ImageDraw.Draw(mark);d.rectangle(f['rawBuckleBounds'],outline='#00cc55',width=3)
 for foot,q in f['points'].items():
  px,py=q['raw'];d.ellipse((px-8,py-8,px+8,py+8),outline='#00aaff'if foot=='near'else'#ff33dd',width=3);d.text((px+10,py-20),f'{foot} {px},{py}',fill='white')
 bg=Image.new('RGBA',im.size,'#645746');bg.alpha_composite(mark);bg.convert('RGB').save(out/f'landmark-{i}.jpg',quality=96)
sheet.save(root/'docs/chapter-1-rc/painted-motion/calm-east-stance-all8.jpg',quality=96)
print(json.dumps({k:report[k]for k in ['status','sourceStridePixels','nativeStridePixels','sceneStridePixels','frameDurationsMs','contactTimesMs','nativeWaistYRange','maximumHeldFrameTravelScenePixels']},indent=2))
