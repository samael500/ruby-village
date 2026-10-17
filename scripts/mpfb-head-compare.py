from pathlib import Path
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[1];out=r/'docs/chapter-1-rc/mpfb';sheet=Image.new('RGB',(1920,1120),'#e8dfce');d=ImageDraw.Draw(sheet)
ref=Image.open(r/'public/assets/characters-v1/ruta-idle-pilot.png').convert('RGBA').crop((0,0,463,430));ref.thumbnail((460,470))
for row in range(2):
 sheet.paste(ref,(10,row*560+55),ref);d.text((10,row*560+15),'APPROVED 2D reference',fill='#34281d')
 for col,name in enumerate(['front','three-quarter','profile']):
  p=r/f'art/characters-mpfb-v1/head-study-{row+1}/{name}.png';im=Image.open(p).convert('RGBA');im.thumbnail((480,480));sheet.paste(im,((col+1)*480,row*560+50),im);d.text(((col+1)*480+10,row*560+15),f'Native head study{row+1} {name} - NOT accepted',fill='#34281d')
d.text((12,1100),'Actual orthographic Blender renders. Native mesh/eyes intact; likeness and hair still fail. No gait/export enabled.',fill='#832f1c');sheet.save(out/'head-studies-1-2-vs-approved.jpg',quality=96)
