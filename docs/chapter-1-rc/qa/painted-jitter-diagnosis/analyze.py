from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
O=Path(__file__).resolve().parent; R=O.parents[3]; P=R/'art/ruta-native-painted-sprites-v2/packing'; M=json.loads((P/'semantic-pivot-trial/manifest.json').read_text()); B=json.loads((P/'full48/manifest.json').read_text()); S=M['fixedScale']
at=np.asarray(Image.open(P/'full48'/B['paintedAtlas']['path']).convert('RGBA'),dtype=float)/255
cells=[]
for r in B['frames']:
 x,y,w,h=r['paintedRect'];a=at[y:y+h,x:x+w];cells.append(a[:,:,:3]*a[:,:,3:]+(1-a[:,:,3:])*.9)
# Integer rigid-translation search only, no output raster or metadata changes.
# Different fixed head windows provide independent consistency diagnostic.
def track(a,b,rect):
 x0,y0,x1,y1=rect;ref=a[y0:y1,x0:x1];v=[]
 for dy in range(-12,13):
  for dx in range(-10,11):
   q=b[y0+dy:y1+dy,x0+dx:x1+dx];v.append((float(np.mean((q-ref)**2)),dx,dy))
 v.sort();err,dx,dy=v[0];return {'shiftNextMinusCurrentRawPx':[dx,dy],'rgbRmsAfterBestIntegerTranslation':err**.5,'rgbRmsNoTranslation':float(np.sqrt(np.mean((b[y0:y1,x0:x1]-ref)**2))),'boundaryMinimum':abs(dx)==10 or abs(dy)==12}
# Top/crown core avoids cell boundary and shoulder. Lower head includes face/hair, not bag.
tracks=[]
for i in range(48):tracks.append({'from':i,'to':(i+1)%48,'upperHead':track(cells[i],cells[(i+1)%48],(55,25,102,49)),'lowerHead':track(cells[i],cells[(i+1)%48],(55,50,102,72))})
d=np.array([r['translationNativeComparisonPx']for r in M['frames']]);step=np.roll(d,-1,axis=0)-d;acc=np.roll(d,-1,axis=0)-2*d+np.roll(d,1,axis=0);f=np.fft.rfft(d-d.mean(axis=0),axis=0);power=(abs(f)**2).sum(axis=1);freq=np.fft.rfftfreq(48,d=M['cycleSeconds']/48)
def stats(v):return {'rmsVector':float(np.sqrt(np.mean((v*v).sum(axis=1)))),'maxVector':float(np.linalg.norm(v,axis=1).max())}
report={'scope':'read-only diagnostic; no new pivots or artwork; integer correlation is NOT exact semantic head tracking','sourceCommit':'50d4074','manifestSha256':hashlib.sha256((P/'semantic-pivot-trial/manifest.json').read_bytes()).hexdigest(),'pivotStepPx':stats(step),'pivotSecondDifferencePx':stats(acc),'dominantPivotFrequencyHz':float(freq[1+np.argmax(power[1:])]),'pivotSpectralPowerFractionAbove6Hz':float(power[freq>6].sum()/power[1:].sum()),'annotationNoiseModelNotMeasurement':{'assumption':'independent uniform +/-1.5 raw px per axis; does not establish actual noise distribution','perAxisPositionRmsNativePx':S*1.5/(3**.5),'perAxisSecondDifferenceRmsNativePx':S*1.5*(2**.5),'worstCaseAdjacentAnnotationErrorNativePx':3*S},'highestSecondDifferences':[{'phase':int(i),'vector':acc[i].tolist(),'length':float(np.linalg.norm(acc[i]))}for i in np.argsort(np.linalg.norm(acc,axis=1))[-10:][::-1]],'headTranslationProbes':tracks,'headProbeWindowDisagreementRawPx':[float(np.linalg.norm(np.array(r['upperHead']['shiftNextMinusCurrentRawPx'])-r['lowerHead']['shiftNextMinusCurrentRawPx']))for r in tracks]}
(O/'analysis.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['headTranslationProbes','headProbeWindowDisagreementRawPx']},indent=2));print('headwindow disagreement median/max',np.median(report['headProbeWindowDisagreementRawPx']),max(report['headProbeWindowDisagreementRawPx']))
