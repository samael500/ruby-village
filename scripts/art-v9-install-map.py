"""Install isolated map-match handoffs into shared inactive v9 contract."""
from pathlib import Path
import json,shutil,hashlib
r=Path(__file__).resolve().parents[1];dest=r/'public/assets/chapter-1/v9';p=dest/'manifest.json';manifest=json.loads(p.read_text())
for sid in ['gate','bakery','post','forest']:
 source=r/f'public/assets/chapter-1-map-match/{sid}';contract=json.loads((source/'manifest.json').read_text());out=dest/sid;out.mkdir(exist_ok=True)
 for file in ['background.webp','wide.webp']:shutil.copy2(source/file,out/file)
 entry=manifest['scenes'][sid];entry.update({'background':f'{sid}/background.webp','wide':{'file':f'{sid}/wide.webp','canvas':contract['wide']['canvas'],'originalRect':contract['wide']['originalRect']},'joinBand':contract.get('joinBand',48),'sourceManifest':str((source/'manifest.json').relative_to(r)),'status':'map-matched-native-guard-passed-art-and-game-review-pending','checks':{**contract['checks'],'fullPolygonVisualAudit':'pending'},'wideStatus':contract.get('wideStatus','painted-join-candidate-review-pending'),'mapMatchSource':contract['source'],'sourceSha256':contract['sourceSha256']})
 if 'recommendedWholeSceneGrade' in contract:entry['recommendedWholeSceneGrade']=contract['recommendedWholeSceneGrade']
 if sid=='bakery':entry['semanticAnchors']['residentFeet']={'x':1360,'y':405,'status':'accepted-arrival-B1-correction-requires-actual-review'}
 entry['checks']['fullPolygonVisualAudit']='pending'
 entry['deliveryFiles']={f:{'bytes':(out/f).stat().st_size,'sha256':hashlib.sha256((out/f).read_bytes()).hexdigest()} for f in ['background.webp','wide.webp']}
manifest['activationStatus']='inactive-until-all-eight-art-and-geometry-reviewed';p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('Installed four independent handoffs into inactive common v9 contract')
