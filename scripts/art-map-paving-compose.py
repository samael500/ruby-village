"""Retain actual painted flagstones and grass edges, protect accepted landmarks."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];A=R/'art/chapter-map-v2';D=R/'public/assets/chapter-map-v2';E=R/'docs/chapter-1-rc/art/map-paving';old=Image.open(A/'accepted-map-native1000.png').convert('RGB');paint=Image.open(A/'generated-paving-01.png').convert('RGB').resize((1000,400),Image.Resampling.LANCZOS);routes=json.loads((A/'routes.json').read_text())['routes'];corridor=Image.new('L',old.size);dr=ImageDraw.Draw(corridor)
for r in routes:dr.line([tuple(p)for p in r['samples']],fill=255,width=40,joint='curve')
# The source artist curved the crossing to the physical banks, endpoints unchanged.
dr.line([(932,292),(910,277),(886,274),(835,270),(786,273),(752,284),(710,302),(668,319),(626,324)],fill=255,width=37,joint='curve')
protect=Image.new('L',old.size);p=ImageDraw.Draw(protect)
for box in [(25,15,240,154),(260,12,475,112),(382,108,453,146),(565,38,651,142),(765,12,961,151),(310,190,449,315),(75,235,140,318)]:p.rectangle(box,fill=255)
p.polygon([(538,185),(642,185),(668,226),(657,290),(540,291)],fill=255);p.ellipse((610,247,680,319),fill=255);p.rectangle((660,236,703,254),fill=255)
color=Image.new('L',old.size);src=paint.load();dst=color.load()
for y in range(400):
 for x in range(1000):
  r,g,b=src[x,y]
  if r>115 and g>100 and b>65 and r>g*1.015 and b>g*.53:dst[x,y]=255
mask=ImageChops.multiply(color,corridor);mask=mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1));mask=ImageChops.multiply(mask,corridor);mask=ImageChops.multiply(mask,ImageChops.invert(protect));base=Image.composite(paint,old,mask);base.save(A/'map-base-before-mill-fix.png')
fix=Image.open(A/'generated-mill-link-02.png').convert('RGB').resize((1000,400),Image.Resampling.LANCZOS);fixCorridor=Image.new('L',old.size);ImageDraw.Draw(fixCorridor).line([(780,274),(750,283),(728,299),(696,308),(663,319),(626,324)],fill=255,width=32,joint='curve');fixColor=Image.new('L',old.size);fs=fix.load();fc=fixColor.load()
for y in range(250,345):
 for x in range(605,805):
  r,g,b=fs[x,y]
  if r>115 and g>100 and b>65 and r>g*1.015 and b>g*.53:fc[x,y]=255
fm=ImageChops.multiply(fixColor,fixCorridor).filter(ImageFilter.MaxFilter(7)).filter(ImageFilter.GaussianBlur(.7));fm=ImageChops.multiply(fm,fixCorridor);fm=ImageChops.multiply(fm,ImageChops.invert(protect));base=Image.composite(fix,base,fm);mask=ImageChops.lighter(mask,fm);corridor=ImageChops.lighter(corridor,fixCorridor);fm.save(A/'mill-fix-paint-mask.png')
base.save(A/'map-base-candidate.png');base.save(D/'map-base.webp','WEBP',lossless=True,method=6);mask.save(A/'painted-paving-and-grass-mask.png');corridor.save(A/'allowed-corridor-mask.png');protect.save(A/'protected-landmarks.png');assert ImageChops.multiply(ImageChops.difference(base,old).convert('L'),ImageChops.invert(corridor)).getbbox()is None;assert ImageChops.multiply(ImageChops.difference(base,old).convert('L'),protect).getbbox()is None
review=base.convert('RGBA');over=Image.new('RGBA',old.size);d=ImageDraw.Draw(over)
for r in routes:
 for label in ['start','end']:
  x,y=r[label];d.ellipse((x-2,y-2,x+2,y+2),fill=(240,20,210,220))
Image.alpha_composite(review,over).convert('RGB').resize((2000,800)).save(E/'registered-endpoints.jpg',quality=95)
meta={'version':2,'status':'painted-paving-candidate-requires-art-and-runtime-review','file':'map-base.webp','nativeSize':[1000,400],'viewBox':[0,0,1000,400],'projection':'entire-image maps to viewBox; contain, never cover crop','nodes':json.loads((R/'public/assets/chapter-map-v1/manifest.json').read_text())['nodes'],'routes':[{k:r[k]for k in ['id','path','start','end']}for r in routes],'source':'art/chapter-map-v2/generated-paving-01.png','millLinkSource':'art/chapter-map-v2/generated-mill-link-02.png','paintedMillCurve':'M932 292 C910 278 901 273 886 274 L835 270 C805 267 784 273 750 283 S720 302 696 308 S648 324 626 324','sourceSha256':hashlib.sha256((A/'generated-paving-01.png').read_bytes()).hexdigest(),'acceptedMapSha256':hashlib.sha256((A/'accepted-map-before.webp').read_bytes()).hexdigest(),'checks':{'outsideAllowedCorridorPixelsChanged':0,'protectedLandmarkPixelsChanged':0,'endpointsChanged':0,'nativeSize':[1000,400],'gameQa':'not-run','physicalPhone':'not-tested'},'requirements':['https://github.com/samael500/ruby-village/issues/48','https://github.com/samael500/ruby-village/issues/62#issuecomment-6233677763'],'layers':{'base':'map-base.webp','completedRoads':{},'buttons':'external accessible DOM; unchanged'},'wide':None};(D/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n');print('Actual painted paving composed; protected landmarks/corridor exterior unchanged')
