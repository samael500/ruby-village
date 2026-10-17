"""Final source geometry evidence and delivery hashes after the wide foliage join."""
from pathlib import Path
from PIL import Image,ImageDraw
import hashlib,json
R=Path(__file__).resolve().parents[1];E=R/'docs/chapter-1-rc/art/map-match-post-forest';contracts={}
for name in ['post','forest']:
 A=R/'art/chapter-1-map-match'/name;D=R/'public/assets/chapter-1-map-match'/name;core=Image.open(D/'background.webp').convert('RGB');layout=json.loads((R/f'docs/blender-chapter-1/layouts/engine/{name}.json').read_text());guide=Image.new('RGBA',core.size);g=ImageDraw.Draw(guide)
 for c in layout['cells']:g.polygon([(p['x'],p['y'])for p in c['polygon']],fill=(255,0,0,40)if c['terrain']else(0,180,255,22),outline=(255,0,0,200)if c['terrain']else(0,110,255,170),width=2)
 for k,col in [('start','#00eb55'),('goal','#e53cff')]:
  p=layout[k]['pixel'];g.ellipse((p['x']-8,p['y']-8,p['x']+8,p['y']+8),fill=col)
 Image.alpha_composite(core.convert('RGBA'),guide).convert('RGB').save(E/f'{name}-full-polygon-review.jpg',quality=95)
 m=json.loads((D/'manifest.json').read_text());v8=R/'public/assets/chapter-1/v8'/('07-post-surroundings.jpg'if name=='post'else'08-edge-surroundings.jpg');m['wide']['referenceRing']={'file':str(v8.relative_to(R)),'nativeSize':list(Image.open(v8).size),'logicalCanvas':[3272,1200],'sha256':hashlib.sha256(v8.read_bytes()).hexdigest()};m['checks']['browserPreview']='12cases-6viewports-per-scene-zero-pageerrors';m['checks']['physicalPhone']='not-tested';m['deliveryFiles']={p.name:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}for p in [D/'background.webp',D/'wide.webp']};(D/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');contracts[name]=m
(E/'delivery-contracts.json').write_text(json.dumps(contracts,indent=2)+'\n')
