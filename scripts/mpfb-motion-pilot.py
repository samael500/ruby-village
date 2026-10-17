"""Native MPFB IK motion study. Rejected appearance is a technical mannequin only."""
from pathlib import Path
import bpy,sys,os,math,json
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';OUT.mkdir(parents=True,exist_ok=True)
SRC=Path('/home/mskorokhod/life/_tools/mpfb2-v2.0.18/src')
OWN=Path('/tmp/ruby-mpfb-motion-config/data');OWN.mkdir(parents=True,exist_ok=True)
orig=bpy.utils.extension_path_user
bpy.utils.extension_path_user=lambda package,*a,**k:str(OWN) if package=='mpfb' else orig(package,*a,**k)
sys.path.insert(0,str(SRC));import mpfb
bpy.context.preferences.addons.new().module='mpfb';mpfb.register()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/characters-mpfb-v1/appearance-v1/ruta-appearance-v1.blend'))
from mpfb.entities.rigging.righelpers.leghelpers.leghelpers import LegHelpers
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
bpy.context.view_layer.objects.active=rig;rig.select_set(True)
for b in rig.pose.bones:b.rotation_mode='XYZ';b.rotation_euler=(0,0,0)
settings=dict(leg_helpers_type='LOWERUPPER',leg_target_rotates_foot=True,leg_target_rotates_lower_leg=False,hide_fk=False,leg_parenting='NONE')
# Official helper creates native four-segment leg IK and independently controlled knee.
for side in ['left','right']:LegHelpers.get_instance(side,settings).apply_ik(rig)
bpy.ops.object.mode_set(mode='OBJECT')
for b in rig.pose.bones:b.rotation_mode='XYZ'
# Disable the separate upper-leg target; use an explicit pole on the complete native leg chain.
for s,word in [('L','left'),('R','right')]:
 for c in rig.pose.bones['upperleg02.'+s].constraints:
  if c.type=='IK':c.mute=True
 c=next(c for c in rig.pose.bones['lowerleg02.'+s].constraints if c.type=='IK')
 c.iterations=200;c.use_stretch=False
 for bn in ['upperleg01','upperleg02','lowerleg01','lowerleg02']:rig.pose.bones[bn+'.'+s].ik_stretch=0
 # Knee control remains native MPFB bone; position ahead of knee, used as pole.
 c.pole_target=rig;c.pole_subtarget=word+'_knee_ik';c.pole_angle=-math.pi/2
# Accessories follow the torso skin instead of being immovable children of the armature object.
for o in list(bpy.data.objects):
 if o.type=='MESH' and o.parent==rig and not any(m.type=='ARMATURE' for m in o.modifiers):
  group=o.vertex_groups.new(name='spine03' if 'scarf' in o.name.lower() else 'root');group.add(list(range(len(o.data.vertices))),1.,'REPLACE')
  mod=o.modifiers.new('Motion study accessory skin','ARMATURE');mod.object=rig
# Correct sole weights: fitted source shoes leaked shin deformation into the rigid sole.
shoe=bpy.data.objects['Ruta.shoes01']
for v in shoe.data.vertices:
 if v.co.z<.09:
  blend=max(0,min(1,(.09-v.co.z)/.04));old={g.group:g.weight for g in v.groups}
  for gi,w in old.items():shoe.vertex_groups[gi].add([v.index],w*(1-blend),'REPLACE')
  group=shoe.vertex_groups.get('foot.'+('L' if v.co.x>0 else 'R'))
  group.add([v.index],old.get(group.index,0)*(1-blend)+blend,'REPLACE')
# Relax native A-pose arms by converting desired world vectors to local bone orientation.
for s in ['L','R']:
 b=rig.pose.bones['upperarm01.'+s];rest=b.bone.matrix_local.to_quaternion();direction=Vector((.09 if s=='L' else -.09,.015,-1)).normalized()
 q=(rest@Vector((0,1,0))).rotation_difference(direction)@rest
 b.rotation_euler=(rest.inverted()@q).to_euler('XYZ')
bpy.context.view_layer.update()
for s in ['L','R']:
 b=rig.pose.bones['lowerarm01.'+s];current=(b.tail-b.head).normalized();desired=Vector((.025 if s=='L' else -.025,-.08,-1)).normalized();q=current.rotation_difference(desired);m=b.matrix.copy();m=Matrix.Translation(m.translation)@q.to_matrix().to_4x4()@m.to_quaternion().to_matrix().to_4x4();b.matrix=m
 bpy.context.view_layer.update()
base_arms={s:rig.pose.bones['upperarm01.'+s].rotation_euler.copy() for s in ['L','R']}
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True
scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene.render.fps=100;scene.render.fps_base=3 # 24 genuine samples in 720ms
scene.frame_start=1;scene.frame_end=24
height=next(o for o in bpy.data.objects if o.name=='Ruta.MPFB.Body').dimensions.z
# Final measured E cycle maximum alpha height251px at384px/1.70m.
projected_height=251/384*1.70
meters_to_scene=136/projected_height;stride=.5687545572916666
N=24
rest={s:rig.data.bones['foot.'+s].matrix_local.copy() for s in ['L','R']}
records=[]
def key(b):
 b.keyframe_insert('location');b.keyframe_insert('rotation_euler')
def foot_at(p,side):
 offset=0 if side=='L' else .5
 u=p+offset;k=math.floor(u);f=u-k
 # Plant 60% of cycle; swing clears 4cm with smooth forward travel.
 start=k*stride-offset*stride+.30*stride
 if f<.6:
  y=start;lift=0.;pitch=0.
  if f<.10:pitch=-.12*(1-f/.10)
  if f>.48:pitch=.26*((f-.48)/.12)
 else:
  t=(f-.6)/.4;smooth=t*t*(3-2*t)
  y=start+stride*smooth;lift=.045*math.sin(math.pi*t)**1.25;pitch=.26*(1-t)-.12*t
 return y,f,lift,pitch
for frame in range(1,26):
 p=(frame-1)/N;scene.frame_set(frame)
 rig.location=(0,-p*stride,0);rig.keyframe_insert('location')
 root=rig.pose.bones['root'];m=root.bone.matrix_local.copy();m.translation+=Vector((.008*math.sin(2*math.pi*p),0,-.020-.016*math.cos(4*math.pi*p)));m=Matrix.Translation(m.translation)@Matrix.Rotation(.026*math.sin(2*math.pi*p),4,'Z')@m.to_quaternion().to_matrix().to_4x4();root.matrix=m;key(root)
 for s,word in [('L','left'),('R','right')]:
  y,f,lift,pitch=foot_at(p,s);m=rest[s].copy();m.translation.x=.070 if s=='L' else -.070;m.translation.y-=y-p*stride;m.translation.z+=lift-.003265625
  # Pitch around local transverse axis; heel/toe roll still under evaluation.
  rotation=Matrix.Rotation(pitch,3,'X');pivot=Vector((0,-.132,-.049)) if pitch>0 else Vector((0,.015,-.05));m.translation+=pivot-rotation@pivot
  m=Matrix.Translation(m.translation)@rotation.to_4x4()@m.to_quaternion().to_matrix().to_4x4()
  b=rig.pose.bones[word+'_foot_ik'];b.matrix=m;key(b)
  knee=rig.pose.bones[word+'_knee_ik'];km=knee.bone.matrix_local.copy();km.translation=Vector((.076 if s=='L' else -.076,-.65,.32));knee.matrix=km;key(knee)
 for s,sgn in [('L',1),('R',-1)]:
  b=rig.pose.bones['upperarm01.'+s];b.rotation_euler=base_arms[s].copy();b.rotation_euler.x+=.14*sgn*math.sin(2*math.pi*p);key(b)
 bpy.context.view_layer.update()
 evaluated=rig.evaluated_get(bpy.context.evaluated_depsgraph_get())
 records.append({'frame':frame,'phase':p,'rootWorld':list(rig.location),'feet':{s:{'phase':foot_at(p,s)[1],'ankleWorld':list(evaluated.matrix_world@evaluated.pose.bones['foot.'+s].head),'toeWorld':list(evaluated.matrix_world@evaluated.pose.bones['toe2-3.'+s].tail),'targetWorld':list(evaluated.matrix_world@evaluated.pose.bones[w+'_foot_ik'].head),'kneeWorld':list(evaluated.matrix_world@evaluated.pose.bones['lowerleg01.'+s].head)}for s,w in [('L','left'),('R','right')]}})
for action in bpy.data.actions:
 for fc in action.fcurves:
  for kp in fc.keyframe_points:kp.interpolation='LINEAR'
# Actual production projection: groundScale=sin(elevation)=.65, angle0.
# Model faces -Y; rotate camera around model for E (+X in scene), not mirror frames.
cam=scene.camera;elevation=math.asin(.65)
cam.data.ortho_scale=1.70
views={'E':Vector((-math.cos(elevation)*4,0,math.sin(elevation)*4)), 'front':Vector((0,-math.cos(elevation)*4,math.sin(elevation)*4)), 'three-quarter':Vector((-2.4,-2.4,math.tan(elevation)*math.sqrt(2*2.4**2)))}
def camera(view,p):
 center=Vector((0,-p*stride,.68));cam.location=center+views[view];cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
# Match E in production by character-forward-to-screen mapping, camera stays genuinely volumetric.
scene.frame_set(1);camera('E',0)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))
report={'status':'TECHNICAL MOTION STUDY NOT FINAL ART','productionEnabled':False,'sourceCommit':'25690fa','source':'appearance-v1 rejected generic mannequin','rigBones':len(rig.data.bones),'baseRigBones':163,'mpfb':list(mpfb.VERSION),'blender':bpy.app.version_string,'trackWidthMeters':.14,'pelvisYawRadians':.026,'cycleMs':720,'poses':24,'projectedHeightMeters':projected_height,'projectedHeightCalibration':'final actual E cycle max alpha height251px at384px ortho1.70; physical stride preserved after natural COM/stance correction','metersToScenePixels':meters_to_scene,'strideMeters':stride,'baselineStudyStrideScenePixels':67.46,'strideScenePixels':stride*meters_to_scene,'projection':{'angle':0,'groundScale':.65,'elevationRadians':elevation},'records':records}
(OUT/'measurements.json').write_text(json.dumps(report,indent=2)+'\n')
if os.environ.get('RUBY_MPFB_RENDER','1')=='1':
 for view in ['E','front','three-quarter']:
  frames=range(1,25) if view=='E' else [1,5,9,13,17,21]
  for f in frames:
   scene.frame_set(f);camera(view,(f-1)/N);scene.render.filepath=str(OUT/view/f'{f:02}.png');bpy.ops.render.render(write_still=True)
