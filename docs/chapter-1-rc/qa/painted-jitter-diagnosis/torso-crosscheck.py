from pathlib import Path
import json,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[3];P=R/'art/ruta-native-painted-sprites-v2/packing/semantic-pivot-trial';a=json.loads((O/'head-similarity.json').read_text());n=json.loads((O/'native-head-projections.json').read_text());m=json.loads((P/'manifest.json').read_text());annotations=json.loads((P/'inputs/semantic-landmarks.json').read_text())['rows'];S=m['fixedScale'];c=np.array([80,48]);head=lambda i:np.array(n['rows'][i]['features']['Head bone head']['nativeFullPx'])*.5
res=[]
for r in a['rows']:
 i=r['phase'];p=r['headSimilarityParameters'];ang=p['rotationDegrees']*np.pi/180;rot=np.array([[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]]);out={'phase':i,'features':{}}
 for key,feature in [('clasp','Satchel warm brass clasp'),('bow','Burgundy bow knot')]:
  pt=lambda k:annotations[k]['paintedClasp']['xy']if key=='clasp'else annotations[k]['bowCrossValidation']['paintedXY']
  if pt(0)is None or pt(i)is None:continue
  native=lambda k:np.array(n['rows'][k]['features'][feature]['nativeFullPx'])*.5
  # Native relative feature/head articulation delta in raw-comparison units; not anatomical identity proof.
  relative=((native(i)-head(i))-(native(0)-head(0)))/S
  predicted=c+p['scale']*rot@(np.array(pt(0))-c)+[p['dx'],p['dy']]+relative
  residual=np.array(pt(i))-predicted
  out['features'][key]={'paintedMeasured':pt(i),'predictedFromHeadSimilarityAndNativeRelativeArticulation':predicted.tolist(),'residualRawPx':residual.tolist(),'length':float(np.linalg.norm(residual)),'systematicViewStyleMismatchUnknown':True}
 res.append(out)
report={'scope':'held-out torso diagnostic only; assumes native relative feature/head displacement comparable despite changed heading, systematic uncertainty unknown; not acceptance metric','headSimilarityNotApplied':True,'rows':res};(O/'torso-crosscheck.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
