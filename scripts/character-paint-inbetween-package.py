"""Register WHOLE newly painted poses; preserve old endpoint positions/speed, measure actual soles."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
r=Path(__file__).resolve().parents[1];p=r/'art/characters-walk-v1/calm-east-v5';o=p/'inbetweens-v6';out=o/'packed';out.mkdir(exist_ok=True)
namespace={'__file__':str(r/'scripts/character-paint-stance-package.py')};exec((r/'scripts/character-paint-stance-package.py').read_text().split('frames=[];sources=[]')[0],namespace)
old=json.loads((p/'stance-corrected/manifest.json').read_text());frames=[]
for i,f in enumerate(old['frames']):
 frames.append(dict(f,sourceFile='stance-corrected/'+f['file']))
 if i==2:
  for n in [1,2]:
   name=f'near23-{n}-whole.png';im=Image.open(o/name).convert('RGBA');gold=[(x,y)for y in range(600,650)for x in range(785,820)if (lambda q:q[3]>128 and q[0]>145 and q[1]>75 and q[2]<110 and q[0]>q[1]*1.2 and q[1]>q[2]*1.5)(im.getpixel((x,y)))];box=[min(x for x,y in gold),min(y for x,y in gold),max(x for x,y in gold),max(y for x,y in gold)];root=[(box[0]+box[2])/2,(box[1]+box[3])/2];toe=max(x for x in range(550,900 if n==1 else 850)if sum(im.getpixel((x,y))[3]>180 for y in range(1187,1228))>=5);x=toe-70;y=max(y for y in range(1100,1230)if any(im.getpixel((xx,y))[3]>180 for xx in range(x-2,x+3)));scale=.188;offset=[160-root[0]*scale,256-y*scale];packed=im.transform((320,320),Image.Transform.AFFINE,(1/scale,0,-offset[0]/scale,0,1/scale,-offset[1]/scale),Image.Resampling.BICUBIC);packed.save(out/f'new-{n}.png');point=[x*scale+offset[0],256];advance=old['frames'][2]['rootAdvanceNative']+old['frames'][2]['points']['near']['native'][0]-point[0];start=advance/old['nativeStridePixels']*720;frames.append({'sourceFile':f'inbetweens-v6/packed/new-{n}.png','source':name,'rawWaistRoot':root,'rawSupport':[x,y],'rawBuckleBounds':box,'wholeFrameTranslation':offset,'planted':'near','points':{'near':{'raw':[x,y],'native':point}},'startMs':start,'rootAdvanceNative':advance,'rootAdvanceScene':advance*136/224,'contact':None})
for i,f in enumerate(frames):
 f['index']=i;f['durationMs']=(frames[i+1]['startMs']if i+1<len(frames)else 720)-f['startMs'];assert f['durationMs']>0,(i,f['durationMs'])
report=dict(old,frames=frames,frameDurationsMs=[f['durationMs']for f in frames],wholeFrameCount=len(frames),targetIntervalMsBefore=old['frames'][2]['durationMs'],targetIntervalsMsAfter=[f['durationMs']for f in frames[2:5]],targetHeldTravelSceneBefore=old['frames'][2]['durationMs']/720*old['sceneStridePixels'],targetHeldTravelSceneAfter=max(f['durationMs']for f in frames[2:5])/720*old['sceneStridePixels'],maximumHeldFrameTravelScenePixels=max(f['durationMs']for f in frames)/720*old['sceneStridePixels'],status='partial-inbetween-experiment-anatomy-review-required',productionEnabled=False)
(o/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');sheet=Image.new('RGB',(1280,345),'#eee5d3');d=ImageDraw.Draw(sheet)
for j,f in enumerate(frames[2:6]):
 im=Image.open(p/f['sourceFile']);sheet.paste(im,(j*320,0),im);d.text((j*320+5,325),f'{f["source"]} {f["durationMs"]:.1f}ms',fill='black')
sheet.save(r/'docs/chapter-1-rc/painted-motion/calm-east-inbetween-near23.jpg',quality=95)
print(json.dumps({k:report[k]for k in ['targetIntervalsMsAfter','targetHeldTravelSceneBefore','targetHeldTravelSceneAfter','maximumHeldFrameTravelScenePixels']},indent=2))
