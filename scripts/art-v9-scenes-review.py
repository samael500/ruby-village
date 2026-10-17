from pathlib import Path
import json,base64
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/review/scenes';out.mkdir(exist_ok=True)
for sid in ['garden','well','bakery','stream','mill','post','forest']:
 source=r/f'art/chapter-1-v9/candidates/{sid}-v4.png'
 if not source.exists():continue
 overlay=(r/f'art/chapter-1-v9/packages/{sid}/geometry-overlay.svg').read_text().split('>',1)[1].rsplit('</svg>',1)[0]
 data=base64.b64encode(source.read_bytes()).decode();svg='<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941"><image width="1672" height="941" href="data:image/png;base64,'+data+'"/>'+overlay+'</svg>'
 (out/f'{sid}-full-geometry.svg').write_text(svg)
print('Scene full geometry overlays prepared')
