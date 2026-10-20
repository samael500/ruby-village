from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,numpy as np,hashlib,math
O=Path(__file__).resolve().parent;V=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1/v4-padded-accessories');raw=V/'generated-v1/painted-padded-accessories-v1.png';im=Image.open(raw).convert('RGB');a=np.asarray(im).astype(float);w,h=im.size;fs=json.loads((O/'actual-new-UV-faces.json').read_text());mask=Image.new('L',im.size);d=ImageDraw.Draw(mask);edges={}
for f in fs:
 pts=[tuple(v)for v in f['uv']];d.polygon([(round(x*(w-1)),round((1-y)*(h-1)))for x,y in pts],fill=255)
 for u,v in zip(pts,pts[1:]+pts[:1]):
  key=tuple(sorted([tuple(round(t,7)for t in u),tuple(round(t,7)for t in v)]));edges[key]=edges.get(key,0)+1
edgepoints=[];edgeMask=Image.new('L',im.size);draw=ImageDraw.Draw(edgeMask)
for (u,v),n in edges.items():
 if n!=1:continue
 p=np.array([u[0]*(w-1),(1-u[1])*(h-1)]);q=np.array([v[0]*(w-1),(1-v[1])*(h-1)]);count=max(1,math.ceil(float(np.linalg.norm(q-p))*4));edgepoints.extend([p+(q-p)*t/count for t in range(count+1)]);draw.line([tuple(p),tuple(q)],fill=255,width=1)
ep=np.array(edgepoints);xy=np.rint(ep).astype(int);assert (xy>=0).all()and(xy[:,0]<w).all()and(xy[:,1]<h).all();m=np.asarray(mask)>0;e=np.asarray(edgeMask)>0;cream=(a[:,:,0]>185)&(a[:,:,1]>170)&(a[:,:,2]>140)&(np.ptp(a,axis=2)<75);olive=(a[:,:,1]>.93*a[:,:,0])&(a[:,:,1]>1.25*a[:,:,2])&(a[:,:,0]<180);mins={}
for label,points in [('actualBoundarySegmentsQuarterTexelSamples',(xy[:,1],xy[:,0])),('rasterBoundarySegments',np.where(e))]:
 for radius in range(31):
  near=np.array(Image.fromarray((cream*255).astype('uint8')).filter(ImageFilter.MaxFilter(2*radius+1)))>0 if radius else cream
  if near[points].any():mins[label]=radius;break
assert not cream[m].any()and not olive[m].any()and min(mins.values())>=3
report={'status':'PASS-scoped-all-boundaries','rawSha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'sourceImageSize':[w,h],'actualPaintedFaces':len(fs),'allUVPolygonTexels':int(m.sum()),'creamLikeInsideAllPolygons':int(cream[m].sum()),'oliveLikeInsideAllPolygons':int(olive[m].sum()),'actualBoundarySegments':sum(n==1 for n in edges.values()),'boundaryContinuousSamplesMaxSpacingTexels':.25,'boundarySamplesIncludingEndpoints':len(ep),'boundarySampleCreamCount':int(cream[xy[:,1],xy[:,0]].sum()),'minDistanceToCreamBackgroundChebyshevTexels':mins,'thresholds':'cream R>185 G>170 B>140 spread<75; olive G>.93R,G>1.25B,R<180','limits':'Actual bound UV extracted independently; raster/quartertexel samples, threshold semantic limits; no bitmap edits or erosion-only acceptance.'}
(O/'padding-results.json').write_text(json.dumps(report,indent=2)+'\n');mask.save(O/'actual-all-polygons.png');edgeMask.save(O/'actual-boundary-segments.png')
