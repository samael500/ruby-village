from pathlib import Path
import json,base64,hashlib
root=Path(__file__).resolve().parents[1]
out=root/'art/chapter-1-v9'; (out/'review').mkdir(exist_ok=True)
manifest={'schemaVersion':1,'status':'pilot-awaiting-art-review','sourceCommit':'add76709d66ab6a138014886642f045e658f53bf','canvas':{'width':1672,'height':941},'sourceOfTruth':'docs/blender-chapter-1/layouts/engine/*.json','scenes':{}}
for f in sorted((root/'docs/blender-chapter-1/layouts/engine').glob('*.json')):
 d=json.loads(f.read_text());sid=d['sceneId'];free=[c for c in d['cells'] if c['terrain'] is None];blocked=[c for c in d['cells'] if c['terrain']]
 def poly(c,fill,opacity=1):
  pts=' '.join(f"{v['x']:.5f},{v['y']:.5f}" for v in c['polygon'])
  return f'<polygon points="{pts}" fill="{fill}" fill-opacity="{opacity}" stroke="{fill}" stroke-width="1"/>'
 masks='<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">'+''.join(poly(c,'#fff') for c in free)+'</svg>'
 (out/'review'/f'{sid}-free-mask.svg').write_text(masks)
 manifest['scenes'][sid]={'status':'pilot-review' if sid=='gate' else 'awaiting-pilot-acceptance','geometrySha256':hashlib.sha256(f.read_bytes()).hexdigest(),'camera':d['camera'],'anchors':{'start':d['start']['pixel'],'goal':d['goal']['pixel']},'freeCells':len(free),'blockedCells':len(blocked),'freeMask':f'art/chapter-1-v9/review/{sid}-free-mask.svg','layers':{}}
 if sid=='gate':
  for state in ['closed','open']:
   data=base64.b64encode((out/'candidates'/f'gate-v2-{state}.png').read_bytes()).decode()
   overlay='<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941"><image width="1672" height="941" href="data:image/png;base64,'+data+'"/>'+''.join(poly(c,'#f04a65',.22) for c in blocked)+''.join(poly(c,'#00adf5',.04) for c in free)
   for c in [d['start'],d['goal']]:
    p=c['pixel'];overlay+=f'<circle cx="{p["x"]}" cy="{p["y"]}" r="12" fill="#ffe36a" stroke="#332640" stroke-width="3"/>'
   overlay+='</svg>';(out/'review'/f'gate-{state}-overlay.svg').write_text(overlay)
(root/'src/scene-v9.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
