"""Translation-only image probe. No source pixels, pivots or player edits."""
from pathlib import Path
import json,numpy as np
from PIL import Image
O=Path(__file__).resolve().parent;R=O.parents[3];P=R/'art/ruta-native-painted-sprites-v2/packing';m=json.loads((P/'full48/manifest.json').read_text());a=np.asarray(Image.open(P/'full48'/m['paintedAtlas']['path']).convert('RGBA'),dtype=float)/255;c=[]
for f in m['frames']:
 x,y,w,h=f['paintedRect'];q=a[y:y+h,x:x+w];c.append(q[:,:,:3]*q[:,:,3:]+(1-q[:,:,3:])*.9)
def sample(img,xx,yy,dx,dy):
 x=xx+dx;y=yy+dy;ix=np.floor(x).astype(int);iy=np.floor(y).astype(int);fx=(x-ix)[...,None];fy=(y-iy)[...,None]
 return img[iy,ix]*(1-fx)*(1-fy)+img[iy,ix+1]*fx*(1-fy)+img[iy+1,ix]*(1-fx)*fy+img[iy+1,ix+1]*fx*fy
def fit(ref,img,rect):
 x0,y0,x1,y1=rect;yy,xx=np.mgrid[y0:y1,x0:x1];target=ref[y0:y1,x0:x1]
 def loss(dx,dy):return float(np.mean((sample(img,xx,yy,dx,dy)-target)**2))
 choices=[(loss(dx,dy),float(dx),float(dy))for dy in range(-18,19)for dx in range(-12,13)];err,dx,dy=min(choices)
 for step in [.5,.25,.125,.0625,.03125]:
  for _ in range(8):
   best=min((loss(dx+sx*step,dy+sy*step),dx+sx*step,dy+sy*step)for sx in [-1,0,1]for sy in [-1,0,1])
   if best[0]>=err-1e-12:break
   err,dx,dy=best
 return {'shift':[dx,dy],'rgbRms':err**.5}
upper=(55,25,102,49);lower=(55,50,102,72);rows=[]
# Common frame0 template prevents accumulated neighbour drift. Additional pair edges independent.
for i in range(48):rows.append({'phase':i,'upperToTemplate0':fit(c[0],c[i],upper),'lowerToTemplate0':fit(c[0],c[i],lower),'upperNextPair':fit(c[i],c[(i+1)%48],upper)})
# Least squares graph reconciles 48 frame0 edges and all48 neighbour edges, gauge p0=0.
A=[];bx=[];by=[]
for i in range(1,48):
 row=np.zeros(47);row[i-1]=1;A.append(row);p=rows[i]['upperToTemplate0']['shift'];bx.append(p[0]);by.append(p[1])
for i in range(48):
 j=(i+1)%48;row=np.zeros(47)
 if j:row[j-1]+=1
 if i:row[i-1]-=1
 A.append(row);p=rows[i]['upperNextPair']['shift'];bx.append(p[0]);by.append(p[1])
A=np.array(A);x=np.r_[0,np.linalg.lstsq(A,bx,rcond=None)[0]];y=np.r_[0,np.linalg.lstsq(A,by,rcond=None)[0]]
for i in range(48):rows[i]['cyclicGraphShift']=[x[i],y[i]];rows[i]['heldOutLowerMinusGraph']=(np.array(rows[i]['lowerToTemplate0']['shift'])-[x[i],y[i]]).tolist()
report={'scope':'diagnostic translation-only image registration, NOT exact semantic correspondence or physical pivot; no raster/metadata changes','templatePhase':0,'upperWindow':upper,'heldOutLowerWindow':lower,'subpixelSearchResolutionRawPx':.03125,'precisionIsNotAccuracy':True,'graph':'unit weighted common-template edges + cyclic neighbour edges; fixed gauge phase0=0; lower patch held out','rows':rows,'rawPairLoopClosureError':np.sum([r['upperNextPair']['shift']for r in rows],axis=0).tolist(),'templateVsGraphRmsRawPx':float(np.sqrt(np.mean([(np.array(r['upperToTemplate0']['shift'])-r['cyclicGraphShift'])**2 for r in rows]))),'lowerVsGraphRmsRawPx':float(np.sqrt(np.mean([np.array(r['heldOutLowerMinusGraph'])**2 for r in rows])))}
(O/'head-template.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='rows'})
