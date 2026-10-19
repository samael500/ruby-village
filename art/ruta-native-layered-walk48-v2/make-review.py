"""Ordinary assembly of actual packed full frames; no per-frame fitting/warping."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;m=json.loads((P/'manifest.json').read_text());spec=m['cameraVariants']['base']['directions']['e'];clip=spec['clips']['walk'];atlas=Image.open(P/clip['atlas']).convert('RGBA');frames=[]
for row in clip['frames']:
 x,y,w,h=row['rect'];frames.append(atlas.crop((x,y,x+w,y+h)))
assert len(frames)==48
sheet=Image.new('RGB',(8*144,6*192),(244,240,226));draw=ImageDraw.Draw(sheet)
for i,im in enumerate(frames):
 thumb=im.resize((128,160),Image.Resampling.LANCZOS);x=(i%8)*144+8;y=(i//8)*192+4;sheet.paste(thumb,(x,y),thumb);draw.text((x,y+164),f'{i:02}  f{clip["frames"][i]["sourceFrame"]:.3f}',fill=(40,30,20))
sheet.save(P/'contact-sheet-48.png')
# Millisecond raster-animation timing approximates exact source duration by cumulative rounding.
total=round(clip['durationSeconds']*1000);times=[round(i*total/48)for i in range(49)];durations=[times[i+1]-times[i]for i in range(48)];assert sum(durations)==total
frames[0].save(P/'actual-e-walk48-loop.webp',format='WEBP',save_all=True,append_images=frames[1:],duration=durations,loop=0,lossless=True,quality=100,method=6,exact=True)
with Image.open(P/'actual-e-walk48-loop.webp')as reread:assert reread.size==(256,320) and reread.n_frames==48
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();(P/'review-artifacts.json').write_text(json.dumps({'status':'ACTUAL-48-SOURCE-POSE-REVIEW-NOT-ART-OR-GAME-ACCEPTANCE','sourceSha256':m['sourceSha256'],'manifestSha256':sha(P/'manifest.json'),'contactSheet':'ordinary8x6 assembly; each complete deliverycanvas uniformly resized .5 only for sheet thumbnails; labels added outsideframe','loop':{'frameCount':48,'size':[256,320],'sourceDurationSeconds':clip['durationSeconds'],'webpDurationMs':total,'frameDurationsMs':durations,'wholeCanvas':True,'noPerFrameFit':True},'files':{p.name:{'sha256':sha(p),'bytes':p.stat().st_size}for p in [P/'contact-sheet-48.png',P/'actual-e-walk48-loop.webp']},'limitations':['Only base/E/Walk48; no six-direction or other-camera actual render.','No spatial travel, turn, contact/no-slip, runtime/gameplay or art-approval claim.','Independent browser/loop review remains separate.']},indent=2)+'\n')
