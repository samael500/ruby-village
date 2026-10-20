"""Install registered mill resources; actual review remains explicit."""
from pathlib import Path
import json,shutil,hashlib
r=Path(__file__).resolve().parents[1];s=r/'art/chapter-1-v9/layers/water/mill-pilot';out=r/'public/assets/chapter-1/v9/mill';out.mkdir(exist_ok=True)
contract=json.loads((s/'manifest.json').read_text());p=out.parent/'manifest.json';m=json.loads(p.read_text());e=m['scenes']['mill']
for f in ['background.webp','wide.webp','wheel-110.png']:shutil.copy2(s/f,out/f)
e.update(background='mill/background.webp',foreground=None,wide={'file':'mill/wide.webp','canvas':dict(zip(['width','height'],contract['wide']['canvas'])),'originalRect':dict(zip(['x','y','width','height'],contract['wide']['originalRect']))},joinBand=48,sourceManifest='art/chapter-1-v9/layers/water/mill-pilot/manifest.json',status='adaptive-mill-source-checked-game-review-pending',wheel={**contract['wheel'],'file':'mill/wheel-110.png'})
e['semanticAnchors']['secondResidentFeet']={'x':1530,'y':450,'status':'same-as-independently-checked-legacy-F1-anchor; layout2-actual-check-pending'}
e['checks']={**json.loads((s/'checks.json').read_text()),'fullPolygonVisualAudit':'pending','gameQa':'pending','artAcceptance':'pending'}
e['deliveryFiles']={f:{'bytes':(out/f).stat().st_size,'sha256':hashlib.sha256((out/f).read_bytes()).hexdigest()} for f in ['background.webp','wide.webp','wheel-110.png']}
p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
