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
adaptive_path=base/'candidates/stream-adaptive-channel-generated-v4.png'
adaptive=adaptive_path.exists()
if adaptive:banks_path=adaptive_path
body_file='adaptive-water-body-mask.png' if adaptive else 'visual-water-body-mask.png'
bank_file='adaptive-water-bank-mask.png' if adaptive else 'visual-water-and-bank-mask.png'
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
visual_body=Image.open(out/body_file) if curved or adaptive else water.copy()
visual_art=Image.open(out/bank_file) if curved or adaptive else water.copy()
side_soft = ImageChops.multiply(visual_art, visual_art.filter(ImageFilter.MinFilter(3 if curved else 7)).filter(ImageFilter.GaussianBlur(1 if curved else 1.4)))
board_edge = ImageChops.subtract(board,board.filter(ImageFilter.MinFilter(13)))
art_alpha = ImageChops.lighter(side_soft,ImageChops.multiply(visual_art,board_edge))
free_interior = free.filter(ImageFilter.MinFilter(3)).point(lambda a:255 if a>250 else 0)
protected_free=Image.open(out/'free-core-mask18.png').point(lambda a:255 if a>250 else 0) if adaptive else free_interior
art_alpha = ImageChops.multiply(art_alpha,ImageChops.invert(protected_free))
logical.putalpha(art_alpha)
# Restore exact dry board, retaining only the accepted water footprint.
native = Image.composite(dry, continuation, board)
if adaptive:
    # Do not count unrelated outer-board antialias mixing as dry-shore work.
    # Free raster pixel centers start from the exact dry plate everywhere.
    native=Image.composite(dry,native,free.point(lambda a:255 if a>=128 else 0))
native.convert('RGB').save(out/'dry-background.webp',lossless=True,method=6)
native = Image.alpha_composite(native, logical).convert('RGB')
native = Image.composite(dry.convert('RGB'),native,protected_free)
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
panels=[]
for channel_mask,color in [(water,(0,120,255,255)),(visual_body,(255,40,180,255))]:
    layer=Image.new('RGBA',size,color)
    layer.putalpha(channel_mask.point(lambda a:round(a*.45)))
    panels.append(Image.alpha_composite(native.convert('RGBA'),layer).convert('RGB').resize((1003,565)))
paired=Image.new('RGB',(2006,565))
paired.paste(panels[0],(0,0));paired.paste(panels[1],(1003,0))
paired.save(out/'logical-versus-visual-review.png')
for name, box in [('entry-review',(760,245,970,355)),('exit-review',(890,705,1100,815)),('bridge-review',(760,340,1100,460))]:
    native.crop(box).resize(((box[2]-box[0])*3,(box[3]-box[1])*3)).save(out/(name+'.png'))
alpha = logical.getchannel('A')
interior = free.filter(ImageFilter.MinFilter(3))
leaks = sum(a>250 and b>250 for a,b in zip(alpha.getdata(),interior.getdata()))
if not adaptive:assert leaks == 0, leaks
diff=ImageChops.difference(native,dry.convert('RGB'))
free_changes=sum(max(p)>0 and a==255 for p,a in zip(diff.getdata(),free_interior.getdata()))
protected_changes=sum(max(p)>0 and a==255 for p,a in zip(diff.getdata(),protected_free.getdata()))
assert protected_changes==0,protected_changes
if not adaptive:assert free_changes==0,free_changes
dry_boundary_changes=0;dry_boundary_max_depth=0;cyan_free_candidates=0
if adaptive:
    import math
    profile=json.loads((out/'adaptive-channel-profile.json').read_text())
    boundary=profile['logicalBoundarySegments']
    def distance(point,edge):
        x,y=point;(a,b),(c,d)=edge;dx=c-a;dy=d-b
        t=max(0,min(1,((x-a)*dx+(y-b)*dy)/(dx*dx+dy*dy)))
        return math.hypot(x-a-t*dx,y-b-t*dy)
    changed_pixels=diff.load();free_pixels=free.load();native_pixels=native.load()
    for y in range(size[1]):
        for x in range(size[0]):
            if free_pixels[x,y]<128 or max(changed_pixels[x,y])==0:continue
            dry_boundary_changes+=1
            depth=min(distance((x,y),edge) for edge in boundary)
            dry_boundary_max_depth=max(dry_boundary_max_depth,depth)
            red,green,blue=native_pixels[x,y]
            if blue>red+12 and green>red+12 and min(blue,green)>70:cyan_free_candidates+=1
    assert dry_boundary_max_depth<=12,(dry_boundary_max_depth,dry_boundary_changes)
    assert cyan_free_candidates==0,cyan_free_candidates
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
water_any_free=sum(a>0 and b>0 for a,b in zip(body.getdata(),free.getdata()))
assert water_any_free==0,water_any_free
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
    'rasterBoundaryTolerancePx':1,
    'bridgeCenterAndEndsAlpha':bridge_alpha,'rejectedOldBendAlpha':at('5,2'),'acceptedNewBendAlpha':at('6,2'),
    'logicalMaskErosionPx':0,'visibleWaterContour':'intrinsically adaptive water with6px dry-edge clearance; separate flat dryshore may extend12px onto ground, core18px protected' if adaptive else ('separate curved artistic channel inside logical zone' if curved else 'full-logical-contour-rejected-by-actual-QA-P1'),
    'actualBodyMask':body_file if curved or adaptive else 'logical-water-mask.png',
    'adaptiveWholeBankProfile':'adaptive-channel-profile.json' if adaptive else None,
    'actualBodyAudit':{'bridgeCenterAndDryEndsAlpha':body_bridge,'waterCellCenterAlpha':body_centers,'bridgeMiddleSharedWaterEdgeAlpha':contacts,'allWaterCellCentersInSameConnectedActualBody':connected_centers,'waterLeakOverAnyFreePixels':water_any_free,'status':'raster-contact-and-connectivity-passed-art-game-review-pending'},
    'bankArtInwardFeatherPx':1 if curved else 3,'entryExitFeather':'disabled within 6px of complete board perimeter',
    'decorativeWater':'outside complete 77-cell union only; separate from logical layer',
    'sourceSha256':{str(p.relative_to(root)):sha(p) for p in [geometry_path,dry_path,continuation_path,banks_path]},
    'outputSha256':{p.name:sha(p) for p in sorted(out.glob('*.png'))},
    'wide':wide_info,
    'checks':{'nativeBankVisualAudit':'pending','entryExitContinuityVisualAudit':'pending','actualGameplay':'not-run'}}
if adaptive:
    report.update({'freeCoreInsetPx':18,'freeCoreChangedRgbPixels':protected_changes,'dryBankBoundaryChangedRgbPixels':dry_boundary_changes,'dryBankBoundaryChangedRgbMaxDepthPx':dry_boundary_max_depth,'allowedDryBankBoundaryDepthPx':12,'sourceCyanCandidateChangedFreePixels':cyan_free_candidates,'cyanDiagnosticRule':'blue>red+12,green>red+12,min(blue,green)>70; diagnostic only, no gameplay terrain inferred from colors','dryShoreSemanticAudit':'pending-flat-earth-and-tiny-pebbles-only-no-water-or-tall-obstacles; not established by pixel counts'})
else:
    report.update({'fullFreePolygonInteriorOpaqueLeakPixels':leaks,'fullFreePolygonInteriorChangedRgbPixels':free_changes})
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
    'visualWaterBodyMask':body_file if curved or adaptive else None,
    'visualWaterBankMask':bank_file if curved or adaptive else None,
    'intrinsicWholeBankProfile':'adaptive-channel-profile.json' if adaptive else None,
    'waterArtOverlay':'logical-water.png','waterArtOverlayRole':'separate painted curved water and banks; legacy filename is not the full logical mask',
    'dryShoreGroundContract':{'allowedFreeBoundaryDepthPx':12,'protectedCoreInsetPx':18,'content':'flat earth/tiny low pebbles only; never water, tall rocks or bushes','roadBridgeOrdering':'ground texture below road and bridge; no foreground cover of deck','freeCoreMask':'free-core-mask18.png'} if adaptive else None,
    'wide':{'file':'wide.webp',**wide_info},'geometry':str(geometry_path.relative_to(root)),
    'checks':'checks.json','status':'root-art-and-actual-game-review-pending'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(report,indent=2))
