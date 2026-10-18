"""Compact native stepping pivot from preserved flat idle; no continuous-walk claim."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-study';SOURCE=ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend';meta=json.loads((SOURCE.parent/'manifest.json').read_text());before=hashlib.sha256(SOURCE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene
rig=bpy.data.objects['Ruta.MPFB.StandardRig'];thumb=bpy.data.objects['Motion ONE strap thumb pinch control'];pole=bpy.data.objects['Motion ONE strap anatomical thumb pole'];controls=[rig,thumb,pole]
for obj in controls:obj.animation_data.action=bpy.data.actions[meta['clips']['idle']['actionBundle'][obj.name]]
scene.frame_set(1);bpy.context.view_layer.update();basis={b.name:b.matrix_basis.copy() for b in rig.pose.bones};flat={s:rig.matrix_world@rig.pose.bones[('left' if s=='L' else 'right')+'_foot_ik'].matrix for s in ['L','R']};knees={s:rig.pose.bones[('left' if s=='L' else 'right')+'_knee_ik'].matrix.copy() for s in ['L','R']};idlethumb=thumb.location.copy();idlepole=pole.location.copy();chest=rig.pose.bones['spine01'].matrix.copy();neck=rig.pose.bones['neck01'].matrix.copy()
angle=math.pi/3;duration=1200;endrotation=Matrix.Rotation(angle,4,'Z');endflat={s:endrotation@flat[s] for s in ['L','R']};bundle={}
for obj in controls:
 action=bpy.data.actions.new('MPFB compact idle pivot60L / '+obj.name);action.use_fake_user=True;obj.animation_data.action=action;bundle[obj.name]=action.name
rig.rotation_mode='XYZ'
def smooth(x):x=max(0,min(1,x));return x*x*x*(10+x*(-15+6*x))
def foot(p,side):
 a,b,c,d=(.12,.18,.44,.50) if side=='L' else (.62,.68,.90,.96)
 heading=0.;lift=0.;pitch=0.;center=flat[side].translation.copy();mode='flat-initial'
 if a<=p<b:pitch=.16*smooth((p-a)/(b-a));mode='toe-off'
 elif b<=p<c:
  u=(p-b)/(c-b);w=smooth(u);center=center.lerp(endflat[side].translation,w);heading=angle*w;lift=.040*max(0,math.sin(math.pi*u))**1.2;pitch=.16*(1-w)-.10*w;mode='swing'
 elif c<=p<d:center=endflat[side].translation.copy();heading=angle;pitch=-.10*(1-smooth((p-c)/(d-c)));mode='heel-roll'
 elif p>=d:center=endflat[side].translation.copy();heading=angle;mode='flat-final'
 az=Matrix.Rotation(heading,3,'Z');roll=Matrix.Rotation(pitch,3,'X');pivot=Vector((0,-.132,-.049)) if pitch>0 else Vector((0,.015,-.05));center+=az@(pivot-roll@pivot)+Vector((0,0,lift));target=Matrix.Translation(center)@az.to_4x4()@roll.to_4x4()@flat[side].to_quaternion().to_matrix().to_4x4();return target,heading,mode
phases=sorted(set([i/120 for i in range(121)]+[.12,.18,.44,.50,.62,.68,.90,.96]));plans=[]
for p in phases:
 frame=1+duration/30*p;scene.frame_set(int(frame),subframe=frame-int(frame))
 for name,m in basis.items():rig.pose.bones[name].matrix_basis=m
 # Small world-root weight transfer, exact zero at endpoints; no root distance fit.
 firstsupport=flat['R'].translation.copy();firstsupport.z=0;firstsupport.normalize();secondsupport=endflat['L'].translation.copy();secondsupport.z=0;secondsupport.normalize();transfer=smooth((p-.48)/.16);balance=firstsupport.lerp(secondsupport,transfer)*(.030*smooth(p/.12)*(1-smooth((p-.88)/.12)))
 yaw=angle*smooth((p-.12)/.78);rig.location=balance;rig.rotation_euler=(0,0,yaw);thumb.location=idlethumb;pole.location=idlepole;bpy.context.view_layer.update()
 root=rig.pose.bones['root'];m=root.matrix.copy();m.translation.z-=.004*math.sin(math.pi*p)**2;root.matrix=m;bpy.context.view_layer.update();spine=rig.pose.bones['spine01'];m=spine.matrix.copy();spine.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(math.radians(2)*math.sin(2*math.pi*p),4,'Z')@m.to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
 head=rig.pose.bones['neck01'];m=head.matrix.copy();head.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(math.radians(6)*math.sin(math.pi*p)**2,4,'Z')@neck.to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update();delta=rig.pose.bones['spine01'].matrix@chest.inverted();thumb.location=delta@idlethumb;pole.location=delta@idlepole
 feet={}
 for side in ['L','R']:
  target,heading,mode=foot(p,side);helper=rig.pose.bones[('left' if side=='L' else 'right')+'_foot_ik'];helper.matrix=rig.matrix_world.inverted()@target;knee=rig.pose.bones[('left' if side=='L' else 'right')+'_knee_ik'];world=balance+Matrix.Rotation((yaw+heading)/2,3,'Z')@knees[side].translation;km=knee.matrix.copy();km.translation=rig.matrix_world.inverted()@world;knee.matrix=km;feet[side]=mode
 bpy.context.view_layer.update();rig.keyframe_insert('location',frame=frame);rig.keyframe_insert('rotation_euler',frame=frame)
 for b in rig.pose.bones:b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_euler',frame=frame)
 for obj in [thumb,pole]:obj.keyframe_insert('location',frame=frame)
 plans.append({'frame':frame,'timeMs':p*duration,'phase':p,'rootNativeMeters':list(balance),'yawRadians':yaw,'plannedFootModes':feet})
for obj in controls:
 for curve in obj.animation_data.action.fcurves:
  for k in curve.keyframe_points:k.interpolation='LINEAR'
keep=set(meta['sourceActions'].values())|set(bundle.values())|{a for clip in meta['clips'].values() for a in clip['actionBundle'].values()}
for action in list(bpy.data.actions):
 if action.name not in keep:bpy.data.actions.remove(action)
scene.frame_start=1;scene.frame_end=41;scene.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb-compact-pivot60-technical.blend'))
result={'status':'UNREVIEWED COMPACT NATIVE PIVOT SOURCE; NO CONTACT/NATURALNESS/ROUTE CLAIM','appearance':'rejected generic technical mannequin','source':'../transitions/mpfb-start-stop-technical.blend','sourceSha256':before,'sourceActions':meta['sourceActions'],'idleActions':meta['clips']['idle']['actionBundle'],'transitionClips':meta['clips'],'turnActions':bundle,'angleRadians':angle,'durationMs':duration,'frames':plans,'worldRootBoundTargetMeters':.10,'rootBalancePlannedMaximumMeters':.030,'entryExit':'Exact preserved flat idle at yaw0/+60, root0; requires stop+settle before pivot and new start afterward. Not a moving-walk join.','contacts':'Loaded support sole fixed in WORLD; Inside L steps first while R supports, then R while L supports; outside-first boot-crossing candidate rejected. Swing reorients foot; heel/toe roll separate.','routeCoverage':'No one-hex/full-body/bag swept-clearance certificate. Root bound alone does not prove actor clearance.','renderStatus':'NOT RENDERED; actual sole/body join measurements first','proofBudget':12}
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before;(OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('PIVOT_SOURCE_BUILT unreviewed; immutable donors unchanged')
