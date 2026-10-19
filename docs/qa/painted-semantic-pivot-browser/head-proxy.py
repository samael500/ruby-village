from pathlib import Path
from PIL import Image
import json,math,statistics
O=Path(__file__).resolve().parent;m=json.load(open(O/'report.json'))['manifest'];paint=Image.open('/tmp/ruby-painted-native48-qa/art/ruta-native-painted-sprites-v2/full48/painted-sheet-v1.png').convert('RGBA');native=Image.open('/tmp/ruby-painted-native48-qa/art/ruta-native-painted-sprites-v2/full48/pose-source-48.png').convert('RGBA');rows=[]
for i,f in enumerate(m['frames']):
 x,y,w,h=f['paintedRect'];a=paint.crop((x,y,x+w,y+h)).getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();x,y,w,h=f['nativeRect'];b=native.crop((x,y,x+w,y+h)).getchannel('A').point(lambda v:255 if v>=128 else 0).getbbox();base=m['fixedScale']*a[1]+m['baselineDisplayOrigin'][1];cand=base+f['translationNativeComparisonPx'][1];rows.append({'phase':i,'rawCrown':a[1],'nativeCrown':b[1],'baselineCrownComparisonPx':base,'candidateCrownComparisonPx':cand,'baselineResidual':base-b[1],'candidateResidual':cand-b[1]})
summary={}
for key in ['baseline','candidate']:
 values=[r[key+'Residual']for r in rows];mean=statistics.mean(values);steps=[{'phases':[(i-1)%48,i],'residualDeltaNativePx':values[i]-values[(i-1)%48]}for i in range(48)];summary[key]={'centeredRmsNativePx':math.sqrt(statistics.mean((v-mean)**2 for v in values)),'centeredPeakToPeakNativePx':max(values)-min(values),'worstSteps':sorted(steps,key=lambda r:-abs(r['residualDeltaNativePx']))[:12],'cycleClosesByConstruction':'phaseindexedarraysperiodic; noaccumulatingtranslation'}
(O/'head-proxy.json').write_text(json.dumps({'scope':'heldoutalpha128crownonlynotheadjointorfaceidentity; hairshape/viewocclusionuncertainty;notfit','summary':summary,'rows':rows},indent=2)+'\n');print(summary)
