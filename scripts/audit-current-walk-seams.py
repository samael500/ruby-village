"""Read-only alpha/joint diagnostic for already exported E-view, no asset edits."""
from pathlib import Path
from collections import deque
from PIL import Image
import json, hashlib
R=Path(__file__).resolve().parents[1];O=R/'docs/chapter-1-rc/qa/current-walk-seams';O.mkdir(parents=True,exist_ok=True)
j=json.loads((R/'art/characters-walk-v1/export-v2/evaluated-joints.json').read_text())['e'];s=json.loads((R/'art/characters-walk-v1/clean-parts-v2/e/parts.json').read_text());a=json.loads((R/'art/blender/characters/manifest.json').read_text())['footAnchor'];scale=224/210;offset=[160-a[0]*scale,256-a[1]*scale]
report={'scope':'Source PNG E Walk16 read-only; alpha probes cannot judge anatomy or white painted cuffs','sourceParts':{},'frames':[]}
for n,p in s['parts'].items():
 im=Image.open(R/'art/characters-walk-v1/clean-parts-v2/e'/p['file']).convert('RGBA').getchannel('A')
 report['sourceParts'][n]={'a':p['a'],'b':p['b'],'alphaA':im.getpixel(tuple(p['a'])),'alphaB':im.getpixel(tuple(p['b'])),'alphaBounds':im.getbbox()}
for i in range(16):
 p=R/f'art/characters-walk-v1/export-v2/renders/e/walk/{i:02}.png';im=Image.open(p).convert('RGBA');al=im.getchannel('A');visited=set();components=[]
 for y in range(im.height):
  for x in range(im.width):
   if (x,y) in visited or al.getpixel((x,y))<128:continue
   q=deque([(x,y)]);visited.add((x,y));pts=[]
   while q:
    u,v=q.popleft();pts.append((u,v))
    for du,dv in [(1,0),(-1,0),(0,1),(0,-1)]:
     z=(u+du,v+dv)
     if 0<=z[0]<im.width and 0<=z[1]<im.height and z not in visited and al.getpixel(z)>=128:visited.add(z);q.append(z)
   if len(pts)>=12:components.append({'pixels':len(pts),'bounds':[min(z[0]for z in pts),min(z[1]for z in pts),max(z[0]for z in pts)+1,max(z[1]for z in pts)+1]})
 probes={}
 for side in ['L','R']:
  for label,bone,index in [('hip','thigh.',0),('knee','shin.',0),('ankle','foot.',0)]:
   pt=j[str(i+1)][bone+side][index];xy=[round(pt[k]*scale+offset[k])for k in range(2)];probes[label+side]={'xy':xy,'alpha':al.getpixel(tuple(xy))}
 report['frames'].append({'phase':i,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'probes':probes,'componentsAlpha128':sorted(components,key=lambda v:-v['pixels'])})
(O/'alpha-joints.json').write_text(json.dumps(report,indent=2)+'\n')
# HTML draws source pixels as-is; no generated replacement, fitting, shifts or warps.
html=['<!doctype html><meta charset="utf-8"><title>E walk seams diagnostic</title><style>body{font:16px sans-serif;background:#eae3d4}main{display:grid;grid-template-columns:repeat(4,640px);gap:8px}figure{margin:0}canvas{image-rendering:pixelated;width:640px;height:640px}</style><h1>E Walk16 — green knee / red hip / blue ankle probes</h1><p>Actual immutable source pixels, 2× nearest display; crosshairs are diagnostic only.</p><main>']
for row in report['frames']:html.append(f'<figure><figcaption>phase {row["phase"]}/16</figcaption><canvas id="f{row["phase"]}" width="320" height="320"></canvas></figure>')
html.append('</main><script>const rows='+json.dumps(report['frames'])+';Promise.all(rows.map(async r=>{const im=new Image;im.src="../../../../art/characters-walk-v1/export-v2/renders/e/walk/"+String(r.phase).padStart(2,"0")+".png";await im.decode();const c=document.getElementById("f"+r.phase).getContext("2d");c.drawImage(im,0,0);for(const[n,p]of Object.entries(r.probes)){c.strokeStyle=n.startsWith("knee")?"lime":n.startsWith("hip")?"red":"blue";const[x,y]=p.xy;c.beginPath();c.moveTo(x-3,y);c.lineTo(x+3,y);c.moveTo(x,y-3);c.lineTo(x,y+3);c.stroke()}})).then(()=>document.body.dataset.ready="true")</script>')
(O/'review.html').write_text('\n'.join(html))
print(json.dumps({'kneeAlphaRanges':{side:[min(r['probes']['knee'+side]['alpha']for r in report['frames']),max(r['probes']['knee'+side]['alpha']for r in report['frames'])]for side in ['L','R']},'disconnectedLargeComponents':[{ 'phase':r['phase'],'components':r['componentsAlpha128']}for r in report['frames']if len(r['componentsAlpha128'])>1]},indent=2))
