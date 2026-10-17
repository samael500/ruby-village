"""Place unchanged native core over independently painted outpaint."""
from pathlib import Path
import base64,json
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/outpaint'
for sid in ['gate','garden']:
 wide=out/f'{sid}-wide-v1.png';core=r/('art/chapter-1-v9/candidates/gate-v3-base.png' if sid=='gate' else 'art/chapter-1-v9/candidates/garden-v4.png')
 def img(p,x,y,w,h):return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"/>'
 (out/f'{sid}-wide-registered.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="4096" height="1600" viewBox="0 0 4096 1600">'+img(wide,0,0,4096,1600)+img(core,1212,329,1672,941)+'</svg>')
