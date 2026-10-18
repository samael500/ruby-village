"""Build watermarked reviews exclusively from actual whole-pose E renders."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/transitions'
frames=[Image.open(OUT/'E'/f'{f:02}.png').convert('RGBA')for f in range(1,56)]
def tile(im,label,size=256):
 canvas=Image.new('RGB',(size,size+40),'#dedcd4');im=im.resize((size,size),Image.Resampling.LANCZOS);canvas.paste(im,(0,40),im);d=ImageDraw.Draw(canvas);d.text((6,4),'TECHNICAL / REJECTED APPEARANCE',fill='#292d2d');d.text((6,21),label,fill='#292d2d');return canvas
review=[]
for f,im in enumerate(frames):
 t=f*30;state='START'if t<360 else'WALK'if t<1080 else'STOP'if t<1440 else'SETTLE'
 review.append(tile(im,f'{state} / {t}ms / actual native 3D',384))
review[0].save(OUT/'E-actual-start-stop.gif',save_all=True,append_images=review[1:],duration=30,loop=0,optimize=False)
selected=[1,4,7,10,13,25,37,40,43,46,49,55];strip=Image.new('RGB',(6*256,2*296),'#dedcd4')
for i,f in enumerate(selected):strip.paste(tile(frames[f-1],f'E actual {30*(f-1)}ms'),((i%6)*256,(i//6)*296))
strip.save(OUT/'E-actual-start-stop-strip.jpg',quality=93)
files={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sorted((OUT/'E').glob('*.png'))};clip=[]
for f,im in enumerate(frames,1):
 box=im.getchannel('A').getbbox();clip.append({'frame':f,'alphaBounds':box,'insideCanvas':bool(box and box[0]>0 and box[1]>0 and box[2]<384 and box[3]<384)})
(OUT/'render-check.json').write_text(json.dumps({'actualRenderedFrames':len(files),'uniqueFrameHashes':len(set(files.values())),'poseIntervalsMs':30,'timelineDurationMs':1620,'gifDurationMs':1650,'gifLastToFirst':'Demonstration replay reset; deliberately not a seamless idle-to-idle spatial loop','watermark':'Technical mannequin, rejected appearance, not final art','bounds':clip,'sha256':files},indent=2)+'\n')
