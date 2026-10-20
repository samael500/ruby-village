"""Stage delivered garden/well into the shared INACTIVE layout-2 contract.
Readiness remains pending until actual game review; no production gate edits.
"""
from pathlib import Path
import hashlib,json,shutil
root=Path(__file__).resolve().parents[1]
dest=root/'public/assets/chapter-1/v9'
p=dest/'manifest.json';manifest=json.loads(p.read_text())
for sid in ['garden','well']:
 source=root/'public/assets/chapter-1-garden-well'
 contract=json.loads((source/f'{sid}-manifest.json').read_text())
 if not contract.get('wide'):
  print(f'{sid}: not installed, wide delivery pending');continue
 out=dest/sid;out.mkdir(exist_ok=True)
 files=['background.webp','wide.webp']
 for file in files:shutil.copy2(source/sid/file,out/file)
 entry=manifest['scenes'][sid]
 entry.update(background=f'{sid}/background.webp',foreground=None,
  wide={**{k:contract['wide'][k] for k in ['canvas','originalRect']},'file':f'{sid}/wide.webp'},
  joinBand=contract['wide'].get('joinBand',48),
  sourceManifest=str((source/f'{sid}-manifest.json').relative_to(root)),
  source=contract['source'],sourceSha256=contract['sourceSha256'],
  status='map-matched-source-candidate-awaiting-actual-game',
  wideStatus='painted-native-join-awaiting-actual-game',residentPresentation='scene-sprite-and-portrait')
 # Garden: right of the single table, looking toward activity and the approach.
 # Source suggested1295,265 is retained in source manifest for comparison.
 # Well source1225,405 clears free ground but overlaps Ruta on arrival;1320 separates actors.
 feet={'garden':(1420,265),'well':(1320,405)}[sid]
 entry['semanticAnchors']['residentFeet']={'x':feet[0],'y':feet[1],'status':'full-alpha-candidate-actual-composition-pending'}
 if sid=='garden':
  entry['semanticAnchors']['tableFrontFeet']={'x':1299,'y':263,'explanation':'single embedded source table bottom center; no separate table sprite'}
 entry['checks']={'sourceGuardManifest':entry['sourceManifest'],'fullPolygonVisualAudit':'pending','gameQa':'not-run','artAcceptance':'pending'}
 entry['deliveryFiles']={file:{'bytes':(out/file).stat().st_size,'sha256':hashlib.sha256((out/file).read_bytes()).hexdigest()} for file in files}
 print(f'{sid}: staged inactive, actual review pending')
manifest['activationStatus']='inactive-until-all-eight-art-and-geometry-reviewed'
p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
