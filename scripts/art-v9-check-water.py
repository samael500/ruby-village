from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import json,hashlib
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/layers/water';report={}
for sid in ['stream','mill']:
 d=json.load(open(r/f'art/chapter-1-v9/packages/{sid}/geometry.json'));f=out/f'{sid}-water.png';im=Image.open(f);a=im.getchannel('A');byid={c['id']:c for c in d['cells']};free=Image.new('L',im.size);dr=ImageDraw.Draw(free)
 for c in d['cells']:
  if c['terrain'] is None:dr.polygon([(v['x'],v['y']) for v in c['polygon']],fill=255)
 interior=free.filter(ImageFilter.MinFilter(3));leak=sum(1 for x,y in zip(a.getdata(),interior.getdata()) if x>250 and y>250)
 assert leak==0,(sid,leak)
 bridge=next(p for p in d['pieces'] if p['kind']=='bridge');cells={cid:a.getpixel((round(byid[cid]['center']['x']),round(byid[cid]['center']['y']))) for cid in bridge['cells']};assert list(cells.values())==[255,0,0],cells
 old='5,2' if sid=='stream' else '1,4';new='6,2' if sid=='stream' else '2,4'
 def alpha(cid):p=byid[cid]['center'];return a.getpixel((round(p['x']),round(p['y'])))
 assert alpha(old)==0 and alpha(new)==255
 report[sid]={'status':'exact-material-mask-passed-bank-art-review-pending','fullFreePolygonInteriorOpaqueLeakPixels':leak,'rasterBoundaryTolerancePx':1,'bridgeCenterAndEndsAlpha':cells,'rejectedOldBend':{'cell':old,'alpha':alpha(old)},'acceptedNewBend':{'cell':new,'alpha':alpha(new)},'sourceSha256':hashlib.sha256(f.read_bytes()).hexdigest()}
(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
