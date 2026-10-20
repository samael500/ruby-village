"""Split a transparent model/pose source sheet by connected alpha components.
Usage: python3 ... sheet.png output-directory sprite portrait [--rows]
Keeps source RGB/alpha. Does not repaint, key a backdrop, or synthesize alpha.
"""
from PIL import Image,ImageFilter,ImageChops
from collections import deque
from pathlib import Path
import sys,json
source=Path(sys.argv[1]);dest=Path(sys.argv[2]);rows='--rows' in sys.argv;names=[n for n in sys.argv[3:] if n!='--rows'];dest.mkdir(parents=True,exist_ok=True)
im=Image.open(source).convert('RGBA');w,h=im.size;alpha=im.getchannel('A');values=alpha.tobytes();seen=bytearray(w*h);components=[]
for start in range(w*h):
 if seen[start] or values[start]<80:continue
 seen[start]=1;q=deque([start]);c=[]
 while q:
  p=q.popleft();c.append(p);x=p%w
  for n in (p-w,p+w,p-1 if x else -1,p+1 if x<w-1 else -1):
   if 0<=n<w*h and not seen[n] and values[n]>=80:seen[n]=1;q.append(n)
 if len(c)>2000:components.append(c)
def center(c):return (sum(p%w for p in c)/len(c),sum(p//w for p in c)/len(c))
components.sort(key=lambda c: (int(center(c)[1]//(h/2)),center(c)[0]) if rows else center(c)[0])
print('components',[(len(c),center(c)) for c in components])
assert len(components)==len(names),(len(components),names)
report=[]
for name,c in zip(names,components):
 mask=Image.new('L',im.size);data=bytearray(w*h)
 for p in c:data[p]=255
 mask.frombytes(bytes(data));mask=mask.filter(ImageFilter.MaxFilter(5));out=im.copy();out.putalpha(ImageChops.multiply(alpha,mask));box=out.getbbox();out=out.crop(box);out.save(dest/f'{name}.png');report.append({'id':name,'sheetRect':list(box),'frameSize':list(out.size),'alphaRange':list(out.getchannel('A').getextrema())})
(dest/(source.stem+'-extraction.json')).write_text(json.dumps(report,indent=2)+'\n')
