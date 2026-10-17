"""Register map-matched post/forest paint while preserving complete free polygons."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];E=R/'docs/chapter-1-rc/art/map-match-post-forest';contracts={}
for name,rect in [('post',(1160,55,1585,418)),('forest',(0,0,1672,941))]:
 A=R/'art/chapter-1-map-match'/name;D=R/'public/assets/chapter-1-map-match'/name;D.mkdir(parents=True,exist_ok=True);old=Image.open(A/'before.webp').convert('RGB');paint=Image.open(A/'generated-core-01.png').convert('RGB');assert old.size==paint.size==(1672,941)
 lp=R/f'docs/blender-chapter-1/layouts/engine/{name}.json';layout=json.loads(lp.read_text());free=Image.new('L',old.size);draw=ImageDraw.Draw(free)
 for c in layout['cells']:
  if not c['terrain']:draw.polygon([(p['x'],p['y'])for p in c['polygon']],fill=255)
 protected=free.filter(ImageFilter.MaxFilter(7));mask=Image.new('L',old.size);ImageDraw.Draw(mask).rectangle(rect,fill=255)
 if name=='post':mask=mask.filter(ImageFilter.GaussianBlur(8))
 mask=ImageChops.multiply(mask,ImageChops.invert(protected));core=Image.composite(paint,old,mask);assert ImageChops.multiply(ImageChops.difference(core,old).convert('L'),free).getbbox()is None
 core.save(A/'core-candidate.png');core.save(D/'background.webp','WEBP',lossless=True,method=6);free.save(A/'full-free-polygons.png');mask.save(A/'edit-mask.png');shutil.copy(R/f'art/chapter-1-v9/map-match/{name}-map-reference.png',A/'map-reference.png')
 guide=Image.new('RGBA',old.size);g=ImageDraw.Draw(guide)
 for c in layout['cells']:g.polygon([(p['x'],p['y'])for p in c['polygon']],fill=(255,0,0,40)if c['terrain']else(0,180,255,22),outline=(255,0,0,200)if c['terrain']else(0,110,255,170),width=2)
 for k,col in [('start','#00eb55'),('goal','#e53cff')]:
  p=layout[k]['pixel'];g.ellipse((p['x']-8,p['y']-8,p['x']+8,p['y']+8),fill=col)
 Image.alpha_composite(core.convert('RGBA'),guide).convert('RGB').save(E/f'{name}-full-polygon-review.jpg',quality=95)
 pair=Image.new('RGB',(1672,941),'#e6d4b4');ref=Image.open(A/'map-reference.png').convert('RGB');ref.thumbnail((540,820));pair.paste(ref,(10,70));crop=core.crop((1130,35,1600,440))if name=='post'else core.crop((1140,0,1530,270));crop.thumbnail((1080,850));pair.paste(crop,(580,70));ImageDraw.Draw(pair).text((12,12),name+' accepted map / actual scene candidate',fill='black');pair.save(E/f'{name}-map-pair.jpg',quality=95)
 contract={'status':'map-match-candidate-requires-art-and-game-review','background':f'assets/chapter-1-map-match/{name}/background.webp','canvas':{'width':1672,'height':941},'camera':layout['camera'],'anchors':{k:layout[k]['pixel']for k in ['start','goal']},'geometrySha256':hashlib.sha256(lp.read_bytes()).hexdigest(),'layoutAdjustmentsSha256':hashlib.sha256((R/'art/blender/chapter-layouts/layout-adjustments.json').read_bytes()).hexdigest(),'source':str((A/'generated-core-01.png').relative_to(R)),'sourceSha256':hashlib.sha256((A/'generated-core-01.png').read_bytes()).hexdigest(),'beforeSha256':hashlib.sha256((A/'before.webp').read_bytes()).hexdigest(),'mapReferenceSha256':hashlib.sha256((R/'public/assets/chapter-map-v1/chapter-map-candidate.webp').read_bytes()).hexdigest(),'registration':{'editableRectangle':list(rect),'protectedFullFreePolygonsGuardPixels':3,'featherRadius':8 if name=='post'else 0},'checks':{'fullFreePolygonPixelsChanged':0,'opaque':True,'nativeSize':[1672,941],'sourceGenerationNativeSize':[1672,941],'gameQa':'not-run','artAcceptance':'pending'},'wide':None};(D/'manifest.json').write_text(json.dumps(contract,indent=2)+'\n');contracts[name]=contract
(E/'core-contracts.json').write_text(json.dumps(contracts,indent=2)+'\n');print('Post/forest native core exported; complete free polygon pixels unchanged')
