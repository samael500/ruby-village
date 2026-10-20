from pathlib import Path
from PIL import Image
import json
O=Path(__file__).resolve().parent;A=O.parent
def scan(P,threshold):
 im=Image.open(P).convert('RGBA');w,h=im.size;a=im.getchannel('A').tobytes();seen=bytearray(w*h);out=[];tiny=[]
 for q,v in enumerate(a):
  if v<=threshold or seen[q]:continue
  todo=[q];seen[q]=1;n=0;mnx=w;mny=h;mxx=mxy=0
  while todo:
   p=todo.pop();n+=1;x=p%w;y=p//w;mnx=min(mnx,x);mxx=max(mxx,x);mny=min(mny,y);mxy=max(mxy,y)
   for xx,yy in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=xx<w and 0<=yy<h:
     j=yy*w+xx
     if not seen[j]and a[j]>threshold:seen[j]=1;todo.append(j)
  (out if n>100 else tiny).append({'pixelCount':n,'bbox':[mnx,mny,mxx+1,mxy+1]})
 out=sorted(out,key=lambda v:(int((v['bbox'][1]+v['bbox'][3])/2/400),v['bbox'][0]));assert len(out)==12,(P,len(out));return {'size':[w,h],'actors':out,'tiny':tiny}
rows=[]
for k in range(4):
 print('SCAN_QUARTER',k,flush=True);v={str(t):scan(A/f'e-quarter{k}/painted-sheet-v1.png',t)for t in[16,128]};actors=v['16']['actors'];xl=max(a['bbox'][2]-(i%4+1)*330 for i,a in enumerate(actors));xu=min(a['bbox'][0]-i%4*330 for i,a in enumerate(actors));yl=max(a['bbox'][3]-(i//4+1)*400 for i,a in enumerate(actors));yu=min(a['bbox'][1]-i//4*400 for i,a in enumerate(actors));assert xl<=xu and yl<=yu,(k,xl,xu,yl,yu);ox=0 if xl<=0<=xu else round((xl+xu)/2);oy=-11 if k==0 else round((yl+yu)/2);assert yl<=oy<=yu;rows.append({'quarter':k,'gridSourceOrigin':[ox,oy],'pitch':[330,400],'feasibleOriginRange':{'x':[xl,xu],'y':[yl,yu]},'thresholds':v});print(k,[ox,oy],v['128']['size'],flush=True)
(O/'quarter-scans.json').write_text(json.dumps({'status':'measured-shared-grid-proposals-no-frame-fit','quarters':rows},indent=2)+'\n')
