"""Assemble only actual whole-frame renders; never synthesize intermediate poses."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pilot'
frames=[Image.open(OUT/'E'/f'{i:02}.png').convert('RGBA')for i in range(1,25)]
def tile(im,label,size=256):
 canvas=Image.new('RGB',(size,size+27),'#dedcd4');im=im.resize((size,size),Image.Resampling.LANCZOS);canvas.paste(im,(0,27),im);ImageDraw.Draw(canvas).text((8,8),label,fill='#292d2d');return canvas
loop=[tile(im,f'TECHNICAL MANNEQUIN / {i+1:02} / 720ms cycle',384)for i,im in enumerate(frames)]
loop[0].save(OUT/'E-actual-cycle.gif',save_all=True,append_images=loop[1:],duration=30,loop=0,optimize=False)
phases=[1,5,9,13,17,21];sheet=Image.new('RGB',(6*256,3*283+40),'#dedcd4');ImageDraw.Draw(sheet).text((8,12),'MPFB NATIVE IK MOTION STUDY / rejected appearance / NOT FINAL RUTA',fill='#292d2d')
for row,view in enumerate(['E','front','three-quarter']):
 for col,f in enumerate(phases):
  im=Image.open(OUT/view/f'{f:02}.png').convert('RGBA');sheet.paste(tile(im,f'{view} / frame {f:02}'),(col*256,row*283+40))
sheet.save(OUT/'actual-three-view-strip.jpg',quality=90)
ground=Image.new('RGB',(6*256,283),'#dedcd4')
for col,f in enumerate(phases):
 im=Image.open(OUT/'fixed-world'/f'{f:02}.png').convert('RGBA');ground.paste(tile(im,f'Fixed WORLD / frame {f:02}'),(col*256,0))
ground.save(OUT/'actual-fixed-world-strip.jpg',quality=90)
close=Image.new('RGB',(1200,1294),'#dedcd4');ImageDraw.Draw(close).text((8,10),'ACTUAL ONE-STRAP CARRY / generic appearance rejected / geometry review',fill='#292d2d')
for row,f in enumerate([1,13]):
 for col,view in enumerate(['front','three-quarter']):
  im=Image.open(OUT/'grip-close'/f'{view}-{f:02}.png').convert('RGBA');close.paste(tile(im,f'{view} actual grip / frame {f:02}',600),(col*600,40+row*627))
close.save(OUT/'actual-grip-close-strip.jpg',quality=92)
files={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted(OUT.glob('*/*.png'))}
assert len(set(files.values()))==len(files),'Unexpected duplicate whole-frame render'
(OUT/'render-check.json').write_text(json.dumps({'actualFrameCount':len(files),'uniqueFrameCount':len(set(files.values())),'cycleGifDurationMs':720,'frameDurationMs':30,'renderSha256':files},indent=2)+'\n')
