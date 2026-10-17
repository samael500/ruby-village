"""Reproducibly split generated alpha sheet; no repainting or alpha synthesis."""
from PIL import Image
from collections import deque
from pathlib import Path
root=Path(__file__).resolve().parents[2]
im=Image.open(root/'art/characters-v1/ruta-pilot-sheet.png'); w,h=im.size
alpha=im.getchannel('A'); values=alpha.tobytes(); seen=bytearray(w*h); components=[]
for start in range(w*h):
 if seen[start] or values[start]<80: continue
 seen[start]=1; q=deque([start]); component=[]
 while q:
  p=q.popleft(); component.append(p); x=p%w
  for n in (p-w,p+w,p-1 if x else -1,p+1 if x<w-1 else -1):
   if 0<=n<w*h and not seen[n] and values[n]>=80: seen[n]=1; q.append(n)
 if len(component)>10000: components.append(component)
components.sort(key=lambda c:sum(p%w for p in c)/len(c))
assert len(components)==3, len(components)
for name,c in zip(['ruta-idle-pilot','ruta-portrait-pilot','ruta-back-study'],components):
 # Preserve original alpha including antialias edges within 2 pixels of its component.
 mask=Image.new('L',im.size); data=bytearray(w*h)
 for p in c: data[p]=255
 mask.frombytes(bytes(data))
 from PIL import ImageFilter,ImageChops
 mask=mask.filter(ImageFilter.MaxFilter(5)); out=im.copy(); out.putalpha(ImageChops.multiply(alpha,mask))
 box=out.getbbox(); out=out.crop(box); out.save(root/f'public/assets/characters-v1/{name}.png')
 print(name,box,out.size)
