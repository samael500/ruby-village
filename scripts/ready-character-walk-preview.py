"""Pack whole Blender renders, preserve their pixels, and audit full alpha."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,statistics,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art'/os.environ.get('READY_PREVIEW_FOLDER','ready-character-walk-v1');frames=[Image.open(OUT/'e'/f'{i:02}.png').convert('RGBA')for i in range(24)]
rows=[]
for i,im in enumerate(frames):
 b=im.getchannel('A').getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<512 and b[3]<640,(i,b)
 rows.append({'index':i,'alphaBounds':list(b),'pngSha256':hashlib.sha256((OUT/'e'/f'{i:02}.png').read_bytes()).hexdigest()})
assert len({r['pngSha256']for r in rows})==24
bg=(236,232,219,255);composites=[]
for i,im in enumerate(frames):
 canvas=Image.new('RGBA',im.size,bg);canvas.alpha_composite(im);d=ImageDraw.Draw(canvas);d.text((12,12),f'E / {i:02} / source {40*i/24:.2f}',fill=(38,42,35));composites.append(canvas.convert('RGB'))
composites[0].save(OUT/'walk-e-large.webp',save_all=True,append_images=composites[1:],duration=round(1000*40/24/24),loop=0,lossless=True)
composites[0].save(OUT/'walk-e-large.gif',save_all=True,append_images=composites[1:],duration=70,loop=0)
grid=Image.new('RGB',(6*256,4*320),(245,242,232))
for i,im in enumerate(composites):grid.paste(im.resize((256,320),Image.Resampling.LANCZOS),((i%6)*256,(i//6)*320))
grid.save(OUT/'walk-e-all24.png')
key=Image.new('RGB',(4*512,2*640),(245,242,232))
for n,i in enumerate([0,3,6,9,12,15,18,21]):key.paste(composites[i],((n%4)*512,(n//4)*640))
key.save(OUT/'walk-e-keyposes-large.png')
# Sprite packing keeps all source pixels and uses the same fixed camera anchor.
atlas=Image.new('RGBA',(6*512,4*640))
for i,im in enumerate(frames):atlas.alpha_composite(im,((i%6)*512,(i//6)*640))
atlas.save(OUT/'walk-e-atlas.png')
(OUT/'render-checks.json').write_text(json.dumps({'status':'24-real-render-pixels-checked-no-runtime-approval','frames':rows,'uniqueFrames':24,'allAnyAlphaWithinCanvas':True,'smallestAnyAlphaMarginPixels':min(min(r['alphaBounds'][0],r['alphaBounds'][1],512-r['alphaBounds'][2],640-r['alphaBounds'][3])for r in rows),'packing':'whole RGBA frames, no per-frame crop/translation/scale','fixedAnchor':json.loads((OUT/'contract.json').read_text())['footAnchor'],'preview':'solid neutral background added only to preview GIF/WebP; PNG/atlas retain original alpha'},indent=2)+'\n')
