"""Flatten actual export renders on a neutral background for anatomy/phase inspection."""
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1];source=root/'art/characters-walk-v1/export-v2/renders';out=root/'docs/chapter-1-rc/painted-motion'
for variant in ['base','calibrated-1']:
 sheet=Image.new('RGB',(1280,1440),'#f9efd9');draw=ImageDraw.Draw(sheet)
 for row,direction in enumerate(['e','se','sw','w','nw','ne']):
  view=direction if variant=='base' else variant+'-'+direction
  for col,index in enumerate([0,4,8,12]):
   path=source/view/'walk'/f'{index:02}.png';im=Image.open(path).crop((64,0,256,288)).resize((144,216));sheet.paste(im,(col*320+85,row*240+20),im);draw.text((col*320+10,row*240+5),f'{view} phase {index}/16',fill='#432')
 sheet.save(out/f'v2-{variant}-six-view-contact.jpg',quality=94)
for direction in ['e','se','sw','w','nw','ne']:
 sheet=Image.new('RGB',(1152,472),'#f9efd9');draw=ImageDraw.Draw(sheet)
 for index in range(16):
  im=Image.open(source/direction/'walk'/f'{index:02}.png').crop((64,0,256,288)).resize((144,216));x=(index%8)*144;y=(index//8)*236;sheet.paste(im,(x,y+20),im);draw.text((x+5,y+3),f'{direction} {index}/16',fill='#432')
 sheet.save(out/f'v2-{direction}-walk-all16.jpg',quality=95)
 samples=[('idle',0),('idle',8)]+[('start',i) for i in [0,2,4,6,8]]+[('stop-L',i) for i in [0,4,8]]+[('stop-R',i) for i in [0,4,8]];sheet=Image.new('RGB',(1152,472),'#f9efd9');draw=ImageDraw.Draw(sheet)
 for index,(state,frame) in enumerate(samples):
  im=Image.open(source/direction/state/f'{frame:02}.png').crop((64,0,256,288)).resize((144,216));x=(index%8)*144;y=(index//8)*236;sheet.paste(im,(x,y+20),im);draw.text((x+5,y+3),f'{state} {frame}',fill='#432')
 sheet.save(out/f'v2-{direction}-transitions.jpg',quality=95)
