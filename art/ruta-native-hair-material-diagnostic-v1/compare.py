from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).resolve().parent;R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1');rows=[]
for view,filename in [('e','e-walk00.png'),('front','front-neutral.png')]:
 paths=[R/filename,O/('normal-zero-'+view+'.png'),O/('uniform-copper-normal-zero-'+view+'.png')];ims=[Image.open(p).convert('RGBA')for p in paths];a=np.array(ims[0]);sheet=Image.new('RGBA',(1536,640))
 for i,(p,im)in enumerate(zip(paths,ims)):
  b=np.array(im);sheet.paste(im,(i*512,0));rows.append({'view':view,'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'changedRGBPixelsVsBaseline':int(np.any(a[:,:,:3]!=b[:,:,:3],axis=2).sum()),'changedAlphaPixelsVsBaseline':int((a[:,:,3]!=b[:,:,3]).sum())})
 sheet.convert('RGB').save(O/(view+'-baseline-normal0-uniform.jpg'),quality=94)
(O/'pixel-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
