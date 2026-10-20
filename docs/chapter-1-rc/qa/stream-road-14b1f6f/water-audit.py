import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
m=json.loads((ROOT/'art/chapter-1-v9/layers/water/stream-pilot/manifest.json').read_text());g=json.loads((ROOT/m['geometry']).read_text());root=ROOT/'art/chapter-1-v9/layers/water/stream-pilot';water=Image.open(root/'logical-water-mask.png').convert('L');free=Image.new('L',(1672,941));draw=ImageDraw.Draw(free)
for c in g['cells']:
 if c['terrain']!='water':draw.polygon([(p['x'],p['y']) for p in c['polygon']],fill=255)
# Exclude only shared raster boundary pixels from the free-region measurement.
from PIL import ImageFilter
interior=free.filter(ImageFilter.MinFilter(3));leak=ImageChops.multiply(water,interior);count=sum(v>32 for v in leak.get_flattened_data())
centers={c['id']:c['center'] for c in g['cells']};samples={k:water.getpixel((round(centers[k]['x']),round(centers[k]['y']))) for k in ['5,1','6,1','7,1']};assert samples=={'5,1':0,'6,1':255,'7,1':0}
candidates=[(x,y) for y in range(941) for x in range(1672) if leak.getpixel((x,y))>32]
def inside_distance(x,y,cell):
 pts=[(p['x'],p['y']) for p in cell['polygon']];cross=[];dist=[]
 for (ax,ay),(bx,by) in zip(pts,pts[1:]+pts[:1]):
  cross.append((bx-ax)*(y-ay)-(by-ay)*(x-ax));u=max(0,min(1,((x-ax)*(bx-ax)+(y-ay)*(by-ay))/((bx-ax)**2+(by-ay)**2)));dist.append(math.hypot(x-ax-u*(bx-ax),y-ay-u*(by-ay)))
 return min(dist) if min(cross)>=-1e-8 or max(cross)<=1e-8 else -1
analytical=[]
for convention,offset in [('pixel integer',0),('pixel center',.5)]:
 vals=[max(inside_distance(x+offset,y+offset,c) for c in g['cells'] if c['terrain']!='water') for x,y in candidates]
 analytical.append({'convention':convention,'coarseCandidateCount':len(candidates),'interiorBeyond1px':sum(v>1 for v in vals),'maxFreeCellInteriorDistance':max(vals)})
assert all(v['interiorBeyond1px']==0 for v in analytical),analytical

(OUT/'water-audit.json').write_text(json.dumps({'canvas':water.size,'waterCells':[c['id'] for c in g['cells'] if c['terrain']=='water'],'coarseRasterCandidatePixels':count,'analyticalBoundaryCheck':analytical,'boundaryExclusion':'1px MinFilter free interior; no erosion of water mask','bridgeEndMiddleEndMaskSamples':samples,'artisticNaturalBankAcceptance':False},indent=2)+'\n');print('PASS mask middle water,ends dry,no interior leak; visual bank quality NOT certified')
