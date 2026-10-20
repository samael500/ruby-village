from pathlib import Path
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import json,hashlib
R=Path('/home/mskorokhod/life/ruby-village');O=Path('/home/mskorokhod/life/ruby-village-stream-road/docs/chapter-1-rc/art/garden-mill-polygon-visual');O.mkdir(parents=True,exist_ok=True)
faces=json.load(open(R/'public/assets/characters-facing-v1/residents-facing-manifest.json'))['characters'];res=json.load(open(R/'public/assets/characters-v1/residents-manifest.json'))['characters'];deliveries=json.load(open(R/'public/assets/characters-v1/delivery-manifest.json'))['deliveries'];common=json.load(open(R/'public/assets/chapter-1/v9/manifest.json'));out={}
def nz(im):return sum(im.histogram()[1:])
for sid,actors in {'garden':[('rabbit',1420,265)],'mill':[('miller',1430,398),('squirrel',1530,450)]}.items():
 e=common['scenes'][sid];native=Image.open(R/'public/assets/chapter-1/v9'/e['background']).convert('RGBA');g=json.load(open(R/f'art/chapter-1-v9/packages/{sid}/geometry.json'));mask=Image.new('L',native.size);d=ImageDraw.Draw(mask)
 for c in g['cells']:
  if c['terrain'] is None or c['terrain']=='water':d.polygon([(p['x'],p['y']) for p in c['polygon']],fill=255)
 core=mask.filter(ImageFilter.MinFilter(3));checks=[];review=native.copy()
 def audit(name,layer):
  a=layer.getchannel('A');checks.append({'name':name,'anyAlphaOverFreeWaterCoarseRaster':nz(ImageChops.multiply(a,mask)),'anyAlphaOverFreeWaterBeyond1pxTolerance':nz(ImageChops.multiply(a,core))})
 for actor,x,y in actors:
  frames=[(name,f,'characters-facing-v1')for name,f in faces[actor]['frames'].items()];legacy=res[actor]['frames']['idle'].copy();delivery=deliveries.get(legacy['image']);
  if delivery:legacy.update({k:delivery[k] for k in ['image','frameSize','footAnchor']})
  frames.append(('legacy-idle',legacy,'characters-v1'))
  for view,f,folder in frames:
   a=Image.open(R/'public/assets'/folder/f['image']).convert('RGBA');scale=res[actor]['sceneHeightPx']/f['frameSize'][1];a=a.resize((round(a.width*scale),round(a.height*scale)),Image.Resampling.LANCZOS);layer=Image.new('RGBA',native.size);layer.alpha_composite(a,(round(x-f['footAnchor'][0]*scale),round(y-f['footAnchor'][1]*scale)));audit(actor+'/'+view,layer)
   if view=='conversation-left':review=Image.alpha_composite(review,layer)
 if sid=='garden':
  for name in ['garden-tree-v1','garden-table-v1']:audit(name,Image.open(R/f'art/chapter-1-v9/garden-well/layers/{name}.png').convert('RGBA'))
  dry=Image.open(R/'art/chapter-1-v9/candidates/garden-clear-v1.png').convert('RGB');guard=core
 else:
  wheel=Image.open(R/'public/assets/chapter-1/v9/mill/wheel-110.png').convert('RGBA');layer=Image.new('RGBA',native.size);layer.alpha_composite(wheel,(1215,108));audit('wheel110',layer);review=Image.alpha_composite(review,layer);dry=Image.open(R/'art/chapter-1-v9/layers/props/mill-dry-map.png').convert('RGB');guard=Image.open(R/'art/chapter-1-v9/layers/water/mill-pilot/free-core-mask18.png').convert('L')
 diff=ImageChops.difference(native.convert('RGB'),dry);changed=sum(1 for v,m in zip(diff.getdata(),guard.getdata()) if m and v!=(0,0,0));out[sid]={'actors':actors,'fullAlphaChecks':checks,'dryPlateGuardChangedRGBPixels':changed,'dryPlateGuard':'all free/water1px interior' if sid=='garden' else 'freeCORE18 only; water intentionally painted, boundary flat dryshore contract≤12px','sourcePolygonVisualAudit':'pending-review-of-generated-evidence'}
 review.convert('RGB').save(O/f'{sid}-native-residents.jpg',quality=95);marks=review.copy();d=ImageDraw.Draw(marks)
 for c in g['cells']:
  xy=[(v['x'],v['y']) for v in c['polygon']];color=(40,220,255) if c['terrain'] is None or c['terrain']=='water' else (255,70,90);d.line(xy+[xy[0]],fill=color,width=2);d.text((c['center']['x']-12,c['center']['y']-5),c['id'],fill=color)
 marks.convert('RGB').save(O/f'{sid}-all77-overlay.jpg',quality=95)
 for i,box in enumerate([(0,200,1672,460),(0,440,1672,650),(0,630,1672,900)]):marks.crop(box).convert('RGB').save(O/f'{sid}-board-strip{i}.jpg',quality=97)
(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
