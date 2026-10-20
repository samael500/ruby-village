"""Mill-only source registration; independent from shared props and runtime."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import hashlib, json

root=Path(__file__).resolve().parents[1]
base=root/'art/chapter-1-v9'
out=base/'layers/water/mill-pilot'
out.mkdir(parents=True,exist_ok=True)
geometry_path=base/'packages/mill/geometry.json'
geometry=json.loads(geometry_path.read_text())
size=(1672,941)
def mask(cells):
    image=Image.new('L',(6688,3764));draw=ImageDraw.Draw(image)
    for cell in cells:
        draw.polygon([(round(p['x']*4),round(p['y']*4)) for p in cell['polygon']],fill=255)
    return image.resize(size,Image.Resampling.LANCZOS)
cells=geometry['cells'];assert len(cells)==77
board=mask(cells)
water=mask([c for c in cells if c['terrain']=='water'])
free=mask([c for c in cells if c['terrain'] is None])
free_inner=free.filter(ImageFilter.MinFilter(3)).point(lambda a:255 if a>250 else 0)
dry_path=base/'layers/props/mill-dry-map.png'
continuation_path=base/'candidates/mill-continuation-v1.png'
banks_path=base/'candidates/mill-bankstrip-wheelclear-v2.png'
dry=Image.open(dry_path).convert('RGBA')
continuation=Image.open(continuation_path).convert('RGBA')
banks=Image.open(banks_path).convert('RGBA')
assert dry.size==continuation.size==banks.size==size
outside=ImageChops.invert(board)
decorative=continuation.copy();decorative.putalpha(outside)
base_native=Image.composite(dry,continuation,board)
# Import only the local old-wheel clearance, wholly above the board. The rest
# of the decorative scene continues to come from the immutable continuation.
clearance=Image.new('L',size);clear_draw=ImageDraw.Draw(clearance)
clear_draw.rectangle((1225,118,1315,208),fill=255)
clearance=clearance.filter(ImageFilter.GaussianBlur(4))
clearance=ImageChops.multiply(clearance,ImageChops.invert(board))
base_native=Image.composite(banks,base_native,clearance)
base_native.convert('RGB').save(out/'dry-background.webp',lossless=True,method=6)
soft=ImageChops.multiply(water,water.filter(ImageFilter.MinFilter(7)).filter(ImageFilter.GaussianBlur(1.4)))
board_edge=ImageChops.subtract(board,board.filter(ImageFilter.MinFilter(13)))
art_alpha=ImageChops.lighter(soft,ImageChops.multiply(water,board_edge))
art_alpha=ImageChops.multiply(art_alpha,ImageChops.invert(free_inner))
logical=banks.copy();logical.putalpha(art_alpha)
native=Image.alpha_composite(base_native,logical).convert('RGB')
native=Image.composite(dry.convert('RGB'),native,free_inner)

# Source RGB is never repainted. Native alpha erosion removes generated fringe
# before the one uniform registered resize; all spokes/paddles remain intact.
wheel_path=base/'candidates/millwheel-v4.png'
wheel=Image.open(wheel_path).convert('RGBA');assert wheel.size==(1254,1254)
source_alpha=wheel.getchannel('A')
wheel.putalpha(source_alpha.filter(ImageFilter.MinFilter(11)))
wheel.save(out/'wheel-native-clean-alpha.png')
wheel=wheel.resize((110,110),Image.Resampling.LANCZOS)
wheel.save(out/'wheel-110.png')
with_wheel=native.convert('RGBA');with_wheel.alpha_composite(wheel,(1215,108))
with_wheel.convert('RGB').save(out/'native-with-wheel.png')
with_wheel.crop((1160,55,1390,285)).resize((690,690)).save(out/'wheel-race-review.png')
for name,im in [('board-mask',board),('free-mask',free),('logical-water-mask',water),('bank-art-alpha',art_alpha),('decorative-outside-board',decorative),('logical-water',logical),('native-background',native)]:im.save(out/(name+'.png'))
native.save(out/'background.webp',lossless=True,method=6)
review=with_wheel.copy();draw=ImageDraw.Draw(review)
for cell in cells:
    points=[(p['x'],p['y']) for p in cell['polygon']]
    draw.line(points+[points[0]],fill=(0,180,255,210) if cell['terrain']=='water' else (255,255,255,100),width=1)
review.save(out/'geometry-overlay.png')
for name,box in [('entry-review',(520,245,730,355)),('exit-review',(520,705,730,815)),('bridge-review',(470,550,780,660))]:native.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3)).save(out/(name+'.png'))
diff=ImageChops.difference(native,dry.convert('RGB'))
changed=sum(max(p)>0 and a==255 for p,a in zip(diff.getdata(),free_inner.getdata()))
leaks=sum(a>250 and b==255 for a,b in zip(art_alpha.getdata(),free_inner.getdata()))
assert changed==leaks==0
byid={c['id']:c for c in cells}
def at(cid):
    p=byid[cid]['center'];return art_alpha.getpixel((round(p['x']),round(p['y'])))
bridge=next(p for p in geometry['pieces'] if p['kind']=='bridge')
bridge_alpha={cid:at(cid) for cid in bridge['cells']}
assert list(bridge_alpha.values())==[255,0,0],bridge_alpha
assert at('1,4')==0 and at('2,4')==255
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks={'status':'exact-mask-checks-passed-bank-wheel-art-and-game-review-pending','fullFreePolygonInteriorOpaqueLeakPixels':leaks,'fullFreePolygonInteriorChangedRgbPixels':changed,'rasterBoundaryTolerancePx':1,'bridgeCenterAndEndsAlpha':bridge_alpha,'rejectedOldBendAlpha':at('1,4'),'acceptedNewBendAlpha':at('2,4'),'boardCells':len(cells),'logicalMaskErosionPx':0,'bankArtInwardFeatherPx':3,'entryExitFeather':'disabled within6px of fullboard perimeter','wheelAlphaNativeErosionPx':5,'sourceSha256':{str(p.relative_to(root)):sha(p) for p in [geometry_path,dry_path,continuation_path,banks_path,wheel_path]},'checks':{'nativeBankVisualAudit':'pending','wheelRaceRegistrationVisualAudit':'pending','actualGameplay':'not-run'}}
(out/'checks.json').write_text(json.dumps(checks,indent=2)+'\n')
manifest={'schemaVersion':1,'scene':'mill','activation':'inactive-source-handoff','canvas':list(size),'camera':geometry['camera'],'anchors':{'start':geometry['start']['pixel'],'goal':geometry['goal']['pixel'],'wheelAxle':{'x':1270,'y':163}},'geometry':str(geometry_path.relative_to(root)),'acceptedLayoutInputs':geometry['inputs'],'layoutChanges':geometry['layoutChanges'],'solution':[{'id':p['id'],'placement':p['placement'],'cells':p['cells']} for p in geometry['pieces']],'path':geometry['path'],'background':'background.webp','backgroundContent':'baked exactwater and decorative millrace; old bearing cleared locally above board; small axle and separate wheel overlay','wheel':{'file':'wheel-110.png','source':str(wheel_path.relative_to(root)),'sourceSize':[1254,1254],'sourcePivot':[627,627],'size':[110,110],'origin':[1215,108],'pivot':[55,55],'worldAxle':[1270,163],'transform':'one uniform110/1254 scale; source alpha erosion5px; no CSS correction','status':'source-alpha-and-axle-art-review-pending'},'dryBackground':'dry-background.webp','logicalWaterOverlay':'logical-water.png','logicalWaterMask':'logical-water-mask.png','wide':None,'wideStatus':'not-started','checks':'checks.json','status':'native-bank-wheel-and-game-review-pending'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(checks,indent=2))
