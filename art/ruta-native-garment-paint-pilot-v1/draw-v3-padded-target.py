from pathlib import Path
from PIL import Image,ImageDraw
import json,gzip,math,hashlib
O=Path(__file__).resolve().parent/'v3-padded-trousers';N=2048;d=json.load(gzip.open(O/'actual-UV-faces.json.gz','rt'));meta=json.load(open(O/'padding-contract.json'));im=Image.new('RGB',(N,N),(231,223,208));paint=ImageDraw.Draw(im);wire=[];brown=(127,80,46)
for f in d['faces']:
 ps=[(round(u*2047),round((1-v)*2047))for u,v in f['uv']];paint.polygon(ps,fill=brown);paint.line(ps+[ps[0]],fill=brown,width=33,joint='curve')
 for x,y in ps:paint.ellipse((x-16,y-16,x+16,y+16),fill=brown)
 wire.append(ps)
im.save(O/'trousers-padded-flat-target.png');guide=im.copy();dr=ImageDraw.Draw(guide)
for ps in wire:dr.line(ps+[ps[0]],fill=(20,180,220),width=1)
guide.save(O/'trousers-actual-UV-wire-guide.png')
bs=[r['actualBoundsPx']for r in meta['selectedCharts']];dist=[]
for i,(a,b)in enumerate(bs):
 for c,e in bs[i+1:]:
  dx=max(0,a[0]-e[0],c[0]-b[0]);dy=max(0,a[1]-e[1],c[1]-b[1]);dist.append(math.hypot(dx,dy))
meta['conservativeMinimumActualChartGapPx']=min(dist);meta['conservativeMinimumAfterTwo16pxBleedsPx']=min(dist)-32;meta['minimumAtlasBorderPx']=min(min(a[0],a[1],2047-b[0],2047-b[1])for a,b in bs);meta['technicalBleedMethod']='native UV polygons filled brown plus radius16px segment/vertex exterior coverage; generated raster not edited';meta['targetSHA256']=hashlib.sha256((O/'trousers-padded-flat-target.png').read_bytes()).hexdigest();assert min(dist)>64;assert meta['minimumAtlasBorderPx']>32
(O/'padding-contract.json').write_text(json.dumps(meta,indent=2));print({k:v for k,v in meta.items()if k.startswith('conservative')or k.startswith('minimum')})
