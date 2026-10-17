import json,math,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent
states=json.loads((OUT/'states/report.json').read_text())['checks'];legacy=json.loads((ROOT/'src/chapter-1.legacy.json').read_text())['scene-v8.json'];motion=json.loads((ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json').read_text());checks=[]
for c in states:
 sid=c['scene'];target=c['arrival'][0];xy=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',target['anchor'])];goal=c['rutaActualArrivalFeet'];dx=xy[0]-goal['x'];dy=xy[1]-goal['y'];length=math.hypot(dx,dy)
 variant=motion['sceneCameraVariant'][sid];directions=motion['directions'] if variant=='base' else motion['cameraVariants'][variant]['directions']
 scores={name:(dx*math.cos(spec['screenAngleRadians'])+dy*math.sin(spec['screenAngleRadians']))/length for name,spec in directions.items()};expected=max(scores,key=scores.get)
 assert c['rutaArrivalDirection']==expected,(sid,expected,c['rutaArrivalDirection'])
 checks.append({'scene':sid,'viewport':c['viewport'],'target':target['id'],'goalFeet':goal,'residentFeet':xy,'expectedNearestAuthoredDirection':expected,'observed':c['rutaArrivalDirection'],'dot':scores[expected]})
edges=json.loads((OUT/'independent-edges.json').read_text());samples=edges[1]['walkSamples'];during=[s for s in samples if s.get('ms') and int(s['ms'])>0];statesDuring={json.dumps(s['residents'],sort_keys=True) for s in during}
# Arrival can switch views once. Any frame-by-frame tracking would generate many states.
assert len(statesDuring)<=2
facings=json.loads((ROOT/'public/assets/characters-facing-v1/residents-facing-manifest.json').read_text())['characters'];views=[(actor,view) for actor,spec in facings.items() for view in spec['frames']]
assert len(views)==8
for actor,spec in facings.items():
 for frame in spec['frames'].values():assert frame.get('mirrored') is False
for page in edges[1]['pages']:
 for a in page['actors']:
  for t in a['transforms']:
   matrix=t['css']
   if matrix.startswith('matrix('):
    v=[float(x) for x in matrix[7:-1].split(',')];assert v[0]*v[3]-v[1]*v[2]>0
(OUT/'geometry-audit.json').write_text(json.dumps({'arrivalFacing':checks,'authoredViews':views,'noAuthoredMirror':True,'normalWalkSamples':len(samples),'distinctResidentStatesWhileWalking':len(statesDuring),'noContinuousTracking':True,'runtimeAncestorTransformsNoReflection':True},indent=2)+'\n');print('PASS12 independent arrival vector directions,8 authored views,no mirror/no continuous tracking')
