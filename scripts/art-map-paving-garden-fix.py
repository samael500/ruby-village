"""Painted narrow garden approach repair in paired neutral/charoite source states."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[1];A=R/'art/chapter-map-v2';D=R/'public/assets/chapter-map-v2';E=R/'docs/chapter-1-rc/art/map-paving';sheet=Image.open(A/'generated-garden-two-states-05.png').convert('RGB').resize((1000,800),Image.Resampling.LANCZOS);gray=sheet.crop((0,0,1000,400));base=Image.open(A/'map-base-candidate.png').convert('RGB');base.save(A/'map-base-before-garden-fix.png');color=Image.new('L',base.size);pix=gray.load();dst=color.load()
for y in range(142,175):
 for x in range(368,412):
  r,g,b=pix[x,y]
  if r>115 and g>100 and b>65 and r>g*1.015 and b>g*.53:dst[x,y]=255
mask=color.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(.6));clip=Image.new('L',base.size);ImageDraw.Draw(clip).rectangle((368,142,411,174),fill=255);mask=ImageChops.multiply(mask,clip);protect=Image.open(A/'protected-landmarks.png');mask=ImageChops.multiply(mask,ImageChops.invert(protect));corridor=Image.open(A/'allowed-corridor-mask.png');mask=ImageChops.multiply(mask,corridor);fixed=Image.composite(gray,base,mask);assert ImageChops.multiply(ImageChops.difference(fixed,base).convert('L'),protect).getbbox()is None;fixed.save(A/'map-base-candidate.png');fixed.save(D/'map-base.webp','WEBP',lossless=True,method=6);mask.save(A/'garden-fix-paint-mask.png');pave=Image.open(A/'painted-paving-and-grass-mask.png');ImageChops.lighter(pave,mask).save(A/'painted-paving-and-grass-mask.png');m=json.loads((D/'manifest.json').read_text());m['gardenApproachRepair']={'source':'art/chapter-map-v2/generated-garden-two-states-05.png','sourceSha256':hashlib.sha256((A/'generated-garden-two-states-05.png').read_bytes()).hexdigest(),'editBounds':[368,142,411,174],'protectedLandmarkPixelsChanged':0,'endpointsChanged':0};(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');out=Image.new('RGB',(880,640),'#e7d5b5');d=ImageDraw.Draw(out)
for i,(im,label)in enumerate([(base,'Before: flower gap'),(fixed,'After: continuous flagstones between flowering edges')]):
 crop=im.crop((355,125,425,175)).resize((840,280));out.paste(crop,(20,i*320+28));d.text((20,i*320+8),label,fill='black')
out.save(E/'garden-approach-before-after.jpg',quality=95)
