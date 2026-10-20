from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).resolve().parent;A=Path('/tmp/ruby-combined-loop/art/ruta-native-hair-volume-study-v1/alpha-aware');z=np.load(O/'uv-centroids.npz')
def linear(a):return np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4)
def sample(path,uv):
 a=linear(np.asarray(Image.open(path).convert('RGB'),dtype=float)/255);h,w=a.shape[:2];x=np.clip(uv[:,0]*w-.5,0,w-1);y=np.clip((1-uv[:,1])*h-.5,0,h-1);ix=np.floor(x).astype(int);iy=np.floor(y).astype(int);jx=np.minimum(ix+1,w-1);jy=np.minimum(iy+1,h-1);fx=(x-ix)[:,None];fy=(y-iy)[:,None];return (a[iy,ix]*(1-fx)+a[iy,jx]*fx)*(1-fy)+(a[jy,ix]*(1-fx)+a[jy,jx]*fx)*fy
s=sample(O/'original-painted-daisy-rgb.png',z['source']);t=sample(A/'fixed-native-rgb-bake.png',z['target']);wrong=np.where(s<=.0031308,s*12.92,1.055*s**(1/2.4)-.055)
metrics={}
for name,e in [('correctLinear',t-s),('wouldBeDoubleGamma',t-wrong)]:metrics[name]={'meanAbsoluteRGB':np.abs(e).mean(axis=0).tolist(),'medianAbsoluteRGB':np.median(np.abs(e),axis=0).tolist(),'meanLumaError':float((e@np.array([.2126,.7152,.0722])).mean())}
(O/'sample-comparison.json').write_text(json.dumps({'samples':len(s),'metrics':metrics,'sourceMeanLinear':s.mean(axis=0).tolist(),'bakeMeanLinear':t.mean(axis=0).tolist(),'bakeSHA256':hashlib.sha256((A/'fixed-native-rgb-bake.png').read_bytes()).hexdigest(),'limits':'Deterministic per-face centroids, unweighted, bilinear decoded-linear PNG samples. No per-pixel bake coverage guarantee; tiny UV chart pixels/bleed/UV interpolation may influence samples.'},indent=2)+'\n')
