"""Extract uniformly registered cells, audit alpha/scale/ground drift; no per-frame realignment."""
import argparse,json,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];parser=argparse.ArgumentParser();parser.add_argument('source');args=parser.parse_args();source=Path(args.source).resolve();image=Image.open(source).convert('RGBA')
out=root/'art/characters-walk-v1/extracted';out.mkdir(parents=True,exist_ok=True);directions=['e','se','sw','w','nw','ne'];records=[];clips={};review=Image.new('RGB',(2048,1536),'#eee6d4');draw=ImageDraw.Draw(review)
# Whole-atlas normalization preserves all relative positions; never hide jitter by realigning cells.
normalized=image.resize((2048,1536),Image.Resampling.LANCZOS);normalized.save(out/'atlas-uniformly-normalized.png')
for row,direction in enumerate(directions):
 frames=[]
 for column in range(8):
  frame=normalized.crop((column*256,row*256,(column+1)*256,(row+1)*256));alpha=frame.getchannel('A');mask=alpha.point(lambda a:255 if a>=96 else 0);bounds=mask.getbbox();pixels=sum(a>=96 for a in alpha.getdata());rig=Image.open(root/f'art/blender/characters/renders/{direction}-{column*2+1:02}.png').convert('RGBA').getchannel('A').point(lambda a:255 if a>=96 else 0).getbbox();name=f'{direction}-{column+1:02}.png';frame.save(out/name)
  issues=[]
  if bounds is None:issues.append('blank-frame')
  elif bounds[0]<2 or bounds[1]<2 or bounds[2]>254 or bounds[3]>254:issues.append('cell-edge-contact-or-overlap')
  if bounds and rig and abs(bounds[3]-rig[3])>12:issues.append('ground-registration-drift-over12px')
  if pixels<500:issues.append('insufficient-figure-alpha')
  records.append({'direction':direction,'frame':column+1,'alphaPixels':pixels,'bounds':bounds,'rigBounds':rig,'groundDelta':bounds[3]-rig[3] if bounds and rig else None,'issues':issues})
  entry={'file':f'art/characters-walk-v1/extracted/{name}','sourceRect':[0,0,256,256],'frameSize':[256,256],'footAnchor':[128,215.26],'durationMs':100}
  if column in [0,4]:entry['contact']='left' if column==0 else 'right'
  frames.append(entry);review.paste(frame,(column*256,row*256),frame);draw.text((column*256+4,row*256+3),f'{direction} {column+1}',fill='#29291f');draw.line((column*256+118,row*256+215,column*256+138,row*256+215),fill='#bd3729',width=1)
 clips[direction]={'loop':True,'frames':frames}
for direction in directions:
 group=[r for r in records if r['direction']==direction and r['bounds']];heights=[r['bounds'][3]-r['bounds'][1] for r in group]
 if heights and max(heights)-min(heights)>18:
  for record in group:record['issues'].append('height-variation-over18px')
status='rejected-registration' if any(r['issues'] for r in records) else 'candidate-requires-anatomy-and-motion-review'
manifest={'schemaVersion':1,'status':status,'productionEnabled':False,'source':str(source.relative_to(root)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceSize':list(image.size),'extraction':'uniform entire-atlas resize to2048x1536, exact256 cell crop; no per-frame reposition/scale/mirroring','frameSize':[256,256],'footAnchor':[128,215.26],'nativeHeightPx':210,'cycleDurationMs':800,'fps':10,'clips':clips}
(root/'public/assets/characters-walk-v1/manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(root/'docs/chapter-1-rc/painted-motion/alpha-registration-audit.json').write_text(json.dumps({'status':status,'transparentPixels':sum(a==0 for a in image.getchannel('A').getdata()),'opaquePixels':sum(a==255 for a in image.getchannel('A').getdata()),'records':records},indent=2)+'\n');review.save(root/'docs/chapter-1-rc/painted-motion/contact-sheet.jpg',quality=92)
print(status)
