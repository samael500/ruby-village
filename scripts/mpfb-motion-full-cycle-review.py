"""Incremental actual loop reviews/skin-contact receipts. No pose synthesis."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,math,itertools,os
ROOT=Path(__file__).resolve().parents[1];motion_root=ROOT/'art/characters-mpfb-v1/motion';OUT=(motion_root/os.environ.get('RUBY_MPFB_OUTPUT_NAMESPACE','full-cycle-technical')).resolve();assert OUT.is_relative_to(motion_root.resolve());REPORT=OUT/'author-loop-check.json';old=json.loads(REPORT.read_text())if REPORT.exists()else{};results={};loops={}
def distance(a,b):return math.sqrt(sum((x-y)**2 for x,y in zip(a,b)))
def max_pair(points):return max((distance(a,b)for a in points for b in points),default=0)
def alpha_components(alpha):
 foreground={i for i,value in enumerate(alpha.tobytes())if value>16};sizes=[]
 while foreground:
  stack=[foreground.pop()];count=0
  while stack:
   point=stack.pop();count+=1;x,y=point%384,point//384
   for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
    nx,ny=x+dx,y+dy;neighbor=ny*384+nx
    if 0<=nx<384 and 0<=ny<384 and neighbor in foreground:foreground.remove(neighbor);stack.append(neighbor)
  if count>=4:sizes.append(count)
 return sorted(sizes,reverse=True)
def tile(im,label,phase):
 canvas=Image.new('RGB',(208,256),'#dedcd4');d=ImageDraw.Draw(canvas);d.text((5,4),'TECHNICAL / APPEARANCE REJECTED',fill='#713b32');d.text((5,19),label,fill='#292d2d');d.text((5,34),f'720ms / actual phase {phase:.3f}',fill='#292d2d');small=im.resize((208,208),Image.Resampling.LANCZOS);canvas.paste(small,(0,48),small);return canvas
for path in sorted(OUT.glob('*/*/receipt.json')):
 receipt=json.loads(path.read_text());key=f'{receipt["cameraVariant"]}/{receipt["direction"]}'
 if not receipt['complete']:continue
 records=[];images=[]
 for frame in receipt['frames']:
  p=path.parent/f'{frame["frame"]:02}.png';assert hashlib.sha256(p.read_bytes()).hexdigest()==frame['sha256'];im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox();assert im.size==(384,384)and box and min(box[:2])>1 and max(box[2:])<383;records.append({'frame':frame['frame'],'sha256':frame['sha256'],'alphaBounds':box,'alphaComponentsAtThreshold16Min4Pixels':alpha_components(im.getchannel('A')),'rootGroundAnchorPixels':frame['rootGroundAnchorPixels']});images.append(im)
 assert len(records)==24;assert len({r['sha256']for r in records})==24;assert len({r['evaluatedNativeBoneMatrixHash']for r in receipt['frames']})==24
 footchecks={}
 for side in ['L','R']:
  flats=[f['feet'][side]for f in receipt['frames']if .1<=f['feet'][side]['phase']<=.46];toes=[f['feet'][side]for f in receipt['frames']if .48<f['feet'][side]['phase']<.6]
  footchecks[side]={'flatWorldSoleDriftMeters':{kind:max_pair([f['sourceSole'][kind]['centerWorldMeters']for f in flats])for kind in ['toe','heel']},'toePushOffWorldDriftMeters':max_pair([f['sourceSole']['toe']['centerWorldMeters']for f in toes])}
 assert max(v for f in footchecks.values()for v in f['flatWorldSoleDriftMeters'].values())<.0001
 assert min(f['minFullRenderLevelBootZ']for f in receipt['frames'])>0
 review=[tile(im,f'{key} / frame {i+1:02}',i/24)for i,im in enumerate(images)];review[0].save(path.parent/'actual-cycle.gif',save_all=True,append_images=review[1:],duration=30,loop=0,optimize=False);loops[key]=review
 results[key]={'sourceSha256':receipt['sourceSha256'],'actualFrameCount':24,'distinctRasterFrames':24,'distinctEvaluatedNativePoses':24,'allContained':True,'maxGroundRootAnchorDistancePixels':max_pair([f['rootGroundAnchorPixels']for f in receipt['frames']]),'minActualRenderLevelBootZ':min(f['minFullRenderLevelBootZ']for f in receipt['frames']),'actualSourceSkinContacts':footchecks,'maxProjectedDirectionErrorRadians':max(abs(f['projectedAngleErrorRadians'])for f in receipt['frames']),'framesWithSecondaryAlphaComponents':sum(len(r['alphaComponentsAtThreshold16Min4Pixels'])>1 for r in records),'reusedCompactProofFrames':sum(f['rasterOrigin'].startswith('byte-identical')for f in receipt['frames']),'records':records}
for group in ['base','calibrated-1']:
 order_group=[f'{group}/{direction}'for direction in ['e','se','sw','w','nw','ne']]
 if all(key in loops for key in order_group):
  strip=Image.new('RGB',(6*208,6*256),'#dedcd4')
  for row,frame in enumerate([0,4,8,12,16,20]):
   for column,key in enumerate(order_group):strip.paste(loops[key][frame],(column*208,row*256))
  strip.save(OUT/group/'actual-six-view-strip.jpg',quality=94)
report={'status':'AUTHOR INCREMENTAL ACTUAL LOOP/GEOMETRY CHECK; INDEPENDENT FULL REVIEW PENDING','completedViewCount':len(results),'actualFrameCount':24*len(results),'authorizedBudget':288,'transitionRasterCount':0,'appearance':'rejected generic engineering mannequin; not final Ruta/game art','frameDurationMs':30,'loopDurationMs':720,'calibration':'one shared native384/ortho1.70 /251reference→136 scene px; no per-direction fit','views':results}
report['nativeAuthoredCyclePoses']=24
report['maxAllGroundRootAnchorDistancePixels']=max_pair([r['rootGroundAnchorPixels']for view in results.values()for r in view['records']])
report['globalDistinctRasterFrameCount']=len({r['sha256']for view in results.values()for r in view['records']})
REPORT.write_text(json.dumps(report,indent=2)+'\n')
if len(results)==12:
 order=[f'{g}/{d}'for g in ['base','calibrated-1']for d in ['e','se','sw','w','nw','ne']];combined=[]
 for frame in range(24):
  sheet=Image.new('RGB',(6*208,2*256+28),'#dedcd4');ImageDraw.Draw(sheet).text((8,8),'ACTUAL 12-VIEW WALK LOOPS / TECHNICAL ONLY / APPEARANCE REJECTED',fill='#713b32')
  for i,key in enumerate(order):sheet.paste(loops[key][frame],((i%6)*208,28+(i//6)*256))
  combined.append(sheet)
 combined[0].save(OUT/'actual-twelve-view-cycles.gif',save_all=True,append_images=combined[1:],duration=30,loop=0,optimize=False)
 combined[0].save(OUT/'actual-twelve-view-phase0.jpg',quality=94)
 links=''.join(f'<li><a href="{key}/actual-cycle.gif">{key}: actual720ms loop</a></li>'for key in order)
 (OUT/'review.html').write_text('<!doctype html><meta charset="utf-8"><title>MPFB technical native walk review</title><style>body{max-width:1280px;margin:24px auto;background:#dedcd4;color:#292d2d;font:16px system-ui}img{width:100%;height:auto}strong{color:#713b32}</style><h1>Actual twelve-view native walk loops</h1><p><strong>TECHNICAL ONLY — GENERIC APPEARANCE REJECTED. NOT FINAL GAME ART.</strong></p><p>24 genuine rendered poses /720ms, base and tilted calibrations, fixed native scale/ground-root anchor. This is a review artifact; no route adapter or game activation.</p><img src="actual-twelve-view-cycles.gif" alt="Twelve genuine native walking loops on one720ms clock"><ul>'+links+'</ul><p><a href="manifest.json">Source/camera manifest</a> · <a href="author-loop-check.json">Actual geometry/frame checks</a> · <a href="adapter-input-contract.json">Native adapter inputs, route adapter pending</a></p>')
 print('AUTHOR_FULL_LOOP_CHECK 12 views / 288 actual frames / 24 reused / no transitions')
else:print('AUTHOR_INCREMENTAL_LOOP_CHECK',len(results),'complete views')
