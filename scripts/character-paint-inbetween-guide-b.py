from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
p=Path(__file__).resolve().parents[1]/'art/characters-walk-v1/calm-east-v5';o=p/'inbetweens-v6';src=Image.open(p/'between-3-fixed.png').convert('RGBA')
for n,dx,fx in [(1,73,-150),(2,36,-75)]:
 im=src.copy();m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([(545,1010),(675,1010),(710,1080),(810,1120),(815,1220),(510,1220)],fill=255);near=src.copy();near.putalpha(ImageChops.multiply(m,src.getchannel('A')))
 f=Image.new('L',im.size);ImageDraw.Draw(f).polygon([(855,1005),(965,975),(1030,1015),(1170,1040),(1170,1190),(900,1190),(850,1080)],fill=255);far=src.copy();far.putalpha(ImageChops.multiply(f,src.getchannel('A')))
 c=Image.new('L',im.size);ImageDraw.Draw(c).rectangle((480,900,1200,1240),fill=255);im.putalpha(ImageChops.multiply(src.getchannel('A'),ImageChops.invert(c)));d=ImageDraw.Draw(im);d.polygon([(575,865),(710,865),(700+dx,1030),(555+dx,1030)],fill='#80573e');d.polygon([(750,820),(850,820),(965+fx,1010),(855+fx,1040)],fill='#795039');im.alpha_composite(far,(fx,15 if n==1 else 7));im.alpha_composite(near,(dx,15));clean=Image.new('RGBA',im.size);clean.alpha_composite(im);clean.save(o/f'near23-{n}-guide-b.png')
