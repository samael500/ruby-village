from PIL import Image,ImageDraw,ImageChops
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[4];D=R/'art/characters-mpfb-v1/motion/full-cycle-technical';O=Path(__file__).resolve().parent;records=[];views=[]
for group in ['base','calibrated-1']:
 for direction in ['e','se','sw','w','nw','ne']:
  receipt=json.loads((D/group/direction/'receipt.json').read_text());frames=[];sheet=Image.new('RGB',(6*192,4*218),'#dedcd4');draw=ImageDraw.Draw(sheet)
  for i,rec in enumerate(receipt['frames']):
   p=D/group/direction/f'{rec["frame"]:02}.png';im=Image.open(p).convert('RGBA');alpha=im.getchannel('A');box=alpha.getbbox();assert im.size==(384,384)and min(box[:2])>1 and max(box[2:])<383;digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest==rec['sha256'];im2=im.resize((192,192));x=i%6*192;y=i//6*218;sheet.paste(im2,(x,y+26),im2);draw.text((x+4,y+3),f'{group}/{direction} frame{rec["frame"]:02}',fill='#302c28');frames.append(im)
   binary=alpha.point(lambda x:255 if x>16 else 0);components=[]
   while binary.getbbox():
    bx=binary.getbbox();seed=next((x,bx[1])for x in range(bx[0],bx[2])if binary.getpixel((x,bx[1])));original=binary.copy();ImageDraw.floodfill(binary,seed,0);diff=ImageChops.difference(original,binary);n=diff.histogram()[255]
    if n>=4:components.append(n)
   records.append(dict(group=group,direction=direction,frame=rec['frame'],sha256=digest,bounds=box,components4connectedMin4=sorted(components,reverse=True)))
  assert len({r['sha256']for r in records if r['group']==group and r['direction']==direction})==24
  sheet.save(O/f'{group}-{direction}-all24.jpg',quality=92)
  # Consecutive+seam raster deltas are evidence, not a motion-quality threshold.
  differences=[]
  for a,b in zip(frames,frames[1:]+frames[:1]):
   ds=ImageChops.difference(a,b);differences.append(sum(sum(t)for t in ds.getdata())/(384*384*4))
  views.append(dict(group=group,direction=direction,adjacentMeanAbsoluteDifferences=differences,seamDifference=differences[-1],largestInteriorDifference=max(differences[:-1])))
assert len(records)==288 and len({r['sha256']for r in records})==288
(O/'png-check.json').write_text(json.dumps(dict(frameCount=288,records=records,views=views),indent=2)+'\n');print('PASS288 allcontained/hashcorrect/distinct',sum(len(r['components4connectedMin4'])>1 for r in records),'withsecondary4component')
