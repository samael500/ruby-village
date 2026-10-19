"""Author isolated native MPFB start/stop actions from accepted technical cycle5ca361b.

Source appearance and pilot are read only. New action bundles explicitly separate
root travel, gait phase, support anchors and thumb controls. No runtime writes.
"""
from pathlib import Path
import bpy,math,json,os,importlib.util
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/transitions';OUT.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('mpfb_phase',ROOT/'scripts/mpfb-motion-phase-api.py');phase=importlib.util.module_from_spec(spec);spec.loader.exec_module(phase)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/characters-mpfb-v1/motion/pilot/mpfb-walk-technical.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];thumb=bpy.data.objects['Motion ONE strap thumb pinch control'];pole=bpy.data.objects['Motion ONE strap anatomical thumb pole'];controls=[rig,thumb,pole]
source_actions={o.name:o.animation_data.action for o in controls};names=[b.name for b in rig.pose.bones];root_rest=rig.data.bones['root'].matrix_local.copy();foot_rest={s:rig.data.bones['foot.'+s].matrix_local.copy()for s in ['L','R']}
for action in source_actions.values():action.use_fake_user=True
# Sample the actual accepted source actions before authoring anything else.
samples={}
for i in range(24):
 scene.frame_set(i+1);bpy.context.view_layer.update();samples[i]={'basis':{n:rig.pose.bones[n].matrix_basis.copy()for n in names},'thumb':thumb.location.copy(),'pole':pole.location.copy()}
scene.frame_set(1);bpy.context.view_layer.update()
for o in controls:o.animation_data.action=None
# Native neutral left arm. Right carry remains the accepted supported gesture.
def aim(name,endname,direction):
 bpy.context.view_layer.update();b=rig.pose.bones[name];end=rig.pose.bones[endname];q=(end.head-b.head).normalized().rotation_difference(Vector(direction).normalized());m=b.matrix.copy();b.matrix=Matrix.Translation(m.translation)@q.to_matrix().to_4x4()@m.to_quaternion().to_matrix().to_4x4();bpy.context.view_layer.update()
def set_foot(side,plan,root_distance):
 m=foot_rest[side].copy();m.translation.x=.070 if side=='L'else-.070;m.translation.y+=root_distance-plan['plannedBaseForwardMeters'];m.translation.z+=plan['liftMeters']-.003265625
 rotation=Matrix.Rotation(plan['pitchRadians'],3,'X');pivot=Vector((0,-.132,-.049))if plan['pitchRadians']>0 else Vector((0,.015,-.05));m.translation+=pivot-rotation@pivot
 rig.pose.bones[('left'if side=='L'else'right')+'_foot_ik'].matrix=Matrix.Translation(m.translation)@rotation.to_4x4()@m.to_quaternion().to_matrix().to_4x4()
idle_root=rig.pose.bones['root'].matrix.copy();idle_delta=phase.IDLE_Z-(idle_root.translation.z-root_rest.translation.z);idle_root.translation.z+=idle_delta;rig.pose.bones['root'].matrix=idle_root;thumb.location.z+=idle_delta;pole.location.z+=idle_delta
for side in ['L','R']:set_foot(side,phase.foot(0.,'flat'),0.)
rig.pose.bones['wrist.L'].rotation_euler=(0,0,0);aim('upperarm01.L','lowerarm01.L',(.08,0,-1));aim('lowerarm01.L','wrist.L',(.025,-.12,-1));aim('wrist.L','finger3-1.L',(.025,-.12,-1))
bpy.context.view_layer.update();idle={'basis':{n:rig.pose.bones[n].matrix_basis.copy()for n in names},'thumb':thumb.location.copy(),'pole':pole.location.copy()}
def blend_matrix(a,b,t):
 al,aq,asc=a.decompose();bl,bq,bsc=b.decompose();return Matrix.LocRotScale(al.lerp(bl,t),aq.slerp(bq,t),asc.lerp(bsc,t))
def source_sample(p):return samples[int(round((p%1)*24))%24]
def apply(plan):
 source=source_sample(plan['sourcePhase']);amount=plan['poseAmplitude']
 for n in names:rig.pose.bones[n].matrix_basis=blend_matrix(idle['basis'][n],source['basis'][n],amount)
 rig.location=(0,-plan['rootDistanceMeters'],0);bpy.context.view_layer.update();before=rig.pose.bones['root'].matrix.copy();after=before.copy();after.translation.z=root_rest.translation.z+plan['rootZ'];after.translation.x+=plan['rootLateralExtraMeters'];rig.pose.bones['root'].matrix=after;delta=after@before.inverted()
 thumb.location=delta@idle['thumb'].lerp(source['thumb'],amount);pole.location=delta@idle['pole'].lerp(source['pole'],amount)
 for side in ['L','R']:
  set_foot(side,plan['feet'][side],plan['rootDistanceMeters']);knee=rig.pose.bones[('left'if side=='L'else'right')+'_knee_ik'];m=knee.matrix.copy();m.translation.x=(.076 if side=='L'else-.076)+plan['rootLateralExtraMeters'];knee.matrix=m
 bpy.context.view_layer.update()
def key(frame):
 rig.keyframe_insert('location',frame=frame)
 for b in rig.pose.bones:
  b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_euler',frame=frame)
 for o in [thumb,pole]:o.keyframe_insert('location',frame=frame)
def new_bundle(label):
 result={}
 for o in controls:
  action=bpy.data.actions.new(label+' / '+o.name);action.use_fake_user=True;o.animation_data_create();o.animation_data.action=action;result[o.name]=action.name
 return result
def activate(bundle):
 for o in controls:o.animation_data.action=bpy.data.actions[bundle[o.name]]
def state_plan(kind,t,side='L'):return phase.sample_clip(kind,t,side)
# Every state has its own action bundle. The active demo composes their root motion once.
manifest=phase.contract();manifest.update({'sourceCycleCommit':'5ca361b','appearance':'rejected generic technical mannequin','sourceBlend':'../pilot/mpfb-walk-technical.blend','blender':bpy.app.version_string,'frameMs':30,'savedActionInterpolation':'LINEAR at 30ms; analytic API root easing is sampled, not exact between keys','frameSize':[384,384],'nativeHeightReferencePx':251,'targetDisplayHeightReferencePx':136,'metersToScenePixels':136/(251/384*1.70),'clips':{},'sourceActions':{n:a.name for n,a in source_actions.items()}})
for kind,duration,sides in [('idle',180,['L']),('start',360,['L','R']),('stop',360,['L','R']),('settle',180,['L'])]:
 for side in sides:
  name=kind+'-'+side if kind in ['start','stop']else kind;bundle=new_bundle('MPFB transition '+name);frames=[]
  for f,t in enumerate(range(0,duration+1,30),1):
   scene.frame_set(f);plan=state_plan(kind,t,side);apply(plan);key(f);frames.append({'frame':f,**plan})
  manifest['clips'][name]={'durationMs':duration,'loop':False,'actionBundle':bundle,'frames':frames,'rootAdvanceMeters':frames[-1]['rootDistanceMeters']}
def demo_plan(time_ms,lead='L'):
 if time_ms<360:p=state_plan('start',time_ms,lead)
 elif time_ms<1080:
  p=state_plan('walk',time_ms-360,lead);p['rootDistanceMeters']+=.2*phase.STRIDE
  for d in p['feet'].values():d['plannedBaseForwardMeters']+=.2*phase.STRIDE
 elif time_ms<1440:
  p=state_plan('stop',time_ms-1080,lead);p['rootDistanceMeters']+=1.2*phase.STRIDE
  for d in p['feet'].values():d['plannedBaseForwardMeters']+=1.2*phase.STRIDE
 else:
  p=state_plan('settle',time_ms-1440,lead);p['rootDistanceMeters']+=1.5*phase.STRIDE
  for d in p['feet'].values():d['plannedBaseForwardMeters']+=1.5*phase.STRIDE
 p['timelineMs']=time_ms;return p
manifest['demos']={}
for lead in ['L','R']:
 bundle=new_bundle('MPFB start walk stop demo '+lead);frames=[]
 for f,t in enumerate(range(0,1621,30),1):
  scene.frame_set(f);plan=demo_plan(t,lead);apply(plan);key(f);frames.append({'frame':f,**plan})
 manifest['demos'][lead]={'durationMs':1620,'actionBundle':bundle,'frames':frames,'contactEvents':[{'timeMs':360,'foot':lead},{'timeMs':720,'foot':'R'if lead=='L'else'L'},{'timeMs':1080,'foot':lead},{'timeMs':1380,'foot':'R'if lead=='L'else'L'}]}
for action in bpy.data.actions:
 if action.name.startswith('MPFB transition')or action.name.startswith('MPFB start walk stop'):
  for curve in action.fcurves:
   for point in curve.keyframe_points:point.interpolation='LINEAR'
# Production base E camera: unmodified scale, elevation asin(.65), genuine spatial projection.
cam=scene.camera;cam.data.type='ORTHO';cam.data.ortho_scale=1.70;elev=math.asin(.65)
def camera():
 center=rig.location+Vector((0,0,.68));cam.location=center+Vector((-4*math.cos(elev),0,4*math.sin(elev)));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
activate(manifest['demos']['L']['actionBundle']);scene.frame_start=1;scene.frame_end=55;scene.frame_set(1);camera();scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.render.fps=100;scene.render.fps_base=3;scene.cycles.samples=8;scene.cycles.use_denoising=True;scene.render.film_transparent=True
anchor=world_to_camera_view(scene,cam,rig.matrix_world.translation);manifest['rootGroundAnchorPixels']=[anchor.x*384,(1-anchor.y)*384];manifest['projection']={'variant':'base','direction':'e','angle':0,'groundScale':.65,'orthoScale':1.70,'elevationRadians':elev,'cameraFollows':'rig object root translation only, not pelvis/feet/bounding box'}
legacy=json.loads((ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json').read_text());manifest['cameraSpecificationsReadOnlyReference']={group:{'camera':value['camera'],'directions':{name:{'screenAngleRadians':d['screenAngleRadians'],'nativeCameraAzimuthRadians':-math.pi+math.atan2(math.sin(d['screenAngleRadians'])/value['camera']['groundScale'],math.cos(d['screenAngleRadians']))}for name,d in value['directions'].items()}}for group,value in legacy['cameraVariants'].items()}
manifest['sixViewExportStatus']='NOT RENDERED; first E transition review required';manifest['status']='TECHNICAL START STOP PROTOTYPE; author and independent visual/contact review pending';bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb-start-stop-technical.blend'));(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if os.environ.get('RUBY_MPFB_RENDER','0')=='1':
 for f in range(1,56):
  scene.frame_set(f);camera();scene.render.filepath=str(OUT/'E'/f'{f:02}.png');bpy.ops.render.render(write_still=True)
print('MPFB_TRANSITIONS',len(manifest['clips']),'clips,2native demos,55frames each; source pilot unchanged')
