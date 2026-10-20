from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).resolve().parent;R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1');rows=[]
for view,file in [('e','e-walk00.png'),('front','front-neutral.png'),('threequarter','threequarter-neutral.png')]:
 a=np.array(Image.open(R/file).convert('RGBA'));b=np.array(Image.open(O/(view+'.png')).convert('RGBA'));old=a[:,:,3]>128;new=b[:,:,3]>128;added=new&~old;removed=old&~new;out=b.copy();out[added]=[255,50,50,255];out[removed]=[20,220,255,255];sheet=Image.new('RGBA',(1536,640))
 for i,x in enumerate([a,b,out]):sheet.paste(Image.fromarray(x),(512*i,0))
 sheet.convert('RGB').save(O/(view+'-before-after-contour.jpg'),quality=94);rows.append({'view':view,'beforeAlpha128BBox':Image.fromarray(old.astype('uint8')*255).getbbox(),'afterAlpha128BBox':Image.fromarray(new.astype('uint8')*255).getbbox(),'newOpaquePixelsOutsideOld':int(added.sum()),'oldOpaquePixelsRemoved':int(removed.sum()),'definition':'actual staticfixedcamera fullactor alpha128; addedred/removedcyan. Internalholesandsurfaceocclusionincluded, notpureexternalHausdorff','beforeSha256':hashlib.sha256((R/file).read_bytes()).hexdigest(),'afterSha256':hashlib.sha256((O/(view+'.png')).read_bytes()).hexdigest()})
(O/'actual-silhouette-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
