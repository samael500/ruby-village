"""Rasterize actual UV polygons/material IDs as technical generation guides, not painted art."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,gzip
O=Path(__file__).resolve().parent;N=2048
for kind in['body']:
 d=json.load(gzip.open(O/(kind+'-uv-faces.json.gz'),'rt'));base=Image.new('RGB',(N,N),(231,223,208));wire=Image.new('RGBA',(N,N),(0,0,0,0));b=ImageDraw.Draw(base);w=ImageDraw.Draw(wire)
 for f in d['faces']:
  ps=[(round(u*(N-1)),round((1-v)*(N-1)))for u,v in f['uv']]
  if len(ps)<3:continue
  b.polygon(ps,fill=tuple(f['color']));w.line(ps+[ps[0]],fill=(38,51,58,110),width=1)
 base.save(O/(kind+'-uv-flat-target.png'));overlay=base.convert('RGBA');overlay.alpha_composite(wire);overlay.convert('RGB').save(O/(kind+'-uv-wire-guide.png'))
print('TECHNICAL_UV_GUIDES_READY')
