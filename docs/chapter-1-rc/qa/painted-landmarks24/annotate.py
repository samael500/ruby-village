"""Render diagnostic overlays from MANUALLY entered semantic coordinates.
Never fits/translates/resizes/rewrites actor RGBA or derives landmarks from bbox.
"""
import json,hashlib,argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
args=argparse.ArgumentParser();args.add_argument('--source-root',default='/home/mskorokhod/life/ruby-village-36-painted-guides');S=Path(args.parse_args().source_root);P=S/'art/painted-ruta-whole24-v1';N=S/'art/painted-ruta-registration24-v1';O=Path(__file__).resolve().parent
# Per row: heelL,toeL,heelR,toeR,estimated ankleL,estimated ankleR,satchel clasp.
# Coordinates manually read from all 24 whole frames and source-labelled grids.
rows=[[(235, 315), (283, 301), (110, 305), (146, 329), [244, 304], [130, 309], [170, 220]],
 [(242, 320), (288, 309), (118, 299), (149, 328), [250, 310], [136, 309], [187, 220]],
 [(228, 325), (277, 318), (117, 296), (146, 327), [236, 314], [133, 309], [187, 220]],
 [(216, 325), (264, 317), (110, 295), (141, 328), [224, 314], [126, 309], [180, 219]],
 [(198, 327), (246, 321), (121, 302), (151, 330), [207, 316], [136, 310], [173, 219]],
 [(189, 326), (237, 320), (140, 301), (172, 329), [198, 315], [155, 310], [181, 222]],
 [(190, 310), (237, 308), (149, 294), (184, 318), [199, 302], [167, 304], [175, 225]],
 [None, None, None, None, None, None, [178, 232]],
 [(146, 310), None, (184, 320), (234, 326), [162, 301], [202, 315], [178, 235]],
 [(135, 304), (178, 311), (211, 316), (258, 314), [153, 302], [222, 309], [173, 232]],
 [(122, 296), (161, 309), (230, 321), (275, 306), [138, 301], [241, 310], None],
 [(115, 287), (150, 309), (242, 321), (287, 303), [131, 294], [253, 309], [184, 227]],
 [(101, 279), (135, 304), (225, 316), (273, 301), [119, 289], [236, 308], [175, 223]],
 [(106, 281), (138, 309), (229, 320), (276, 306), [123, 292], [240, 310], [181, 223]],
 [(107, 278), (136, 307), (213, 319), (261, 307), [124, 289], [224, 309], [190, 223]],
 [(118, 280), (146, 305), (210, 321), (257, 311), [135, 289], [221, 311], None],
 [(120, 285), (153, 310), (193, 327), (240, 320), [138, 292], [204, 317], [167, 224]],
 [(146, 285), (177, 309), (193, 327), (241, 321), [163, 292], [204, 317], [184, 218]],
 [(159, 266), None, (179, 302), (227, 296), [174, 280], [190, 293], [174, 205]],
 [None, (209, 277), (155, 296), (203, 299), [192, 265], [171, 282], [177, 205]],
 [(190, 279), (231, 283), (149, 298), (197, 302), [202, 269], [165, 284], [180, 203]],
 [(213, 287), (258, 283), (135, 297), (179, 301), [224, 271], [151, 285], [180, 201]],
 [(231, 292), (276, 278), (122, 290), (162, 303), [242, 270], [139, 286], [175, 199]],
 [(242, 289), (287, 275), (121, 288), (160, 301), [253, 267], [138, 284], [177, 200]]]
native=json.loads((N/'native-landmarks24.json').read_text());frames=[];hashes={}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10)
colors={'heelL':'#00b85a','toeL':'#00b85a','heelR':'#d42cff','toeR':'#d42cff','estimatedAnkleL':'#1477ff','estimatedAnkleR':'#ff8c00','satchelClaspCenter':'#e32828'}
sheet=Image.new('RGB',(384*6,450*4),'#eee')
for i,points in enumerate(rows):
 f={'index':i,'coordinateSystem':'whole packed frame 384x416; x right, y down; unchanged source pixels','annotator':'independent QA, manual visual semantic annotation','ankleL':None,'ankleR':None,'hip':None,'waistBuckleCenter':None,'heelL':points[0],'toeL':points[1],'heelR':points[2],'toeR':points[3],'estimatedAnkleCenter':{'L':points[4],'R':points[5]},'satchelClaspCenter':points[6],'visibility':{},'uncertaintyPx':{},'notes':[],'nativeSideAssociation':{'sourceFrame':native['frames'][i]['sourceFrame'],'ankleLGuidePx':native['frames'][i]['markers']['ankleL']['guideDeliveryPx'],'ankleRGuidePx':native['frames'][i]['markers']['ankleR']['guideDeliveryPx'],'method':'anatomical side associated by native phase/order plus visible drawn leg continuity, never fixed screen-side'}}
 for k in ['ankleL','ankleR']:f['visibility'][k]='occluded_by_opaque_boot';f['uncertaintyPx'][k]=None
 for k in ['hip','waistBuckleCenter']:f['visibility'][k]='not_unambiguously_visible';f['uncertaintyPx'][k]=None
 for k in ['heelL','toeL','heelR','toeR']:
  f['visibility'][k]='visible_drawn_contour'if f[k]else'occluded_or_anatomical_association_ambiguous';f['uncertaintyPx'][k]=3 if f[k]else None
 for side in ['L','R']:
  k='estimatedAnkle'+side;f['visibility'][k]='estimated_center_from_visible_boot_bend_NOT_visible_joint'if f['estimatedAnkleCenter'][side]else'not_estimated_due_to_overlap';f['uncertaintyPx'][k]=(10 if i in [6,8,18,19]else 8)if f['estimatedAnkleCenter'][side]else None
 f['visibility']['satchelClaspCenter']='visible_satchel_flap_hardware_NOT_waist_buckle'if f['satchelClaspCenter']else'hand_occlusion_or_unclear';f['uncertaintyPx']['satchelClaspCenter']=3 if f['satchelClaspCenter']else None
 if i==7:f['notes'].append('Crossing boots: native ankles nearly overlap in x/y and painted anatomy cannot be assigned confidently; bilateral contour/joint-proxy points left null rather than swapping guessed L/R.')
 if i in [8,18]:f['notes'].append('Back/left toe contour occluded at front boot overlap; toeL remains null.')
 if i==19:f['notes'].append('Raised L toe identifiable above front R boot; L heel hidden behind front leg. L estimated center is broad visual inference only, 10px uncertainty.')
 f['notes'].append('Physical ankle bone heads hidden; estimatedAnkleCenter is an artist proxy inside opaque boot, not a physical joint measurement. Heel/toe are 2D profile landmarks, not native sole-region mean vertices.')
 path=P/f'frame-{i:02}.png';hashes[str(path.relative_to(S))]=hashlib.sha256(path.read_bytes()).hexdigest();im=Image.open(path).convert('RGBA');canvas=Image.new('RGB',im.size,'#eee');canvas.paste(im,mask=im.getchannel('A'));d=ImageDraw.Draw(canvas)
 for k,p in zip(['heelL','toeL','heelR','toeR','estimatedAnkleL','estimatedAnkleR','satchelClaspCenter'],points):
  if p is None:continue
  x,y=p;c=colors[k];rad=f['uncertaintyPx'][k];d.ellipse((x-rad,y-rad,x+rad,y+rad),outline=c,width=1);d.line((x-3,y,x+3,y),fill=c,width=1);d.line((x,y-3,x,y+3),fill=c,width=1);d.text((x+4,y-13),k.replace('estimatedAnkle','eA'),font=font,fill=c,stroke_width=1,stroke_fill='white')
 d.text((4,4),f'{i:02}: contours / estimated centers, NOT bones',font=font,fill='black');canvas.save(O/f'overlay-{i:02}.png');panel=Image.new('RGB',(384,450),'white');panel.paste(canvas,(0,0));pd=ImageDraw.Draw(panel);pd.text((4,419),'Green=L / magenta=R contour; blue/orange=ESTIMATE',font=font,fill='black');pd.text((4,434),'Ankle/hip/waist buckle physical points: null',font=font,fill='black');sheet.paste(panel,(i%6*384,i//6*450));frames.append(f)
hashes['art/painted-ruta-whole24-v1/packing.json']=hashlib.sha256((P/'packing.json').read_bytes()).hexdigest()
for name in ['native-landmarks24.json','manual-painted-landmarks-template.json','scale-study.json']:p=N/name;hashes[str(p.relative_to(S))]=hashlib.sha256(p.read_bytes()).hexdigest()
metadata={'status':'manual_semantic_annotation_NOT_physical_joint_registration_NOT_art_acceptance','sourceFrameSize':[384,416],'oneGlobalScaleInitializationOnly':json.loads((N/'scale-study.json').read_text())['proposedGlobalArtSourcePxToGuideDeliveryPx'],'scaleApplied':False,'perFrameResizeOrWarp':False,'coordinateSource':'manual inspection of whole frames and coordinate-labelled grids; no bbox-extremum or auto-fit landmarks','definitions':{'ankleL/ankleR':'physical joint center: occluded -> null in all24','estimatedAnkleCenter':'manual visual guess of internal ankle center from boot bend; separate from physical ankle, 8-10px uncertainty','heelL/heelR':'visible rear-most heel/outsole profile midpoint of drawn boot, not native mean vertex landmark or inferred floor contact','toeL/toeR':'visible frontmost toe profile midpoint on drawn boot; not bbox bottom, physical contact or native vertex-mean counterpart','satchelClaspCenter':'center of visible large gold flap clasp on satchel; NOT waist belt buckle or Hips joint','waistBuckleCenter':'null: waist-belt hardware cannot be identified independently of satchel/strap fittings','uncertaintyPx':'manual radial visual uncertainty estimate in original art pixels; not statistical confidence or measured residual'},'sourceHashes':hashes,'frames':frames}
(O/'manual-painted-landmarks24.json').write_text(json.dumps(metadata,indent=2)+'\n');sheet.save(O/'overlays24-sheet.png')
# Ensure diagnostic work never changes a source frame.
assert all(hashlib.sha256((S/p).read_bytes()).hexdigest()==v for p,v in hashes.items())
print('MANUAL frames',len(frames),'source hashes preserved',len(hashes))
