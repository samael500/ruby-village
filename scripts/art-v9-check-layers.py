"""Read-only raster checks for exported registered art layers."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[1];out=root/'art/chapter-1-v9/layers';d=json.loads((root/'docs/blender-chapter-1/layouts/engine/gate.json').read_text());m=Image.new('1',(1672,941));draw=ImageDraw.Draw(m)
for c in d['cells']:
 if c['terrain'] is None:draw.polygon([(v['x'],v['y']) for v in c['polygon']],fill=1)
report={}
for n in ['foreground-fixed','gate-closed','gate-open']:
 f=out/(n+'.png');im=Image.open(f);assert im.size==(1672,941) and im.mode=='RGBA';a=im.getchannel('A');overlap=sum(1 for v,p in zip(a.getdata(),m.getdata()) if v>0 and p)
 report[n]={'size':list(im.size),'alphaRange':list(a.getextrema()),'nontransparentBounds':list(a.getbbox()),'freePolygonOverlapPixels':overlap,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 if n!='gate-closed':assert overlap==0,(n,overlap)
manifest=json.loads((out/'manifest.json').read_text());a,b,c,d,e,f=manifest['gate']['openMatrix'];x,y=manifest['gate']['hingePivot'];assert abs(a*x+c*y+e-x)<1e-6 and abs(b*x+d*y+f-y)<1e-6
report['hingeFixedPoint']='passed';(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
