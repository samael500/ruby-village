"""Local frozen-template algorithm adaptation; tracking arrays only, immutable RGBA."""
from pathlib import Path
import json,numpy as np,hashlib
from PIL import Image
O=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads((O/'baseline-manifest.json').read_text());c=[]
for f in m['frames']:
 im=Image.open(O/f['file']).convert('RGBA');im=im.resize((165,213),Image.Resampling.BILINEAR);q=np.asarray(im,dtype=float)/255;c.append(q[:,:,:3]*q[:,:,3:]+(1-q[:,:,3:])*.9)
def sample(img,xx,yy,dx,dy):
 x=xx+dx;y=yy+dy;ix=np.floor(x).astype(int);iy=np.floor(y).astype(int);fx=(x-ix)[...,None];fy=(y-iy)[...,None]
 return img[iy,ix]*(1-fx)*(1-fy)+img[iy,ix+1]*fx*(1-fy)+img[iy+1,ix]*(1-fx)*fy+img[iy+1,ix+1]*fx*fy
def fit(ref,img,rect):
 x0,y0,x1,y1=rect;yy,xx=np.mgrid[y0:y1,x0:x1];target=ref[y0:y1,x0:x1]
 def loss(dx,dy):
  if dx==int(dx) and dy==int(dy):return float(np.mean((img[y0+int(dy):y1+int(dy),x0+int(dx):x1+int(dx)]-target)**2))
  return float(np.mean((sample(img,xx,yy,dx,dy)-target)**2))
 choices=[(loss(dx,dy),float(dx),float(dy))for dy in range(-18,19)for dx in range(-12,13)];err,dx,dy=min(choices)
 for step in [.5,.25,.125,.0625,.03125]:
  for _ in range(8):
   best=min((loss(dx+sx*step,dy+sy*step),dx+sx*step,dy+sy*step)for sx in [-1,0,1]for sy in [-1,0,1])
   if best[0]>=err-1e-12:break
   err,dx,dy=best
 return {'shift':[dx,dy],'rgbRms':err**.5}

upper=(50,20,115,49);lower=(80,50,132,82);rows=[]
for i in range(48):
 print('HEAD_MATCH',i,flush=True);rows.append({'phase':i,'upperToTemplate0':fit(c[0],c[i],upper),'lowerToTemplate0':fit(c[0],c[i],lower),'upperNextPair':fit(c[i],c[(i+1)%48],upper)})
A=[];bx=[];by=[]
for i in range(1,48):
 row=np.zeros(47);row[i-1]=1;A.append(row);p=rows[i]['upperToTemplate0']['shift'];bx.append(p[0]);by.append(p[1])
for i in range(48):
 j=(i+1)%48;row=np.zeros(47)
 if j:row[j-1]+=1
 if i:row[i-1]-=1
 A.append(row);p=rows[i]['upperNextPair']['shift'];bx.append(p[0]);by.append(p[1])
A=np.array(A);x=np.r_[0,np.linalg.lstsq(A,bx,rcond=None)[0]];y=np.r_[0,np.linalg.lstsq(A,by,rcond=None)[0]];q=np.array([x,y]).T*2
n=json.loads((O/'inputs/native-head-projections.json').read_text());native=np.array([r['features']['Head bone head']['nativeFullPx']for r in n['rows']])*.5;path=native-native[0];S=m['fixedGlobalScale'];base=path-S*q;gauge=-np.median(base,axis=0);head=base+gauge
for i in range(48):
 rows[i]['cyclicGraphShiftTrackingPx']=[x[i],y[i]];rows[i]['cyclicGraphShiftSourceRawPx']=q[i].tolist();rows[i]['heldOutLowerMinusGraphSourceRawPx']=((np.array(rows[i]['lowerToTemplate0']['shift'])-[x[i],y[i]])*2).tolist()
report={'status':'SEPARATE-HEAD-TRANSLATION-METADATA-TRIAL-NOT-ACCEPTED-CORRECTION','frozenAlgorithmSha256':sha(O/'inputs/frozen-head-template.py'),'adaptations':['inputframes/path namespace','one fixed HALF-size tracking image only; asset pixels never resampled','integer coarse loss uses equivalent direct integer slices, original subpixel refinement unchanged','same common-template+cyclic-neighbour LS graph, phase0gauge','one median translation gauge relative to new rawbaseline, not oldclasp fit'],'trackingArraySize':[165,213],'assetFrameSize':[330,426],'upperWindowTracking':upper,'heldOutLowerWindowTracking':lower,'trackingToSourceScale':2,'subpixelSearchResolutionSourceRawPx':.0625,'precisionIsNotAccuracy':True,'nativeSourceHeadSha256':sha(O/'inputs/native-head-projections.json'),'rawPairLoopClosureTrackingPx':np.sum([r['upperNextPair']['shift']for r in rows],axis=0).tolist(),'templateVsGraphRmsSourceRawPx':float(np.sqrt(np.mean([(np.array(r['upperToTemplate0']['shift'])*2-r['cyclicGraphShiftSourceRawPx'])**2 for r in rows]))),'heldOutLowerVsGraphRmsSourceRawPx':float(np.sqrt(np.mean([np.array(r['heldOutLowerMinusGraphSourceRawPx'])**2for r in rows]))),'heldOutLowerMaxNormSourceRawPx':max(float(np.linalg.norm(r['heldOutLowerMinusGraphSourceRawPx']))for r in rows),'rows':rows};(O/'head-template-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n')
trial=json.loads(json.dumps(m));trial.update({'status':'HIGH-DETAIL48-SEPARATE-HEAD-TRANSLATION-QUALITY-CANDIDATE-NOT-RUNTIME','headRegistration':{'method':'frozen common phase0 upper-template+cyclic-neighbour graph translation only; lower face held out','nativePath':'actual nativeHeadbonehead delta HALF256x320 source; no retiming/smoothing','constantGauge':gauge.tolist(),'gaugeDefinition':'negativecoordinatewisemedian(nativeHeadDelta−fixedS*headGraphShift); mediantranslation0 relative baseline','sourceHeadTemplateSha256':sha(O/'head-template-diagnostic.json'),'nativeSourceHeadSha256':sha(O/'inputs/native-head-projections.json'),'fixedScaleUnchanged':True,'rawRGBAUnchanged':True,'noScaleRotationWarp':True,'totalUncertainty':None,'sourcePixelTranslationPrecisionNotAnatomyAccuracy':True}})
for i,f in enumerate(trial['frames']):f['headTranslationNativePx']=head[i].tolist();f['headShiftSourceRawPx']=q[i].tolist();f['heldOutLowerResidualSourceRawPx']=rows[i]['heldOutLowerMinusGraphSourceRawPx'];f['nativeHeadEndpointHalfPx']=native[i].tolist()
(O/'manifest.json').write_text(json.dumps(trial,indent=2)+'\n');print('HEAD_TRIAL_READY',report['heldOutLowerVsGraphRmsSourceRawPx'],report['heldOutLowerMaxNormSourceRawPx'],flush=True)
