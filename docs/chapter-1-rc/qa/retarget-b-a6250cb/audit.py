"""Independent saved-Blender retarget audit. No source saves or author-file edits."""
import bpy,json,math,hashlib,re,statistics,sys,argparse
from pathlib import Path
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
parser=argparse.ArgumentParser();parser.add_argument('--source-root');parser.add_argument('--source-commit',default='a6250cb');parser.add_argument('--output-dir');args=parser.parse_args(sys.argv[sys.argv.index('--')+1:]if '--'in sys.argv else[])
R=Path(args.source_root)if args.source_root else Path(__file__).resolve().parents[4];O=Path(args.output_dir)if args.output_dir else Path(__file__).resolve().parent;O.mkdir(parents=True,exist_ok=True);P=R/'art/ruta-native-proportions-study-v2/b-neutral/ruta-proportion-proposal.blend';C=R/'art/ruta-native-proportions-study-v2/b-neutral/rest-transform-contract.json';c=json.loads(C.read_text());S=R/c['source'];hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [P,C,S]}
def curves(a):return{(f.data_path,f.array_index):f for l in a.layers for s in l.strips for bag in s.channelbags for f in bag.fcurves}
def actiondata(a):return{key:{'extrapolation':f.extrapolation,'modifiers':[m.type for m in f.modifiers],'keys':[{'co':list(k.co),'left':list(k.handle_left),'right':list(k.handle_right),'interpolation':k.interpolation,'leftType':k.handle_left_type,'rightType':k.handle_right_type,'easing':k.easing}for k in f.keyframe_points]}for key,f in curves(a).items()}
def meshes(rig):return[o for o in bpy.context.scene.objects if o.type=='MESH'and o.parent==rig]
def restsnap(rig):
 out={}
 for o in meshes(rig):
  out[o.name]={'coords':[list(v.co)for v in o.data.vertices],'weights':[[[o.vertex_groups[g.group].name,g.weight]for g in v.groups]for v in o.data.vertices],'faces':[list(p.vertices)for p in o.data.polygons],'localMatrix':[list(r)for r in o.matrix_local]}
 return out
def usebounds(rig):
 out={}
 for o in meshes(rig):
  used=set(i for p in o.data.polygons for i in p.vertices);vs=[o.data.vertices[i].co for i in used];out[o.name]=[[min(v[a]for v in vs),max(v[a]for v in vs)]for a in range(3)]
 allpts=[o.data.vertices[i].co for o in meshes(rig)for i in set(i for p in o.data.polygons for i in p.vertices)];out['ALL']=[[min(v[a]for v in allpts),max(v[a]for v in allpts)]for a in range(3)];return out
def prepare(path,action):
 bpy.ops.wm.open_mainfile(filepath=str(path));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.data.pose_position='POSE'
 for t in rig.animation_data.nla_tracks:t.mute=True
 a=bpy.data.actions[action];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0];p=rig.data.bones['Root'].head_local.copy();p.z=0;rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-p);bpy.context.view_layer.update();return sc,rig
sc,rig=prepare(S,'Walk');originalActions={a.name:actiondata(a)for a in bpy.data.actions};oldbones={b.name:{'head':list(b.head_local),'tail':list(b.tail_local),'parent':b.parent.name if b.parent else None}for b in rig.data.bones};originalMeshes=restsnap(rig);oldbounds=usebounds(rig)
# Independent expected rest affine transforms from original bones + stated factors.
new={}
for b in rig.data.bones:
 n=b.name;v=oldbones[n];par=v['parent'];head=Vector(v['head'])*c['parameters']['body']if not par else new[par]['head']+(Vector(v['head'])-Vector(oldbones[par]['head']))*c['bones'][par]['scale'];new[n]={'head':head,'tail':head+(Vector(v['tail'])-Vector(v['head']))*c['bones'][n]['scale']}
def feetindices(rig):
 feet=bpy.data.objects['Adventurer_Feet'];ids={}
 for side in ['L','R']:ids[side]=[v.index for v in feet.data.vertices if sum(g.weight for g in v.groups if feet.vertex_groups[g.group].name.endswith('.'+side))>.5]
 return ids
def sample(sc,rig):
 ids=feetindices(rig);feet=bpy.data.objects['Adventurer_Feet'];rows=[];fps=sc.render.fps/sc.render.fps_base
 for i in range(401):
  frame=i/10;sc.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();ev=feet.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();coords=[ev.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear();row={'frame':frame,'seconds':frame/fps,'root':list(rig.matrix_world@rig.pose.bones['Root'].head),'feet':{}}
  for side in ['L','R']:row['feet'][side]={'ankle':list(rig.matrix_world@rig.pose.bones['Foot.'+side].head),'soleMinimumZ':min(coords[j].z for j in ids[side])}
  rows.append(row)
 return rows
oldmotion=sample(sc,rig)
sc,rig=prepare(P,c['retargetedActions']['Walk']['action']);actions={a.name:actiondata(a)for a in bpy.data.actions};newmesh=restsnap(rig);bounds=usebounds(rig);boneErrors=[];contractOldErrors=[]
for b in rig.data.bones:
 n=b.name
 for key,vec in [('head',b.head_local),('tail',b.tail_local)]:
  boneErrors.append((vec-new[n][key]).length);contractOldErrors.append((Vector(c['bones'][n]['old'+key.title()])-Vector(oldbones[n][key])).length)
restErrors=[];topologyWeights=True
for name,m in originalMeshes.items():
 q=newmesh[name];topologyWeights &= m['weights']==q['weights']and m['faces']==q['faces']and m['localMatrix']==q['localMatrix']
 for index,co in enumerate(m['coords']):
  p=Vector(co);ws=[(name,w)for name,w in m['weights'][index]if name in new and w>0];total=sum(w for n,w in ws);expected=sum(((new[n]['head']+(p-Vector(oldbones[n]['head']))*c['bones'][n]['scale'])*w for n,w in ws),Vector())/total if total else p*c['parameters']['body'];restErrors.append((Vector(q['coords'][index])-expected).length)
originalActionsPreserved={n:actions.get(n)==a for n,a in originalActions.items()};retargetChecks={}
for name,entry in c['retargetedActions'].items():
 old=originalActions[name];target=actions[entry['action']];keytimes=True;rotationExact=True;otherExact=True;maxValueError=0;maxHandleError=0;channelFactors=[]
 for key,v in old.items():
  w=target[key];path,axis=key;match=re.match(r'pose.bones\["(.+)"\]\.location$',path);factor=1
  if match:
   bone=match.group(1);parent=oldbones[bone]['parent'];factor=c['bones'][parent]['scale']if parent else c['parameters']['body'];channelFactors.append({'bone':bone,'axis':axis,'factor':factor})
  elif 'rotation'in path:rotationExact &=v==w
  else:otherExact &=v==w
  for a,z in zip(v['keys'],w['keys']):
   keytimes &=a['co'][0]==z['co'][0]and a['left'][0]==z['left'][0]and a['right'][0]==z['right'][0]
   maxValueError=max(maxValueError,abs(z['co'][1]-a['co'][1]*factor));maxHandleError=max(maxHandleError,abs(z['left'][1]-a['left'][1]*factor),abs(z['right'][1]-a['right'][1]*factor))
 retargetChecks[name]={'sourceCurveCount':len(old),'targetCurveCount':len(target),'keyTimesAndHandleXExactlyPreserved':keytimes,'rotationCurvesAndHandlesExactlyPreserved':rotationExact,'nonLocationNonRotationExactlyPreserved':otherExact,'maximumKeyValueScalingError':maxValueError,'maximumHandleYScalingError':maxHandleError,'locationChannelFactors':channelFactors,'factorListMatchesContract':channelFactors==entry['translationChannels']}
# Evaluate all whole skinned mesh vertices, not merely the armature, at loop endpoints.
def fullsnap(frame):
 sc.frame_set(frame);bpy.context.view_layer.update();result={}
 for o in meshes(rig):
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();result[o.name]=[ev.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear()
 return result
v0=fullsnap(0);v40=fullsnap(40);dist=[(p-q).length for n in v0 for p,q in zip(v0[n],v40[n])];seam={'meshCount':len(v0),'evaluatedVertexCount':len(dist),'maxEndpointDistanceMeters':max(dist),'rmsEndpointDistanceMeters':math.sqrt(sum(v*v for v in dist)/len(dist))}
newmotion=sample(sc,rig)
# Same reference diagnostic contact threshold, scaled with body for fair physical-size comparison.
def motionmetrics(rows,tolerance,referenceContact=None):
 floor=min(r['feet'][side]['soleMinimumZ']for r in rows for side in ['L','R']);speeds=[];sideResult={}
 for side in ['L','R']:
  flags=[r['feet'][side]['soleMinimumZ']<=floor+tolerance for r in rows]if referenceContact is None else referenceContact[side];vv=[];vertical=[]
  for i,(a,z)in enumerate(zip(rows,rows[1:])):
   if flags[i]and flags[i+1]:
    dt=z['seconds']-a['seconds'];v=[(z['feet'][side]['ankle'][j]-a['feet'][side]['ankle'][j])/dt for j in range(3)];vv.append(-v[0]);vertical.append(v[2]);speeds.append(-v[0])
  sideResult[side]={'contactIndices':[i for i,v in enumerate(flags)if v],'soleZRange':[min(r['feet'][side]['soleMinimumZ']for r in rows),max(r['feet'][side]['soleMinimumZ']for r in rows)],'backwardAnkleSpeedRange':[min(vv),max(vv)],'backwardAnkleSpeedMedian':statistics.median(vv),'verticalAnkleSpeedRange':[min(vertical),max(vertical)],'contactIntervalCount':len(vv)}
 speed=statistics.median(speeds);res=[v-speed for v in speeds];return{'floor':floor,'tolerance':tolerance,'perFoot':sideResult,'medianBackwardAnkleSpeedMetersPerSecond':speed,'strideAtMedianSpeedMeters':speed*(rows[-1]['seconds']-rows[0]['seconds']),'speedResidualRmsMetersPerSecond':math.sqrt(statistics.mean(v*v for v in res)),'inPlaceRootTravelMeters':max(math.dist(r['root'],rows[0]['root'])for r in rows)}
oldmetric=motionmetrics(oldmotion,.025);newmetric=motionmetrics(newmotion,.025*c['parameters']['body']);ref={s:[i in oldmetric['perFoot'][s]['contactIndices']for i in range(401)]for s in ['L','R']};newOnSourceWindow=motionmetrics(newmotion,.025*c['parameters']['body'],ref)
# Saved camera and normalized Root are fixed; test all24 actual projected phases.
camFingerprint={'matrixWorld':[list(r)for r in sc.camera.matrix_world],'type':sc.camera.data.type,'orthoScale':sc.camera.data.ortho_scale,'resolution':[sc.render.resolution_x,sc.render.resolution_y,sc.render.resolution_percentage]};projected=[]
for i in range(24):
 frame=40*i/24;sc.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();root=rig.matrix_world@rig.pose.bones['Root'].head;q=world_to_camera_view(sc,sc.camera,root);projected.append({'index':i,'frame':frame,'rootWorld':list(root),'rootNativeCameraPixels':[q.x*512,(1-q.y)*640],'cameraMatrixWorld':[list(r)for r in sc.camera.matrix_world],'cameraOrthoScale':sc.camera.data.ortho_scale})
# Neutral pose markers and actual rest used-vertex geometry, independently re-read.
a=bpy.data.actions[c['retargetedActions']['Idle_Neutral']['action']];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0];rig.matrix_world=Matrix.Translation(-Vector((rig.data.bones['Root'].head_local.x,rig.data.bones['Root'].head_local.y,0)));sc.frame_set(0);bpy.context.view_layer.update();neutral={n:list(rig.matrix_world@rig.pose.bones[n].head)for n in ['Root','Hips','UpperLeg.L','UpperArm.L','LowerArm.L','Wrist.L','Middle4.L','Neck','Head']}
result={'sourceCommit':args.source_commit,'sourceHashes':hashes,'boneCount':len(oldbones),'meshCount':len(originalMeshes),'restContractOldBoneMaxErrorMeters':max(contractOldErrors),'restBoneTransformMaxErrorMeters':max(boneErrors),'restMeshWeightedTransformMaxErrorMeters':max(restErrors),'restMeshVertexCount':len(restErrors),'weightsFacesObjectLocalsExactlyPreserved':bool(topologyWeights),'sourceOriginalShaMatchesContract':hashlib.sha256(S.read_bytes()).hexdigest()==c['sourceSha256'],'originalActionsExactlyPreserved':originalActionsPreserved,'retargetChecks':retargetChecks,'fullMeshWalkSeam0to40':seam,'camera':camFingerprint,'projected24':projected,'restBounds':bounds,'restBodyHeight':bounds['ALL'][2][1]-bounds['ALL'][2][0],'restBoundsVersusContractMaxErrorMeters':max(abs(bounds['ALL'][axis][end]-c['restMeshBoundsAfter']['body'][axis][end])for axis in range(3)for end in range(2)),'neutralPoseJointHeads':neutral,'originalMotion':oldmetric,'retargetMotion':newmetric,'retargetOnOriginalContactWindows':newOnSourceWindow,'contactDefinition':'actual evaluated boot side minimum <= each-model global boot floor +25mm(original)/17.5mm(B); diagnostic not authored contacts or no-slip certificate','motionSamples':{'original':oldmotion,'retarget':newmotion},'sourceFilesUnchanged':all(hashlib.sha256((R/p).read_bytes()).hexdigest()==v for p,v in hashes.items()),'artAcceptance':False,'runtimeOrPhysicalPhoneTest':False}
(O/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print('AUDIT_DONE',json.dumps({k:result[k]for k in ['restBoneTransformMaxErrorMeters','restMeshWeightedTransformMaxErrorMeters','weightsFacesObjectLocalsExactlyPreserved','fullMeshWalkSeam0to40','restBodyHeight','sourceFilesUnchanged']}),flush=True)
