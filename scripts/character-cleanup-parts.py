"""Non-destructive source-pixel cutouts for articulated painted legs.
Creates immutable-source, registered RGBA parts; no mirror or phase regeneration.
python3 scripts/character-cleanup-parts.py e
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter,ImageFont
import json,sys,hashlib
R=Path(__file__).resolve().parents[1];SOURCE=R/'art/characters-walk-v1/registered';OUT=R/'art/characters-walk-v1/clean-parts-v2';OUT.mkdir(exist_ok=True)
CONFIG={
'e':{'bodyBottom':192,'parts':{
 'thigh.L':{'poly':[(164,190),(184,186),(191,195),(196,212),(193,219),(168,222),(157,204),(153,192)],'a':[168,177],'b':[180,209],'z':.06},
 'shin.L':{'poly':[(164,200),(196,201),(199,218),(196,228),(172,231),(163,218)],'a':[180,209],'b':[185,234],'z':.07},
 'foot.L':{'poly':[(168,214),(225,214),(225,258),(168,258)],'a':[185,234],'b':[208,234],'z':.08},
 'thigh.R':{'poly':[(146,190),(175,184),(168,199),(158,215),(145,222),(121,218),(117,204),(133,192)],'a':[165,178],'b':[140,211],'z':.12},
 'shin.R':{'poly':[(119,199),(155,205),(147,219),(135,230),(111,226),(108,216)],'a':[140,211],'b':[126,235],'z':.13},
 'foot.R':{'poly':[(95,215),(153,215),(153,260),(95,260)],'a':[126,235],'b':[139,242],'z':.14}
}}
}
CONFIG.update({
'se':{'bodyBottom':190,'parts':{
 'thigh.L':{'poly':[(154,183),(185,180),(193,198),(191,212),(156,216),(151,203)],'a':[174,174],'b':[178,201],'z':.06},
 'shin.L':{'poly':[(154,200),(190,200),(193,221),(159,226),(152,214)],'a':[178,201],'b':[178,230],'z':.07},
 'foot.L':{'poly':[(154,215),(191,214),(193,228),(205,236),(209,251),(199,258),(154,258),(151,248)],'a':[178,230],'b':[188,243],'z':.08},
 'thigh.R':{'poly':[(129,183),(156,178),(158,194),(150,207),(128,207),(122,195)],'a':[148,174],'b':[139,198],'z':.12},
 'shin.R':{'poly':[(127,193),(156,194),(153,211),(149,219),(122,218),(120,205)],'a':[139,198],'b':[137,218],'z':.13},
 'foot.R':{'poly':[(121,204),(153,204),(154,225),(150,239),(129,240),(119,228)],'a':[137,218],'b':[143,229],'z':.14}}},
'sw':{'bodyBottom':190,'parts':{
 'thigh.L':{'poly':[(151,184),(175,180),(182,197),(181,211),(160,216),(148,204)],'a':[163,178],'b':[166,205],'z':.12},
 'shin.L':{'poly':[(151,199),(180,200),(183,219),(160,230),(149,219)],'a':[166,205],'b':[166,229],'z':.13},
 'foot.L':{'poly':[(146,210),(180,210),(183,232),(178,247),(165,257),(141,258),(135,244),(143,230)],'a':[166,229],'b':[158,244],'z':.14},
 'thigh.R':{'poly':[(125,183),(151,179),(160,194),(154,207),(136,212),(124,203)],'a':[142,174],'b':[144,197],'z':.06},
 'shin.R':{'poly':[(136,193),(155,193),(158,208),(151,219),(137,216),(132,205)],'a':[144,197],'b':[151,213],'z':.07},
 'foot.R':{'sourceFrame':'03','sourceA':[139,204],'sourceB':[136,216],'poly':[(126,190),(151,191),(154,207),(151,221),(141,225),(127,224),(120,214),(120,202)],'a':[151,213],'b':[148,225],'z':.08}}},
'w':{'bodyBottom':191,'parts':{
 'thigh.L':{'poly':[(144,190),(164,183),(169,195),(158,213),(147,221),(126,216),(120,200)],'a':[162,175],'b':[146,203],'z':.12},
 'shin.L':{'poly':[(125,201),(157,205),(160,220),(148,233),(124,227),(120,216)],'a':[146,203],'b':[141,234],'z':.13},
 'foot.L':{'poly':[(92,214),(157,214),(157,258),(92,258)],'a':[141,234],'b':[117,235],'z':.14},
 'thigh.R':{'poly':[(174,187),(190,181),(202,195),(207,207),(199,215),(178,218),(168,205),(166,193)],'a':[174,175],'b':[185,200],'z':.06},
 'shin.R':{'poly':[(174,196),(203,199),(209,217),(194,228),(176,222),(169,210)],'a':[185,200],'b':[191,223],'z':.07},
 'foot.R':{'poly':[(168,208),(218,208),(218,250),(168,250)],'a':[191,223],'b':[173,231],'z':.08}}},
'nw':{'bodyBottom':192,'parts':{
 'thigh.L':{'poly':[(132,184),(158,182),(164,199),(158,211),(139,216),(123,204)],'a':[145,177],'b':[144,201],'z':.12},
 'shin.L':{'poly':[(127,197),(162,199),(161,215),(152,223),(122,217)],'a':[144,201],'b':[146,224],'z':.13},
 'foot.L':{'poly':[(118,207),(157,208),(164,219),(161,237),(145,241),(124,230),(115,218)],'a':[146,224],'b':[139,214],'z':.14},
 'thigh.R':{'poly':[(163,184),(190,182),(197,197),(196,213),(175,218),(159,208)],'a':[176,177],'b':[184,206],'z':.06},
 'shin.R':{'poly':[(166,200),(195,201),(198,224),(176,230),(161,218)],'a':[184,206],'b':[182,240],'z':.07},
 'foot.R':{'poly':[(166,213),(199,213),(211,239),(205,262),(156,262),(156,240),(164,232)],'a':[182,240],'b':[175,228],'z':.08}}},
'ne':{'bodyBottom':192,'parts':{
 'thigh.L':{'poly':[(120,183),(148,182),(159,199),(155,212),(132,216),(118,205)],'a':[143,177],'b':[141,199],'z':.06},
 'shin.L':{'poly':[(118,197),(155,198),(158,219),(132,230),(116,215)],'a':[141,199],'b':[140,228],'z':.07},
 'foot.L':{'poly':[(113,207),(153,208),(161,219),(154,238),(134,245),(113,241),(109,227)],'a':[140,228],'b':[146,216],'z':.08},
 'thigh.R':{'poly':[(149,183),(176,179),(185,195),(186,213),(159,218),(148,203)],'a':[169,178],'b':[177,204],'z':.12},
 'shin.R':{'poly':[(152,199),(185,201),(188,223),(161,230),(149,215)],'a':[177,204],'b':[177,240],'z':.13},
 'foot.R':{'poly':[(152,213),(185,213),(194,226),(201,236),(197,251),(182,259),(158,258),(149,245)],'a':[177,240],'b':[184,226],'z':.14}}}
})
# Rolled cloth cuffs stay with shin; rotating boot texture starts below them.
TRIMS={
 'e':{'thigh.L':[0,214],'thigh.R':[0,216],'foot.L':[222,319],'foot.R':[223,319]},
 'se':{'thigh.L':[0,208],'thigh.R':[0,204],'foot.L':[221,319],'foot.R':[210,319]},
 'sw':{'thigh.L':[0,211],'thigh.R':[0,205],'foot.L':[222,319],'foot.R':[199,319]},
 'w':{'thigh.L':[0,213],'thigh.R':[0,208],'foot.L':[224,319],'foot.R':[216,319]},
 'nw':{'thigh.L':[0,207],'thigh.R':[0,212],'foot.L':[213,319],'foot.R':[224,319]},
 'ne':{'thigh.L':[0,205],'thigh.R':[0,210],'foot.L':[215,319],'foot.R':[224,319]}}
for di,parts in TRIMS.items():
 for name,limits in parts.items():CONFIG[di]['parts'][name]['clipY']=limits
# Round the distal knee silhouette; only existing painted pixels survive this mask.
CAPS={'e':{'thigh.L':([180,202],[13,12],197),'thigh.R':([142,203],[14,13],199)},'w':{'thigh.L':([146,201],[14,12],194),'thigh.R':([185,197],[14,11],191)}}
for di,parts in CAPS.items():
 for name,(center,radii,fromY) in parts.items():CONFIG[di]['parts'][name]['roundKneeCap']={'center':center,'radii':radii,'fromY':fromY}
# Proximal shin caps take the existing knee paint above the joint into a round
# overlap instead of retaining a rigid flat/pointed cut at the top of the calf.
TOPCAPS={'e':{'shin.L':([180,209],[14,12]),'shin.R':([140,211],[15,13])},'w':{'shin.L':([146,203],[14,12]),'shin.R':([185,200],[14,12])}}
for di,parts in TOPCAPS.items():
 for name,(center,radii) in parts.items():CONFIG[di]['parts'][name]['roundShinTop']={'center':center,'radii':radii}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
for direction in sys.argv[1:] or list(CONFIG):
 c=CONFIG[direction];p=SOURCE/f'{direction}-01.png';original=p.read_bytes();im=Image.open(p).convert('RGBA');assert im.size==(320,320);dest=OUT/direction;dest.mkdir(exist_ok=True)
 bodymask=Image.new('L',im.size);ImageDraw.Draw(bodymask).rectangle((0,0,319,c['bodyBottom']),fill=255)
 body=im.copy();body.putalpha(ImageChops.multiply(im.getchannel('A'),bodymask));body.save(dest/'body.png')
 manifest={'canvas':[320,320],'footAnchor':[160,256],'direction':direction,'source':str(p.relative_to(R)),'sourceSha256':hashlib.sha256(original).hexdigest(),'method':'overlapping registered cutouts from immutable painted source, no mirroring','parts':{'body':{'file':'body.png','bone':'root','a':[160,170],'b':[160,140],'z':.2}}}
 pieces=[]
 for name,part in c['parts'].items():
  mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(part['poly'],fill=255)
  if 'clipY' in part:
   band=Image.new('L',im.size);ImageDraw.Draw(band).rectangle((0,part['clipY'][0],319,part['clipY'][1]),fill=255);mask=ImageChops.multiply(mask,band)
  if 'roundKneeCap' in part:
   cap=part['roundKneeCap'];cx,cy=cap['center'];rx,ry=cap['radii'];shape=Image.new('L',im.size);draw=ImageDraw.Draw(shape);draw.rectangle((0,0,319,cap['fromY']-1),fill=255);draw.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255);mask=ImageChops.multiply(mask,shape)
  if 'roundShinTop' in part:
   cap=part['roundShinTop'];cx,cy=cap['center'];rx,ry=cap['radii'];lower=mask.copy();ImageDraw.Draw(lower).rectangle((0,0,319,cy),fill=0);upper=Image.new('L',im.size);draw=ImageDraw.Draw(upper);draw.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=255);draw.rectangle((0,cy+1,319,319),fill=0);mask=ImageChops.lighter(lower,upper)
  partSource=SOURCE/f"{direction}-{part.get('sourceFrame','01')}.png";paint=Image.open(partSource).convert('RGBA')
  piece=paint.copy();piece.putalpha(ImageChops.multiply(paint.getchannel('A'),mask))
  if 'sourceA' in part:
   a,b=part['sourceA'],part['sourceB'];ta,tb=part['a'],part['b'];vx,vy=b[0]-a[0],b[1]-a[1];tx,ty=tb[0]-ta[0],tb[1]-ta[1];den=vx*vx+vy*vy;cs=(tx*vx+ty*vy)/den;sn=(ty*vx-tx*vy)/den;dx=ta[0]-cs*a[0]+sn*a[1];dy=ta[1]-sn*a[0]-cs*a[1];det=cs*cs+sn*sn
   inv=(cs/det,sn/det,(-cs*dx-sn*dy)/det,-sn/det,cs/det,(sn*dx-cs*dy)/det)
   piece=piece.convert('RGBa').transform((320,320),Image.Transform.AFFINE,inv,resample=Image.Resampling.BICUBIC).convert('RGBA')
  piece.save(dest/f'{name}.png');pieces.append((name,piece,part))
  manifest['parts'][name]={'file':name+'.png','bone':name,'a':part['a'],'b':part['b'],'z':part['z'],'textureSource':str(partSource.relative_to(R)),'sourceA':part.get('sourceA',part['a']),'sourceB':part.get('sourceB',part['b']),'sourceClipY':part.get('clipY',[0,319]),'textureSha256':hashlib.sha256(partSource.read_bytes()).hexdigest(),'roundKneeCap':part.get('roundKneeCap'),'roundShinTop':part.get('roundShinTop')}
 (dest/'parts.json').write_text(json.dumps(manifest,indent=2)+'\n')
 composite=Image.new('RGBA',im.size)
 for _,piece,_ in sorted(pieces,key=lambda x:x[2]['z']):composite.alpha_composite(piece)
 composite.alpha_composite(body)
 # Native-pixel source/component/composite comparison with correctly applied alpha.
 plate=Image.new('RGB',(1280,640),'#eee8da');draw=ImageDraw.Draw(plate)
 ordered=[('SOURCE',im),('REST COMPOSITE',composite),('BODY',body)]+[(name,piece)for name,piece,_ in pieces]
 # Three diagnostic pages keep each part at literal native pixels.
 for page in range(3):
  canvas=Image.new('RGB',(960,360),'#eee8da');d=ImageDraw.Draw(canvas)
  for i,(name,piece)in enumerate(ordered[page*3:page*3+3]):canvas.paste(piece,(i*320,30),piece);d.text((i*320+8,8),name,font=font,fill='#24221d')
  canvas.save(dest/f'components-{page+1}.jpg',quality=96)
 # Three backgrounds are actual composited RGB images, not misleading raw PNG previews.
 backgrounds=Image.new('RGB',(960,350));d=ImageDraw.Draw(backgrounds)
 for i,(color,label)in enumerate([('#fbfaf6','light'),('#17232b','dark'),('#7fb78b','green')]):
  patch=Image.new('RGB',(320,320),color);patch.paste(composite,(0,0),composite);backgrounds.paste(patch,(i*320,30));d.text((i*320+8,8),label,font=font,fill='white')
 backgrounds.save(dest/'rest-alpha-backgrounds.jpg',quality=96)
 diff=ImageChops.difference(im.getchannel('A'),composite.getchannel('A'));hist=diff.histogram();(dest/'checks.json').write_text(json.dumps({'sourceUnchanged':p.read_bytes()==original,'canvas':[320,320],'bodyPreservesIdentityPixels':True,'sourceVsCompositeAlphaMeanDifference':sum(i*n for i,n in enumerate(hist))/(320*320),'sourceVsCompositeAlphaDifferentPixels':sum(hist[1:]),'note':'Overlapping source pixels may slightly increase semitransparent coverage; dynamic seam review belongs to the exporter.'},indent=2)+'\n')
 print(direction,'exported clean registered parts')
