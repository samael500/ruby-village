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
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
for direction in sys.argv[1:] or list(CONFIG):
 c=CONFIG[direction];p=SOURCE/f'{direction}-01.png';original=p.read_bytes();im=Image.open(p).convert('RGBA');assert im.size==(320,320);dest=OUT/direction;dest.mkdir(exist_ok=True)
 bodymask=Image.new('L',im.size);ImageDraw.Draw(bodymask).rectangle((0,0,319,c['bodyBottom']),fill=255)
 body=im.copy();body.putalpha(ImageChops.multiply(im.getchannel('A'),bodymask));body.save(dest/'body.png')
 manifest={'canvas':[320,320],'footAnchor':[160,256],'direction':direction,'source':str(p.relative_to(R)),'sourceSha256':hashlib.sha256(original).hexdigest(),'method':'overlapping registered cutouts from immutable painted source, no mirroring','parts':{'body':{'file':'body.png','bone':'root','a':[160,170],'b':[160,140],'z':.2}}}
 pieces=[]
 for name,part in c['parts'].items():
  mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon(part['poly'],fill=255)
  piece=im.copy();piece.putalpha(ImageChops.multiply(im.getchannel('A'),mask));piece.save(dest/f'{name}.png');pieces.append((name,piece,part))
  manifest['parts'][name]={'file':name+'.png','bone':name,'a':part['a'],'b':part['b'],'z':part['z']}
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
