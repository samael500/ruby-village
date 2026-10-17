"""Headless reproducible technical motion prototype, not final 2D artwork.
/tmp/blender-4.5.3-linux-x64/blender -b -t 2 --python scripts/character-rig.py
"""
import bpy, math, json, os
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1]; OUT=R/'art/characters-walk-v1/holistic-pilot-v4/volume'; frames=OUT/'renders'; frames.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene; scene.render.engine='BLENDER_WORKBENCH'; scene.render.resolution_x=512; scene.render.resolution_y=512; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.render.film_transparent=True
scene.display.shading.light='STUDIO'; scene.display.shading.color_type='MATERIAL'; scene.display.shading.show_shadows=True; scene.display.shading.show_cavity=True; scene.display.shading.cavity_type='BOTH'; scene.display.shading.show_specular_highlight=False; scene.view_settings.view_transform='Standard'
scene.render.fps=200; scene.render.fps_base=9; scene.frame_start=1; scene.frame_end=16
palette={'skin':(.91,.62,.39,1),'hair':(.32,.12,.045,1),'shirt':(.88,.83,.66,1),'vest':(.22,.29,.12,1),'scarf':(.48,.025,.035,1),'pants':(.29,.16,.08,1),'boot':(.16,.075,.03,1),'bag':(.32,.14,.045,1),'white':(.95,.96,.90,1),'blue':(.045,.27,.48,1),'black':(.025,.02,.018,1)}
mats={}
for name,color in palette.items():
 m=bpy.data.materials.new(name); m.diffuse_color=color; mats[name]=m
# Armature has explicit IK contacts and a keyed shared cycle.
data=bpy.data.armatures.new('RutaMotionRig'); rig=bpy.data.objects.new('RutaMotionRig',data); scene.collection.objects.link(rig); bpy.context.view_layer.objects.active=rig; rig.select_set(True); bpy.ops.object.mode_set(mode='EDIT')
def bone(name,head,tail,parent=None,deform=True):
 b=data.edit_bones.new(name); b.head=head; b.tail=tail; b.use_deform=deform
 if parent: b.parent=data.edit_bones[parent]
 return b
bone('root',(0,0,.9),(0,0,1.1)); bone('torso',(0,0,.9),(0,0,1.48),'root'); bone('head',(0,0,1.48),(0,0,1.95),'torso')
for side,x in [('L',.145),('R',-.145)]:
 bone('thigh.'+side,(x,0,.94),(x,-.045,.52),'root'); bone('shin.'+side,(x,-.045,.52),(x,0,.13),'thigh.'+side)
 bone('foot.'+side,(x,0,.13),(x,-.23,.13),None,True)
 bone('pole.'+side,(x,-1,.55),(x,-1,.7),None,False)
 sx=.28 if side=='L' else -.28
 bone('arm.'+side,(sx,0,1.4),(sx*1.18,0,1.02),'torso'); bone('forearm.'+side,(sx*1.18,0,1.02),(sx*1.15,-.015,.83),'arm.'+side)
bpy.ops.object.mode_set(mode='OBJECT'); rig.select_set(False)
for side in ['L','R']:
 con=rig.pose.bones['shin.'+side].constraints.new('IK'); con.target=rig; con.subtarget='foot.'+side; con.chain_count=2; con.pole_target=rig; con.pole_subtarget='pole.'+side; con.pole_angle=-math.pi/2
# Rigid weighted meshes keep technical limb articulation explicit and editable.
def attach(obj,b):
 if b:
  obj.parent=rig
  vg=obj.vertex_groups.new(name=b); vg.add(list(range(len(obj.data.vertices))),1,'REPLACE'); mod=obj.modifiers.new('Ruta armature','ARMATURE'); mod.object=rig
 return obj
def ell(name,loc,scale,mat,b):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=loc); o=bpy.context.object; o.name=name; o.scale=scale; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(mats[mat]);
 for poly in o.data.polygons: poly.use_smooth=True
 attach(o,b); return o
def link(name,a,b,radius,mat,bone):
 a,b=Vector(a),Vector(b); o=ell(name,(a+b)/2,(radius,radius,(b-a).length/2+radius*.3),mat,bone); o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
ell('trousers hips',(0,0,.94),(.23,.15,.17),'pants','root')
ell('cream shirt',(0,0,1.22),(.27,.16,.33),'shirt','torso'); ell('olive vest',(0,.01,1.22),(.275,.165,.28),'vest','torso')
# Front open cream shirt panel.
ell('shirt front',(0,-.163,1.24),(.075,.022,.24),'shirt','torso')
ell('neck',(0,0,1.53),(.09,.09,.13),'skin','head'); ell('head',(0,-.005,1.78),(.265,.23,.31),'skin','head')
ell('loose hair back',(0,.13,1.61),(.30,.16,.40),'hair','head')
ell('hair cap',(0,.055,1.94),(.28,.23,.17),'hair','head')
for x in [-.25,.25]:
 ell('loose hair side',(x,.015,1.64),(.105,.15,.34),'hair','head'); ell('ear',(x,-.045,1.75),(.05,.04,.08),'skin','head')
for x in [-.096,.096]:
 ell('eye white',(x,-.216,1.80),(.055,.025,.071),'white','head'); ell('blue iris',(x,-.239,1.80),(.028,.012,.044),'blue','head'); ell('pupil',(x,-.25,1.80),(.013,.009,.027),'black','head')
ell('nose',(0,-.242,1.725),(.035,.045,.041),'skin','head'); ell('smile',(0,-.225,1.64),(.065,.013,.017),'scarf','head')
ell('neck scarf knot',(0,-.17,1.48),(.065,.05,.055),'scarf','torso'); link('scarf end L',(0,-.18,1.46),(-.065,-.18,1.29),.04,'scarf','torso');link('scarf end R',(0,-.18,1.46),(.055,-.18,1.28),.035,'scarf','torso')
for side,x in [('L',.145),('R',-.145)]:
 link('trouser upper '+side,(x,0,.94),(x,-.045,.52),.11,'pants','thigh.'+side);link('trouser lower '+side,(x,-.045,.52),(x,0,.16),.09,'pants','shin.'+side)
 ell('boot '+side,(x,-.10,.105),(.115,.21,.10),'boot','foot.'+side)
 sx=.28 if side=='L' else -.28
 link('shirt sleeve '+side,(sx,0,1.4),(sx*1.18,0,1.02),.075,'shirt','arm.'+side); link('forearm '+side,(sx*1.18,0,1.02),(sx*1.15,-.015,.83),.05,'skin','forearm.'+side);ell('hand '+side,(sx*1.15,-.015,.82),(.055,.05,.07),'skin','forearm.'+side)
# Satchel remains at character right (-X), never mirrored; one diagonal strap.
ell('single satchel',(-.29,0,.91),(.14,.13,.17),'bag','root');link('one strap front',(.20,-.18,1.47),(-.29,-.17,.98),.028,'bag','torso');link('one strap back',(.20,.17,1.47),(-.29,.17,.98),.028,'bag','torso')
# One continuous volumetric trouser surface, not separately stretched painted planes.
parts=[o for o in scene.objects if o.type=='MESH' and (o.name=='trousers hips' or o.name.startswith('trouser upper') or o.name.startswith('trouser lower'))]
bpy.ops.object.select_all(action='DESELECT')
for o in parts:
 for mod in list(o.modifiers):o.modifiers.remove(mod)
 o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);bpy.ops.object.join();pants=bpy.context.object;pants.name='continuous volumetric trousers'
for group in list(pants.vertex_groups):pants.vertex_groups.remove(group)
remesh=pants.modifiers.new('Continuous cloth union','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.018;remesh.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=remesh.name)
smooth=pants.modifiers.new('Cloth surface relaxation','SMOOTH');smooth.factor=.6;smooth.iterations=4;bpy.ops.object.modifier_apply(modifier=smooth.name)
groups={n:pants.vertex_groups.new(name=n)for n in ['root','thigh.L','shin.L','thigh.R','shin.R']}
for v in pants.data.vertices:
 x,y,z=v.co;root_weight=max(0,min(1,(z-.79)/.14));side='L' if x>=0 else 'R';shin_weight=max(0,min(1,(.60-z)/.16));weights={'root':root_weight,'thigh.'+side:(1-root_weight)*(1-shin_weight),'shin.'+side:(1-root_weight)*shin_weight}
 for name,w in weights.items():
  if w>0:groups[name].add([v.index],w,'REPLACE')
mod=pants.modifiers.new('Continuous weighted cloth skin','ARMATURE');mod.object=rig;pants.parent=rig
# Verify one connected mesh before rendering any poses.
links={v.index:set()for v in pants.data.vertices}
for edge in pants.data.edges:
 a,b=edge.vertices;links[a].add(b);links[b].add(a)
seen=set();stack=[0]
while stack:
 index=stack.pop()
 if index in seen:continue
 seen.add(index);stack.extend(links[index]-seen)
assert len(seen)==len(pants.data.vertices),('disconnected trousers',len(seen),len(pants.data.vertices))
(OUT/'mesh-audit.json').write_text(json.dumps({'status':'technical whole-volume experiment, appearance NOT accepted','pantsVertices':len(seen),'pantsConnectedComponents':1,'sourceOfMovement':'one3DIKaction, continuous skinned volume, rigid solid boots','cycleDurationMs':720,'frameCount':16,'appearanceLimitation':'Original capsule motion model is not approved Ruta; this proves continuous geometry only'},indent=2))
for frame in range(1,18):
 phase=(frame-1)/16; angle=phase*math.tau
 root=rig.pose.bones['root']; root.location=(0,-.02-.012*math.cos(2*angle),0);root.keyframe_insert(data_path='location',frame=frame)
 for side,offset in [('L',0),('R',.5)]:
  t=(phase+offset)%1; control=rig.pose.bones['foot.'+side]
  # 0..half: planted foot moves backward at constant speed; half..1: swing forward.
  y=(-.18+.72*t) if t<.5 else (.18-.72*(t-.5)); z=0 if t<.5 else .09*math.sin((t-.5)*math.tau)
  # Control bone local Y points forward (-Y world), local Z points up.
  control.location=(0,-y,z);control.keyframe_insert(data_path='location',frame=frame)
  arm=rig.pose.bones['arm.'+side];arm.rotation_mode='XYZ';arm.rotation_euler.x=.20*math.sin(angle+offset*math.tau);arm.keyframe_insert(data_path='rotation_euler',frame=frame)
 h=rig.pose.bones['head'];h.rotation_mode='XYZ';h.rotation_euler.z=.015*math.sin(angle);h.keyframe_insert(data_path='rotation_euler',frame=frame)
# Exact sample interpolation; one action, same geometry for all cameras.
for fc in rig.animation_data.action.fcurves:
 for key in fc.keyframe_points: key.interpolation='LINEAR'
camd=bpy.data.cameras.new('ExportCamera');cam=bpy.data.objects.new('ExportCamera',camd);scene.collection.objects.link(cam);cam.location=(0,-8,4.8);target=Vector((0,0,1.0));cam.rotation_euler=(target-Vector(cam.location)).to_track_quat('-Z','Y').to_euler();camd.type='ORTHO';camd.ortho_scale=2.65;scene.camera=cam
scene.frame_set(1);bpy.context.view_layer.update();ground=world_to_camera_view(scene,cam,Vector((0,0,0)));anchor=[round(ground.x*512,3),round((1-ground.y)*512,3)]
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-motion-prototype.blend'))
manifest={'schemaVersion':1,'status':'technical-motion-prototype-not-final-art','source':'ruta-motion-prototype.blend','frameSize':[512,512],'footAnchor':anchor,'nativeHeightPx':210,'strideWorldUnits':.72,'cycleDurationMs':720,'fps':200/9,'clips':{}}
# Camera elevation determines route projection. Solve world yaw for each screen vector.
elevation=math.atan2(cam.location.z-1,8);dirs=['e']
for i,d in enumerate(dirs):
 a=i*math.pi/3; wx=math.cos(a);wy=-math.sin(a)/math.sin(elevation);yaw=math.atan2(wx,-wy);rig.rotation_euler.z=yaw
 manifest['clips'][d]={'loop':True,'yawRadians':yaw,'frames':[]}
 for f in range(1,17):
  scene.frame_set(f);bpy.context.view_layer.update();scene.render.filepath=str(frames/f'{d}-{f:02}.png');bpy.ops.render.render(write_still=True)
  item={'file':f'renders/{d}-{f:02}.png','sourceRect':[0,0,512,512],'footAnchor':anchor,'durationMs':45}
  if f in [1,9]:item['contact']='left' if f==1 else 'right'
  manifest['clips'][d]['frames'].append(item)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
