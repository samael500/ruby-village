"""Pack whole-pose calm E candidate with ONE scale and explicit waist-root registration."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
root=Path(__file__).resolve().parents[1];p=root/'art/characters-walk-v1/calm-east-v5';out=p/'frames';out.mkdir(exist_ok=True)
spec=[('key-0-tight.png',[796,630]),('between-1-raw.png',[796,627]),('key-1-passing.png',[817,630]),('between-3-fixed.png',[797,628]),('key-2-raw.png',[806,630]),('between-5-contact-cleanup.png',[803,631]),('key-3-passing.png',[787,630]),('between-7-contact-cleanup.png',[805,629])]
items=[];sheet=Image.new('RGB',(1280,690),'#eee5d3');d=ImageDraw.Draw(sheet);feet=Image.new('RGB',(2800,580),'#eee5d3');fd=ImageDraw.Draw(feet)
for i,(filename,waist)in enumerate(spec):
 im=Image.open(p/filename).convert('RGBA');assert im.size==(1254,1254);offset=[round(160-waist[0]*.188),round(149-waist[1]*.188)];frame=im.transform((320,320),Image.Transform.AFFINE,(1/.188,0,-offset[0]/.188,0,1/.188,-offset[1]/.188),Image.Resampling.BICUBIC);frame.save(out/f'{i:02}.png');x=(i%4)*320;y=(i//4)*345;sheet.paste(frame,(x,y),frame);d.text((x+10,y+323),f'{i}/8 whole frame / 90ms',fill='#333');d.ellipse((x+157,y+146,x+163,y+152),outline='#02a75f',width=1)
 crop=im.crop((400,1000,1100,1254));cx=(i%4)*700;cy=(i//4)*290;feet.paste(crop,(cx,cy),crop);fd.text((cx+5,cy+260),f'phase{i}: source crop x400..1100 y1000..1254',fill='#333')
 for sx in range(400,1100,100):fd.line((cx+sx-400,cy,cx+sx-400,cy+254),fill='#a99');fd.text((cx+sx-398,cy+2),str(sx),fill='#222')
 for sy in [1050,1100,1150,1200]:fd.line((cx,cy+sy-1000,cx+700,cy+sy-1000),fill='#a99');fd.text((cx+2,cy+sy-998),str(sy),fill='#222')
 items.append({'index':i,'phase':i/8,'file':f'frames/{i:02}.png','source':filename,'sourceSha256':hashlib.sha256((p/filename).read_bytes()).hexdigest(),'rawWaistRoot':waist,'nativeWaistRoot':[160,149],'wholeFrameTranslation':offset,'durationMs':90,'nearCargoPocketLeg': 'planted' if i<4 else 'swing','farPlainLeg':'swing'if i<4 else'planted'})
manifest={'status':'whole-pose-pilot-needs-motion-audit-and-art-review','productionEnabled':False,'cycleDurationMs':720,'frameSize':[320,320],'footAnchor':[160,256],'nativeHeight':224,'sceneDisplayHeight':136,'sourceCanvas':[1254,1254],'uniformRawToNativeScale':.188,'nativeToSceneScale':136/224,'registration':'translation only by visible waist-buckle center; no bbox/headmass normalization, no per-frame size scaling','frames':items}
(p/'animation-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');sheet.save(root/'docs/chapter-1-rc/painted-motion/calm-east-v5-all8.jpg',quality=96);feet.save(p/'painted-soles-source-grid.jpg',quality=97)
print('8wholeframes packed, one.188 scale,90ms/frame; footplant not certified')
