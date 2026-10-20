from pathlib import Path
from PIL import Image
import hashlib,json
R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style');O=Path(__file__).resolve().parent
paths=[]
for q in range(4):
 d=R/f'art/ruta-native-painted-production-v1/e-quarter{q}'
 paths += sorted(d.glob('*.png'))+sorted(d.glob('*.json'))+[d/'beige-review.jpg']
paths += [R/'public/assets/characters-v1/optimized/ruta-idle-pilot.webp',R/'art/ruta-native-painted-sprites-v2/full48/painted-sheet-v1.png']
a=[]
for p in paths:
 x={'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
 if p.suffix in ['.png','.jpg','.webp']:
  im=Image.open(p);x.update(size=im.size,mode=im.mode)
 a.append(x)
(O/'source-inventory.json').write_text(json.dumps({'rootCheckpoint':'d05eb76','files':a},indent=2)+'\n')
# Exact accepted guide pixels composited for transparent low-alpha scatter; no source modification.
for q in [1,2]:
 p=next((R/f'art/ruta-native-painted-production-v1/e-quarter{q}').glob('accepted-poses-*.png'));im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,(236,226,206,255));bg.alpha_composite(im);bg.convert('RGB').save(O/f'accepted-quarter{q}-composite.jpg',quality=94)
