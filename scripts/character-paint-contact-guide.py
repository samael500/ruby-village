"""NONFINAL pose guides only: move a full painted boot, then require whole-pose art cleanup."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
root=Path(__file__).resolve().parents[1];p=root/'art/characters-walk-v1/calm-east-v5'
for phase,polygon,delta in [(5,[(810,1020),(950,1015),(1100,1110),(1100,1225),(800,1225),(800,1120)],(-100,0)),(7,[(480,1010),(660,1005),(720,1080),(770,1160),(770,1220),(475,1220)],(110,0))]:
 im=Image.open(p/f'between-{phase}-fixed.png').convert('RGBA');mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(polygon,fill=255);mask=ImageChops.multiply(mask,im.getchannel('A'));part=im.copy();part.putalpha(mask);original_alpha=im.getchannel('A');im.putalpha(ImageChops.subtract(original_alpha,mask));im.alpha_composite(part,delta);clean=Image.new('RGBA',im.size);clean.alpha_composite(im);im=clean;im.save(p/f'contact-position-guide-{phase}.png');mask.save(p/f'contact-position-guide-{phase}-mask.png')
