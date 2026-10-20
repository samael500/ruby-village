"""Audit actual resident alpha against full accepted playable polygons.
This measures candidate anchors; it does not accept artwork or invent missing anchors.
"""
import json
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
manifest=json.loads((root/'public/assets/chapter-1/v9/manifest.json').read_text())
residents=json.loads((root/'public/assets/characters-v1/residents-manifest.json').read_text())['characters']
delivery=json.loads((root/'public/assets/characters-v1/delivery-manifest.json').read_text())['deliveries']
ids={'garden':['rabbit'],'well':['teacher'],'bakery':['baker'],'stream':['squirrel'],'mill':['miller','squirrel'],'post':['hedgehog']}
checks=[]
for scene,actors in ids.items():
 engine=json.loads((root/f'docs/blender-chapter-1/layouts/engine/{scene}.json').read_text())
 playable=Image.new('1',(1672,941));draw=ImageDraw.Draw(playable)
 for cell in engine['cells']:
  if cell['terrain'] in ['ground','water']:draw.polygon([(p['x'],p['y']) for p in cell['polygon']],fill=1)
 for index,actor in enumerate(actors):
  key='residentFeet' if index==0 else 'secondResidentFeet';anchor=manifest['scenes'][scene].get('semanticAnchors',{}).get(key)
  if not anchor:checks.append({'scene':scene,'resident':actor,'result':'missing-semantic-anchor'});continue
  source=residents[actor];frame=source['frames']['idle'];frame=delivery.get(frame['image'],frame)
  alpha=Image.open(root/'public/assets/characters-v1'/frame['image']).getchannel('A')
  scale=source['sceneHeightPx']/frame['frameSize'][1];width=round(alpha.width*scale);height=round(alpha.height*scale)
  alpha=alpha.resize((width,height),Image.Resampling.LANCZOS)
  x=round(anchor['x']-frame['footAnchor'][0]*scale);y=round(anchor['y']-frame['footAnchor'][1]*scale)
  overlap=0
  for row in range(height):
   for col in range(width):
    xx=x+col;yy=y+row
    if 0<=xx<1672 and 0<=yy<941 and alpha.getpixel((col,row))>32 and playable.getpixel((xx,yy)):overlap+=1
  checks.append({'scene':scene,'resident':actor,'feet':[anchor['x'],anchor['y']],'bounds':[x,y,width,height],'opaquePixelsOverPlayablePolygons':overlap,'result':'clear' if overlap==0 else 'failed-clearance','scope':'candidate source anchor, actual optimized sprite alpha; visual scene review still required'})
out=root/'docs/chapter-1-rc/art/coordinator-review/resident-clearance.json';out.write_text(json.dumps(checks,indent=2)+'\n');print(json.dumps(checks,indent=2))
