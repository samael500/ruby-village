"""Source guide with whole-bank clearance to the actual logical union edge.

This is an intrinsic varying-width source specification, not post-hoc clipping
of already painted stones. Logical polygons and camera remain unchanged.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,math
root=Path(__file__).resolve().parents[1];base=root/'art/chapter-1-v9'
out=base/'layers/water/mill-pilot'
geometry=json.loads((base/'packages/mill/geometry.json').read_text())
water_cells=sorted([c for c in geometry['cells'] if c['terrain']=='water'],key=lambda c:c['r'])
points=[(640,260)]+[(c['center']['x'],c['center']['y']) for c in water_cells]+[(650,810)]
def edges(cells):
    result={}
    for cell in cells:
        vertices=cell['polygon']
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            edge=tuple(sorted([(round(a['x'],5),round(a['y'],5)),(round(b['x'],5),round(b['y'],5))]))
            result[edge]=result.get(edge,0)+1
    return {edge for edge,count in result.items() if count==1}
logical_edges=edges(water_cells)
board_edges=edges(geometry['cells'])
# The channel must enter/exit through the board perimeter, not stop6px before
# it. Only these coincident outer-board edges are exempt, never dry-cell edges.
ends=logical_edges & board_edges
boundary=logical_edges-ends
def distance(point,edge):
    x,y=point;(a,b),(c,d)=edge;dx=c-a;dy=d-b
    t=max(0,min(1,((x-a)*dx+(y-b)*dy)/(dx*dx+dy*dy)))
    return math.hypot(x-a-t*dx,y-b-t*dy)
samples=[]
for i in range(len(points)-1):
    p0=points[max(0,i-1)];p1=points[i];p2=points[i+1];p3=points[min(len(points)-1,i+2)]
    for j in range(64):
        t=j/64;xy=[]
        for k in (0,1):
            a,b,c,d=p0[k],p1[k],p2[k],p3[k]
            xy.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
        samples.append(tuple(xy))
samples.append(points[-1])
clearances=[min(distance(point,edge) for edge in boundary) for point in samples]
raw=[min(22,clearance-12) for clearance in clearances]
assert min(raw)>9,min(raw)
# Smooth conservative minima; smoothing can only narrow, never exceed budget.
radii=[min(raw[i],sum(raw[max(0,i-5):i+6])/len(raw[max(0,i-5):i+6])) for i in range(len(raw))]
def ribbon(extra):
    left=[];right=[]
    for i,(x,y) in enumerate(samples):
        before=samples[max(0,i-1)];after=samples[min(len(samples)-1,i+1)]
        dx=after[0]-before[0];dy=after[1]-before[1];length=math.hypot(dx,dy)
        radius=radii[i]+extra;nx=-dy/length*radius;ny=dx/length*radius
        left.append((round((x+nx)*4),round((y+ny)*4)))
        right.append((round((x-nx)*4),round((y-ny)*4)))
    mask=Image.new('L',(6688,3764));ImageDraw.Draw(mask).polygon(left+right[::-1],fill=255)
    return mask.resize((1672,941),Image.Resampling.LANCZOS)
logical=Image.open(out/'logical-water-mask.png')
paint_body=ImageChops.multiply(ribbon(0),logical)
water_support=ImageChops.multiply(ribbon(6),logical)
# The generated water reaches the original brown support. Keep that complete
# water support strictly inside truth. Dry flat shoreline gets its own wider
# support; this does not expand the visible-water layer or gameplay footprint.
bank=ribbon(20)
board=Image.open(out/'board-mask.png')
bank=ImageChops.multiply(bank,board)
bp=bank.load();lp=logical.load()
max_depth=0
for y in range(bank.height):
    for x in range(bank.width):
        if not bp[x,y] or lp[x,y]>250:continue
        depth=min(distance((x,y),edge) for edge in logical_edges)
        if depth>12:bp[x,y]=0
        elif bp[x,y]>250:max_depth=max(max_depth,depth)
water_support.save(out/'adaptive-water-body-mask.png');bank.save(out/'adaptive-water-bank-mask.png')
# Exact Euclidean18px inset of each convex free polygon, for the protected core.
core=Image.new('L',(6688,3764));cd=ImageDraw.Draw(core)
def intersect(a,b,c,d):
    rx=b[0]-a[0];ry=b[1]-a[1];sx=d[0]-c[0];sy=d[1]-c[1]
    t=((c[0]-a[0])*sy-(c[1]-a[1])*sx)/(rx*sy-ry*sx)
    return (a[0]+t*rx,a[1]+t*ry)
for cell in geometry['cells']:
    if cell['terrain'] is not None:continue
    vertices=[(p['x'],p['y']) for p in cell['polygon']];lines=[]
    center=cell['center']
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy);nx=-dy/length;ny=dx/length
        if (center['x']-a[0])*nx+(center['y']-a[1])*ny<0:nx=-nx;ny=-ny
        lines.append(((a[0]+18*nx,a[1]+18*ny),(b[0]+18*nx,b[1]+18*ny)))
    inset=[intersect(*lines[i-1],*lines[i]) for i in range(len(lines))]
    cd.polygon([(round(x*4),round(y*4)) for x,y in inset],fill=255)
core=core.resize((1672,941),Image.Resampling.LANCZOS)
core.save(out/'free-core-mask18.png')
dry=Image.open(out/'dry-background.webp').convert('RGB')
material=Image.open(base/'candidates/water-material-v1.png').convert('RGB')
target=Image.composite(material,dry,paint_body)
target_path=base/'candidates/mill-adaptive-channel-edit-target-v4.png'
if not target_path.exists():target.save(target_path)
guide=target.convert('RGBA')
for color,mask in [((185,85,20,255),ImageChops.subtract(water_support,paint_body)),((0,210,255,255),paint_body)]:
    layer=Image.new('RGBA',guide.size,color);layer.putalpha(mask.point(lambda a:round(a*.6)));guide=Image.alpha_composite(guide,layer)
draw=ImageDraw.Draw(guide)
for edge in boundary:draw.line(edge,fill=(255,40,180,255),width=1)
guide_path=out/'adaptive-channel-edit-guide.png'
if not guide_path.exists():guide.save(guide_path)
margin=min(c-r-6 for c,r in zip(clearances,radii))
assert margin>=6-1e-9,margin
report={'purpose':'adaptive source width; strict water support separate from allowed flat dry shore; immutable logical truth unchanged','nativeCanvas':[1672,941],'camera':geometry['camera'],'centerline':'Catmull-Rom through all seven accepted water centers','distanceMetric':'exact native-pixel Euclidean distance to exposed union segments bordering dry ground; shared internal water edges removed','sourcePaintTargetBodyRadiusRangePx':[min(radii),max(radii)],'strictWaterSupportRadiusRangePx':[min(radii)+6,max(radii)+6],'minimumStrictWaterSupportClearancePx':margin,'requiredWaterToDryBoundaryMarginPx':6,'dryShoreArtSupportAdditionalRadiusPx':14,'maxDryShoreFreeBoundaryDepthPx':max_depth,'allowedDryShoreFreeBoundaryDepthPx':12,'protectedFreeCoreInsetPx':18,'shoreContentRestriction':'flat damp earth and tiny low pebbles only; no water, tall rocks or shrubs on free ground; source visual review pending','rasterTolerancePx':1,'endpointException':'Only boundary segments coincident with complete77-board outside perimeter; permits decorative entry/exit continuity. No dry-cell boundary exception.','exemptOuterBoardEdges':list(ends),'logicalBoundarySegments':list(boundary),'profile':[{'point':[round(x,4),round(y,4)],'clearance':round(c,4),'sourcePaintBodyRadius':round(r,4),'strictWaterSupportRadius':round(r+6,4),'dryArtRadiusBefore12pxBoundaryGuard':round(r+20,4)} for (x,y),c,r in zip(samples,clearances,radii)],'status':'adaptive-water-and-dryshore-guide-passed-source-art-and-actual-game-review-pending'}
(out/'adaptive-channel-profile.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['profile','logicalBoundarySegments','exemptOuterBoardEdges']},indent=2))
