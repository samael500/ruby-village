"""Account scoped24 diagnostic renders and two isolated native sources."""
from pathlib import Path
import json,re,datetime
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/turn-variants-study'
frames=[];times=[]
for variant in ['right60','left120']:
 p=OUT/variant;review=json.loads((p/'render-check.json').read_text());assert review['actualRenderedPoseCount']==12 and review['allContained'];frames.extend(p.glob('E/*.png'))
 for time in re.findall(r'^Time: ([0-9:.]+)',(p/'render.log').read_text(),re.M):
  seconds=0.
  for part in time.split(':'):seconds=seconds*60+float(part)
  times.append(seconds)
assert len(frames)==len(times)==24
sources=list(OUT.glob('*/*.blend'));assert len(sources)==2
result={'status':'SCOPED TECHNICAL24POSE PROOF ONLY; NO FULL TURN BATCH','actualNativePngCount':24,'posesPerVariant':12,'cameraCount':1,'calibration':'base E,384px ortho1.70m,groundScale.65,one251to136scale','newPackedSourceCount':2,'packedSourceBytes':sum(p.stat().st_size for p in sources),'nativePngBytes':sum(p.stat().st_size for p in frames),'cyclesSamples':8,'blenderThreads':2,'cyclesReportedRenderWallSecondsTotal':sum(times),'cyclesReportedLongestRenderWallSeconds':max(times),'cpuUtilizationMeasured':False,'wallClockNote':'Reported Cycles wall intervals do not establish CPU utilization. No inferred cause for scheduling delays.','newRight120SourceOrRaster':False,'newPivotSourceOrRaster':False,'appearance':'rejected generic technical mannequin; no styled batch','donorSourcesChanged':False}
(OUT/'resource-budget.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
