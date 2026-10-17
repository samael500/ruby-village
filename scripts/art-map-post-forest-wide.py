"""Join painted wide ring to native core through a protected outer foliage band."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter,ImageChops
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1];E=R/'docs/chapter-1-rc/art/map-match-post-forest'
for name in ['post','forest']:
 A=R/'art/chapter-1-map-match'/name;D=R/'public/assets/chapter-1-map-match'/name;raw=Image.open(A/'generated-wide-01.png').convert('RGB');ring=raw.resize((3272,1200),Image.Resampling.LANCZOS);before=A/'core-before-wide-join.png'
 if not before.exists():shutil.copy(A/'core-candidate.png',before)
 core=Image.open(before).convert('RGB');mask=Image.new('L',core.size);draw=ImageDraw.Draw(mask)
 for margin in range(73):
  t=max(0,(72-margin)/72);value=round(255*t*t*(3-2*t));draw.rectangle((margin,margin,1671-margin,940-margin),fill=value)
 free=Image.open(A/'full-free-polygons.png');mask=ImageChops.multiply(mask,ImageChops.invert(free.filter(ImageFilter.MaxFilter(7))));joined=Image.composite(ring.crop((800,129,2472,1070)),core,mask);assert ImageChops.multiply(ImageChops.difference(joined,core).convert('L'),free).getbbox()is None
 joined.save(A/'core-candidate.png');joined.save(D/'background.webp','WEBP',lossless=True,method=6);ring.paste(joined,(800,129));ring.save(A/'wide-candidate.png');ring.save(D/'wide.webp','WEBP',lossless=True,method=6);mask.save(A/'wide-core-join-mask.png');assert ring.crop((800,129,2472,1070)).tobytes()==joined.tobytes();assert Image.open(D/'wide.webp').crop((800,129,2472,1070)).convert('RGB').tobytes()==Image.open(D/'background.webp').convert('RGB').tobytes()
 m=json.loads((D/'manifest.json').read_text());m['wide']={'file':f'assets/chapter-1-map-match/{name}/wide.webp','canvas':{'width':3272,'height':1200},'originalRect':{'x':800,'y':129,'width':1672,'height':941},'source':str((A/'generated-wide-01.png').relative_to(R)),'sourceSize':list(raw.size),'sourceSha256':hashlib.sha256((A/'generated-wide-01.png').read_bytes()).hexdigest(),'registration':'painted v8 ring reference at logical canvas, builtin seam repaint, protected72px foliage join inside core perimeter','corePixelExact':True,'opaque':True};m['registration']['wideCorePerimeterJoinPixels']=72;m['checks']['wideNativeCoreExact']=True;m['checks']['fullFreePolygonPixelsChanged']=0
 if name=='forest':m['recommendedWholeSceneGrade']={'status':'candidate-requires-artistic-review','scope':'background,wide,characters,road,scene-props together; excludes HUD','type':'svg-feColorMatrix','colorInterpolationFilters':'sRGB','values':[.76,0,0,0,.018,0,.78,0,0,.026,0,0,.86,0,.065,0,0,0,1,0],'note':'Apply once to scene group. Deliveries remain ungraded to avoid grading actors differently.'}
 (D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('Wide/core exact; full free polygon pixels unchanged;72px outer foliage join only')
