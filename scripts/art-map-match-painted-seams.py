"""Apply localized builtin painted cleanup only to decorative ring, preserving free ground."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json
root=Path(__file__).resolve().parents[1];checks={}
for name in ['gate','bakery']:
 f=root/'art/chapter-1-map-match'/name;o=root/'public/assets/chapter-1-map-match'/name
 generated=Image.open(f/'seam-painted-01.png').convert('RGB').resize((3272,1200),Image.Resampling.LANCZOS);wide=Image.open(f/'wide-seam72.png').convert('RGB');core=Image.open(f/'core-candidate.png').convert('RGB');layout=json.loads((root/f'docs/blender-chapter-1/layouts/engine/{name}.json').read_text());guard=Image.new('L',core.size);d=ImageDraw.Draw(guard)
 for cell in layout['cells']:
  if not cell['terrain']:d.polygon([(p['x'],p['y'])for p in cell['polygon']],fill=255)
 guard=guard.filter(ImageFilter.MaxFilter(13));mask=Image.new('L',wide.size);p=mask.load()
 for y in range(1200):
  for x in range(3272):
   a=x-800;b=y-129
   if 0<=a<1672 and 0<=b<941:
    distance=min(a,b,1671-a,940-b);t=max(0,1-distance/72)
    if guard.getpixel((a,b)):t=0
   else:
    distance=max(-a,a-1671,-b,b-940,0);t=min(1,max(0,(192-distance)/80))
   p[x,y]=round(255*t*t*(3-2*t))
 # Original central core replaces prior candidate before applying painted ring.
 wide.paste(core,(800,129));result=Image.composite(generated,wide,mask);delivered=result.crop((800,129,2472,1070));diff=ImageChops.difference(delivered,core);assert all(ImageChops.multiply(c,guard).getbbox() is None for c in diff.split());assert diff.crop((72,72,1600,869)).getbbox() is None
 result.save(f/'wide-painted-seams.png');delivered.save(f/'core-painted-seams.png');mask.save(f/'painted-seam-mask.png');result.save(o/'wide.webp','WEBP',lossless=True,method=6);delivered.save(o/'background.webp','WEBP',lossless=True,method=6)
 assert ImageChops.difference(Image.open(o/'background.webp').convert('RGB'),Image.open(o/'wide.webp').convert('RGB').crop((800,129,2472,1070))).getbbox() is None
 m=json.loads((o/'manifest.json').read_text());m['decorativeSeam']={'method':'builtin imagegen local painted cleanup, constrained source-pixel composite','coreBandPixels':72,'outerAdjacencyPixels':192,'freePolygonGuardPixels':6,'fullFreePolygonPixelsChanged':0,'geometryChanges':0,'coreInteriorPixelsChanged':0,'wideOriginalRectBitExact':True,'originalCorePreserved':'core-candidate.png','source':'seam-painted-01.png','status':'candidate-pending-art-review'};checks[name]=m['decorativeSeam'];(o/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
(root/'docs/chapter-1-rc/art/map-match-gate-bakery/painted-seam-validation.json').write_text(json.dumps(checks,indent=2)+'\n')
print(checks)
