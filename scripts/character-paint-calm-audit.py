"""Audit actual painted sole landmarks, never substitute guide coordinates for measurements."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math
root=Path(__file__).resolve().parents[1];p=root/'art/characters-walk-v1/calm-east-v5';m=json.loads((p/'animation-manifest.json').read_text());raw=[{'nearX':950,'farX':740},{'nearX':900},{'nearX':850},{'nearX':730},{'nearX':680,'farX':1000},{'farX':950},{'farX':800},{'farX':720}];annotated=[]
# Forefoot underside pixels manually selected from painted-soles-source-grid.jpg. Snap Y to actual alpha boundary.
for i,(frame,points)in enumerate(zip(m['frames'],raw)):
 im=Image.open(p/frame['source']).convert('RGBA');d=ImageDraw.Draw(im);record={'frame':i,'source':frame['source'],'rawWaistRoot':frame['rawWaistRoot'],'points':{},'uncertaintySourcePixels':8,'note':'manual visible forefoot-pad correspondence, not exact3Dground truth'}
 for foot in ['near','far']:
  if foot+'X' not in points:continue
  x=points[foot+'X'];ys=[y for y in range(1050,1220)if any(im.getpixel((xx,y))[3]>180 for xx in range(x-2,x+3))];y=max(ys);point=[x,y];record['points'][foot]={'source':point,'native':[x*.188+frame['wholeFrameTranslation'][0],y*.188+frame['wholeFrameTranslation'][1]]};d.ellipse((x-9,y-9,x+9,y+9),outline='#00ccff'if foot=='near'else'#ff00bb',width=3);d.text((x+12,y-25),f'{foot}:{x},{y}',fill='white')
 bg=Image.new('RGBA',im.size,'#645746');bg.alpha_composite(im);bg.convert('RGB').save(p/f'sole-landmark-{i}.jpg',quality=95);annotated.append(record)
# Full-cycle stride from actual half-cycle change of same painted forefoot pad, separate physical feet.
near_half=(950-m['frames'][0]['rawWaistRoot'][0])-(680-m['frames'][4]['rawWaistRoot'][0]);far_half=(1000-m['frames'][4]['rawWaistRoot'][0])-(740-m['frames'][0]['rawWaistRoot'][0]);stride_source=near_half+far_half;stride_native=stride_source*.188;stride_scene=stride_native*136/224
stance={}
for foot,indices in [('near',range(4)),('far',range(4,8))]:
 samples=[]
 for i in indices:
  marker=annotated[i]['points'][foot];x=marker['native'][0]+stride_native*i/8;samples.append({'frame':i,'worldNativeX':x,'worldNativeY':marker['native'][1]})
 xs=[s['worldNativeX']for s in samples];ys=[s['worldNativeY']for s in samples];stance[foot]={'samples':samples,'horizontalSpreadNativePixels':max(xs)-min(xs),'verticalSpreadNativePixels':max(ys)-min(ys),'horizontalSpreadScenePixels':(max(xs)-min(xs))*136/224}
report={'status':'NOT-FOOTPLANT-PASS','sourceStridePixels':stride_source,'nativeStridePixels':stride_native,'sceneStridePixelsAtHeight136':stride_scene,'uniformRawToNativeScale':.188,'nativeHeight':224,'sceneHeight':136,'cycleDurationMs':720,'halfCycleNearSourcePixels':near_half,'halfCycleFarSourcePixels':far_half,'units':'source1254canvas → packed320canvas via.188 → native scene pixels via136/224','landmarks':annotated,'stanceAuditAtConstantSpeed':stance,'limitations':['Manual correspondence uncertainty±8sourcepx','Painted boot rotation/shape changes and partial occlusion limit exact sole correspondence','Constant-speed support points drift beyond1scene pixel; this is not ready for production','Do not fix with unexplained movement multiplier or per-frame character scale']}
(p/'painted-sole-audit.json').write_text(json.dumps(report,indent=2)+'\n');m['strideCalibration']={k:report[k]for k in ['status','sourceStridePixels','nativeStridePixels','sceneStridePixelsAtHeight136','units']};m['paintedSoleAudit']='painted-sole-audit.json';(p/'animation-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps({k:report[k]for k in ['status','sourceStridePixels','nativeStridePixels','sceneStridePixelsAtHeight136','stanceAuditAtConstantSpeed']},indent=2))
