from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import json,hashlib
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;M=json.loads((R/'public/assets/chapter-1/v9/manifest.json').read_text());actors={'bakery':[('baker',1360,405)],'post':[('hedgehog',1370,405)]};faces=json.loads((R/'public/assets/characters-facing-v1/residents-facing-manifest.json').read_text())['characters'];res=json.loads((R/'public/assets/characters-v1/residents-manifest.json').read_text())['characters'];rows=[]
for sid in ['gate','bakery','post','forest']:
 scene=M['scenes'][sid];D=R/'public/assets/chapter-1/v9';native=Image.open(D/scene['background']).convert('RGB');wide=Image.open(D/scene['wide']['file']).convert('RGB');rect=scene['wide']['originalRect'];assert wide.crop((rect['x'],rect['y'],rect['x']+rect['width'],rect['y']+rect['height'])).tobytes()==native.tobytes();g=json.loads((R/f'art/chapter-1-v9/packages/{sid}/geometry.json').read_text());free=Image.new('L',native.size);draw=ImageDraw.Draw(free)
 for c in g['cells']:
  if c['terrain']is None or c['terrain']=='water':draw.polygon([(p['x'],p['y'])for p in c['polygon']],fill=255)
 checks=[]
 for actor,x,y in actors.get(sid,[]):
  frames=[(name,f,'characters-facing-v1')for name,f in faces[actor]['frames'].items()]
  legacy=res[actor]['frames']['idle'].copy();delivery=json.loads((R/'public/assets/characters-v1/delivery-manifest.json').read_text())['deliveries'].get(legacy['image'])
  if delivery:legacy.update({'image':delivery['image'],'frameSize':delivery['frameSize'],'footAnchor':delivery['footAnchor']})
  frames.append(('legacy-idle',legacy,'characters-v1'))
  for view,f,folder in frames:
   scale=res[actor]['sceneHeightPx']/f['frameSize'][1];alpha=Image.open(R/'public/assets'/folder/f['image']).getchannel('A');alpha=alpha.resize((round(alpha.width*scale),round(alpha.height*scale)),Image.Resampling.LANCZOS);mask=Image.new('L',native.size);mask.paste(alpha,(round(x-f['footAnchor'][0]*scale),round(y-f['footAnchor'][1]*scale)));count=sum(v>0 for v in ImageChops.multiply(mask,free).get_flattened_data());checks.append({'actor':actor,'view':view,'feet':[x,y],'anyAlphaOverPlayableGroundWater':count})
 rows.append({'scene':sid,'nativeSize':native.size,'wideSize':wide.size,'wideExactCore':True,'sourceManifestStatus':scene['status'],'residentAlphaChecks':checks})
path=R/'art/blender/chapter-layouts/layout-adjustments.json';sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha=='6baed82d3dea0e1b6472582751bcd0ccb9d41c872f50c9b865838b17e7b1cf6e';(O/'geometry.json').write_text(json.dumps({'acceptedLayoutHash':sha,'scenes':rows},indent=2)+'\n');print('native/wide/layoutPASS; residentalpha',[(r['scene'],max((c['anyAlphaOverPlayableGroundWater']for c in r['residentAlphaChecks']),default=0))for r in rows])
