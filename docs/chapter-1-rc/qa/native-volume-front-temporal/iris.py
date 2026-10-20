"""Diagnostics only. Whole native PNG iris-color connected components; no registration/edits."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--require48',action='store_true');args=p.parse_args();D=Path(args.source);O=Path(__file__).resolve().parent;files=sorted(D.glob('*.png'))
if args.require48:assert len(files)==48
rows=[]
for f in files:
 a=np.array(Image.open(f).convert('RGBA'));r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);mask=(a[:,:,3]>200)&(b>70)&(b>r*1.2)&(g>r*1.1)&(b>g*.9);seen=np.zeros(mask.shape,bool);comps=[]
 for y,x in np.argwhere(mask):
  if seen[y,x]:continue
  stack=[(int(y),int(x))];seen[y,x]=True;pts=[]
  while stack:
   yy,xx=stack.pop();pts.append((xx,yy))
   for dy,dx in [(0,1),(0,-1),(1,0),(-1,0)]:
    ny,nx=yy+dy,xx+dx
    if 0<=ny<mask.shape[0]and 0<=nx<mask.shape[1]and mask[ny,nx]and not seen[ny,nx]:seen[ny,nx]=True;stack.append((ny,nx))
  if len(pts)>=4:
   q=np.array(pts);comps.append({'areaPixels':len(pts),'centerXY':q.mean(axis=0).tolist(),'bbox':[int(q[:,0].min()),int(q[:,1].min()),int(q[:,0].max()+1),int(q[:,1].max()+1)]})
 comps.sort(key=lambda c:c['areaPixels'],reverse=True);selected=sorted(comps[:2],key=lambda c:c['centerXY'][0]);entry={'phase':int(f.stem),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'components':comps,'twoLargestSortedX':selected,'confidence':'requires visual component overlay review; iris-color region centroid, not anatomical eye center'}
 if len(selected)==2:
  cs=np.array([x['centerXY']for x in selected]);entry.update(midpoint=cs.mean(axis=0).tolist(),interIrisDistancePixels=float(np.linalg.norm(cs[1]-cs[0])))
 rows.append(entry)
(O/('iris-all48.json'if args.require48 else'iris-probe.json')).write_text(json.dumps({'threshold':'alpha>200,B>70,B>1.2R,G>1.1R,B>.9G;4connected,minarea4','frames':rows,'limits':'Thresholded visible blue-region centroid/area depends on antialiasing, occlusion, gaze and shading. Not exact joints; no fit/warp/production registration.'},indent=2)+'\n')
