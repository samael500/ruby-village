from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,gzip,shutil,hashlib
O=Path(__file__).resolve().parent;T=O/'trousers-only';S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-stable-texture-generation-v1/trousers');I=T/'generated-v1';I.mkdir(exist_ok=True)
for n in ['painted-trousers-uv-v1.png','generation-provenance.json','inputs.json','prompt-v1.txt']:shutil.copy2(S/n,I/n)
im=Image.open(I/'painted-trousers-uv-v1.png').convert('RGB');a=np.asarray(im).astype(float);mask=Image.new('L',im.size);dr=ImageDraw.Draw(mask)
for f in json.load(gzip.open(T/'trousers-only-face-UV.json.gz','rt'))['faces']:dr.polygon([(round(u*(im.width-1)),round((1-v)*(im.height-1)))for u,v in f['uv']],fill=255)
m=np.asarray(mask)>0;interior=np.asarray(mask.filter(ImageFilter.MinFilter(7)))>0;bg=np.median(np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3)]),axis=0)
cream=(a[:,:,0]>185)&(a[:,:,1]>170)&(a[:,:,2]>140)&((a.max(axis=2)-a.min(axis=2))<75);green=(a[:,:,1]>a[:,:,0]*.93)&(a[:,:,1]>a[:,:,2]*1.25)&(a[:,:,0]<180);distance=np.linalg.norm(a-bg,axis=2)
report={'status':'palette-and-coverage-suitable-for-bounded-actual-render-not-final-art','textureSHA256':hashlib.sha256((I/'painted-trousers-uv-v1.png').read_bytes()).hexdigest(),'size':im.size,'nativeUVInteriorTexels':int(interior.sum()),'creamLikeInteriorFraction':float(cream[interior].mean()),'oliveLikeInteriorFraction':float(green[interior].mean()),'backgroundLikeInteriorDistance35Fraction':float((distance[interior]<35).mean()),'backgroundLikeWholeUVFraction':float((distance[m]<35).mean()),'definition':'actual nativeUV polygons; 3px erosion; same cream/olive tests as mixed validation; RGB35 background diagnostic. No pixel or UV edits.'}
assert report['creamLikeInteriorFraction']<.01 and report['oliveLikeInteriorFraction']<.01 and report['backgroundLikeInteriorDistance35Fraction']<.01
(O/'selected-texture-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
