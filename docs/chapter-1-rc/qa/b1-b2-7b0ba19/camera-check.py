from pathlib import Path
from PIL import Image
import json,math
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;rows=[];alpha=Image.open(R/'public/assets/chapter-1/v9/gate/gate-open.webp').getchannel('A');box=alpha.getbbox()
for p in O.glob('*/*/report.json'):
 run=json.loads(p.read_text())
 for state in run['states']:
  lay=state['layout'];paint=lay['painted'];resident=lay['residents'];fore=lay['foregrounds'];assert all(abs(a-b)<1e-6 for a,b in zip(paint,resident));assert fore and all(abs(a-b)<1e-6 for a,b in zip(paint,fore[0])) # First foreground is #board; later entries are hidden prologue/result clones.
  if state['label']!='arrival':continue
  rb=state['ruta']['box'];panel=lay['story']['top'];row=dict(scene=run['scene'],viewport=run['viewport'],label=state['label'],sharedLayerMatrices=True,paintedMatrix=paint,panelTop=panel,fieldBottom=lay['field']['bottom'],rutaViewportBox=rb,rutaCompleteFrameAbovePanel=rb['y']+rb['h']<=panel+1e-6)
  if run['scene']=='gate':
   a,b,c,d,e,f=paint;points=[(a*x+c*y+e,b*x+d*y+f)for x in [box[0],box[2]]for y in [box[1],box[3]]];bounds=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)];row.update(gateNativeAlphaBounds=box,gateTransformedAlphaBounds=bounds,gatePixelsBelowPanel=max(0,bounds[3]-panel),gatePixelsBelowField=max(0,bounds[3]-lay['field']['bottom']))
  rows.append(row)
assert all(r['rutaCompleteFrameAbovePanel']for r in rows)
assert any(r.get('gatePixelsBelowPanel',0)>30 for r in rows)
(O/'camera-check.json').write_text(json.dumps(rows,indent=2)+'\n');print([(r['scene'],r['viewport'],r.get('gatePixelsBelowPanel'),r['rutaCompleteFrameAbovePanel'])for r in rows])
