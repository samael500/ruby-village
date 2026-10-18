"""Registered source-only stream pilot. No terrain/camera inference from pixels.

Decorative continuation is forbidden inside the complete 77-cell footprint.
The exact logical water alpha has no erosion at its board entry/exit.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import hashlib, json

root = Path(__file__).resolve().parents[1]
base = root/'art/chapter-1-v9'
out = base/'layers/water/stream-pilot'
out.mkdir(parents=True, exist_ok=True)
geometry_path = base/'packages/stream/geometry.json'
geometry = json.loads(geometry_path.read_text())
size = (1672, 941)
scale = 4
def polygon_mask(cells):
    mask = Image.new('L', (size[0]*scale, size[1]*scale))
    draw = ImageDraw.Draw(mask)
    for cell in cells:
        draw.polygon([(round(p['x']*scale),round(p['y']*scale)) for p in cell['polygon']],fill=255)
    return mask.resize(size, Image.Resampling.LANCZOS)
cells = geometry['cells']
assert len(cells) == 77
board = polygon_mask(cells)
water = polygon_mask([c for c in cells if c['terrain']=='water'])
free = polygon_mask([c for c in cells if c['terrain'] is None])
dry_path = base/'candidates/stream-dry-v1.png'
continuation_path = base/'candidates/stream-continuation-v1.png'
banks_path = base/'candidates/stream-bankstrip-generated-v2.png'
curved_path=base/'candidates/stream-curved-channel-generated-v3.png'
curved=curved_path.exists()
if curved:banks_path=curved_path
dry = Image.open(dry_path).convert('RGBA')
continuation = Image.open(continuation_path).convert('RGBA')
banks = Image.open(banks_path).convert('RGBA')
assert dry.size == continuation.size == banks.size == size
outside = ImageChops.invert(board)
decorative = continuation.copy()
decorative.putalpha(outside)
logical = banks.copy()
# Feather only the inside of the banks. The first/last water-cell edges at the
# complete board perimeter remain fully open to decorative continuation.
visual_body=Image.open(out/'visual-water-body-mask.png') if curved else water.copy()
visual_art=Image.open(out/'visual-water-and-bank-mask.png') if curved else water.copy()
side_soft = ImageChops.multiply(visual_art, visual_art.filter(ImageFilter.MinFilter(3 if curved else 7)).filter(ImageFilter.GaussianBlur(1 if curved else 1.4)))
board_edge = ImageChops.subtract(board,board.filter(ImageFilter.MinFilter(13)))
art_alpha = ImageChops.lighter(side_soft,ImageChops.multiply(visual_art,board_edge))
free_interior = free.filter(ImageFilter.MinFilter(3)).point(lambda a:255 if a>250 else 0)
art_alpha = ImageChops.multiply(art_alpha,ImageChops.invert(free_interior))
logical.putalpha(art_alpha)
# Restore exact dry board, retaining only the accepted water footprint.
native = Image.composite(dry, continuation, board)
native.convert('RGB').save(out/'dry-background.webp',lossless=True,method=6)
native = Image.alpha_composite(native, logical).convert('RGB')
native = Image.composite(dry.convert('RGB'),native,free_interior)
for name, im in [('board-mask',board),('free-mask',free),('logical-water-mask',water),('bank-art-alpha',art_alpha),('decorative-outside-board',decorative),('logical-water',logical),('native-background',native)]:
    im.save(out/(name+'.png'))
native.save(out/'background.webp',lossless=True,method=6)
# Explicit registration artifact; transparent outer region is not painted outpaint.
wide_info={'status':'INCOMPLETE-native-registration-only-no-painted-outer-source','canvas':[4096,1600],'originalRect':[1212,329,1672,941]}
wide_source=base/'candidates/stream-wide-generated-v2.png'
fit_path=out/'wide-registration-fit.json'
if wide_source.exists() and fit_path.exists():
    fit=json.loads(fit_path.read_text())
    painted=Image.open(wide_source).convert('RGB').resize((round(4096*fit['scale']),round(1600*fit['scale'])),Image.Resampling.LANCZOS)
    canvas=Image.new('RGB',(4096,1600))
    canvas.paste(painted,tuple(fit['translation']))
    blend=Image.new('L',size)
    draw=ImageDraw.Draw(blend)
    for inset in range(49):
        draw.rectangle((inset,inset,size[0]-1-inset,size[1]-1-inset),fill=round(inset*255/48))
    blend=ImageChops.lighter(blend,board)
    patch=canvas.crop((1212,329,2884,1270))
    canvas.paste(Image.composite(native,patch,blend),(1212,329))
    wide=canvas.crop((412,200,3684,1400))
    wide.save(out/'wide-registered.png')
    wide.save(out/'wide.webp',lossless=True,method=6)
    wide_info={'status':'painted-registered-native-guard-passed-join-and-game-review-pending','canvas':[3272,1200],'originalRect':[800,129,1672,941],'joinBandPx':48,'sourceAffine':fit,'source':str(wide_source.relative_to(root))}
    guarded=wide.crop((800,129,2472,1070))
    delta=ImageChops.difference(native,guarded)
    board_inner=board.filter(ImageFilter.MinFilter(3))
    changed=sum(max(p)>0 and a>250 for p,a in zip(delta.getdata(),board_inner.getdata()))
    assert changed==0,changed
    wide_info['fullBoardInteriorChangedRgbPixels']=changed
else:
    wide = Image.new('RGBA',(4096,1600))
    wide.paste(native,(1212,329))
    wide.save(out/'registered-wide-INCOMPLETE.png')
review = native.convert('RGBA')
draw = ImageDraw.Draw(review)
for cell in cells:
    points=[(p['x'],p['y']) for p in cell['polygon']]
    draw.line(points+[points[0]],fill=(0,180,255,210) if cell['terrain']=='water' else (255,255,255,100),width=1)
review.save(out/'geometry-overlay.png')
for name, box in [('entry-review',(760,245,970,355)),('exit-review',(890,705,1100,815)),('bridge-review',(760,340,1100,460))]:
    native.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3)).save(out/(name+'.png'))
alpha = logical.getchannel('A')
interior = free.filter(ImageFilter.MinFilter(3))
leaks = sum(a>250 and b>250 for a,b in zip(alpha.getdata(),interior.getdata()))
assert leaks == 0, leaks
diff=ImageChops.difference(native,dry.convert('RGB'))
free_changes=sum(max(p)>0 and a==255 for p,a in zip(diff.getdata(),free_interior.getdata()))
assert free_changes==0,free_changes
byid={c['id']:c for c in cells}
def at(cid):
    p=byid[cid]['center'];return alpha.getpixel((round(p['x']),round(p['y'])))
bridge=next(p for p in geometry['pieces'] if p['kind']=='bridge')
bridge_alpha={cid:at(cid) for cid in bridge['cells']}
assert list(bridge_alpha.values())==[255,0,0],bridge_alpha
assert at('5,2')==0 and at('6,2')==255
body=visual_body
def body_at(cid):
    p=byid[cid]['center'];return body.getpixel((round(p['x']),round(p['y'])))
body_bridge={cid:body_at(cid) for cid in bridge['cells']}
assert list(body_bridge.values())==[255,0,0],body_bridge
body_centers={c['id']:body_at(c['id']) for c in cells if c['terrain']=='water'}
assert all(a==255 for a in body_centers.values()),body_centers
body_free=sum(a>250 and b==255 for a,b in zip(body.getdata(),free_interior.getdata()))
assert body_free==0
contacts={}
middle=byid[bridge['cells'][0]]['center']
for cid in ['6,0','6,2']:
    other=byid[cid]['center'];point=(round((middle['x']+other['x'])/2),round((middle['y']+other['y'])/2))
    contacts[cid]={'point':point,'alpha':body.getpixel(point)}
assert all(v['alpha']==255 for v in contacts.values()),contacts
# Flood the actual visible body, rather than substituting the logical mask.
seed=byid['6,0']['center'];seed=(round(seed['x']),round(seed['y']))
pixels=body.load();visited={seed};pending=[seed]
while pending:
    x,y=pending.pop()
    for point in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
        a,b=point
        if 0<=a<size[0] and 0<=b<size[1] and point not in visited and pixels[a,b]>=128:
            visited.add(point);pending.append(point)
connected_centers={c['id']:(round(c['center']['x']),round(c['center']['y'])) in visited for c in cells if c['terrain']=='water'}
assert all(connected_centers.values()),connected_centers
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={'status':'exact-mask-checks-passed-native-art-review-pending','canvas':list(size),
    'camera':geometry['camera'],'boardCells':len(cells),'waterCells':[c['id'] for c in cells if c['terrain']=='water'],
    'fullFreePolygonInteriorOpaqueLeakPixels':leaks,'rasterBoundaryTolerancePx':1,
    'fullFreePolygonInteriorChangedRgbPixels':free_changes,
    'bridgeCenterAndEndsAlpha':bridge_alpha,'rejectedOldBendAlpha':at('5,2'),'acceptedNewBendAlpha':at('6,2'),
    'logicalMaskErosionPx':0,'visibleWaterContour':'separate curved artistic channel inside logical zone' if curved else 'full-logical-contour-rejected-by-actual-QA-P1',
    'actualBodyMask':'visual-water-body-mask.png' if curved else 'logical-water-mask.png',
    'actualBodyAudit':{'bridgeCenterAndDryEndsAlpha':body_bridge,'waterCellCenterAlpha':body_centers,'bridgeMiddleSharedWaterEdgeAlpha':contacts,'allWaterCellCentersInSameConnectedActualBody':connected_centers,'freeInteriorOpaqueLeakPixels':body_free,'status':'raster-contact-and-connectivity-passed-art-game-review-pending'},
    'bankArtInwardFeatherPx':1 if curved else 3,'entryExitFeather':'disabled within 6px of complete board perimeter',
    'decorativeWater':'outside complete 77-cell union only; separate from logical layer',
    'sourceSha256':{str(p.relative_to(root)):sha(p) for p in [geometry_path,dry_path,continuation_path,banks_path]},
    'outputSha256':{p.name:sha(p) for p in sorted(out.glob('*.png'))},
    'wide':wide_info,
    'checks':{'nativeBankVisualAudit':'pending','entryExitContinuityVisualAudit':'pending','actualGameplay':'not-run'}}
(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
manifest={'schemaVersion':1,'scene':'stream','activation':'inactive-source-handoff-for-root-game-review',
    'canvas':list(size),'camera':geometry['camera'],
    'anchors':{'start':geometry['start']['pixel'],'goal':geometry['goal']['pixel'],'residentFeet':{'x':1400,'y':225,'status':'existing-native-anchor-game-review-pending'}},
    'acceptedLayoutInputs':geometry['inputs'],'layoutChanges':geometry['layoutChanges'],
    'solution':[{'id':piece['id'],'placement':piece['placement'],'cells':piece['cells']} for piece in geometry['pieces']],
    'path':geometry['path'],
    'background':'background.webp','backgroundContent':'baked exact logical water plus guarded dry board and outside-board decorative continuation; do not stack logical-water.png again',
    'dryBackground':'dry-background.webp','logicalWaterOverlay':'logical-water.png','logicalWaterMask':'logical-water-mask.png',
    'logicalWaterMaskRole':'immutable full accepted77-board water polygons for rules/diagnostic truth, not visible shoreline',
    'visualWaterBodyMask':'visual-water-body-mask.png' if curved else None,
    'visualWaterBankMask':'visual-water-and-bank-mask.png' if curved else None,
    'waterArtOverlay':'logical-water.png','waterArtOverlayRole':'separate painted curved water and banks; legacy filename is not the full logical mask',
    'wide':{'file':'wide.webp',**wide_info},'geometry':str(geometry_path.relative_to(root)),
    'checks':'checks.json','status':'root-art-and-actual-game-review-pending'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(report,indent=2))
