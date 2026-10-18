import bpy,json,math,hashlib,importlib.util
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;SRC=ROOT/'art/characters-mpfb-v1/motion/transitions';source=SRC/'mpfb-start-stop-technical.blend';meta=json.loads((SRC/'manifest.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];controls=[bpy.data.objects[n]for n in meta['sourceActions']]
def activate(bundle):
 assert len(bundle)==3
 for name,action in bundle.items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels;m.show_viewport=True
probe=shoe.copy();probe.name='Independent QA sole index probe';scene.collection.objects.link(probe);probe.hide_render=True
for m in probe.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
ids={}
for side,sign in [('L',1),('R',-1)]:
 vs=[v for v in shoe.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vs);bottom=[v for v in vs if v.co.z<=z+.004];lo=min(v.co.y for v in bottom);hi=max(v.co.y for v in bottom);ids[side]={'toe':[v.index for v in bottom if v.co.y<=lo+.2*(hi-lo)],'heel':[v.index for v in bottom if v.co.y>=hi-.2*(hi-lo)]}
def snapshot(frame):
 scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();d=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(d);es=shoe.evaluated_get(d);ep=probe.evaluated_get(d);feet={}
 for side,word in [('L','left'),('R','right')]:
  ankle=er.matrix_world@er.pose.bones['foot.'+side].head;target=er.matrix_world@er.pose.bones[word+'_foot_ik'].head;markers={}
  for kind,indices in ids[side].items():
   ps=[ep.matrix_world@ep.data.vertices[i].co for i in indices];markers[kind]={'center':list(sum(ps,Vector())/len(ps)),'minZ':min(p.z for p in ps)}
  feet[side]={'markers':markers,'ankleWorld':list(ankle),'targetError':(ankle-target).length}
 return {'frame':frame,'timeMs':(frame-1)*30,'root':list(er.matrix_world.translation),'pelvisZ':(er.matrix_world@er.pose.bones['root'].head).z,'floorMinZ':min((es.matrix_world@v.co).z for v in es.data.vertices),'feet':feet,'pose':[v for b in er.pose.bones for row in b.matrix for v in row],'thumbLocal':list(bpy.data.objects['Motion ONE strap thumb pinch control'].location),'poleLocal':list(bpy.data.objects['Motion ONE strap anatomical thumb pole'].location)}
def maxdelta(a,b):return max(abs(x-y)for x,y in zip(a,b))
def flat_runs(records,side):
 first=records[0]['feet'][side]['markers'];reference=first['toe']['center'][2]-first['heel']['center'][2];runs=[];current=[]
 for r in records:
  m=r['feet'][side]['markers'];flat=abs(m['toe']['center'][2]-m['heel']['center'][2]-reference)<.0002 and min(m[k]['minZ']for k in m)<.002
  if flat:current.append(r)
  elif current:runs.append(current);current=[]
 if current:runs.append(current)
 result=[]
 for run in runs:
  if len(run)<3:continue
  result.append({'startMs':run[0]['timeMs'],'endMs':run[-1]['timeMs'],'markerDriftM':{k:max((Vector(a['feet'][side]['markers'][k]['center'])-Vector(b['feet'][side]['markers'][k]['center'])).length for a in run for b in run)for k in ['toe','heel']}})
 return result
reports={}
for lead in ['L','R']:
 activate(meta['demos'][lead]['actionBundle']);records=[snapshot(1+i/4)for i in range(217)];root=[-r['root'][1]for r in records];assert all(b>=a-1e-7 for a,b in zip(root,root[1:]));settle=[r for r in records if r['timeMs']>=1440];rs={r['timeMs']:r for r in records};trailing='R'if lead=='L'else'L'
 metrics={'floorMinZ':min(r['floorMinZ']for r in records),'maxActualAnkleTargetErrorM':max(f['targetError']for r in records for f in r['feet'].values()),'rootDistanceM':root[-1]-root[0],'rootMonotonic':True,'settleRootDriftM':max(abs(v+settle[0]['root'][1])for v in [-r['root'][1]for r in settle]),'settlePelvisRiseM':settle[-1]['pelvisZ']-settle[0]['pelvisZ'],'flatMeasuredRuns':{s:flat_runs(records,s)for s in ['L','R']},'firstLeadHeelAdvanceM':rs[0]['feet'][lead]['markers']['heel']['center'][1]-rs[360]['feet'][lead]['markers']['heel']['center'][1],'stopTrailingHeelAdvanceM':rs[1080]['feet'][trailing]['markers']['heel']['center'][1]-rs[1380]['feet'][trailing]['markers']['heel']['center'][1],'firstSwingLeadMaxHeelZ':max(r['feet'][lead]['markers']['heel']['minZ']for r in records if r['timeMs']<=360),'stopSwingTrailingMaxHeelZ':max(r['feet'][trailing]['markers']['heel']['minZ']for r in records if 1080<=r['timeMs']<=1440),'settleSkinWorldDriftM':{s:{k:max((Vector(a['feet'][s]['markers'][k]['center'])-Vector(b['feet'][s]['markers'][k]['center'])).length for a in settle for b in settle)for k in ['toe','heel']}for s in ['L','R']},'savedRootSegmentVelocitiesMPerSec':{str(t):(-rs[t+30]['root'][1]+rs[t]['root'][1])/.03 for t in [0,330,360,1050,1080,1410,1440,1590]}}
 reports[lead]={'summary':metrics,'records':[{k:v for k,v in r.items()if k!='pose'}for r in records]}
# Compare all three bundled object poses at boundaries, normalizing rig object root travel.
joins={}
for lead,walkframe in [('L',1),('R',13)]:
 def sample(bundle,frame):activate(bundle);return snapshot(frame)
 idle=sample(meta['clips']['idle']['actionBundle'],1);start0=sample(meta['clips']['start-'+lead]['actionBundle'],1);start1=sample(meta['clips']['start-'+lead]['actionBundle'],13);walk=sample(meta['sourceActions'],walkframe);stop0=sample(meta['clips']['stop-'+lead]['actionBundle'],1);stop1=sample(meta['clips']['stop-'+lead]['actionBundle'],13);settle0=sample(meta['clips']['settle']['actionBundle'],1);settle1=sample(meta['clips']['settle']['actionBundle'],7)
 for label,a,b in [('idle-start',idle,start0),('start-walk',start1,walk),('walk-stop',walk,stop0),('stop-settle',stop1,settle0),('settle-idle',settle1,idle)]:
  joins[lead+'/'+label]={'rootNormalizedActualSoleJoinMaxDistanceM':max(((Vector(a['feet'][side]['markers'][kind]['center'])-Vector(a['root']))-(Vector(b['feet'][side]['markers'][kind]['center'])-Vector(b['root']))).length for side in ['L','R']for kind in ['toe','heel']),'rootRelativeBoneMatrixMaxDelta':maxdelta(a['pose'],b['pose']),'thumbLocalMaxDelta':maxdelta(a['thumbLocal'],b['thumbLocal']),'poleLocalMaxDelta':maxdelta(a['poleLocal'],b['poleLocal'])}
# Read isolated API, but independently test queue boundaries and actual derivatives, not author assertions.
spec=importlib.util.spec_from_file_location('qa_phase',ROOT/'scripts/mpfb-motion-phase-api.py');api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api);apiChecks=[]
for lead in ['L','R']:
 for kind,duration in [('start',360),('stop',360),('settle',180)]:
  values=[api.sample_clip(kind,t,lead)for t in range(duration+1)];assert all(b['rootDistanceMeters']>=a['rootDistanceMeters']-1e-10 for a,b in zip(values,values[1:]));errors=[]
  for t in range(1,duration):
   derivative=(api.sample_clip(kind,t+.001,lead)['rootDistanceMeters']-api.sample_clip(kind,t-.001,lead)['rootDistanceMeters'])/.000002;errors.append(abs(derivative-api.sample_clip(kind,t,lead)['rootVelocityMetersPerSecond']))
  phaseDeltas=[b['sourcePhase']-a['sourcePhase']for a,b in zip(values,values[1:])];phaseDeltas=[d+1 if d<-.5 else d for d in phaseDeltas];assert min(phaseDeltas)>=-1e-8
  apiChecks.append({'sourcePhaseMonotonicModulo1':True,'lead':lead,'clip':kind,'monotonicRoot':True,'numericVelocityMaxError':max(errors),'startVelocity':values[0]['rootVelocityMetersPerSecond'],'endVelocity':values[-1]['rootVelocityMetersPerSecond']})
for i in range(1001):
 p=i/1000;q=api.request_stop(p);expected=math.ceil((p%1)*2-1e-8)/2;assert abs(q['waitMs']-(expected-p%1)*720)<1e-5 and 0<=q['waitMs']<=360+1e-7 and q['entryPhase']in [0,.5]
(OUT/'measure.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'method':'Fresh Blender reopen, all three actions activated together;217quarterframes each native lead. Render-level1 full boots; independent bottom4mm/20% source skin markers; flat contact runs derived from measured sole pitch/height, no target-only drift readback.','demos':reports,'bundleJoins':joins,'APIchecks':apiChecks,'queuePhasesChecked':1001,'arbitraryRouteRuntime':'NOT IMPLEMENTED or certified'},indent=2)+'\n');print(json.dumps({'demos':{s:r['summary']for s,r in reports.items()},'joins':joins},indent=2))
