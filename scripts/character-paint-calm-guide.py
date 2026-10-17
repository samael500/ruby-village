from PIL import Image,ImageDraw
from pathlib import Path
import math,json
p=Path(__file__).resolve().parents[1]/'art/characters-walk-v1/calm-east-v5';p.mkdir(exist_ok=True);poses=[]
for i in range(4):
 im=Image.new('RGB',(627,627),'#eee5d3');d=ImageDraw.Draw(im);hip=(360,350);near=[(410,555),(360,555),(310,555),(360,540)][i];far=[(310,553),(360,538),(410,553),(360,553)][i]
 def leg(ankle,color):
  dx=ankle[0]-hip[0];dy=ankle[1]-hip[1];distance=math.hypot(dx,dy);bend=math.sqrt(max(0,108**2-distance**2/4));k=((hip[0]+ankle[0])/2+dy/distance*bend,(hip[1]+ankle[1])/2-dx/distance*bend);d.line([hip,k,ankle],fill=color,width=42);d.ellipse((k[0]-21,k[1]-21,k[0]+21,k[1]+21),fill=color);d.rounded_rectangle((ankle[0]-25,ankle[1]-10,ankle[0]+60,ankle[1]+40),radius=12,fill=color);return{'hip':hip,'knee':k,'ankle':ankle,'soleHeel':[ankle[0]-20,ankle[1]+40],'soleToe':[ankle[0]+55,ankle[1]+40]}
 farj=leg(far,'#ca615c');nearj=leg(near,'#477ec3');d.rounded_rectangle((320,200,390,367),radius=30,fill='#888');d.ellipse((305,55,415,200),fill='#999');d.polygon([(405,120),(435,137),(407,150)],fill='#999');d.line((318,230,300,325,310,380),fill='#aaa',width=20);d.line((388,230,403,330,396,381),fill='#aaa',width=20);d.line((250,596,490,596),fill='#444',width=1);im.save(p/f'guide-key-{i}.png');poses.append({'phase':i/4,'near':nearj,'far':farj,'camera':'same right-facing profile','nearPhysicalIdentity':'cargo pocket leg','armGuide':'hands relaxed below waist, small contra-swing'})
(p/'guide-contract.json').write_text(json.dumps({'sourceCanvas':[627,627],'root':[360,350],'scaleTo320':.37,'targetDisplayHeight':136,'cycleDurationMs':720,'nearSoleHalfCycleDeltaSource':100,'derivedDisplayStridePixels':100*.37*2*136/224,'keys':poses},indent=2)+'\n')
