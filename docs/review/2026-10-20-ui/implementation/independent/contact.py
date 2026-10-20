from PIL import Image,ImageDraw
from pathlib import Path
p=Path('/tmp/ui79-independent'); names=['gate','garden','well','bakery','stream','mill','post','forest']; sheet=Image.new('RGB',(800,220),'white');d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=Image.open(p/f'844-{n}.png'); crop=im.crop((10,58,62,103)).resize((104,90));x=(i%4)*200;y=(i//4)*110;sheet.paste(crop,(x,y));d.text((x+108,y+30),n,fill='black')
sheet.save(p/'miniatures-contact.jpg')
