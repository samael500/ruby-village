from pathlib import Path
from PIL import Image
import json,collections
root=Path(__file__).resolve().parents[1];folder=root/'art/characters-walk-v1/holistic-pilot-v4';sheet=Image.open(folder/'four-key-whole-01.png').convert('RGBA');w=sheet.width//2;out=folder/'frames';out.mkdir(exist_ok=True);report=[]
for i in range(4):
 im=(Image.open(folder/'opposite-contact-01.png').convert('RGBA').resize((w,w),Image.Resampling.LANCZOS) if i==2 else sheet.crop(((i%2)*w,(i//2)*w,(i%2+1)*w,(i//2+1)*w)))
 alpha=im.getchannel('A');strong=alpha.point(lambda a:255 if a>64 else 0);bounds=strong.getbbox();xs=[]
 # Register head/hair mass, not swinging boot bounds; translation only after one uniform source scale.
 for y in range(bounds[1],min(bounds[3],bounds[1]+170)):
  for x in range(bounds[0],bounds[2]):
   if strong.getpixel((x,y)):xs.append(x)
 center=sum(xs)/len(xs);scale=.37;resized=im.resize((round(w*scale),round(w*scale)),Image.Resampling.LANCZOS);offset=[round(160-center*scale),round(256-bounds[3]*scale)];canvas=Image.new('RGBA',(320,320));canvas.alpha_composite(resized,tuple(offset));canvas.save(out/f'{i:02}.png');report.append({'phase':i/4,'source':'opposite-contact-01.png'if i==2 else'four-key-whole-01.png','cell':i,'sourceCellSize':w,'uniformSourceScale':scale,'translation':offset,'groundSoleRegistration':'visible alpha sole baseline256; not physical footplant verification','durationMs':180})
(folder/'pilot-registration.json').write_text(json.dumps({'status':'four-key coarse pilot, no production','cycleDurationMs':720,'frameSize':[320,320],'frames':report,'warning':'Only4keys; no start/stop/turn, no six-direction set; phase/anatomy/identity need actual loop review'},indent=2)+'\n')
