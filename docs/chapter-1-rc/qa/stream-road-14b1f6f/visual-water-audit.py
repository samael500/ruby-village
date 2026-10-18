import json,hashlib,subprocess
from pathlib import Path
from PIL import Image,ImageChops,ImageFilter
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;src=ROOT/'art/chapter-1-v9/layers/water/stream-pilot';m=json.loads((src/'manifest.json').read_text());g=json.loads((ROOT/m['geometry']).read_text());cells={c['id']:c for c in g['cells']};truth=Image.open(src/'logical-water-mask.png').convert('L');body=Image.open(src/'visual-water-body-mask.png').convert('L');art=Image.open(src/'visual-water-and-bank-mask.png').convert('L');old=subprocess.check_output(['git','show','c64b249:art/chapter-1-v9/layers/water/stream-pilot/logical-water-mask.png'],cwd=ROOT);unchanged=hashlib.sha256(old).hexdigest()==hashlib.sha256((src/'logical-water-mask.png').read_bytes()).hexdigest();assert unchanged
point=lambda k:(round(cells[k]['center']['x']),round(cells[k]['center']['y']))
centers={k:body.getpixel(point(k))for k in cells if cells[k]['terrain']=='water'};ends={k:body.getpixel(point(k))for k in ['5,1','6,1','7,1']};assert all(v==255 for v in centers.values()) and ends=={'5,1':0,'6,1':255,'7,1':0}
a=cells['6,1']['center'];contacts={}
for k in ['6,0','6,2']:
 b=cells[k]['center'];xy=(round((a['x']+b['x'])/2),round((a['y']+b['y'])/2));contacts[k]={'xy':xy,'bodyAlpha':body.getpixel(xy)};assert body.getpixel(xy)==255
seed=point('6,0');stack=[seed];seen={seed};pix=body.load();w,h=body.size
while stack:
 x,y=stack.pop()
 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=xx<w and 0<=yy<h and (xx,yy)not in seen and pix[xx,yy]>=128:seen.add((xx,yy));stack.append((xx,yy))
connected={k:point(k)in seen for k in centers};assert all(connected.values())
free=Image.open(src/'free-mask.png').convert('L').filter(ImageFilter.MinFilter(3)).point(lambda v:255 if v>250 else 0);diff=ImageChops.difference(Image.open(src/'native-background.png').convert('RGB'),Image.open(ROOT/'art/chapter-1-v9/candidates/stream-dry-v1.png').convert('RGB'));changed=0
for delta,mask in zip(diff.getdata(),free.getdata()):
 if mask and max(delta)>0:changed+=1
assert changed==0
leak=sum(v>32 for v in ImageChops.multiply(body,free).get_flattened_data());assert leak==0
(OUT/'visual-water-audit.json').write_text(json.dumps({'logicalTruthMaskUnchangedFromC64b249':unchanged,'truthSha256':hashlib.sha256(old).hexdigest(),'visibleBodyCenterAlpha':centers,'bridgeEndMiddleEndActualBodyAlpha':ends,'bridgeMiddleSharedContacts':contacts,'actualBody4ConnectedCenters':connected,'actualBodyConnectedPixelCount':len(seen),'freeInteriorRgbChanged':changed,'freeInteriorBodyLeak':leak,'method':'1px conservative free interior; actual visual body mask measured separately from full immutable truthmask; native PNG vs canonical dry source RGB'},indent=2)+'\n');print('PASS actual curved body centers255/connectivity/sharedcontacts255/bridgeends0/freeRGB0/truth unchanged')
