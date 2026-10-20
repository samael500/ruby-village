from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
O=Path(__file__).resolve().parent;S=O.parent/'daisy-scalp-anchored-refinement';im=Image.new('RGB',(1536,1372),'#e9e2d4');draw=ImageDraw.Draw(im);rows=[]
for col,name in enumerate(['e-walk00','front-diagnostic','threequarter-diagnostic']):
 for row,(folder,title)in enumerate([(S,'Original native RGB'),(O,'Fixed painted RGB / ORIGINAL alpha')]):
  q=Image.open(folder/(name+'.png')).convert('RGBA');assert q.size==(512,640);x=col*512;y=row*672;draw.text((x+7,y+7),title+' | '+name,fill='#252525');im.paste(q,(x,y+32),q)
 a=np.asarray(Image.open(S/(name+'.png')).convert('RGBA'))[:,:,3];b=np.asarray(Image.open(O/(name+'.png')).convert('RGBA'))[:,:,3];diff=abs(a.astype(int)-b.astype(int));rows.append({'view':name,'comparedPixels':int(a.size),'actualRenderedAlphaIdentical':bool(np.array_equal(a,b)),'changedAlphaPixels':int((diff!=0).sum()),'maxAlphaDelta8bit':int(diff.max())})
draw.text((8,1350),'Daisy Hair by Elvaerwyn / MakeHuman Community hair02 / CC-BY. One fixed RGB repaint, native UV and original alpha retained. Art review pending.',fill='#252525');im.save(O/'original-painted-threeview-comparison.jpg',quality=94);(O/'actual-alpha-comparison.json').write_text(json.dumps({'scope':'actualbeforeafterrenderedalpha, samegeometrycamera128AA; no newalpha generated','rows':rows},indent=2)+'\n');rgb=Image.open(O/'inputs/painted-daisy-rgb-v1.png');(O/'rgb-input-inspection.json').write_text(json.dumps({'mode':rgb.mode,'size':rgb.size,'channelExtrema':rgb.getextrema(),'sha256':hashlib.sha256((O/'inputs/painted-daisy-rgb-v1.png').read_bytes()).hexdigest(),'modified':False},indent=2)+'\n')
