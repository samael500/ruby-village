from pathlib import Path
import json,numpy as np
O=Path('/tmp/ruby-contact-forward-qa/docs/chapter-1-rc/qa/contact-forward/reproduced');d=json.loads((O/'diagnostic.json').read_text());c=json.loads((O/'forward-distance-curve.json').read_text());a=np.load(O/'actual-sole-samples.npz');m=json.loads((O/'sample-source.json').read_text());p=a['positions'];s=np.array([r['distanceMeters']for r in c['samples']]);t=a['sample_times'];rows=[]
# Per-material-vertex intervals, no changing centroid. Main soft weight >10% of own rest area.
for j in range(p.shape[1]):
 active=np.maximum(0,1-np.maximum(0,p[:,j,2]-c['contactInference']['floorM'])/.0175)**2>.1
 starts=np.where(active & ~np.r_[False,active[:-1]])[0];ends=np.where(active & ~np.r_[active[1:],False])[0]
 for lo,hi in zip(starts,ends):
  if t[hi]-t[lo]<.03:continue
  f=-p[lo:hi+1,j,1];cur=f+s[lo:hi+1];uni=f+c['strideMeters']/c['durationSeconds']*t[lo:hi+1]
  rows.append({'vertex':m['columnVertexIds'][j],'side':m['columnSides'][j],'region':m['columnRegions'][j],'firstSample':int(lo),'lastSample':int(hi),'seconds':float(t[hi]-t[lo]),'curveForwardSpanM':float(np.ptp(cur)),'sameStrideUniformForwardSpanM':float(np.ptp(uni))})
(O/'material-point-drift-intervals.json').write_text(json.dumps({'definition':'one fixed material vertex, weight/restarea>.1, contiguous non-wrapped interval >=30ms; span not net displacement','intervals':rows},indent=2)+'\n')
d['materialPointIntervals']={'count':len(rows),'curveForwardSpanMedianM':float(np.median([x['curveForwardSpanM']for x in rows])),'curveForwardSpanMaxM':max(x['curveForwardSpanM']for x in rows),'sameStrideUniformSpanMedianM':float(np.median([x['sameStrideUniformForwardSpanM']for x in rows])),'sameStrideUniformSpanMaxM':max(x['sameStrideUniformForwardSpanM']for x in rows)}
(O/'diagnostic.json').write_text(json.dumps(d,indent=2)+'\n')
W,H=1000,420
pts=lambda values,low,high:' '.join(f'{60+880*i/(len(values)-1):.2f},{350-280*(float(v)-low)/(high-low):.2f}'for i,v in enumerate(values))
v=[x['velocityMps']for x in c['samples']]
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="420" viewBox="0 0 1000 420"><rect width="1000" height="420" fill="white"/><g font-family="sans-serif" font-size="16" fill="#222"><text x="50" y="28">B source Walk — candidate forward speed, native world m/s; NOT no-slip proof</text><text x="50" y="385">0s → 1.666667s; blue fitted 25ms smoothing, orange same-stride constant</text><text x="50" y="410">Height-inferred support gaps are interpolated; no ankle contacts or camera fitting.</text><text x="10" y="75">1.0</text><text x="10" y="350">0.6</text></g><path d="M60 70V350H940" fill="none" stroke="#aaa"/><polyline points="{pts(v,.6,1)}" fill="none" stroke="#236bb0" stroke-width="3"/><polyline points="{pts([c['strideMeters']/c['durationSeconds']]*481,.6,1)}" fill="none" stroke="#d47827" stroke-width="2"/></svg>'''
(O/'velocity-diagnostic.svg').write_text(svg)
print(json.dumps({'sensitivity':[(r['heightBandM'],r['strideM'],r['contactAware'],r['zeroTotalWeightFraction'],r['bothFootConfidenceFraction'])for r in d['heightBandSensitivity']],'drift':d['materialPointIntervals']},indent=2))
