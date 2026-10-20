from pathlib import Path
from PIL import Image,ImageChops
from xml.etree import ElementTree as ET
import json
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;out=[]
for p in O.glob('*/*/report.json'):
 run=json.loads(p.read_text());w,h=run['viewport']
 for state in run['states']:
  if not state['ruta']:continue
  svg=ET.fromstring('<g>'+state['ruta']['markup']+'</g>')[0];x,y,sw,sh=map(float,svg.get('viewBox').split());href=svg[0].get('href');alpha=Image.open(R/'public'/href.split('/ruby-village/')[1]).getchannel('A').crop((round(x),round(y),round(x+sw),round(y+sh)));box=state['ruta']['box'];mask=Image.new('L',(w,h));mask.paste(alpha.resize((round(box['w']),round(box['h'])),Image.Resampling.LANCZOS),(round(box['x']),round(box['y'])))
  for actor in state['actors']:
   a=Image.open(R/'public'/actor['href'].split('/ruby-village/')[1]).getchannel('A');box=actor['box'];other=Image.new('L',(w,h));other.paste(a.resize((round(box['w']),round(box['h'])),Image.Resampling.LANCZOS),(round(box['x']),round(box['y'])));over=ImageChops.multiply(mask,other);count=sum(v>0 for v in over.get_flattened_data());out.append(dict(scene=run['scene'],viewport=[w,h],state=state['label'],actor=actor['id'],view=actor['view'],overlapAnyAlphaViewportPixels=count,bounds=over.getbbox()))
(O/'pairwise.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
