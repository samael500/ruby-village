"""Independent native60deg step-turn feasibility source; no old action edits."""
from pathlib import Path
import bpy,math,json,hashlib,importlib.util
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/turn-study';SOURCE=ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend';meta=json.loads((SOURCE.parent/'manifest.json').read_text());before=hashlib.sha256(SOURCE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
rig=bpy.data.objects['Ruta.MPFB.StandardRig'];thumb=bpy.data.objects['Motion ONE strap thumb pinch control'];pole=bpy.data.objects['Motion ONE strap anatomical thumb pole'];controls=[rig,thumb,pole];scene=bpy.context.scene
for name,action in meta['sourceActions'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
spec=importlib.util.spec_from_file_location('phase',ROOT/'scripts/mpfb-motion-phase-api.py');phase=importlib.util.module_from_spec(spec);spec.loader.exec_module(phase)
def set_frame(value):scene.frame_set(int(value),subframe=value-int(value))
names=[b.name for b in rig.pose.bones];samples=[];flat={}
phases=sorted(set([i/96 for i in range(97)]+[.1,.48,.5,.6,.98]))
for p in phases:
 set_frame(1+24*p);bpy.context.view_layer.update();samples.append({'basis':{n:rig.pose.bones[n].matrix_basis.copy()for n in names},'thumb':thumb.location.copy(),'pole':pole.location.copy(),'neck':rig.pose.bones['neck01'].matrix.copy(),'chest':rig.pose.bones['spine01'].matrix.copy(),'knees':{s:rig.pose.bones[('left'if s=='L'else'right')+'_knee_ik'].matrix.copy()for s in ['L','R']}})
 if abs(p-.125)<1e-12:flat['L']=rig.matrix_world@rig.pose.bones['left_foot_ik'].matrix
 if abs(p-.625)<1e-12:flat['R']=rig.matrix_world@rig.pose.bones['right_foot_ik'].matrix;flat['R'].translation.y+=phase.STRIDE
for obj in controls:obj.animation_data.action=None
rig.rotation_mode='XYZ';angle=math.pi/3;duration=.720;ramp=1/6
# Smooth angular-velocity ramps, constant native forward speed; no endpoint fit.
def primitive(u):return 2.5*u**4-3*u**5+u**6
def yaw(p):
 area=ramp*primitive(p/ramp)if p<ramp else(1-ramp)-ramp*primitive((1-p)/ramp)if p>1-ramp else p-ramp/2
 return angle*area/(1-ramp)
resolution=4096;path=[Vector()]
for i in range(1,resolution+1):
 a=yaw((i-1)/resolution);b=yaw(i/resolution);path.append(path[-1]+Vector((math.sin(a)+math.sin(b),-math.cos(a)-math.cos(b),0))*phase.STRIDE/(2*resolution))
def position(p):
 f=max(0,min(resolution,p*resolution));i=min(resolution-1,int(f));return path[i].lerp(path[i+1],f-i)
end=path[-1];rotation=Matrix.Rotation(angle,4,'Z');finalflat={s:Matrix.Translation(end)@rotation@flat[s]for s in ['L','R']}
def smooth(u):return phase.smooth(u)
def foot_target(p,s):
 # Source cadence: R swings .10→.50, L swings .60→1.00.
 start,finish=(.1,.5)if s=='R'else(.6,1.);u=max(0,min(1,(p-start)/(finish-start)));w=smooth(u);land=flat[s].translation.lerp(finalflat[s].translation,w);heading=angle*w;pitch=phase.cycle_foot(p,s)['pitchRadians'];lift=phase.cycle_foot(p,s)['liftMeters'];roll=Matrix.Rotation(pitch,3,'X');az=Matrix.Rotation(heading,3,'Z');pivot=Vector((0,-.132,-.049))if pitch>0 else Vector((0,.015,-.05));land+=az@(pivot-roll@pivot)+Vector((0,0,lift));return Matrix.Translation(land)@az.to_4x4()@roll.to_4x4()@flat[s].to_quaternion().to_matrix().to_4x4(),heading
bundle={}
for obj in controls:
 action=bpy.data.actions.new('MPFB native60L turn / '+obj.name);action.use_fake_user=True;obj.animation_data_create();obj.animation_data.action=action;bundle[obj.name]=action.name
plans=[]
phases=sorted(set([i/96 for i in range(97)]+[.1,.48,.5,.6,.98]))
for i,p in enumerate(phases):
 frame=1+24*p;set_frame(frame);sample=samples[i]
 for n in names:rig.pose.bones[n].matrix_basis=sample['basis'][n]
 rig.location=position(p);rig.rotation_euler=(0,0,yaw(p));thumb.location=sample['thumb'];pole.location=sample['pole'];bpy.context.view_layer.update();root=rig.pose.bones['root'];m=root.matrix.copy();lean=math.radians(4)*math.sin(math.pi*p)**2;root.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(lean,4,'Y')@m.to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
 neck=rig.pose.bones['neck01'];m=neck.matrix.copy();neck.matrix=Matrix.Translation(m.translation)@Matrix.Rotation(math.radians(8)*math.sin(math.pi*p)**2,4,'Z')@sample['neck'].to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update();delta=rig.pose.bones['spine01'].matrix@sample['chest'].inverted();thumb.location=delta@sample['thumb'];pole.location=delta@sample['pole']
 for side in ['L','R']:
  target,footyaw=foot_target(p,side);helper=rig.pose.bones[('left'if side=='L'else'right')+'_foot_ik'];helper.matrix=rig.matrix_world.inverted()@target;knee=rig.pose.bones[('left'if side=='L'else'right')+'_knee_ik'];middle=(yaw(p)+footyaw)/2;world=position(p)+Matrix.Rotation(middle,3,'Z')@sample['knees'][side].translation;km=knee.matrix.copy();km.translation=rig.matrix_world.inverted()@world;knee.matrix=km
 bpy.context.view_layer.update();rig.keyframe_insert('location',frame=frame);rig.keyframe_insert('rotation_euler',frame=frame)
 for b in rig.pose.bones:b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_euler',frame=frame)
 for obj in [thumb,pole]:obj.keyframe_insert('location',frame=frame)
 plans.append({'frame':frame,'timeMs':p*720,'phase':p,'headingRadians':yaw(p),'rootNativeMeters':list(position(p))})
for obj in controls:
 for curve in obj.animation_data.action.fcurves:
  for point in curve.keyframe_points:point.interpolation='LINEAR'
scene.frame_start=1;scene.frame_end=25;scene.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb-native60-turn-technical.blend'))
result={'status':'UNREVIEWED NATIVE FEASIBILITY SOURCE; NO RENDER/CONTACT/EXIT PASS CLAIM','appearance':'rejected generic mannequin','source':'../transitions/mpfb-start-stop-technical.blend','sourceSha256':before,'sourceActions':meta['sourceActions'],'turnActions':bundle,'angleRadians':angle,'durationMs':720,'maximumKeySpacingMs':7.5,'exactContactEventPhases':[.1,.48,.5,.6,.98],'rootArcLengthPlannedMeters':phase.STRIDE,'rootDisplacementPlannedMeters':list(end),'heading':'smooth velocity ramps120ms, constant native forward speed, no endpoint distance fit','contacts':'world flat-foot transforms fixed until native toe-off; swing reorients to exit heading','entryExit':'phase0 heel strike; actual evaluated joins must pass before rendering; no independent foot offsets','cameraProofBudget':12,'renderStatus':'NOT RENDERED','120degreeStatus':'NOT AUTHORED; compose only after60deg exit join pass','frames':plans};assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before;(OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('TURN_SOURCE_BUILT unreviewed; straight source unchanged')
