from pathlib import Path
from PIL import Image,ImageDraw
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-uv-paint/art/ruta-native-uv-paint-pilot-v1/renders');im=Image.new('RGB',(1536,1372),'#e9e2d4');d=ImageDraw.Draw(im)
for col,(old,new,label)in enumerate([('e-00.png','e-walk00.png','E / actual source Walk0'),('front-neutral.png','front-diagnostic.png','Front diagnostic'),('threequarter-neutral.png','threequarter-diagnostic.png','Three-quarter diagnostic')]):
 for row,(p,title)in enumerate([(S/old,'Previous native hair'),(O/new,'Daisy asset / fit NOT accepted')]):
  q=Image.open(p).convert('RGBA');assert q.size==(512,640);x=col*512;y=row*672;d.text((x+8,y+7),title+' | '+label,fill='#252525');im.paste(q,(x,y+32),q)
d.text((8,1350),'Daisy Hair by Elvaerwyn / MakeHuman Community hair02 / CC-BY. Hair rest-fit + fixed warm tint; original body/rig/gait unchanged.',fill='#252525');im.save(O/'source-daisy-threeview-comparison.jpg',quality=94)
