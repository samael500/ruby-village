from pathlib import Path
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;D=O.parent/'daisy-native-pilot';im=Image.new('RGB',(1536,1372),'#e9e2d4');d=ImageDraw.Draw(im)
for col,name in enumerate(['e-walk00','front-diagnostic','threequarter-diagnostic']):
 for row,(folder,label)in enumerate([(D,'Original fixed Daisy fit'),(O,'Scalp-protected lower-length refinement')]):
  q=Image.open(folder/(name+'.png')).convert('RGBA');assert q.size==(512,640);x=col*512;y=row*672;d.text((x+7,y+7),label+' | '+name,fill='#252525');im.paste(q,(x,y+32),q)
d.text((8,1350),'Daisy Hair by Elvaerwyn / MakeHuman Community hair02 / CC-BY. Lower rest-length geometry + separate normal .9 -> .25 study. NOT accepted likeness.',fill='#252525');im.save(O/'original-refined-threeview-comparison.jpg',quality=94)
