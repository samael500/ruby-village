from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
p=Path(__file__).parent;c=json.loads((p/'source-contract.json').read_text());im=Image.new('RGB',(768,780),'#e8deca');d=ImageDraw.Draw(im);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15);d.text((12,8),'Рута: шесть статических ракурсов, не проверка ходьбы',font=font,fill='#3b332a')
for i,key in enumerate(['e','se','sw','w','nw','ne']):
 row=c['cameraVariants']['base']['directions'][key]['clips']['walk']['frames'][0];file=p/row['file'];assert hashlib.sha256(file.read_bytes()).hexdigest()==row['sha256'];actor=Image.open(file).convert('RGBA').resize((256,320),Image.Resampling.LANCZOS);x=i%3*256;y=40+i//3*352;im.paste(actor,(x,y),actor);d.text((x+8,y+322),key.upper()+' · цельный кадр 00',font=font,fill='#3b332a')
d.text((12,756),'Одна камера и Root; без зеркалирования и покадрового fit. Внешность ещё не принята.',font=font,fill='#3b332a');im.save(p/'six-static-views.jpg',quality=94)
