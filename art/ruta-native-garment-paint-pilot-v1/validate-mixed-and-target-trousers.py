from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,gzip,hashlib,shutil,collections
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-stable-texture-generation-v1/garments');R=O/'rejected-mixed-v1';R.mkdir(exist_ok=True)
for n in ['painted-garment-uv-v1.png','generation-provenance.json','inputs.json','prompt-v1.txt']:shutil.copy2(S/n,R/n)
im=Image.open(R/'painted-garment-uv-v1.png').convert('RGB');a=np.asarray(im);N=im.width;d=json.load(gzip.open(O/'body-uv-faces.json.gz','rt'));groups=collections.defaultdict(list)
for f in d['faces']:groups[f['material']].append(f)
rows=[];overlay=im.copy();od=ImageDraw.Draw(overlay)
for mat,fs in groups.items():
 mask=Image.new('L',im.size);dr=ImageDraw.Draw(mask)
 for f in fs:dr.polygon([(round(u*(N-1)),round((1-v)*(N-1)))for u,v in f['uv']],fill=255)
 inside=np.asarray(mask.filter(ImageFilter.MinFilter(7)))>0
 cream=(a[:,:,0]>185)&(a[:,:,1]>170)&(a[:,:,2]>140)&((a.max(axis=2).astype(int)-a.min(axis=2).astype(int))<75)
 green=(a[:,:,1].astype(float)>a[:,:,0]*.93)&(a[:,:,1].astype(float)>a[:,:,2]*1.25)&(a[:,:,0]<180)
 rows.append({'oliveLikeInteriorFraction':float(green[inside].mean())if inside.any()else None,'backgroundLikeInteriorFraction':float((np.linalg.norm(a.astype(float)-np.array([230,225,211]),axis=2)[inside]<25).mean())if inside.any()else None,'material':mat,'erodedInteriorTexels':int(inside.sum()),'creamLikeInteriorFraction':float(cream[inside].mean())if inside.any()else None})
 if 'cargo' in mat.lower() or 'brown' in mat.lower():
  for f in fs:
   ps=[(round(u*(N-1)),round((1-v)*(N-1)))for u,v in f['uv']];od.line(ps+[ps[0]],fill=(0,255,255),width=1)
overlay.save(R/'actual-brown-UV-boundaries-QA.png');(R/'palette-validation.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256((R/'painted-garment-uv-v1.png').read_bytes()).hexdigest(),'definition':'Creamlike RGB r>185,g>170,b>140,spread<75; masks nativeUV polygons eroded3px. Color proxy not material semantics.','perMaterial':rows},indent=2))
# Minimal atlas preserves actual global UV coordinates, no rescaling/repacking.
fs=[f for f in d['faces']if f['object']=='Ruta stock long trousers'];T=O/'trousers-only';T.mkdir(exist_ok=True);flat=Image.new('RGB',(2048,2048),(231,223,208));draw=ImageDraw.Draw(flat)
for f in fs:draw.polygon([(round(u*2047),round((1-v)*2047))for u,v in f['uv']],fill=(127,80,46))
flat.save(T/'trousers-only-flat-target.png')
with gzip.open(T/'trousers-only-face-UV.json.gz','wt')as z:json.dump({'UVLayer':'RutaPaint','globalUVUnchanged':True,'faces':fs},z)
print(json.dumps(rows,indent=2))
