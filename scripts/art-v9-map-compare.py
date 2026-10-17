from pathlib import Path
import base64,json
r=Path(__file__).resolve().parents[1];out=r/'art/chapter-1-v9/map-match';source=out/'accepted-map-reference.webp';mapdata=base64.b64encode(source.read_bytes()).decode()
rects={'gate':[0,0,490,340],'garden':[490,0,520,340],'well':[1010,0,440,340],'bakery':[1450,0,533,340],'forest':[0,320,500,410],'post':[500,320,500,410],'mill':[1000,320,430,410],'stream':[1430,320,553,410]}
rows=[]
for sid,rect in rects.items():
 x,y,w,h=rect;(out/f'{sid}-map-reference.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="{x} {y} {w} {h}"><image width="1983" height="793" href="data:image/webp;base64,{mapdata}"/></svg>')
 src=r/('art/chapter-1-v9/candidates/gate-v3-base.png' if sid=='gate' else f'art/chapter-1-v9/candidates/{sid}-v4.png');data=base64.b64encode(src.read_bytes()).decode();yy=len(rows)*460
 rows.append(f'<text x="20" y="{yy+30}" font-size="25">{sid}: accepted map / current scene candidate (before correction)</text><svg x="0" y="{yy+45}" width="600" height="400" viewBox="{x} {y} {w} {h}"><image width="1983" height="793" href="data:image/webp;base64,{mapdata}"/></svg><image x="610" y="{yy+45}" width="710" height="400" href="data:image/png;base64,{data}"/>')
(out/'map-scene-before-contact.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="3680" viewBox="0 0 1320 3680"><rect width="1320" height="3680" fill="#f4eddb"/>'+''.join(rows)+'</svg>')
(out/'map-source-rects.json').write_text(json.dumps(rects,indent=2)+'\n')
