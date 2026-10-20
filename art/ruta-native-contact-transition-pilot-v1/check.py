from pathlib import Path
import bpy,json,math,hashlib,numpy as np
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;R=O.parents[1];P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');bpy.ops.wm.open_mainfile(filepath=str(P));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];feet=bpy.data.objects['Adventurer_Feet'];rest=rig.data.bones['Root'].head_local.copy();rest.z=0;contract=json.load(open(O/'build-contract.json'));meta=json.load(open(R/'art/ruta-final-sole-compatibility-v1/final-samples/sample-source.json'));ids=meta['columnVertexIds'];sides={s:[ids.index(i)for i in meta['regions'][s]['sole']]for s in ['L','R']};N=160
with bpy.data.libraries.load(str(O/'contact-actions.blend'),link=False)as(src,dst):dst.actions=list(src.actions)
def evaluate(action,time,root=(0,0,0)):
 rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(time*24),subframe=(time*24)%1);rig.matrix_world=Matrix.Translation(Vector(root)-rest);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=feet.evaluated_get(dg);me=ev.to_mesh();points=np.array([list(ev.matrix_world@me.vertices[i].co)for i in ids]);ev.to_mesh_clear();bones={p.name:(p.head.copy(),p.matrix.to_quaternion().copy())for p in rig.pose.bones};return points,bones,list(rig.pose.bones['Root'].location)
def rootAt(c,t):
 u=t/c['durationSeconds'];T=c['durationSeconds'];p=c['rootHermite'];return(2*u**3-3*u*u+1)*np.array(p['p0'])+(u**3-2*u*u+u)*T*np.array(p['v0'])+(-2*u**3+3*u*u)*np.array(p['p1'])+(u**3-u*u)*T*np.array(p['v1'])
def angular(a,b,dt):
 q=b@a.conjugated()
 if q.w<0:q.negate()
 xyz=np.array([q.x,q.y,q.z]);length=np.linalg.norm(xyz);return xyz*(2*math.atan2(length,q.w)/max(length,1e-30)/dt)

joins=[];trajectories={};h=.0001
for clip,c in contract['clips'].items():
 act=c['action'];T=c['durationSeconds']
 for edge,source,sourceTime in [('start','Idle_Neutral_ProportionProposal'if clip=='start'else'Walk_ProportionProposal',0 if clip=='start'else 5/24),('end','Walk_ProportionProposal'if clip=='start'else'Idle_Neutral_ProportionProposal',5/24 if clip=='start'else 0)]:
  time=0 if edge=='start'else T;_,a,_=evaluate(act,time);_,b,_=evaluate(source,sourceTime);inner=time+h if edge=='start'else time-h;_,aa,_=evaluate(act,inner);sourceInner=sourceTime-h if (clip=='stop'and edge=='start')else sourceTime+h;_,bb,_=evaluate(source,sourceInner)
  if sourceTime==0 and edge=='end':sourceInner=h;_,bb,_=evaluate(source,h)
  errors=[];vels=[];rots=[];ang=[]
  for n,(pa,qa)in a.items():
   pb,qb=b[n];errors.append(((pa-pb).length,n));rots.append((qa.rotation_difference(qb).angle,n));va=(np.array(aa[n][0])-pa)/h if edge=='start'else(np.array(pa)-aa[n][0])/h;vb=(np.array(pb)-bb[n][0])/h if (clip=='stop'and edge=='start')else(np.array(bb[n][0])-pb)/h;vb=np.zeros(3)if sourceTime==0 else vb;vels.append((float(np.linalg.norm(va-vb)),n));wa=angular(qa,aa[n][1],h)if edge=='start'else angular(aa[n][1],qa,h);wb=angular(bb[n][1],qb,h)if (clip=='stop'and edge=='start')else angular(qb,bb[n][1],h);wb=np.zeros(3)if sourceTime==0 else wb;ang.append((float(np.linalg.norm(wa-wb)),n))
  joins.append({'clip':clip,'edge':edge,'sourceAction':source,'sourceTimeSeconds':sourceTime,'maximumBoneHeadPositionErrorM':max(errors),'maximumBoneRotationErrorRadians':max(rots),'maximumBoneHeadVelocityDifferenceMps':max(vels),'maximumBoneAngularVelocityDifferenceRadps':max(ang),'velocityDefinition':'one-sided prototype linear baked endpoint vs outgoing Walk-right tangent for Start-end / incoming Walk-left for Stop-start; static Idle0 zero tangent (original Idle breathing preserved, not played)'})
 points=[];roots=[]
 for j in range(N+1):
  t=j/N*T;root=rootAt(c,t);p,_,rl=evaluate(act,t,root);points.append(p);roots.append(rl)
 points=np.array(points);roots=np.array(roots);support='R'if clip=='start'else'L';endIndex=N//2 if clip=='start'else N;contact=points[:endIndex+1,sides[support]];span=np.ptp(contact,axis=0);allmin=float(points[:,:,2].min());floor=-.001194837037473917
 trajectories[clip]={'action':act,'durationSeconds':T,'externalRootEndXYZM':c['rootDistanceMetadata'][-1]['rootXYZM'],'RootBoneMaximumLocalTranslationM':float(abs(roots).max()),'allSoleMinZNativeM':allmin,'maximumDepthBelowInferredFloorM':max(0,floor-allmin),'supportSide':support,'supportIntervalSeconds':[0,endIndex/N*T],'allSupportMaterialVertexMaximumAxisSpanM':span.max(axis=0).tolist(),'allSupportMaterialVertexMaximumEuclideanSpanBoundM':float(np.linalg.norm(span,axis=1).max()),'leadSwingPeakMinimumSoleHeightM':float(points[:,sides['L'if clip=='start'else'R'],2].min(axis=1).max()),'fixedWorldSoleTrajectoriesSaved':True}
 np.savez_compressed(O/(clip+'-sole-trajectories.npz'),positions=points,times=np.linspace(0,T,N+1),vertex_ids=np.array(ids))
# Numeric acceptance is deliberately separate from clip existence.
feasible=not contract['reachFailures'] and all(r['maximumBoneHeadPositionErrorM'][0]<.0001 and r['maximumBoneRotationErrorRadians'][0]<.002 for r in joins)
velocityGate=all(r['maximumBoneHeadVelocityDifferenceMps'][0]<.03 and r['maximumBoneAngularVelocityDifferenceRadps'][0]<.3 for r in joins)
report={'status':'ENDPOINT-POSE-FEASIBLE-VELOCITY-PENDING'if feasible else'ENDPOINT-POSE-FAIL','endpointPoseGate':feasible,'endpointVelocityGate':velocityGate,'joins':joins,'clips':trajectories,'limitations':['Native Root external metadata uses analytic Hermite parameters, source Root constant; no runtime adapter authored','Footproxycontact preserves source curvedsole; inferredfloor notphysicalcollision','No no-slip or user acceptance claim','No actual render until pose+velocity gates assessed']};(O/'numeric-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2),flush=True)
# Separate held FOOT control from actual skin surface drift; do not infer contact from bones alone.
c=contract['clips']['start'];control=[]
for j in range(81):
 time=j/80*.2;evaluate(c['action'],time,rootAt(c,time));control.append([list(row)for row in rig.matrix_world@rig.pose.bones['Foot.R'].matrix])
point=np.load(O/'start-sole-trajectories.npz')['positions'][:81,sides['R']];extent=np.ptp(point,axis=0);index=int(np.argmax(np.linalg.norm(extent,axis=1)));vertexId=ids[sides['R'][index]];weights={feet.vertex_groups[g.group].name:g.weight for g in feet.data.vertices[vertexId].groups};(O/'support-drift-cause.json').write_text(json.dumps({'supportFootAll16WorldMatrixEntrySpans':np.ptp(np.array(control),axis=0).tolist(),'largestSelectedSoleSpanVertexId':vertexId,'vertexWeights':weights,'vertexWorldAxisSpanM':extent[index].tolist(),'scope':'held Foot control is not by itself proof that skinned sole point is static'},indent=2))
