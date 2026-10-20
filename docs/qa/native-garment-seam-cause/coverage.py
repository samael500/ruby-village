from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
O=Path(__file__).resolve().parent;B=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1');j=json.loads((O/'actual-uv.json').read_text());rows=[]
for obj in j['objects']:
 file=B/('trousers-only/generated-v1/painted-trousers-uv-v1.png'if'trousers'in obj['object']else'rejected-mixed-v1/painted-garment-uv-v1.png');im=Image.open(file).convert('RGB');a=np.array(im);w,h=im.size;edge={}
 for f in obj['faces']:
  pts=[tuple(round(float(x),7)for x in uv)for uv in f['uv']]
  for u,v in zip(pts,pts[1:]+pts[:1]):
   k=tuple(sorted([u,v]));edge[k]=edge.get(k,0)+1
 mask=Image.new('L',im.size);draw=ImageDraw.Draw(mask)
 for f in obj['faces']:draw.polygon([(x*(w-1),(1-y)*(h-1))for x,y in f['uv']],fill=255)
 m=np.array(mask)>0;linear=np.where(a/255<=.04045,a/255/12.92,((a/255+.055)/1.055)**2.4);bg=np.array([232,225,210]if'trousers'in obj['object']else[234,227,211])/255;bg=np.where(bg<=.04045,bg/12.92,((bg+.055)/1.055)**2.4);dist=np.linalg.norm(linear-bg,axis=2);cov=m&(dist<.15);ov=im.copy();d=ImageDraw.Draw(ov)
 for (u,v),n in edge.items():
  if n==1:d.line([(u[0]*(w-1),(1-u[1])*(h-1)),(v[0]*(w-1),(1-v[1])*(h-1))],fill=(0,255,255),width=1)
 ov.save(O/('trousers-actual-island-boundaries.png'if'trousers'in obj['object']else'feet-actual-island-boundaries.png'))
 rows.append({'object':obj['object'],'UVRasterPixels':int(m.sum()),'BeigeLikePixelsInsideActualUVPolygons':int(cov.sum()),'beigeLikeLinearDistanceBelow':.15,'rawRGBA':Image.open(file).mode,'islandBoundarySegments':sum(n==1 for n in edge.values())})
(O/'coverage.json').write_text(json.dumps({'coverage':rows,'packedImages':j['packedImages'],'limits':'Rasterization/texel source coverage diagnostic, not shader filtered screen pixels or cleanup mask.'},indent=2)+'\n')
