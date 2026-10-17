"""Review-only comparison sheets from actual map/scene assets; no product graphics generated."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];out=root/'docs/chapter-1-rc/art/map-match-gate-bakery';sheet=Image.new('RGB',(1560,1020),'#f8efd8');d=ImageDraw.Draw(sheet)
for row,name,box in [(0,'gate',(170,45,650,430)),(1,'bakery',(1030,10,1640,440))]:
 folder=root/'art/chapter-1-map-match'/name
 for col,title,image in [(0,'Approved map',Image.open(folder/'map-reference.png')),(1,'Before',Image.open(folder/'before.png').crop(box)),(2,'Map-match candidate',Image.open(folder/'core-candidate.png').crop(box))]:
  image.thumbnail((495,430));x=col*520+12;y=row*510+50;sheet.paste(image,(x,y));d.text((x,row*510+15),f'{name}: {title}',fill='#48321f')
sheet.save(out/'map-before-after-comparison.jpg',quality=96)
