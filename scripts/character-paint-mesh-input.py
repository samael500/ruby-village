"""Manual cutout masks from ONE painted east view, no per-phase painting."""
from PIL import Image,ImageDraw,ImageChops
from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];source=r/'art/characters-walk-v1/registered/e-01.png';out=r/'art/characters-walk-v1/mesh-pilot';out.mkdir(parents=True,exist_ok=True);image=Image.open(source).convert('RGBA')
parts={
'back-thigh':{'poly':[(158,171),(174,181),(157,214),(139,224),(121,215),(138,189)],'bone':'thigh.R','a':[165,178],'b':[140,211]},
'back-shin':{'poly':[(126,204),(150,213),(141,239),(117,244),(105,233)],'bone':'shin.R','a':[140,211],'b':[126,235]},
'back-boot':{'poly':[(172,224),(197,223),(203,230),(217,230),(222,244),(215,251),(184,257),(174,250)],'bone':'foot.R','a':[185,234],'b':[208,234]},
'front-thigh':{'poly':[(161,171),(183,174),(191,194),(194,214),(167,221),(155,192)],'bone':'thigh.L','a':[168,177],'b':[180,209]},
'front-shin':{'poly':[(166,202),(194,204),(197,234),(178,243),(166,233)],'bone':'shin.L','a':[180,209],'b':[185,234]},
'front-boot':{'poly':[(172,224),(197,223),(203,230),(217,230),(222,244),(215,251),(184,257),(174,250)],'bone':'foot.L','a':[185,234],'b':[208,234]}}
combined=Image.new('L',image.size)
for name,p in parts.items():
 mask=Image.new('L',image.size);ImageDraw.Draw(mask).polygon(p['poly'],fill=255);combined=ImageChops.lighter(combined,mask);piece=image.copy();piece.putalpha(ImageChops.multiply(image.getchannel('A'),mask));piece.save(out/f'{name}.png')
# Upper body remains original painted pixels. Overlap at hip deliberately covers cut seams.
mask=Image.new('L',image.size);ImageDraw.Draw(mask).rectangle((0,0,319,183),fill=255);body=image.copy();body.putalpha(ImageChops.multiply(image.getchannel('A'),mask));body.save(out/'body.png')
(out/'parts.json').write_text(json.dumps({'source':str(source.relative_to(r)),'status':'experimental-manual-cutout-not-final','canvas':[320,320],'footAnchor':[160,256],'parts':parts,'note':'small overlaps retain source cloth pixels; no independent phase generation; torso/face/hair/satchel remain ONE source image; east boot texture reused unmirrored for both sides in experimental pilot (hidden-side boot art not authored)'},indent=2)+'\n')
