from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
import json,hashlib,subprocess,math,numpy as np
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'art/chapter-1-v9/layers/water/stream-pilot';m=json.loads((D/'manifest.json').read_text());g=json.loads((R/m['geometry']).read_text());cells={c['id']:c for c in g['cells']};body=np.array(Image.open(D/m['visualWaterBodyMask']).convert('L'));truth=Image.open(D/'logical-water-mask.png');old=subprocess.check_output(['git','show','14b1f6f:art/chapter-1-v9/layers/water/stream-pilot/logical-water-mask.png'],cwd=R);assert hashlib.sha256(old).hexdigest()==hashlib.sha256((D/'logical-water-mask.png').read_bytes()).hexdigest();dry=np.array(Image.open(R/'art/chapter-1-v9/candidates/stream-dry-v1.png').convert('RGB'));native=np.array(Image.open(D/'native-background.png').convert('RGB'));changed=np.max(np.abs(native.astype(int)-dry.astype(int)),axis=2)>0
# Independently rasterise free interiors and exact18px convex cores from actual polygons.
yy,xx=np.mgrid[0:941,0:1672];free=np.zeros(body.shape,bool);core=free.copy();depth=np.zeros(body.shape,float)
for c in cells.values():
 if c['terrain'] is not None:continue
 ps=[(p['x'],p['y'])for p in c['polygon']];ds=[]
 for a,b in zip(ps,ps[1:]+ps[:1]):
  dx=b[0]-a[0];dy=b[1]-a[1];sign=1 if dx*(c['center']['y']-a[1])-dy*(c['center']['x']-a[0])>=0 else -1;ds.append(sign*(dx*(yy-a[1])-dy*(xx-a[0]))/math.hypot(dx,dy))
 mind=np.minimum.reduce(ds);free|=mind>1;core|=mind>=18
assert np.count_nonzero(body[free])==0
assert np.count_nonzero(changed&core)==0
# Boundary dry edits: use all author raster free pixels, but independently measure distance to each real exposed water edge.
edge_counts={}
for c in cells.values():
 if c['terrain']!='water':continue
 ps=[(p['x'],p['y'])for p in c['polygon']]
 for a,b in zip(ps,ps[1:]+ps[:1]):
  k=tuple(sorted((tuple(round(t,6)for t in a),tuple(round(t,6)for t in b))));edge_counts[k]=edge_counts.get(k,0)+1
edges=[k for k,v in edge_counts.items()if v==1];authorfree=np.array(Image.open(D/'free-mask.png').convert('L'))>=128;cy,cx=np.nonzero(changed&authorfree);dist=np.full(cx.shape,np.inf)
for a,b in edges:
 dx=b[0]-a[0];dy=b[1]-a[1];t=np.clip(((cx-a[0])*dx+(cy-a[1])*dy)/(dx*dx+dy*dy),0,1);dist=np.minimum(dist,np.hypot(cx-a[0]-t*dx,cy-a[1]-t*dy))
assert float(dist.max())<=12
samples={k:int(body[round(c['center']['y']),round(c['center']['x'])])for k,c in cells.items()if c['terrain']=='water' or k in ['5,1','7,1']};assert samples['5,1']==samples['7,1']==0 and all(samples[k]==255 for k,c in cells.items()if c['terrain']=='water')
colors=native[cy,cx].astype(int);cyan=int(np.count_nonzero((colors[:,2]>colors[:,0]+12)&(colors[:,1]>colors[:,0]+12)&(np.minimum(colors[:,1],colors[:,2])>70)));assert cyan==0
out=dict(logicalMaskUnchangedFrom14b1f6f=True,logicalMaskSha256=hashlib.sha256(old).hexdigest(),independentFreeInteriorWaterAlphaNonzero=0,independent18pxProtectedCoreRgbChanges=0,freeCoreSampling='integer pixel positions signed Euclidean convex-polygon distance>=18px',authorRasterFreeBoundaryChangedPixels=len(cx),independentMaximumDistanceToExposedWaterBoundaryPx=float(dist.max()),allowedDryShoreDepthPx=12,changedBoundaryCyanDiagnosticPixels=cyan,actualBodyCenterSamples=samples,geometrySha256=hashlib.sha256((R/m['geometry']).read_bytes()).hexdigest());(O/'independent-mask.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
Image.open(D/'native-background.png').crop((840,465,1075,685)).resize((705,660)).save(O/'native-bank-5-3-5-4.png')
