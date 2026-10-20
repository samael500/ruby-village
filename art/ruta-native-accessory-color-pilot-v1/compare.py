from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).resolve().parent;R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1');rows=[]
for view,file in [('e','e-walk00.png'),('front','front-neutral.png')]:
 old=R/file;new=O/(view+'.png');a=np.array(Image.open(old).convert('RGBA'));b=np.array(Image.open(new).convert('RGBA'));mask=np.any(a[:,:,:3]!=b[:,:,:3],axis=2);ys,xs=np.where(mask);rows.append({'view':view,'beforeSha256':hashlib.sha256(old.read_bytes()).hexdigest(),'afterSha256':hashlib.sha256(new.read_bytes()).hexdigest(),'changedRGBPixels':int(mask.sum()),'changedAlphaPixels':int((a[:,:,3]!=b[:,:,3]).sum()),'changedBounds':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],'meanRGBChangedBefore':a[:,:,:3][mask].mean(axis=0).tolist(),'meanRGBChangedAfter':b[:,:,:3][mask].mean(axis=0).tolist()});im=Image.new('RGBA',(1024,640));im.paste(Image.fromarray(a),(0,0));im.paste(Image.fromarray(b),(512,0));im.convert('RGB').save(O/(view+'-before-after.jpg'),quality=94)
(O/'pixel-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
