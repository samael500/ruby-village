from pathlib import Path
from PIL import Image
import numpy as np,json
O=Path(__file__).resolve().parent;j=json.loads((O/'timings.json').read_text());rows=[]
for row in j['rows']:
 a=np.array(Image.open(row['file']).convert('RGBA')).astype(float);b=np.array(Image.open(row['reference']).convert('RGBA')).astype(float);d=np.abs(a-b);fg=(a[:,:,3]>0)|(b[:,:,3]>0);edge=((a[:,:,3]>0)&(a[:,:,3]<255))|((b[:,:,3]>0)&(b[:,:,3]<255));face=d[185:280,205:310,:3];rows.append({'phase':row['phase'],'meanAbsForegroundRGBbytes':d[:,:,:3][fg].mean(axis=0).tolist(),'p99AbsForegroundRGBbytes':float(np.percentile(d[:,:,:3][fg],99)),'maxAbsForegroundRGBbytes':float(d[:,:,:3][fg].max()),'alpha128MaskChangedPixels':int(((a[:,:,3]>=128)!=(b[:,:,3]>=128)).sum()),'meanAbsAlphaBytes':float(d[:,:,3][fg].mean()),'meanAbsEdgeRGBbytes':d[:,:,:3][edge].mean(axis=0).tolist(),'faceROIXYXY':[205,185,310,280],'faceMeanAbsRGBbytes':face.mean(axis=(0,1)).tolist(),'faceP99AbsRGBbytes':float(np.percentile(face,99))})
(O/'pixel-comparison.json').write_text(json.dumps({'samples32vs128':rows,'limits':'Static raw-byte difference, no perceptual acceptance; same source/pose/camera but different sampling and concurrent timing environment. Face ROI includes hair/skin, not semantic stable-landmark claim.'},indent=2)+'\n')
