from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-sprites-v2/full48/painted-sheet-v1.png');M=Path('/tmp/ruby-painted-native-pack/art/ruta-native-painted-sprites-v2/packing/semantic-pivot-trial/manifest.json');im=Image.open(P).convert('RGBA');n=json.loads((O/'native-head-projections.json').read_text());m=json.loads(M.read_text());S=m['fixedScale'];rows=[]
for i in range(48):
 ox=i%8*162;oy=30+i//8*200;pts=[]
 for y in range(34,65):
  for x in range(96,118):
   r,g,b,a=im.getpixel((ox+x,oy+y))
   if a>=128 and b>r*1.15 and b>g*1.03 and b>70:pts.append([x,y])
 p=[sum(v[j]for v in pts)/len(pts)for j in range(2)]if pts else None;t=m['frames'][i]['translationNativeComparisonPx'];h=n['rows'][i]['features']['Head bone head']['nativeFullPx'];rows.append({'phase':i,'visibleBluePatchCentreRawPx':p,'selectedPixelCount':len(pts),'selectedRawPixels':pts,'definition':'centroid of visible chromatically blue iris-region pixels; NOT anatomical iris/pupil centre','review':'all six magnified ruler rows visually inspected; blue samples lie at visible eye, tiny/desaturated mask can bias centre','uncertaintyRawPx':1.5 if len(pts)<3 and pts else 1. if pts else None,'nullMeaning':'no threshold-selected chromatic pixels; eye still visually exists; NOT occluded/missing-eye inference'if not pts else None,'trialTranslationNativeComparisonPx':t,'nativeHeadHalfPx':[v/2 for v in h],'trialEyeNativeComparisonPx':[S*p[j]+m['baselineDisplayOrigin'][j]+t[j]for j in range(2)]if p else None})
checks=[]
for i,a in enumerate(rows):
 b=rows[(i+1)%48];p=a['visibleBluePatchCentreRawPx'];q=b['visibleBluePatchCentreRawPx'];h=a['nativeHeadHalfPx'];k=b['nativeHeadHalfPx']
 if p and q:
  dr=[q[j]-p[j]for j in range(2)];e=[b['trialEyeNativeComparisonPx'][j]-a['trialEyeNativeComparisonPx'][j]-(k[j]-h[j])for j in range(2)];checks.append({'from':i,'to':(i+1)%48,'rawEyeDeltaPx':dr,'afterTrialMinusNativeHeadBobDeltaNativeComparisonPx':e,'residualNormPx':math.hypot(*e),'annotationWorstCaseDifferenceRawPx':a['uncertaintyRawPx']+b['uncertaintyRawPx'],'notExactMotionResidual':'Head bone pivot is not authored eye feature; true head rotation/gaze, repaint shape/color and threshold bias remain'})
report={'status':'HEAD-JITTER-DIAGNOSTIC-NOT-FIX-NOT-ANATOMICAL-CORRESPONDENCE','rawSha256':hashlib.sha256(P.read_bytes()).hexdigest(),'trialManifestSha256':hashlib.sha256(M.read_bytes()).hexdigest(),'nativeProjectionSha256':hashlib.sha256((O/'native-head-projections.json').read_bytes()).hexdigest(),'fixedScale':S,'coordinateUnits':'raw162x200 cell unless nativeComparison specified (256x320 source half)','rows':rows,'worstAdjacentResiduals':sorted(checks,key=lambda x:x['residualNormPx'],reverse=True),'unmeasured':['exact nose tip is not separable at raw profile resolution','anatomical iris centre differs from visible chromatic patch','two reliable widely separated head landmarks absent, so no defensible scale/rotation estimate from this table','No pixel/atlas/pivot edits or implemented correction']};(O/'eye-patch-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report['worstAdjacentResiduals'][:8],indent=2))
