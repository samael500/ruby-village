from pathlib import Path
import base64
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/outpaint'
for sid in ['gate','garden','well','bakery','stream','mill','post','forest']:
 f=r/('art/chapter-1-v9/candidates/gate-v3-base.png' if sid=='gate' else f'art/chapter-1-v9/candidates/{sid}-v4.png');data=base64.b64encode(f.read_bytes()).decode();(out/f'{sid}-registered-template.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="4096" height="1600" viewBox="0 0 4096 1600"><rect width="4096" height="1600" fill="white"/><image x="1212" y="329" width="1672" height="941" href="data:image/png;base64,'+data+'"/></svg>')
