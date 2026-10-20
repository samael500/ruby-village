"""One L first-step/stop pair; native actions in-place + external Root path, no source edits."""
from pathlib import Path
import bpy,json,math,hashlib,numpy as np
from mathutils import Matrix,Vector,Quaternion
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(P)=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';bpy.ops.wm.open_mainfile(filepath=str(P));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rest=rig.data.bones['Root'].head_local.copy();rest.z=0;rig.matrix_world=Matrix.Translation(-rest);names=[b.name for b in rig.pose.bones];F=Vector((0,-1,0));I='Idle_Neutral_ProportionProposal';W='Walk_ProportionProposal';eps=.001
for tr in rig.animation_data.nla_tracks:tr.mute=True
def ah(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right),k.interpolation)for k in f.keyframe_points])for f in a.fcurves]).encode()).hexdigest()
originalHashes={a.name:ah(a)for a in bpy.data.actions}
def sample(action,frame):
 rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(frame),subframe=frame%1);bpy.context.view_layer.update();basis={n:[np.array(x)for x in rig.pose.bones[n].matrix_basis.decompose()]for n in names};feet={s:[np.array(x)for x in (rig.matrix_world@rig.pose.bones['Foot.'+s].matrix).decompose()]for s in ['L','R']};offset={s:np.array(rig.pose.bones['Foot.'+s].matrix.inverted()@rig.pose.bones['LowerLeg.'+s].tail)for s in ['L','R']};return {'basis':basis,'feet':feet,'offset':offset}
i=sample(I,0);ip=sample(I,eps*24);w=sample(W,5);wm=sample(W,5-eps*24);wp=sample(W,5+eps*24)
def aligned(a,b):return -b if np.dot(a,b)<0 else b
# align quaternions and derive tangent components in seconds.
for n in names:
 for d in [ip,w,wm,wp]:d['basis'][n][1]=aligned(i['basis'][n][1],d['basis'][n][1])
for s in ['L','R']:
 for d in [ip,w,wm,wp]:d['feet'][s][1]=aligned(i['feet'][s][1],d['feet'][s][1])
vi={key:{n:[(b-a)/eps for a,b in zip(i[key][n],ip[key][n])]for n in i[key]}for key in ['basis','feet']};vw={key:{n:[(b-a)/(2*eps)for a,b in zip(wm[key][n],wp[key][n])]for n in w[key]}for key in ['basis','feet']};vio={s:(ip['offset'][s]-i['offset'][s])/eps for s in ['L','R']};vwo={s:(wp['offset'][s]-wm['offset'][s])/(2*eps)for s in ['L','R']}
def H(a,b,va,vb,u,T):return (2*u**3-3*u*u+1)*a+(u**3-2*u*u+u)*T*va+(-2*u**3+3*u*u)*b+(u**3-u*u)*T*vb
def transform(parts):return Matrix.LocRotScale(Vector(parts[0]),Quaternion(parts[1]).normalized(),Vector(parts[2]))
def interp(a,b,va,vb,u,T):return [H(x,y,dx,dy,u,T)for x,y,dx,dy in zip(a,b,va,vb)]
# Delivery idle is static Idle0: zero endpoint tangents, original breathing action retained unchanged.
vi={key:{n:[np.zeros_like(a)for a in parts]for n,parts in i[key].items()}for key in ['basis','feet']};vio={side:np.zeros(3)for side in ['L','R']}
rootEndStart=Vector((0,-.14,0));rootEndStop=Vector((-.021197920897975564,-.1401984873227775,-.00027357182989362627));speed=.6668266186550812;Tstop=.42049457355359643
vwRight={key:{n:[(b-a)/eps for a,b in zip(w[key][n],wp[key][n])]for n in w[key]}for key in ['basis','feet']};vwLeft={key:{n:[(b-a)/eps for a,b in zip(wm[key][n],w[key][n])]for n in w[key]}for key in ['basis','feet']}
sourceposes={'start':(i,w,vi,vwRight,.4,rootEndStart),'stop':(w,i,vwLeft,vi,Tstop,rootEndStop)}
rig.animation_data.action=None;records={};actions=[];reachFailures=[]
# Keep all source action data retained; build independent numeric bake first.
for clip,(a,b,va,vb,T,end)in sourceposes.items():
 samples=[];rootrows=[];maxAimError=0.;N=80
 for j in range(N+1):
  u=j/N;time=u*T
  # C1 root path, monotone forward; endpoint speed inherited from measured Walk.
  r0=np.zeros(3);r1=np.array(end);rv0=np.array(F*speed)if clip=='stop'else np.zeros(3);rv1=np.array(F*speed)if clip=='start'else np.zeros(3);root=H(r0,r1,rv0,rv1,u,T);rig.matrix_world=Matrix.Translation(Vector(root)-rest)
  for n in names:
   parts=interp(a['basis'][n],b['basis'][n],va['basis'][n],vb['basis'][n],u,T);pb=rig.pose.bones[n];pb.location=Vector(parts[0]);pb.rotation_quaternion=Quaternion(parts[1]).normalized();pb.scale=Vector(parts[2])
  bpy.context.view_layer.update()
  for side in ['L','R']:
   A=[x.copy()for x in a['feet'][side]];B=[x.copy()for x in b['feet'][side]];A[0]+=r0;B[0]+=r1;VA=[x.copy()for x in va['feet'][side]];VB=[x.copy()for x in vb['feet'][side]];VA[0]+=rv0;VB[0]+=rv1
   vlocal=u;localT=T
   if clip=='start'and side=='R':
    # Initial right support is genuinely fixed, then released into source trailing-foot pose.
    if u<=.5:target=transform(i['feet'][side])
    else:
     target=transform(interp(A,B,[np.zeros_like(x)for x in VA],VB,(u-.5)*2,T/2))
   else:
    parts=interp(A,B,VA,VB,u,T)
    if (clip=='start'and side=='L')or(clip=='stop'and side=='R'):parts[0][2]+=(.065 if clip=='start'else .03)*16*u*u*(1-u)*(1-u)
    target=transform(parts)
   targetLocal=rig.matrix_world.inverted()@target;foot=rig.pose.bones['Foot.'+side];foot.matrix=targetLocal;bpy.context.view_layer.update()
   off=H(a['offset'][side],b['offset'][side],vio[side]if clip=='start'else (w['offset'][side]-wm['offset'][side])/eps,(wp['offset'][side]-w['offset'][side])/eps if clip=='start'else vio[side],u,T);ankle=targetLocal@Vector(off);up=rig.pose.bones['UpperLeg.'+side];low=rig.pose.bones['LowerLeg.'+side];hip=up.head.copy();knee=low.head.copy();L1=up.length;L2=low.length;axis=ankle-hip;distance=axis.length
   if distance>L1+L2+1e-5 or distance<abs(L1-L2)-1e-5:reachFailures.append({'clip':clip,'sample':j,'side':side,'distanceM':distance,'lengthsM':[L1,L2]})
   axis.normalize();pole=knee-hip-axis*(knee-hip).dot(axis)
   if pole.length<1e-8:pole=Vector((0,-1,0))-axis*axis.dot(Vector((0,-1,0)))
   pole.normalize();along=(L1*L1-L2*L2+distance*distance)/(2*max(distance,1e-8));height=math.sqrt(max(0,L1*L1-along*along));K=hip+axis*along+pole*height
   def aim(pb,endPoint):
    old=pb.tail-pb.head;new=endPoint-pb.head;q=old.rotation_difference(new);mat=pb.matrix.copy();rotation=q@mat.to_quaternion();pb.matrix=Matrix.LocRotScale(mat.translation,rotation,mat.to_scale());bpy.context.view_layer.update()
   aim(up,K);aim(low,ankle);maxAimError=max(maxAimError,(low.tail-ankle).length)
  bpy.context.view_layer.update();samples.append({n:[list(pb.location),list(pb.rotation_quaternion),list(pb.scale)]for n in names for pb in [rig.pose.bones[n]]});rootrows.append({'timeSeconds':time,'sourceActionFrame':time*24,'rootXYZM':root.tolist(),'walkJoinPhase':.125 if (clip=='start'and j==N)or(clip=='stop'and j==0)else None})
 action=bpy.data.actions.new('RutaContact_'+('FirstStepL'if clip=='start'else'StopL')+'_PROTOTYPE');action.use_fake_user=True;rig.animation_data.action=action
 for j,pose in enumerate(samples):
  frame=j/N*T*24
  for n,parts in pose.items():
   pb=rig.pose.bones[n];pb.location=parts[0];pb.rotation_quaternion=parts[1];pb.scale=parts[2]
   for path in ['location','rotation_quaternion','scale']:pb.keyframe_insert(data_path=path,frame=frame,group=n)
 for fc in action.fcurves:
  n=fc.group.name;channel=0 if fc.data_path.endswith('location')else 1 if fc.data_path.endswith('rotation_quaternion')else 2;values=np.array([key.co.y for key in fc.keyframe_points]);times=np.array([key.co.x for key in fc.keyframe_points]);slopes=np.gradient(values,times);slopes[0]=float(va['basis'][n][channel][fc.array_index])/24;slopes[-1]=float(vb['basis'][n][channel][fc.array_index])/24
  for k,key in enumerate(fc.keyframe_points):
   key.interpolation='BEZIER';key.handle_left_type='FREE';key.handle_right_type='FREE';left=(times[k]-times[k-1])/3 if k else(times[1]-times[0])/3;right=(times[k+1]-times[k])/3 if k+1<len(times)else(times[-1]-times[-2])/3;key.handle_left=(times[k]-left,values[k]-left*slopes[k]);key.handle_right=(times[k]+right,values[k]+right*slopes[k])
 actions.append(action);records[clip]={'action':action.name,'durationSeconds':T,'sampleCount':N+1,'rootDistanceMetadata':rootrows,'maximumLowerLegTargetErrorM':maxAimError,'rootHermite':{'p0':[0,0,0],'p1':list(end),'v0':list(F*speed)if clip=='stop'else[0,0,0],'v1':list(F*speed)if clip=='start'else[0,0,0]},'contactDefinition':'actual sole geometry check follows; source foot motion inherited, not certified static support'};rig.animation_data.action=None
assert all(ah(bpy.data.actions[n])==h for n,h in originalHashes.items());assert sha(P)=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706'
# Real action assets only; source scene/body stays read-only and is never saved over.
bpy.data.libraries.write(str(O/'contact-actions.blend'),set(actions),fake_user=True,compress=True)
(O/'build-contract.json').write_text(json.dumps({'status':'NUMERIC-PROTOTYPE-PENDING-JOIN-AND-SOLE-GATE','sourceSHA256':sha(P),'originalActionHashes':originalHashes,'idleDelivery':'static Idle0 pose, zero tangents; original Idle action unchanged','RootBoneConstantInPlace':True,'RootTravelExternalOnly':True,'clips':records,'reachFailures':reachFailures,'noRuntimeSourceRigRestGeometryChanges':True},indent=2));print('ACTION_PAIR_BUILT','reachFailures',len(reachFailures),flush=True)
