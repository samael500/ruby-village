"""Registered masks and transforms of painted source props; no new bitmap art."""
from pathlib import Path
import json,base64
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/layers/props';out.mkdir(parents=True,exist_ok=True)
def img(p,extra=''):return '<image width="1672" height="941" '+extra+' href="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'"/>'
head='<svg xmlns="http://www.w3.org/2000/svg" width="1672" height="941" viewBox="0 0 1672 941">'
def polygons(sid,terrain):
 d=json.load(open(r/f'art/chapter-1-v9/packages/{sid}/geometry.json'));return ''.join('<polygon points="'+' '.join(f"{p['x']:.5f},{p['y']:.5f}" for p in c['polygon'])+'" fill="white"/>' for c in d['cells'] if c['terrain']==terrain)
# Flower painting is clipped to the complete accepted flower footprint; its
# perimeter fades inward, never onto free ground.
flower=polygons('well','flower');defs='<defs><filter id="soft"><feMorphology operator="erode" radius="6"/><feGaussianBlur stdDeviation="2"/></filter><mask id="flowers" maskUnits="userSpaceOnUse"><g filter="url(#soft)">'+flower+'</g></mask></defs>'
body=img(r/'art/chapter-1-v9/candidates/well-clear-v1.png')+'<g mask="url(#flowers)">'+img(r/'art/chapter-1-v9/candidates/well-v4.png')+'</g>'
(out/'well-composite.svg').write_text(head+defs+body+'</svg>')
# One dominant map-matched apple tree. Only accepted tree blocker polygons
# receive its ground-level source pixels. Above-board crown remains visible.
trees=polygons('garden','tree');treeMask=trees+'<rect x="570" y="0" width="640" height="270" fill="white"/>'
defs='<defs><mask id="orchard" maskUnits="userSpaceOnUse">'+treeMask+'</mask><clipPath id="table"><path d="M1087 418 Q1095 397 1156 397 Q1219 398 1231 421 L1231 436 L1210 454 L1207 493 L1194 498 L1193 457 L1146 462 L1142 503 L1128 504 L1129 459 L1107 451 L1103 488 L1092 490 L1094 446 Q1085 439 1087 418Z"/><path d="M1034 389 L1072 378 L1089 387 L1091 435 L1115 451 L1111 470 L1090 468 L1092 497 L1081 501 L1077 465 L1054 460 L1058 491 L1048 497 L1044 453Z"/><path d="M1245 382 L1280 389 L1294 398 L1281 450 L1288 471 L1274 482 L1262 459 L1231 468 L1224 460 L1239 440Z"/><ellipse cx="1253" cy="486" rx="49" ry="35"/><ellipse cx="1159" cy="403" rx="36" ry="27"/></clipPath></defs>'
base=img(r/'art/chapter-1-v9/candidates/garden-clear-v1.png');source=img(r/'art/chapter-1-v9/candidates/garden-map-v1.png');body=base+'<g mask="url(#orchard)">'+source+'</g>'
# Source chair/table/basket group [1030,375,280,155] -> [1215,170,168,93].
body+='<g transform="translate(1215 170) scale(.6) translate(-1030 -375)"><g clip-path="url(#table)">'+source+'</g></g>'
(out/'garden-composite.svg').write_text(head+defs+body+'</svg>')
# Mill facade update is confined to upper-right occupied/outer region; dry
# playable ground is kept from the original cleared source plate.
d=json.load(open(r/'art/chapter-1-v9/packages/mill/geometry.json'));free=''.join('<polygon points="'+' '.join(f"{p['x']},{p['y']}" for p in c['polygon'])+'" fill="black" stroke="black" stroke-width="4"/>' for c in d['cells'] if c['terrain'] is None)
defs='<defs><mask id="facade" maskUnits="userSpaceOnUse"><rect x="1210" y="40" width="462" height="390" fill="white"/>'+free+'</mask></defs>'
body=img(r/'art/chapter-1-v9/candidates/mill-dry-v1.png')+'<g mask="url(#facade)">'+img(r/'art/chapter-1-v9/candidates/mill-map-v1.png')+'</g>'
(out/'mill-dry-map.svg').write_text(head+defs+body+'</svg>')
print('Well/garden/mill registered prop composites prepared')
