from pathlib import Path
from PIL import Image
import json,hashlib
O=Path(__file__).resolve().parent;Q=O.parent;R=O.parents[3];P=Q/'painted-sheet-v1.png';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sourcehash=sha(P);im=Image.open(P).convert('RGBA');w,h=im.size;assert(w,h)==(1295,1214)
def components(threshold):
 a=im.getchannel('A').tobytes();seen=bytearray(w*h);out=[];small=[]
 for q,v in enumerate(a):
  if v<=threshold or seen[q]:continue
  todo=[q];seen[q]=1;cnt=0;xmin=w;ymin=h;xmax=ymax=0
  while todo:
   p=todo.pop();cnt+=1;x=p%w;y=p//w;xmin=min(xmin,x);xmax=max(xmax,x);ymin=min(ymin,y);ymax=max(ymax,y)
   for xx,yy in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=xx<w and 0<=yy<h:
     n=yy*w+xx
     if not seen[n]and a[n]>threshold:seen[n]=1;todo.append(n)
  rec={'pixelCount':cnt,'rawBBox':[xmin,ymin,xmax+1,ymax+1]};(out if cnt>100 else small).append(rec)
 return sorted(out,key=lambda x:(round((x['rawBBox'][1]+11)/400),x['rawBBox'][0])),small
checks={}
for threshold in[16,128]:
 cs,tiny=components(threshold);assert len(cs)==12;records=[]
 for i,c in enumerate(cs):
  x=i%4*330;y=i//4*400-11;a,b,z,t=c['rawBBox'];margins=[a-x,b-y,x+330-z,y+400-t];assert min(margins)>=0,(threshold,i,margins);records.append({**c,'phase':i,'sourceGridRect':[x,y,330,400],'margins':margins})
 checks[str(threshold)]={'largeComponentCount':len(cs),'components':records,'smallComponentCount':len(tiny),'smallComponents':tiny,'minLargeComponentMarginPx':min(min(x['margins'])for x in records)}
atlas=Image.new('RGBA',(1320,1225));atlas.paste(im,(0,11));assert atlas.crop((0,11,w,h+11)).tobytes()==im.tobytes();atlas.save(O/'painted-whole-padded.png');rows=[]
for i in range(12):
 x=i%4*330;y=i//4*400;c=atlas.crop((x,y,x+330,y+400));p=O/f'frames/{i:02d}.png';c.save(p);assert Image.open(p).convert('RGBA').tobytes()==c.tobytes();mask16=c.getchannel('A').point(lambda a:255 if a>16 else 0);allbox=mask16.getbbox();rows.append({'alpha16AllPixelBBox':list(allbox),'alpha16AllPixelMargins':[allbox[0],allbox[1],330-allbox[2],400-allbox[3]],'phase':i,'atlasRect':[x,y,330,400],'sourceRect':[x,y-11,330,400],'file':f'frames/{i:02d}.png','rgbaSha256':hashlib.sha256(c.tobytes()).hexdigest(),'pngSha256':sha(p)})
oldManifest=R/'art/ruta-native-painted-sprites-v2/packing/head-pivot-trial/manifest.json';(O/'old-reference-manifest.json').write_bytes(oldManifest.read_bytes());old=json.loads(oldManifest.read_text());oldP=(oldManifest.parent/old['paintedAtlas']['path']).resolve();oldAtlas=Image.open(oldP).convert('RGBA');f=old['frames'][0];x,y,bw,bh=f['paintedRect'];old0=oldAtlas.crop((x,y,x+bw,y+bh));new0=atlas.crop((0,0,330,400));bbox=lambda a:a.getchannel('A').point(lambda x:255 if x>128 else 0).getbbox();ob=bbox(old0);nb=bbox(new0);S=old['fixedScale']*(ob[3]-ob[1])/(nb[3]-nb[1]);oldOrigin=[old['baselineDisplayOrigin'][j]+f['headTranslationNativePx'][j]for j in[0,1]];target=[oldOrigin[0]+(ob[0]+ob[2])/2*old['fixedScale'],oldOrigin[1]+ob[1]*old['fixedScale']];T=[target[0]-(nb[0]+nb[2])/2*S,target[1]-nb[1]*S]
tail=atlas.crop((0,1200,1320,1225));assert tail.getchannel('A').getextrema()[1]<=1;assert sha(P)==sourcehash
report={'status':'FIRST12CONSECUTIVEPHASES-QUALITY-CANDIDATE-NOT-FULL-LOOP-NOT-RUNTIME','sourceRawSha256':sourcehash,'rawSize':[w,h],'packing':{'sourceGridOrigin':[0,-11],'pitch':[330,400],'layout':[4,3],'atlasSize':[1320,1225],'transparentPadding':{'top':11,'right':25},'originalRawAllPixelsPreservedAt':[0,11],'unframedBottomAtlasRows':[1200,1225],'unframedBottomMaxAlpha':1,'noPerActorFitTranslateResizeCleanup':True,'extractionOnlyCommonGridCells':True,'note':'whole commoncells containactors; original extra bottomlowalpha retained byte-exact in atlas, not cleaned'},'containment':checks,'frames':rows,'atlas':{'file':'painted-whole-padded.png','sha256':sha(O/'painted-whole-padded.png')},'oldReference':{'manifest':'old-reference-manifest.json','originalManifestPath':'../../../ruta-native-painted-sprites-v2/packing/head-pivot-trial/manifest.json','manifestSha256':sha(oldManifest),'atlasSha256':sha(oldP)},'staticDisplayCalibration':{'definition':'ONE global phase0 silhouette-height and top-centre calibration against oldphase0 for SAMEapparentstaticactorheight ONLY; not physicalanchor, not motionfix. No per-frame fitting; atlas/frames remain nativeRGBA.','oldPhase0Alpha128BBox':list(ob),'newPhase0Alpha128BBox':list(nb),'newGlobalScale':S,'newGlobalOrigin':T,'all12SameScaleOrigin':True},'playback':{'phaseCount':12,'firstPhase':0,'lastPhase':11,'fps':28.8,'quarterSeconds':12/28.8,'initialPaused':True,'loop':False,'forwardThenStop':True}};(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('PACKED',checks['16']['minLargeComponentMarginPx'],S,T)
