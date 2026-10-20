"""Deterministic geometry handoff; never generates or edits painted art."""
from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parents[1]
out=root/'art/chapter-1-v9/packages';out.mkdir(exist_ok=True)
for f in sorted((root/'docs/blender-chapter-1/layouts/engine').glob('*.json')):
 d=json.loads(f.read_text());sid=d['sceneId'];dest=out/sid;dest.mkdir(exist_ok=True)
 def poly(c,fill,opacity=1):
  pts=' '.join(f"{v['x']:.5f},{v['y']:.5f}" for v in c['polygon'])
  return f'<polygon points="{pts}" fill="{fill}" fill-opacity="{opacity}" stroke="{fill}" stroke-width="1"/>'
 def svg(body):return '<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">'+body+'</svg>'
 for terrain in ['free','blocked','water']:
  cells=[c for c in d['cells'] if (c['terrain'] is None if terrain=='free' else bool(c['terrain']) if terrain=='blocked' else c['terrain']=='water')]
  (dest/f'{terrain}-mask.svg').write_text(svg(''.join(poly(c,'white') for c in cells)))
 full=''.join(poly(c,'#ec476b' if c['terrain'] else '#00b7ff',.22 if c['terrain'] else .04) for c in d['cells'])
 for c in [d['start'],d['goal']]:
  p=c['pixel'];full+=f'<circle cx="{p["x"]}" cy="{p["y"]}" r="12" fill="#ffe36a" stroke="#332640" stroke-width="3"/>'
 (dest/'geometry-overlay.svg').write_text(svg(full))
 (dest/'geometry.json').write_bytes(f.read_bytes())
 contract={'schemaVersion':1,'sceneId':sid,'status':'awaiting-pilot-acceptance' if sid!='gate' else 'pilot-awaiting-art-review','canvas':{'width':1672,'height':941,'origin':[0,0],'crop':[0,0,1672,941]},'source':str(f.relative_to(root)),'sourceSha256':hashlib.sha256(f.read_bytes()).hexdigest(),'camera':d['camera'],'start':d['start'],'goal':d['goal'],'layers':{'background':'opaque canvas; no characters/UI/grid/solution','foreground':'RGBA same canvas/crop; no free-hex occlusion','gateClosed':'RGBA same canvas/crop' if sid=='gate' else None,'gateOpen':'RGBA same canvas/crop' if sid=='gate' else None,'water':'separate shores/water; no constructed bridge' if sid in ['stream','mill'] else None,'wheel':'RGBA independent wheel, fixed pivot' if sid=='mill' else None},'rules':['Preserve every full free polygon, not only cell center','Blockers require meaningful decoration across their whole footprints','Shared transform for every image, geometry and character feet','No production activation until art acceptance and matching game data integration']}
 (dest/'contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
print('8 exact geometry packages prepared')
