from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
from PIL import ImageChops
R=Path('/home/mskorokhod/life/ruby-village'); O=Path('/home/mskorokhod/life/ruby-village-stream-road/docs/chapter-1-rc/art/full8-source-audit');O.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=R/'public/assets/chapter-1/v9/manifest.json';data=json.loads(m.read_text());out={'commonManifestSha256':sha(m),'scope':'source geometry/registered images only; does not certify semantic visual acceptance or actual game','scenes':{}}
thumb=[]
for sid,e in data['scenes'].items():
 gp=R/f'art/chapter-1-v9/packages/{sid}/geometry.json';g=json.loads(gp.read_text());b=R/'public/assets/chapter-1/v9'/e['background'];w=R/'public/assets/chapter-1/v9'/e['wide']['file'];im=Image.open(b).convert('RGB');wide=Image.open(w).convert('RGB');rect=e['wide']['originalRect'];crop=wide.crop((rect['x'],rect['y'],rect['x']+rect['width'],rect['y']+rect['height']));diff=ImageChops.difference(im,crop); cnt=sum(1 for p in diff.getdata() if p!=(0,0,0));cells=g['cells']; mask=Image.new('L',im.size); md=ImageDraw.Draw(mask)
 for c in cells: md.polygon([(v['x'],v['y']) for v in c['polygon']],fill=255)
 boardcnt=sum(1 for p,v in zip(diff.getdata(),mask.getdata()) if v and p!=(0,0,0));d=ImageDraw.Draw(im)
 for c in cells:
  xy=[(v['x'],v['y']) for v in c['polygon']];col=(20,240,240) if c['terrain']=='water' else ((90,255,80) if c['terrain']=='free' else (255,80,70));d.line(xy+[xy[0]],fill=col,width=2);p=c['center'];d.text((p['x']-12,p['y']-5),c['id'],fill=col)
 im.save(O/f'{sid}-polygons.jpg',quality=92);t=im.resize((501,282));ImageDraw.Draw(t).text((8,8),sid,fill='white');thumb.append(t)
 out['scenes'][sid]={'geometrySha256':sha(gp),'manifestGeometryHashMatches':sha(gp)==e.get('geometrySha256'),'cameraMatches':g['camera']==e['camera'],'anchorsMatch':all(g[k]['pixel']==e['anchors'][k] for k in ['start','goal']),'cellCount':len(cells),'allCellsSixVertices':all(len(c['polygon'])==6 for c in cells),'nativeSize':list(Image.open(b).size),'wideSize':list(wide.size),'wideNativeRgbChangedPixels':cnt,'wideProtected77BoardRgbChangedPixels':boardcnt,'backgroundSha256':sha(b),'wideSha256':sha(w),'sourceManifest':e.get('sourceManifest'),'sourceChecks':e.get('checks'),'technicalStatus':'passed' if len(cells)==77 and boardcnt==0 and g['camera']==e['camera'] and sha(gp)==e.get('geometrySha256') else 'failed','artAcceptance':'pending','fullPolygonVisualAudit':'pending-semantic-review-not-inferred-from-pixel-counts'}
canvas=Image.new('RGB',(1002,1128));
for i,t in enumerate(thumb):canvas.paste(t,((i%2)*501,(i//2)*282))
canvas.save(O/'all8-polygons.jpg',quality=92);(O/'report.json').write_text(json.dumps(out,indent=2)+'\n')
for s,v in out['scenes'].items():print(s,{k:v[k] for k in ['technicalStatus','manifestGeometryHashMatches','cameraMatches','anchorsMatch','cellCount','wideNativeRgbChangedPixels']})
