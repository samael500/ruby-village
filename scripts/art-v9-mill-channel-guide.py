"""Separate the artistic mill channel from immutable logical water cells.

The smooth guide is source-edit guidance, not an inferred gameplay footprint.
All visible channel/bank alpha stays inside accepted logical water polygons.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import json,math
root=Path(__file__).resolve().parents[1]
base=root/'art/chapter-1-v9';out=base/'layers/water/mill-pilot'
d=json.loads((base/'packages/mill/geometry.json').read_text())
water_cells=[c for c in d['cells'] if c['terrain']=='water']
water_cells.sort(key=lambda c:c['r'])
points=[(640,260)]+[(c['center']['x'],c['center']['y']) for c in water_cells]+[(650,810)]
ground=[(x,y/.65) for x,y in points]
samples=[]
for i in range(len(ground)-1):
 p0=ground[max(0,i-1)];p1=ground[i];p2=ground[i+1];p3=ground[min(len(ground)-1,i+2)]
 for j in range(48):
  t=j/48
  coords=[]
  for axis in (0,1):
   a,b,c,e=p0[axis],p1[axis],p2[axis],p3[axis]
   coords.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-e)*t*t+(-a+3*b-3*c+e)*t*t*t))
  samples.append(tuple(coords))
samples.append(ground[-1])
left=[];right=[]
for i,(x,y) in enumerate(samples):
 before=samples[max(0,i-1)];after=samples[min(len(samples)-1,i+1)]
 dx=after[0]-before[0];dy=after[1]-before[1];length=math.hypot(dx,dy)
 half=33+2.5*math.sin(i*.041)
 nx=-dy/length*half;ny=dx/length*half
 left.append((round((x+nx)*4),round((y+ny)*.65*4)))
 right.append((round((x-nx)*4),round((y-ny)*.65*4)))
body=Image.new('L',(6688,3764));ImageDraw.Draw(body).polygon(left+right[::-1],fill=255)
body=body.resize((1672,941),Image.Resampling.LANCZOS)
logical=Image.open(out/'logical-water-mask.png')
body=ImageChops.multiply(body,logical)
bank=ImageChops.multiply(body.filter(ImageFilter.MaxFilter(17)),logical)
bank=ImageChops.multiply(bank,ImageChops.invert(Image.open(out/'free-mask.png').filter(ImageFilter.MinFilter(3)).point(lambda a:255 if a>250 else 0)))
delivery_bank=ImageChops.multiply(body.filter(ImageFilter.MaxFilter(49)),logical)
delivery_bank=ImageChops.multiply(delivery_bank,ImageChops.invert(Image.open(out/'free-mask.png').filter(ImageFilter.MinFilter(3)).point(lambda a:255 if a>250 else 0)))
body.save(out/'visual-water-body-mask.png')
delivery_bank.save(out/'visual-water-and-bank-mask.png')
dry=Image.open(out/'dry-background.webp').convert('RGB')
material=Image.open(base/'candidates/water-material-v1.png').convert('RGB')
target=Image.composite(material,dry,body)
target.save(base/'candidates/mill-curved-channel-edit-target-v3.png')
guide=target.convert('RGBA')
bank_strip=ImageChops.subtract(bank,body)
for color,mask in [((180,80,15,255),bank_strip),((0,210,255,255),body)]:
 layer=Image.new('RGBA',guide.size,color);layer.putalpha(mask.point(lambda a:round(a*.6)));guide=Image.alpha_composite(guide,layer)
outline=ImageChops.subtract(logical,logical.filter(ImageFilter.MinFilter(3)))
layer=Image.new('RGBA',guide.size,(255,40,180,255));layer.putalpha(outline);guide=Image.alpha_composite(guide,layer)
guide.save(out/'curved-channel-edit-guide.png')
(out/'visual-channel-contract.json').write_text(json.dumps({'purpose':'artistic channel only; exact logical-water-mask.png remains unchanged gameplay truth','groundScale':.65,'method':'smooth Catmull-Rom centerline through all accepted water-cell centers;66±5px ground width;8px source-edit shoreline guidance;24px delivery art support to retain whole painted stones/earth and adjacent dry grass; clipped inside logical union','controlPoints':points,'waterCellCenters':{c['id']:c['center'] for c in water_cells},'logicalWaterMask':'logical-water-mask.png','actualVisualWaterBodyMask':'visual-water-body-mask.png','actualArtBankMask':'visual-water-and-bank-mask.png','status':'guide-only-native-art-and-game-review-pending'},indent=2)+'\n')
print('Mill curved channel guide prepared; logical mask unchanged')
