from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,gzip,hashlib,shutil
O=Path(__file__).resolve().parent/'v4-padded-accessories';S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-stable-texture-generation-v1/accessories-padded');I=O/'generated-v1';I.mkdir(exist_ok=True)
for n in ['painted-padded-accessories-v1.png','generation-provenance.json','inputs.json','prompt-v1.txt']:shutil.copy2(S/n,I/n)
im=Image.open(I/'painted-padded-accessories-v1.png').convert('RGB');a=np.asarray(im).astype(float);w,h=im.size;fs=json.load(gzip.open(O/'actual-UV-faces.json.gz','rt'))['faces'];mask=Image.new('L',im.size);dr=ImageDraw.Draw(mask)
for f in fs:dr.polygon([(round(u*(w-1)),round((1-v)*(h-1)))for u,v in f['uv']],fill=255)
m=np.asarray(mask)>0;boundary=m&~(np.asarray(mask.filter(ImageFilter.MinFilter(3)))>0);cream=(a[:,:,0]>185)&(a[:,:,1]>170)&(a[:,:,2]>140)&((a.max(axis=2)-a.min(axis=2))<75);green=(a[:,:,1]>.93*a[:,:,0])&(a[:,:,1]>1.25*a[:,:,2])&(a[:,:,0]<180)
bg=Image.fromarray((cream*255).astype('uint8'));minimum=None
for r in range(31):
 near=np.asarray(bg.filter(ImageFilter.MaxFilter(2*r+1)))>0 if r else cream
 if (near&boundary).any():minimum=r;break
report={'status':'coverage-pending','rawSHA256':hashlib.sha256((I/'painted-padded-accessories-v1.png').read_bytes()).hexdigest(),'imageSize':[w,h],'actualUVTexels':int(m.sum()),'actualBoundaryTexels':int(boundary.sum()),'nonerodedCreamLikeFraction':float(cream[m].mean()),'nonerodedOliveLikeFraction':float(green[m].mean()),'boundaryCreamLikeFraction':float(cream[boundary].mean()),'minimumBoundaryToBackgroundChebyshevPixels':minimum,'conservativeEuclideanDistanceLowerBoundPixels':minimum-1 if minimum is not None else 30,'definition':'actual UV raster union, boundary=union minus1px erosion; background/cream R>185,G>170,B>140,spread<75. Min distance by square neighborhood dilation is Chebyshev pixel distance; no pixel edits.'}
report['status']='SUITABLE-FOR-TWO-ACTUAL-RENDERS'if report['nonerodedCreamLikeFraction']==0 and report['nonerodedOliveLikeFraction']==0 and minimum is not None and minimum>=3 else'FAIL-DO-NOT-RENDER'
q=im.copy();p=ImageDraw.Draw(q)
for f in fs:
 ps=[(round(u*(w-1)),round((1-v)*(h-1)))for u,v in f['uv']];p.line(ps+[ps[0]],fill=(0,200,255),width=1)
q.save(O/'generated-actual-UV-wire-QA.png');(O/'generated-padding-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
