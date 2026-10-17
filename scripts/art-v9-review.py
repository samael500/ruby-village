"""Compose review SVGs only; original paintings are never modified."""
from pathlib import Path
import json,base64,hashlib
from PIL import Image
root=Path(__file__).resolve().parents[1];art=root/'art/chapter-1-v9';review=art/'review'
def image(p,x=0,y=0,w=1672,h=941):
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"/>'
def svg(body,w=1672,h=941):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'+body+'</svg>'
base=art/'candidates/gate-v3-base.png';fg=art/'candidates/gate-v3-foreground-closed.png'
composite=image(base)+image(fg)
(review/'gate-v3-composite.svg').write_text(svg(composite))
geometry=(art/'packages/gate/geometry-overlay.svg').read_text().split('>',1)[1].rsplit('</svg>',1)[0]
(review/'gate-v3-full-geometry.svg').write_text(svg(composite+geometry))
reference=root/'docs/ui-v7/references/00-gameplay-reference.png'
comparison=image(reference,0,40,836,470.5)+image(base,836,40,836,470.5)+image(fg,836,40,836,470.5)
comparison+='<text x="20" y="28" fill="#302310" font-size="22">Repository art reference</text><text x="856" y="28" fill="#302310" font-size="22">v3 layered candidate — unaccepted</text>'
(review/'gate-v3-reference-comparison.svg').write_text(svg('<rect width="1672" height="511" fill="#f1e4c9"/>'+comparison,1672,511))
records=[]
for p in sorted((art/'candidates').glob('*.png')):
 im=Image.open(p);rec={'path':str(p.relative_to(root)),'size':list(im.size),'mode':im.mode,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'provenance':'current built-in image_gen edit' if 'v3' in p.name else 'recovered prior candidate; original prompt/tool record unavailable','status':'unaccepted'}
 if 'A' in im.getbands():rec['alphaExtrema']=list(im.getchannel('A').getextrema())
 records.append(rec)
(art/'provenance.json').write_text(json.dumps({'schemaVersion':1,'records':records},indent=2)+'\n')
print('Review SVGs, hashes and alpha metadata saved')
