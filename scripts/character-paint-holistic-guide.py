from pathlib import Path
from PIL import Image,ImageDraw
import math,json
out=Path(__file__).resolve().parents[1]/'art/characters-walk-v1/holistic-pilot-v4';sheet=Image.new('RGB',(1024,1024),'#eee5d3');poses=[]
for i in range(4):
 im=Image.new('RGB',(512,512),'#eee5d3');d=ImageDraw.Draw(im);hip=(256,285);near=[(310,445),(256,445),(202,445),(256,415)][i];far=[(202,439),(256,409),(310,439),(256,439)][i]
 # Ground sole semantic positions; two-link knee forced toward walking direction.
 def leg(foot,color):
  ankle=(foot[0]-12,foot[1]-18);dx=ankle[0]-hip[0];dy=ankle[1]-hip[1];dist=math.hypot(dx,dy);half=dist/2;bend=math.sqrt(max(0,91**2-half**2));knee=((hip[0]+ankle[0])/2+dy/dist*bend,(hip[1]+ankle[1])/2-dx/dist*bend);d.line([hip,knee,ankle],fill=color,width=35);d.ellipse((knee[0]-17,knee[1]-17,knee[0]+17,knee[1]+17),fill=color);d.rounded_rectangle((foot[0]-29,foot[1]-24,foot[0]+28,foot[1]),radius=8,fill=color);return [hip,knee,ankle,foot]
 farj=leg(far,'#d35c52');nearj=leg(near,'#3e79ca');d.rounded_rectangle((218,175,285,294),radius=30,fill='#777');d.ellipse((207,53,300,178),fill='#999');d.polygon([(293,103),(320,116),(294,124)],fill='#999');d.line((180,449,340,449),fill='#777',width=2);d.text((25,470),['1 NEAR BLUE FRONT contact / FAR RED back','2 NEAR BLUE planted / FAR RED passing','3 NEAR BLUE BACK / FAR RED front contact','4 NEAR BLUE passing / FAR RED planted'][i],fill='#222');sheet.paste(im,((i%2)*512,(i//2)*512));poses.append({'phase':i/4,'near':nearj,'far':farj})
sheet.save(out/'four-key-physical-guide.png');(out/'four-key-physical-guide.json').write_text(json.dumps(poses,indent=2)+'\n')
