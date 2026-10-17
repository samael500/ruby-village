"""Nonfinal flat-color whole-pose guides; never consumed as animation frames."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
p=Path(__file__).resolve().parents[1]/'art/characters-walk-v1/calm-east-v5';out=p/'inbetweens-v6';out.mkdir(exist_ok=True)
source=Image.open(p/'phase-2-guide-only-painted.png').convert('RGBA');swing=Image.open(p/'between-3-fixed.png').convert('RGBA')
for number,near_dx,far_dx in [(1,-36,60),(2,-73,120)]:
 im=source.copy();alpha=im.getchannel('A');m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([(650,1035),(805,1035),(850,1105),(945,1130),(945,1235),(635,1235)],fill=255);near=im.copy();near.putalpha(ImageChops.multiply(m,alpha))
 m2=Image.new('L',im.size);ImageDraw.Draw(m2).polygon([(855,1005),(965,975),(1030,1015),(1170,1040),(1170,1190),(900,1190),(850,1080)],fill=255);far=swing.copy();far.putalpha(ImageChops.multiply(m2,swing.getchannel('A')))
 clear=Image.new('L',im.size);ImageDraw.Draw(clear).rectangle((480,890,1180,1240),fill=255);im.putalpha(ImageChops.multiply(alpha,ImageChops.invert(clear)))
 d=ImageDraw.Draw(im);d.polygon([(670,850),(788,853),(790+near_dx,1040),(657+near_dx,1040),(630+near_dx,982)],fill='#80573e');d.polygon([(727,820),(800,830),(700+far_dx,1010),(619+far_dx,1010),(650+far_dx,930)],fill='#795039');im.alpha_composite(far,(-150 if number==1 else -75,15 if number==1 else 7));im.alpha_composite(near,(near_dx,0));clean=Image.new('RGBA',im.size);clean.alpha_composite(im);clean.save(out/f'near23-{number}-guide.png')
