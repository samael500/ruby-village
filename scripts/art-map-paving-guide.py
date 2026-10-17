"""Immutable route geometry and painted-paving edit guide; guide is never delivered."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import re,json
R=Path(__file__).resolve().parents[1];A=R/'art/chapter-map-v2';S=R/'src/map-trails.ts';routes=re.findall(r"\['([^']+)','([^']+)'\]",S.read_text());assert len(routes)==7

def points(d):
 t=re.findall(r'[MCSL]|-?\d+(?:\.\d+)?',d);i=0;cmd=None;p=(0.,0.);last=None;out=[]
 while i<len(t):
  if t[i]in'MCSL':cmd=t[i];i+=1
  n={'M':2,'L':2,'C':6,'S':4}[cmd];v=list(map(float,t[i:i+n]));i+=n
  if cmd=='M':p=tuple(v);out.append(p);last=None
  elif cmd=='L':p=tuple(v);out.append(p);last=None
  else:
   if cmd=='C':a=tuple(v[:2]);b=tuple(v[2:4]);end=tuple(v[4:])
   else:a=(2*p[0]-last[0],2*p[1]-last[1])if last else p;b=tuple(v[:2]);end=tuple(v[2:])
   for k in range(1,81):
    q=k/80;z=1-q;out.append((z**3*p[0]+3*z*z*q*a[0]+3*z*q*q*b[0]+q**3*end[0],z**3*p[1]+3*z*z*q*a[1]+3*z*q*q*b[1]+q**3*end[1]))
   p=end;last=b
 return out
im=Image.open(A/'accepted-map-before.webp').convert('RGB');guide=im.copy();draw=ImageDraw.Draw(guide);allroutes=[];native=im.size;scale=native[0]/1000
for id,d in routes:
 ps=points(d);allroutes.append({'id':id,'path':d,'start':list(ps[0]),'end':list(ps[-1]),'samples':[list(p)for p in ps]});xy=[(x*scale,y*native[1]/400)for x,y in ps];draw.line(xy,fill='#d03e88',width=round(3*scale),joint='curve')
 mask=Image.new('L',(1000,400));ImageDraw.Draw(mask).line(ps,fill=255,width=20,joint='curve');mask=mask.filter(ImageFilter.GaussianBlur(2));mask.save(A/f'route-{id}-corridor.png')
guide.save(A/'paving-guide.png');im.resize((1000,400),Image.Resampling.LANCZOS).save(A/'accepted-map-native1000.png');(A/'routes.json').write_text(json.dumps({'viewBox':[0,0,1000,400],'routes':allroutes,'source':'src/map-trails.ts','deliveredGuide':False},indent=2)+'\n')
