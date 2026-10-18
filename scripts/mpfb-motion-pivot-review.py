"""Watermarked review of exactly12 genuine turn poses; replay is NOT a loop."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,os
ROOT=Path(__file__).resolve().parents[1];VARIANT='pivot60L';OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-study';meta=json.loads((OUT/'raster-path-metadata.json').read_text());records=meta['renderedFrames'];images=[];checks=[]
def tile(im,rec,size):
 c=Image.new('RGB',(size,size+48),'#dedcd4');d=ImageDraw.Draw(c);d.text((6,4),'TECHNICAL / REJECTED APPEARANCE',fill='#713b32');d.text((6,19),f'{VARIANT.upper()} / {rec["timeMs"]}ms / yaw {math.degrees(rec["headingRadians"]):.1f}',fill='#292d2d');d.text((6,34),'DEMO REPLAY RESET / NOT A CYCLE',fill='#713b32');small=im.resize((size,size),Image.Resampling.LANCZOS);c.paste(small,(0,48),small)
 def cross(point,color,r=3):
  x,y=point[0]*size/384,48+point[1]*size/384;d.line((x-r,y,x+r,y),fill=color);d.line((x,y-r,x,y+r),fill=color)
 cross(rec['rootGroundAnchorPixels'],'#cc1698',4)
 for side,color in [('L','#07854d'),('R','#c36c00')]:
  for marker in rec['actualSourceSoleMarkers'][side].values():cross(marker['projectedPixels'],color,2)
 return c
sheet=Image.new('RGB',(6*256,2*304),'#dedcd4')
for i,rec in enumerate(records):
 p=OUT/'E'/f'{rec["frame"]:02}.png';assert hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256'];im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox();assert box and min(box[:2])>1 and max(box[2:])<383;sheet.paste(tile(im,rec,256),((i%6)*256,(i//6)*304));images.append(tile(im,rec,384));checks.append({'frame':rec['frame'],'alphaBounds':box,'sha256':rec['sha256']})
assert len(checks)==12 and len({r['sha256']for r in checks})==12;durations=[b['timeMs']-a['timeMs']for a,b in zip(records,records[1:])]+[120];images[0].save(OUT/'actual-turn-demo.gif',save_all=True,append_images=images[1:],duration=durations,loop=0,optimize=False);sheet.save(OUT/'actual-turn-strip.jpg',quality=94)
result={'status':'AUTHOR FRAME CHECK; TURN NATURALNESS/INDEPENDENT REVIEW PENDING','actualRenderedPoseCount':12,'allContained':True,'uniqueFrameCount':12,'nativeClipDurationMs':meta['durationMs'],'reviewGifDurationMs':sum(durations),'gifReplayReset':True,'loopClaim':'No cyclic raster claim. Composition terminal rig closure is separately measured; no complete closed-turn raster loop rendered.','cameraScale':'fixed384 / ortho1.70 / same251→136 calibration; no frame fit','records':checks};(OUT/'render-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='records'},indent=2))
