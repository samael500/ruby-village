"""Encode unchanged painted sources for review; no geometry inferred from color."""
from pathlib import Path
from PIL import Image
import json,hashlib
r=Path(__file__).resolve().parents[1];out=r/'public/assets/chapter-1/v9';out.mkdir(parents=True,exist_ok=True)
manifest={'schemaVersion':1,'version':'chapter-1-v9-painted-2026-10-17','styleStatus':'accepted-by-Maksim-2026-10-17','activationStatus':'inactive-until-all-eight-geometry-audited','canvas':{'width':1672,'height':941},'scenes':{}}
residents={'garden':[1280,245],'bakery':[1290,405],'post':[1370,405],'stream':[1400,225],'mill':[1430,398]}
for sid in ['gate','garden','well','bakery','stream','mill','post','forest']:
 source=r/('art/chapter-1-v9/candidates/gate-v3-base.png' if sid=='gate' else f'art/chapter-1-v9/candidates/{sid}-v4.png')
 if not source.exists():continue
 dest=out/sid;dest.mkdir(exist_ok=True);im=Image.open(source);assert im.size==(1672,941);im.convert('RGB').save(dest/'background.webp',quality=93,method=6)
 geom=r/f'art/chapter-1-v9/packages/{sid}/geometry.json';d=json.loads(geom.read_text());entry={'status':'style-approved-geometry-pending','background':f'{sid}/background.webp','foreground':None,'wide':None,'wideStatus':'pending-outpaint','source':str(source.relative_to(r)),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'geometrySha256':hashlib.sha256(geom.read_bytes()).hexdigest(),'camera':d['camera'],'anchors':{'start':d['start']['pixel'],'goal':d['goal']['pixel']},'semanticAnchors':{},'checks':{'fullPolygonVisualAudit':'pending'}}
 if sid in residents:entry['semanticAnchors']['residentFeet']={'x':residents[sid][0],'y':residents[sid][1],'status':'scene-illustration-candidate-foot-anchor-pending-review'}
 else:entry['residentPresentation']='portrait-only'
 if sid=='gate':
  for name in ['foreground-fixed','gate-closed','gate-open']:
   p=r/f'art/chapter-1-v9/layers/{name}.png';Image.open(p).save(dest/(name+'.webp'),lossless=True,method=6)
  entry.update({'foreground':'gate/foreground-fixed.webp','gateClosed':'gate/gate-closed.webp','gateOpen':'gate/gate-open.webp','status':'style-approved-layer-checks-passed-runtime-review-pending'})
  entry['semanticAnchors'].update({'looseStoneFeet':{'x':685.5960043841964,'y':494.75,'sourceCell':'3,3'},'basketGround':{'x':721.5960043841964,'y':506.75}})
 if sid=='garden':entry['semanticAnchors']['tableFrontFeet']={'x':1280,'y':245,'explanation':'below the actual painted apple table, outside top playable row; goal remains clear'}
 if sid in ['stream','mill']:entry['status']='geometry-failed-correction-in-progress';entry['checks']['fullPolygonVisualAudit']='failed-water-location'
 manifest['scenes'][sid]=entry
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('Staged',len(manifest['scenes']),'review scenes; runtime remains inactive')
