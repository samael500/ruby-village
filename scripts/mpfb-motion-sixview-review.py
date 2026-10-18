"""Watermark and inspect 24 actual pose renders without synthesizing images."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/sixview-proof';manifest=json.loads((OUT/'manifest.json').read_text());sheet=Image.new('RGB',(6*256,4*304+46),'#dedcd4');draw=ImageDraw.Draw(sheet);draw.text((8,8),'TECHNICAL CAMERA PROOF / REJECTED GENERIC APPEARANCE / NOT FINAL GAME ART',fill='#292d2d');draw.text((8,26),'Same scale in all views. Pink + = ground root; green/orange = actual sole toe/heel centres L/R.',fill='#292d2d');records=[];row=0
for group,spec in manifest['cameraVariants'].items():
 for frame in [1,13]:
  for column,(direction,data)in enumerate(spec['directions'].items()):
   p=OUT/group/direction/f'{frame:02}.png';im=Image.open(p).convert('RGBA');alpha=im.getchannel('A');box=alpha.getbbox();foreground={i for i,value in enumerate(alpha.tobytes())if value>16};components=[]
   while foreground:
    seed=foreground.pop();stack=[seed];count=0;xs=[];ys=[]
    while stack:
     point=stack.pop();count+=1;x,y=point%384,point//384;xs.append(x);ys.append(y)
     for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
      nx,ny=x+dx,y+dy;neighbor=ny*384+nx
      if 0<=nx<384 and 0<=ny<384 and neighbor in foreground:foreground.remove(neighbor);stack.append(neighbor)
    if count>=4:components.append({'pixels':count,'bounds':[min(xs),min(ys),max(xs)+1,max(ys)+1]})
   components.sort(key=lambda c:-c['pixels']);record=next(r for r in data['frames']if r['frame']==frame);tile=Image.new('RGB',(256,304),'#dedcd4');small=im.resize((256,256),Image.Resampling.LANCZOS);tile.paste(small,(0,48),small);d=ImageDraw.Draw(tile);d.text((6,4),f'TECHNICAL / {spec["label"]} / {direction.upper()}',fill='#292d2d');d.text((6,19),f'phase {(frame-1)/24:g} / fixed ortho 1.70m',fill='#292d2d');d.text((6,34),'REJECTED APPEARANCE',fill='#713b32')
   def cross(point,color,r=3):
    x,y=point[0]*2/3,48+point[1]*2/3;d.line((x-r,y,x+r,y),fill=color,width=1);d.line((x,y-r,x,y+r),fill=color,width=1)
   cross(record['rootGroundAnchorPixels'],'#cc1698',5)
   for side,color in [('L','#07854d'),('R','#c36c00')]:
    for marker in record['actualSourceSoleMarkers'][side].values():cross(marker['projectedPixels'],color,2)
   sheet.paste(tile,(column*256,row*304+46));records.append({'path':str(p.relative_to(OUT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'alphaBounds':box,'fullBodyBagContained':bool(box and min(box[:2])>1 and max(box[2:])<383),'alphaComponentsAtThreshold16Min4Pixels':components,'actualAlphaHeightPx':box[3]-box[1],'displayAlphaHeightAtFixedCalibrationPx':(box[3]-box[1])*136/251,'rootGroundAnchorPixels':record['rootGroundAnchorPixels']})
  row+=1
sheet.save(OUT/'actual-two-calibration-proof-strip.jpg',quality=94)
anchors=[r['rootGroundAnchorPixels']for r in records];pairs={}
for r in records:pairs.setdefault('/'.join(r['path'].split('/')[:2]),[]).append(r)
max_top_shift=max(max(r['alphaBounds'][1]for r in pair)-min(r['alphaBounds'][1]for r in pair)for pair in pairs.values())
check={'status':'AUTHOR GEOMETRIC/FRAME CHECK; independent visual review pending','actualFrameCount':len(records),'uniqueFrameCount':len({r['sha256']for r in records}),'allContained':all(r['fullBodyBagContained']for r in records),'maxRootAnchorDistancePixels':max(math.dist(a,b)for a in anchors for b in anchors),'nativeHeightReferencePx':251,'maxWithinViewTwoPoseTopEdgeShiftPixels':max_top_shift,'heightInterpretation':'Angle-dependent silhouettes may vary naturally; no per-frame/per-direction rescaling. Fixed 136/251 display conversion.','records':records};assert check['actualFrameCount']==24;assert check['allContained'];assert check['uniqueFrameCount']==24;assert check['maxRootAnchorDistancePixels']<.001;(OUT/'render-check.json').write_text(json.dumps(check,indent=2)+'\n');print(json.dumps({k:v for k,v in check.items()if k!='records'},indent=2))
