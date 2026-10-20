from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,gzip
O=Path(__file__).resolve().parent;rows=[]
for key,path in [('mixed',O/'rejected-mixed-v1/painted-garment-uv-v1.png'),('trousers',O/'trousers-only/generated-v1/painted-trousers-uv-v1.png')]:
 a=np.asarray(Image.open(path).convert('RGB')).astype(float)/255;lin=np.where(a<=.04045,a/12.92,((a+.055)/1.055)**2.4);border=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3)]);measured=np.median(border,axis=0)*255;bg=np.array([234,227,211]if key=='mixed'else[232,225,210])/255;bg=np.where(bg<=.04045,bg/12.92,((bg+.055)/1.055)**2.4);dist=np.linalg.norm(lin-bg,axis=2)
 fs=json.load(gzip.open(O/'body-uv-faces.json.gz','rt'))['faces'];names=set(f['material']for f in fs)
 for name in sorted(names):
  if key=='trousers'and name!='Ruta warm loose cargo cloth':continue
  if key=='mixed'and name in ['Ruta warm loose cargo cloth','Ruta cream shirt','Ruta olive sleeveless vest','Gold','Ruta warm brass detail','Ruta burgundy neck bow']:continue
  mask=Image.new('L',(a.shape[1],a.shape[0]));d=ImageDraw.Draw(mask)
  for f in fs:
   if f['material']==name:d.polygon([(round(u*(a.shape[1]-1)),round((1-v)*(a.shape[0]-1)))for u,v in f['uv']],fill=255)
  m=np.asarray(mask)>0;interior=np.asarray(mask.filter(ImageFilter.MinFilter(7)))>0
  rows.append({'texture':key,'material':name,'measuredBorderMedianSRGBBytes':measured.tolist(),'guardNonzeroInteriorFraction':float((dist[interior]<.60).mean()),'guardNonzeroWholeUVFraction':float((dist[m]<.60).mean()),'interiorDistanceQuantiles':np.quantile(dist[interior],[0,.001,.01,.1,.5]).tolist(),'guardFullInteriorFraction':float((dist[interior]<.30).mean())})
(O/'v2-native-gutter-guard/collateral-check.json').write_text(json.dumps({'shaderDistanceSpace':'linearRGB','thresholds':[.30,.60],'rows':rows,'limitations':'Color proximity is a diagnostic, not semantic proof; strict brown-only assignment protects cream/brass. No PNG pixels modified.'},indent=2));print(json.dumps(rows,indent=2))
