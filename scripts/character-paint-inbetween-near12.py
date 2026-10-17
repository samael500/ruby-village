"""NONFINAL positional guides only; imagegen must repaint continuous complete figures."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
p=Path(__file__).resolve().parents[1]/'art/characters-walk-v1/calm-east-v5';o=p/'inbetweens-v6';src=Image.open(p/'phase-2-guide-only-painted.png').convert('RGBA')
for n,dx in [(1,60),(2,30)]:
 im=src.copy();m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([(675,1030),(800,1030),(850,1100),(950,1135),(950,1235),(640,1235),(640,1120)],fill=255);boot=src.copy();boot.putalpha(ImageChops.multiply(m,src.getchannel('A')));im.putalpha(ImageChops.multiply(src.getchannel('A'),ImageChops.invert(m)));ImageDraw.Draw(im).polygon([(680,975),(800,975),(800+dx,1040),(675+dx,1040)],fill='#80573e');im.alpha_composite(boot,(dx,-7 if n==1 else -3));clean=Image.new('RGBA',im.size);clean.alpha_composite(im);clean.save(o/f'near12-{n}-guide.png')
