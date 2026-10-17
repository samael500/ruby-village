"""Nonfinal complete-body guide; existing actual boots, later whole-pose imagegen repaint."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
p=Path(__file__).resolve().parents[1]/'art/characters-walk-v1/calm-east-v5';o=p/'inbetweens-v6';base=Image.open(p/'phase-7-guide-only-painted.png').convert('RGBA');ref=Image.open(p/'phase-6-guide-only-painted.png').convert('RGBA')
for n,dx,fx in [(1,50,65),(2,25,130)]:
 im=base.copy();m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([(645,1010),(745,1000),(795,1070),(880,1140),(900,1220),(600,1220),(600,1100)],fill=255);support=base.copy();support.putalpha(ImageChops.multiply(m,base.getchannel('A')))
 sm=Image.new('L',im.size);ImageDraw.Draw(sm).polygon([(677,995),(785,995),(805,1060),(890,1080),(901,1165),(680,1175),(640,1120),(640,1040)],fill=255);swing=ref.copy();swing.putalpha(ImageChops.multiply(sm,ref.getchannel('A')))
 c=Image.new('L',im.size);ImageDraw.Draw(c).rectangle((500,900,1190,1240),fill=255);im.putalpha(ImageChops.multiply(base.getchannel('A'),ImageChops.invert(c)));d=ImageDraw.Draw(im);d.polygon([(595,870),(735,870),(745+dx,1030),(645+dx,1030)],fill='#795039');d.polygon([(750,850),(875,850),(785+fx,1030),(677+fx,1030)],fill='#80573e');im.alpha_composite(support,(dx,0));im.alpha_composite(swing,(fx,10 if n==1 else 20));clean=Image.new('RGBA',im.size);clean.alpha_composite(im);clean.save(o/f'far67-{n}-guide.png')
