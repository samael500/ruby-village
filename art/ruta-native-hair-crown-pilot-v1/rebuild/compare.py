from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
O=Path(__file__).resolve().parent;R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1');rows=[]
for view,file in [('e','e-walk00.png'),('front','front-neutral.png')]:
 a=Image.open(R/file).convert('RGBA');b=Image.open(O/(view+'.png')).convert('RGBA');ar=np.array(a);br=np.array(b);get=lambda x:Image.fromarray(x[:,:,3]).getbbox();rows.append({'view':view,'beforeAlphaBBoxAny':get(ar),'afterAlphaBBoxAny':get(br),'beforeAlphaBBox128':Image.fromarray((ar[:,:,3]>128).astype('uint8')*255).getbbox(),'afterAlphaBBox128':Image.fromarray((br[:,:,3]>128).astype('uint8')*255).getbbox(),'changedAlphaPixels':int((ar[:,:,3]!=br[:,:,3]).sum()),'sourceRenderSha256':hashlib.sha256((R/file).read_bytes()).hexdigest(),'actualRenderSha256':hashlib.sha256((O/(view+'.png')).read_bytes()).hexdigest()});im=Image.new('RGBA',(1024,640));im.paste(a,(0,0));im.paste(b,(512,0));im.convert('RGB').save(O/(view+'-before-after.jpg'),quality=94)
(O/'silhouette-comparison.json').write_text(json.dumps(rows,indent=2)+'\n')
