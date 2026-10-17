"""Assemble registered rig phases as imagegen pose constraints; never generates final art."""
from PIL import Image
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1];out=root/'art/characters-walk-v1/source';out.mkdir(parents=True,exist_ok=True)
directions=['e','se','sw','w','nw','ne'];sheet=Image.new('RGBA',(2048,1536))
for row,direction in enumerate(directions):
 for column,frame in enumerate(range(1,17,2)):
  sheet.alpha_composite(Image.open(root/f'art/blender/characters/renders/{direction}-{frame:02}.png').convert('RGBA'),(column*256,row*256))
sheet.save(out/'rig-6x8-registered.png')
(out/'input-contract.json').write_text(json.dumps({'sourceManifest':'art/blender/characters/manifest.json','sourceBlend':'art/blender/characters/ruta-motion-prototype.blend','directions':directions,'selectedFrames':list(range(1,17,2)),'grid':[8,6],'cellSize':[256,256],'footAnchor':[128,215.26],'cycleDurationMs':800,'frameDurationMs':100,'contacts':{'0':'left','4':'right'},'note':'uniform every-other-frame sampling from one 16-phase rig, no mirrored sprites','sha256':hashlib.sha256((out/'rig-6x8-registered.png').read_bytes()).hexdigest()},indent=2)+'\n')
