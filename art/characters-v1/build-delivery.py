"""Deterministic delivery resize/encode only; source PNG and active manifests unchanged.
python3 art/characters-v1/build-delivery.py
"""
from pathlib import Path
from PIL import Image,ImageChops,ImageStat,ImageDraw,ImageFont
import json,hashlib,math
R=Path(__file__).resolve().parents[2];A=R/'public/assets/characters-v1';O=A/'optimized';O.mkdir(exist_ok=True);D=R/'docs/chapter-1-rc/characters/delivery';D.mkdir(parents=True,exist_ok=True)
pilot=json.loads((A/'manifest.json').read_text())['characters']['ruta'];res=json.loads((A/'residents-manifest.json').read_text());poses=json.loads((A/'poses-manifest.json').read_text());sources=[]
for id in ['idle-pilot','portrait-pilot']:
 f=pilot['frames'][id];portrait=id=='portrait-pilot';sources.append((f,150 if portrait else 136,384 if portrait else 512,None))
for character in res['characters'].values():
 for which,f in character['frames'].items():sources.append((f,150 if which=='portrait' else character['sceneHeightPx'],384 if which=='portrait' else 512,None))
for id,f in poses['frames'].items():sources.append((f,f['sceneHeightPx'],108 if id=='basket-ground' else 512,f.get('nativeStandingHeightPx')))
manifest={'version':1,'encoding':{'format':'WebP','quality':92,'method':6,'alpha':'lossless; decoded alpha compared bit-for-bit with resized source'},'deliveries':{},'totals':{}}
checks=[];comparisons=[];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
for f,sceneHeight,maxHeight,standing in sources:
 original=f['image'];p=A/original;sourceBytes=p.read_bytes();sourceHash=hashlib.sha256(sourceBytes).hexdigest();im=Image.open(p).convert('RGBA');w,h=im.size;factor=min(1,maxHeight/h);size=(max(1,round(w*factor)),max(1,round(h*factor)));small=im.resize(size,Image.Resampling.LANCZOS);name=Path(original).stem+'.webp';dest=O/name
 small.save(dest,'WEBP',quality=92,method=6,exact=True,alpha_quality=100);decoded=Image.open(dest).convert('RGBA');assert decoded.getchannel('A').tobytes()==small.getchannel('A').tobytes();assert p.read_bytes()==sourceBytes
 sx,sy=size[0]/w,size[1]/h;anchor=f['footAnchor'];scaledAnchor=None if anchor is None else[anchor[0]*sx,anchor[1]*sy]
 entry={'original':original,'optimized':'optimized/'+name,'image':'optimized/'+name,'frameSize':list(size),'sourceRect':[0,0,*size],'footAnchor':scaledAnchor,'sceneHeightPx':sceneHeight,'bytes':dest.stat().st_size,'originalBytes':len(sourceBytes),'sourcehash':sourceHash,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'originalFrameSize':[w,h],'originalFootAnchor':anchor,'resizeScale':[sx,sy],'originalSceneScale':sceneHeight/h,'sceneWidthPx':w*sceneHeight/h,'losslessAlphaVerified':True}
 if standing:entry['nativeStandingHeightPx']=standing*sy;entry['originalNativeStandingHeightPx']=standing;entry['sceneStandingHeightPx']=136
 manifest['deliveries'][original]=entry
 # Exact native anchor ratios remain invariant in both axes after integer-rounded export.
 if anchor:
  assert abs(scaledAnchor[0]/size[0]-anchor[0]/w)<1e-12 and abs(scaledAnchor[1]/size[1]-anchor[1]/h)<1e-12
 # Compare against full-resolution source at 2x actual scene height, preserving source aspect.
 display=(round(w*sceneHeight/h*2),round(sceneHeight*2));full=im.resize(display,Image.Resampling.LANCZOS);opt=decoded.resize(display,Image.Resampling.LANCZOS)
 metrics={}
 for color,label in [('#fbfaf6','light'),('#17232b','dark'),('#7fb78b','green')]:
  left=Image.new('RGB',display,color);left.paste(full,(0,0),full);right=Image.new('RGB',display,color);right.paste(opt,(0,0),opt);diff=ImageChops.difference(left,right);stat=ImageStat.Stat(diff);mse=sum(x*x for x in stat.rms)/3;psnr=99 if not mse else 10*math.log10(255*255/mse);metrics[label]={'psnrDb':psnr,'meanAbsoluteError':sum(stat.mean)/3,'maxChannelError':max(hi for lo,hi in diff.getextrema())}
  comparisons.append((label,original,left,right))
 checks.append({'original':original,'losslessAlpha':True,'sourceUnchanged':True,'anchorNormalizedError':0,'display2x':list(display),'comparisons':metrics})
manifest['totals']={'images':len(sources),'originalBytes':sum(e['originalBytes']for e in manifest['deliveries'].values()),'optimizedBytes':sum(e['bytes']for e in manifest['deliveries'].values())};manifest['totals']['savedFraction']=1-manifest['totals']['optimizedBytes']/manifest['totals']['originalBytes'];(A/'delivery-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(D/'checks.json').write_text(json.dumps({'images':checks,'totals':manifest['totals'],'note':'Transfer saving only after runtime opts into variants. Original files remain present by design.'},indent=2)+'\n')
# Every image at literal 2x scene display size, not enlarged to arbitrary preview resolution.
for label in ['light','dark','green']:
 pairs=[x for x in comparisons if x[0]==label];tileW=800;tileH=430;sheet=Image.new('RGB',(tileW*2,tileH*math.ceil(len(pairs)/2)),{'light':'#fbfaf6','dark':'#17232b','green':'#7fb78b'}[label]);d=ImageDraw.Draw(sheet)
 for i,(_,name,left,right) in enumerate(pairs):
  ox=(i%2)*tileW;oy=(i//2)*tileH;ink='white' if label=='dark' else'#25251e';d.text((ox+10,oy+8),name+'   PNG | WebP q92 (2x game)',font=font,fill=ink)
  # each panel is 390 wide; images fit because target max widths are <390px.
  sheet.paste(left,(ox+max(5,(390-left.width)//2),oy+55));sheet.paste(right,(ox+400+max(5,(390-right.width)//2),oy+55))
 sheet.save(D/f'comparison-2x-{label}.jpg',quality=96)
print(json.dumps(manifest['totals'],indent=2))
# Focused native-size excerpts for easy visual inspection without a giant sheet.
for label,i,name in [('dark',17,'crouch'),('light',18,'basket'),('green',19,'rabbit-baking'),('dark',1,'ruta-portrait')]:
 im=Image.open(D/f'comparison-2x-{label}.jpg');x=(i%2)*800;y=(i//2)*430;im.crop((x,y,x+800,y+430)).save(D/f'detail-{name}-{label}.jpg',quality=96)
