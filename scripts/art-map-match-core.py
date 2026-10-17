"""Register generated facade edits; keep every full free polygon and original border unchanged."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,hashlib
root=Path(__file__).resolve().parents[1]
contracts={}
for name,rect,scale,pivot in [('gate',(180,55,642,408),.92,(400,220)),('bakery',(1030,15,1620,420),1,(0,0))]:
 folder=root/'art/chapter-1-map-match'/name;out=root/'public/assets/chapter-1-map-match'/name;out.mkdir(parents=True,exist_ok=True);before=Image.open(folder/'before.png').convert('RGB');generated=Image.open(folder/'generated-core-01.png').convert('RGB');assert before.size==generated.size==(1672,941)
 if scale!=1:
  px,py=pivot;generated=generated.transform(before.size,Image.Transform.AFFINE,(1/scale,0,px-px/scale,0,1/scale,py-py/scale),Image.Resampling.BICUBIC)
 layout_path=root/f'docs/blender-chapter-1/layouts/engine/{name}.json';layout=json.loads(layout_path.read_text());free=Image.new('L',before.size);draw=ImageDraw.Draw(free)
 for cell in layout['cells']:
  if not cell['terrain']:draw.polygon([(p['x'],p['y'])for p in cell['polygon']],fill=255)
 protected=free.filter(ImageFilter.MaxFilter(7));mask=Image.new('L',before.size);ImageDraw.Draw(mask).rectangle(rect,fill=255);mask=mask.filter(ImageFilter.GaussianBlur(9));mask=ImageChops.multiply(mask,ImageChops.invert(protected));candidate=Image.composite(generated,before,mask)
 candidate.save(folder/'core-candidate.png');candidate.save(out/'background.webp','WEBP',lossless=True,method=6);mask.save(folder/'edit-mask.png');free.save(folder/'full-free-polygons.png')
 difference=ImageChops.difference(candidate,before);changed_free=ImageChops.multiply(difference.convert('L'),free).getbbox();assert changed_free is None,(name,changed_free)
 overlay=candidate.convert('RGBA');guide=Image.new('RGBA',before.size);d=ImageDraw.Draw(guide)
 for cell in layout['cells']:d.polygon([(p['x'],p['y'])for p in cell['polygon']],fill=(255,0,0,40)if cell['terrain']else(0,170,255,25),outline=(255,0,0,220)if cell['terrain']else(0,110,255,170),width=2)
 for label,color in [('start','#00eb55'),('goal','#e53cff')]:
  p=layout[label]['pixel'];d.ellipse((p['x']-7,p['y']-7,p['x']+7,p['y']+7),fill=color)
 Image.alpha_composite(overlay,guide).convert('RGB').save(folder/'full-polygon-review.jpg',quality=95)
 contracts[name]={'status':'map-match-candidate-requires-art-and-game-review','background':f'assets/chapter-1-map-match/{name}/background.webp','canvas':{'width':1672,'height':941},'camera':layout['camera'],'anchors':{'start':layout['start']['pixel'],'goal':layout['goal']['pixel']},'geometrySha256':hashlib.sha256(layout_path.read_bytes()).hexdigest(),'layoutAdjustmentsSha256':hashlib.sha256((root/'art/blender/chapter-layouts/layout-adjustments.json').read_bytes()).hexdigest(),'source':str((folder/'generated-core-01.png').relative_to(root)),'sourceSha256':hashlib.sha256((folder/'generated-core-01.png').read_bytes()).hexdigest(),'registration':{'facadeUniformScale':scale,'pivot':list(pivot),'editableRectangle':list(rect),'featherRadius':9,'protectedFullFreePolygonsGuardPixels':3},'checks':{'fullFreePolygonPixelsChanged':0,'opaque':True,'nativeSize':[1672,941],'sourceGenerationNativeSize':[1672,941],'gameQa':'not-run','artAcceptance':'pending'},'foreground':{'reuseExisting':name=='gate','note':'Existing gate/fence layers are below y692; facade edit is above y435 and leaves their pixels unchanged'}if name=='gate'else None,'wide':None}
 (out/'manifest.json').write_text(json.dumps(contracts[name],indent=2)+'\n')
(root/'docs/chapter-1-rc/art/map-match-gate-bakery/core-contracts.json').write_text(json.dumps(contracts,indent=2)+'\n')
print('Gate/bakery core candidate exported; complete free polygon pixels unchanged, no geometric inputs modified')
