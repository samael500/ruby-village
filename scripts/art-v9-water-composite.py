"""Native material masks: unchanged painted dry plate + painted water material.
No logical terrain is inferred from colors. All masks come from accepted polygons.
"""
from pathlib import Path
import json,base64
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/layers/water';out.mkdir(parents=True,exist_ok=True)
def image(f,extra=''):
 return '<image width="1672" height="941" '+extra+' href="data:image/png;base64,'+base64.b64encode(f.read_bytes()).decode()+'"/>'
head='<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">'
for sid in ['stream','mill']:
 d=json.load(open(r/f'art/chapter-1-v9/packages/{sid}/geometry.json'));polys=''
 for c in d['cells']:
  if c['terrain']=='water':polys+='<polygon points="'+' '.join(f"{v['x']:.5f},{v['y']:.5f}" for v in c['polygon'])+'" fill="white" stroke="white" stroke-width="0.3"/>'
 defs='<defs><filter id="erode"><feMorphology operator="erode" radius="5"/></filter><filter id="shoreShade"><feColorMatrix type="matrix" values=".52 0 0 0 0 0 .48 0 0 0 0 0 .43 0 0 0 0 0 1 0"/></filter><mask id="water" maskUnits="userSpaceOnUse">'+polys+'</mask><mask id="shore" maskUnits="userSpaceOnUse">'+polys+'<g filter="url(#erode)">'+polys.replace('fill="white"','fill="black"').replace('stroke="white"','stroke="black"')+'</g></mask></defs>'
 dry=r/f'art/chapter-1-v9/candidates/{sid}-dry-v1.png';material=r/'art/chapter-1-v9/candidates/water-material-v1.png'
 water='<g mask="url(#water)">'+image(material)+'</g><g mask="url(#shore)">'+image(dry,'filter="url(#shoreShade)"')+'</g>'
 (out/f'{sid}-water.svg').write_text(head+defs+water+'</svg>')
 (out/f'{sid}-composite.svg').write_text(head+defs+image(dry)+water+'</svg>')
 (out/f'{sid}-mask.svg').write_text(head+polys+'</svg>')
print('Exact native water overlays + dry composites prepared')
