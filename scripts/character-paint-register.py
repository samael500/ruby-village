"""Authorized deterministic mask cleanup/repacking only. No pixel painting or pose invention."""
from PIL import Image,ImageDraw
from pathlib import Path
import json,collections,math
root=Path(__file__).resolve().parents[1];src=root/'art/characters-walk-v1/extracted';out=root/'art/characters-walk-v1/registered';out.mkdir(parents=True,exist_ok=True);directions=['e','se','sw','w','nw','ne'];records=[];sheet=Image.new('RGB',(2560,1920),'#eee5d3');draw=ImageDraw.Draw(sheet);manifest=json.loads((root/'public/assets/characters-walk-v1/manifest.json').read_text())
for row,d in enumerate(directions):
 for col in range(8):
  image=Image.open(src/f'{d}-{col+1:02}.png').convert('RGBA');alpha=image.getchannel('A');pixels=alpha.load();seen=set();components=[]
  # Retain all connected opaque anatomy/clothes components >=40px; discard isolated matte debris.
  for y in range(256):
   for x in range(256):
    if pixels[x,y]<32 or (x,y) in seen:continue
    component=[];queue=[(x,y)];seen.add((x,y))
    while queue:
     a,b=queue.pop();component.append((a,b))
     for c,e in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
      if 0<=c<256 and 0<=e<256 and (c,e) not in seen and pixels[c,e]>=32:seen.add((c,e));queue.append((c,e))
    components.append(component)
  kept=[max(components,key=len)] if components else [];mask=Image.new('L',(256,256));m=mask.load()
  for component in kept:
   for x,y in component:m[x,y]=pixels[x,y]
  image.putalpha(mask);bounds=mask.point(lambda a:255 if a>=96 else 0).getbbox();assert bounds
  footRegion=mask.crop((0,int(bounds[1]+(bounds[3]-bounds[1])*.78),256,256));feet=footRegion.point(lambda a:255 if a>=96 else 0).getbbox();assert feet
  midpoint=(feet[0]+feet[2])/2;dx=round(160-midpoint);dy=256-bounds[3]
  result=Image.new('RGBA',(320,320));result.alpha_composite(image,(dx,dy));result.save(out/f'{d}-{col+1:02}.png');frame=manifest['clips'][d]['frames'][col];frame.update(file=f'art/characters-walk-v1/registered/{d}-{col+1:02}.png',sourceRect=[0,0,320,320],frameSize=[320,320],footAnchor=[160,256])
  sheet.paste(result,(col*320,row*320),result);draw.text((col*320+5,row*320+4),f'{d}{col+1}',fill='#332c23');draw.line((col*320+150,row*320+256,col*320+170,row*320+256),fill='#bb3424',width=1)
  records.append({'direction':d,'frame':col+1,'translation':[dx,dy],'sourceBoundsAfterMask':bounds,'feetMidpoint':midpoint,'removedComponents':len(components)-len(kept),'method':'alpha>=32 largest connected body component; lower22percent silhouette feet midpoint; whole-cell integer translation only','manualStatus':'requires visual gait/foot contact review'})
manifest.update(status='repacked-candidate-phase-review-pending',productionEnabled=False,frameSize=[320,320],footAnchor=[160,256],nativeHeightPx=224,extraction='uniform entire-atlas normalization; alpha component cleanup; whole-cell integer translation to feet midpoint; no pose painting or framewise scaling')
rig=json.loads((root/'art/blender/characters/manifest.json').read_text());manifest['strideWorldUnits']=.72;manifest['sourceRigNativeHeightPx']=210;manifest['targetDisplayHeightPx']=136;manifest['projectedStridePixels']={d:round(.72*256/2.65*(136/210)*math.hypot(math.sin(c['yawRadians']),math.cos(c['yawRadians'])*math.sin(math.atan2(3.8,8))),5) for d,c in rig['clips'].items()};manifest['phaseMapping']={str(i):i*2+1 for i in range(8)};manifest['footContactsVerifiedOnPaintedPixels']=False
(root/'public/assets/characters-walk-v1/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(root/'docs/chapter-1-rc/painted-motion/repacking.json').write_text(json.dumps(records,indent=2)+'\n');sheet.save(root/'docs/chapter-1-rc/painted-motion/registered-contact-sheet.jpg',quality=92)
print('48 candidate cells repacked; visual phase review still mandatory')
