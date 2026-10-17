import json,math
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
root=Path(__file__).resolve().parents[2]; j=json.loads((root/'src/chapter-1.legacy.json').read_text()); actors=json.loads((root/'docs/chapter-1-rc/art/coordinator-review/resident-composites/anchors.json').read_text())['actors']; residents=json.loads((root/'public/assets/characters-v1/residents-manifest.json').read_text())['characters']; delivery=json.loads((root/'public/assets/characters-v1/delivery-manifest.json').read_text())['deliveries']
actors['well']=[['teacher',1225,405]]
checks=[]
for scene,people in actors.items():
 camera=j['scene-v8.json'][scene]['camera'];R=camera['radius'];a=camera['angle'];c=math.cos(a);s=math.sin(a);terrain=j['chapter-1.logical.json'][scene]['terrain'];mask=Image.new('L',(1672,941));d=ImageDraw.Draw(mask)
 for row in range(7):
  for col in range(11):
   q=col-row//2
   if terrain.get(f'{q},{row}','ground') not in ('ground','water'):continue
   x=math.sqrt(3)*R*(q+row/2);y=1.5*R*row;points=[]
   for i in range(6):
    xx=x+R*math.cos(math.radians(i*60-90));yy=y+R*math.sin(math.radians(i*60-90));points.append((camera['origin']['x']+c*xx-s*yy,camera['origin']['y']+camera['groundScale']*(s*xx+c*yy)))
   d.polygon(points,fill=255)
 for actor,x,y in people:
  res=residents[actor];orig=res['frames']['idle'];frame=delivery.get(orig['image'],orig);scale=res['sceneHeightPx']/frame['frameSize'][1];im=Image.open(root/'public/assets/characters-v1'/frame['image']).getchannel('A');im=im.resize((round(im.width*scale),round(im.height*scale)));alpha=Image.new('L',mask.size);alpha.paste(im,(round(x-frame['footAnchor'][0]*scale),round(y-frame['footAnchor'][1]*scale)));overlap=sum(1 for v in ImageChops.multiply(mask,alpha).getdata() if v>32);checks.append({'scene':scene,'resident':actor,'feet':[x,y],'alphaOverPlayablePixels':overlap,'scope':'legacy layout1, ground and water full polygons, actual optimized alpha>32'})

assert all(c['alphaOverPlayablePixels']==0 for c in checks)
(root/'docs/chapter-1-rc/evidence/residents-runtime/clearance.json').write_text(json.dumps(checks,indent=2)+'\n')
print('PASS7 actual-alpha legacy geometry clearances')
