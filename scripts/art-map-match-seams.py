"""Register only external72px decorative wide perimeter; original core stays exact."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,hashlib
root=Path(__file__).resolve().parents[1];checks={}
for name in ['gate','bakery']:
 f=root/'art/chapter-1-map-match'/name;o=root/'public/assets/chapter-1-map-match'/name
 source=Image.open(f/'core-candidate.png').convert('RGB');wide=Image.open(f/'wide-registered-candidate.png').convert('RGB');patch=wide.crop((800,129,2472,1070));layoutpath=root/f'docs/blender-chapter-1/layouts/engine/{name}.json';layout=json.loads(layoutpath.read_text());guard=Image.new('L',source.size);d=ImageDraw.Draw(guard)
 for cell in layout['cells']:
  if not cell['terrain']:d.polygon([(p['x'],p['y']) for p in cell['polygon']],fill=255)
 guard=guard.filter(ImageFilter.MaxFilter(13));mask=Image.new('L',source.size);px=mask.load()
 for y in range(941):
  for x in range(1672):
   distance=min(x,y,1671-x,940-y);t=max(0,1-distance/72);px[x,y]=round(255*t*t*(3-2*t))
 mask=ImageChops.multiply(mask,ImageChops.invert(guard));delivered=source.copy();diff=ImageChops.difference(delivered,source);assert all(ImageChops.multiply(channel,guard).getbbox() is None for channel in diff.split());assert diff.crop((72,72,1600,869)).getbbox() is None
 delivered.save(f/'core-seam72.png');mask.save(f/'decorative-seam72-mask.png');delivered.save(o/'background.webp','WEBP',lossless=True,method=6);
 pixels=wide.load();src=source.load()
 for wy in range(57,1142):
  for wx in range(728,2544):
   x=wx-800;y=wy-129
   if 0<=x<1672 and 0<=y<941:continue
   distance=max(-x, x-1671, -y, y-940,0)
   if distance>=72:continue
   sx=-x if x<0 else 3342-x if x>=1672 else x;sy=-y if y<0 else 1880-y if y>=941 else y;t=1-distance/72;t=t*t*(3-2*t);original=pixels[wx,wy];ref=src[sx,sy];pixels[wx,wy]=tuple(round(original[c]*(1-t)+ref[c]*t)for c in range(3))
 wide.paste(delivered,(800,129));wide.save(f/'wide-seam72.png');wide.save(o/'wide.webp','WEBP',lossless=True,method=6)
 assert ImageChops.difference(Image.open(o/'background.webp').convert('RGB'),Image.open(o/'wide.webp').convert('RGB').crop((800,129,2472,1070))).getbbox() is None
 m=json.loads((o/'manifest.json').read_text());m['decorativeSeam']={'bandPixels':72,'method':'external reflected peripheral texture feather; original core untouched','fullFreePolygonGuardPixels':6,'originalCorePreserved':str((f/'core-candidate.png').relative_to(root)),'deliveredCore':str((f/'core-seam72.png').relative_to(root)),'wideOriginalRectBitExact':True,'geometryChanges':0,'freePolygonPixelsChanged':0};m['wideStatus']='seam72-candidate-actual-review';(o/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');checks[name]=m['decorativeSeam']
(root/'docs/chapter-1-rc/art/map-match-gate-bakery/seam72-validation.json').write_text(json.dumps(checks,indent=2)+'\n');print(checks)
