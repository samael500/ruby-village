from pathlib import Path
from PIL import Image,ImageChops
from xml.etree import ElementTree as ET
import json
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;reports=json.loads((O/'report.json').read_text());results=[]
for run in reports:
 for page in run['pages']:
  if not page['rutaMarkup']:continue
  svg=ET.fromstring('<g>'+page['rutaMarkup']+'</g>')[0];x,y,w,h=map(float,svg.get('viewBox').split());href=svg[0].get('href');alpha=Image.open(R/'public'/href.split('/ruby-village/')[1]).getchannel('A').crop((round(x),round(y),round(x+w),round(y+h)));box=page['ruta']['box'];ruta=Image.new('L',tuple(run['viewport']));ruta.paste(alpha.resize((round(box['w']),round(box['h'])),Image.Resampling.LANCZOS),(round(box['x']),round(box['y'])));teacher=page['actors'][0];tbox=teacher['box'];ta=Image.open(R/'public'/teacher['href'].split('/ruby-village/')[1]).getchannel('A');other=Image.new('L',ruta.size);other.paste(ta.resize((round(tbox['w']),round(tbox['h'])),Image.Resampling.LANCZOS),(round(tbox['x']),round(tbox['y'])));over=ImageChops.multiply(ruta,other);count=sum(v>0 for v in over.get_flattened_data());assert count==0,(run['viewport'],page['state'],count);results.append({'viewport':run['viewport'],'state':page['state'],'teacherView':teacher['view'],'alphaOverlapAnyNonzero':count,'boundingBoxOverlap':page['rutaTeacherViewportBoxIntersection'],'method':'actual recorded native sprite frame crop and viewport matrix boxes; PIL Lanczos alpha resampling to viewport pixels; subpixel raster rounding stated'})
(O/'pairwise-alpha.json').write_text(json.dumps(results,indent=2)+'\n');print('PASS',len(results),'actual recorded state pairwisealpha0')
