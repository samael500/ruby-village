"""Actual rendered PNG comparison; scales review panels equally by visible height, never model assets."""
from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];out=r/'docs/chapter-1-rc/mpfb';canvas=Image.new('RGB',(1800,1080),'#e8dfce');d=ImageDraw.Draw(canvas)
items=[('APPROVED 2D reference',r/'public/assets/characters-v1/ruta-idle-pilot.png')]+[(f'MPFB v{i} REJECT / not final',r/f'art/characters-mpfb-v1/appearance-v{i}/ruta-e-pilot.png')for i in range(1,5)]
for j,(label,p)in enumerate(items):
 im=Image.open(p).convert('RGBA');b=im.getchannel('A').getbbox();im=im.crop(b);im.thumbnail((345,940));x=j*360+(360-im.width)//2;canvas.paste(im,(x,75),im);d.text((j*360+8,20),label,fill='#38281d')
d.text((12,1035),'Actual Blender renders. All four studies fail approved Ruta likeness; none is production or gait evidence.',fill='#822b1c');canvas.save(out/'appearance-v1-v4-vs-approved.jpg',quality=96)
