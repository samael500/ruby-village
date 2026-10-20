from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,gzip,hashlib,shutil,numpy as np
O=Path('/home/mskorokhod/life/ruby-village-36-uv-paint/art/ruta-native-uv-paint-pilot-v1');S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-stable-texture-generation-v1/hair');I=O/'inputs';I.mkdir(exist_ok=True)
for n in ['painted-hair-uv-v1.png','generation-provenance.json','inputs.json','prompt-v1.txt']:shutil.copy2(S/n,I/n)
im=Image.open(I/'painted-hair-uv-v1.png').convert('RGB');w,h=im.size;m=Image.new('L',im.size);dr=ImageDraw.Draw(m)
d=json.load(gzip.open(O/'hair-uv-faces.json.gz','rt'))
for f in d['faces']:dr.polygon([(round(u*(w-1)),round((1-v)*(h-1)))for u,v in f['uv']],fill=255)
a=np.asarray(im).astype(float);mask=np.asarray(m)>0;inside=np.asarray(m.filter(ImageFilter.MinFilter(7)))>0
border=np.concatenate([a[:10].reshape(-1,3),a[-10:].reshape(-1,3),a[:,:10].reshape(-1,3),a[:,-10:].reshape(-1,3)]);bg=np.median(border,axis=0);dist=np.linalg.norm(a-bg,axis=2)
r={'status':'diagnostic-only-not-UV-match-PASS','sourceSHA256':hashlib.sha256((I/'painted-hair-uv-v1.png').read_bytes()).hexdigest(),'size':[w,h],'uvDefinition':'actual native UVMap polygons, normalized; rasterized at output size, no UV modification','backgroundMedianRGB':bg.tolist(),'interiorErosionPixels':3,'uvTexels':int(mask.sum()),'interiorTexels':int(inside.sum()),'thresholdSensitivity':[]}
for t in [15,25,35,50]:
 bad=dist<t;r['thresholdSensitivity'].append({'RGBDistanceBelow':t,'wholeUVBackgroundLikeFraction':float(bad[mask].mean()),'erodedInteriorBackgroundLikeFraction':float(bad[inside].mean())})
qa=a.astype('uint8').copy();bad=inside&(dist<35);qa[bad]=[255,0,180];out=Image.fromarray(qa);ed=ImageDraw.Draw(out)
for f in d['faces']:
 ps=[(round(u*(w-1)),round((1-v)*(h-1)))for u,v in f['uv']];ed.line(ps+[ps[0]],fill=(0,255,255),width=1)
out.save(O/'hair-uv-coverage-overlay.png');(O/'hair-uv-coverage.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
