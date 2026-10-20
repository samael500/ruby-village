from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
O=Path(__file__).resolve().parent;proof=json.load(open(O/'render-proof.json'));images=[Image.open(O/('e-'+n+'32.png')).convert('RGBA')for n in ['baseline','candidate']];arrays=[np.array(i)for i in images];bounds=proof['views'][0]['eyeGlobeProjectedBounds'];xmin=max(0,math.floor(min(x['boundsPx'][0][0]for x in bounds)));ymin=max(0,math.floor(min(x['boundsPx'][0][1]for x in bounds)));xmax=min(512,math.ceil(max(x['boundsPx'][1][0]for x in bounds)));ymax=min(640,math.ceil(max(x['boundsPx'][1][1]for x in bounds)));rows=[]
for name,a in zip(['baseline','candidate'],arrays):
 rgba=a[ymin:ymax,xmin:xmax].astype(int);mask=(rgba[:,:,2]>rgba[:,:,0]+25)&(rgba[:,:,2]>rgba[:,:,1]+10)&(rgba[:,:,2]>70)&(rgba[:,:,3]>128);rows.append({'state':name,'blueRGBThresholdPixelCountWithinFixedEyeGeometryROI':int(mask.sum()),'alpha128ActorBBox':Image.fromarray((a[:,:,3]>128).astype('uint8')*255).getbbox()})
sheet=Image.new('RGBA',(1024,680),(233,227,212,255));d=ImageDraw.Draw(sheet)
for j,im in enumerate(images):sheet.alpha_composite(im,(512*j,40));d.text((512*j+12,12),'Tone+expression SAME32AA: '+('baseline'if j==0 else'clearance, CONTACTRISKOPEN'),fill=(25,20,15))
sheet.convert('RGB').save(O/'e-before-after.jpg',quality=95);box=(250,175,335,280);close=Image.new('RGBA',(680,460),(233,227,212,255));d=ImageDraw.Draw(close)
for j,im in enumerate(images):close.alpha_composite(im.crop(box).resize((340,420),Image.Resampling.NEAREST),(340*j,40));d.text((340*j+8,12),'baseline'if j==0 else'candidate',fill=(25,20,15))
close.convert('RGB').save(O/'e-face-common-crop.jpg',quality=95);r={'actualFixedGeometryEyeROI':[xmin,ymin,xmax,ymax],'blueProxyDefinition':'B>R+25 andB>G+10 andB>70 alpha>128 insideunchangedprojectedglobeROI; notsemanticiris/faceacceptance','rows':rows,'commonFaceEvidenceCrop':box,'noPixelRegistration':True,'geometryRisk':'RESThead/ear-side contacts increased, candidateNOTselected'};(O/'blue-eye-visibility-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
