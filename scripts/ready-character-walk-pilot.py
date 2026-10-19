"""Render a real CC0 rig/action; no image deformation or synthetic poses."""
from pathlib import Path
import bpy,json,math,hashlib,os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-walk-v1';FRAMES=OUT/'e';FRAMES.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'source/adventurer-imported.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];meshes=[o for o in scene.objects if o.type=='MESH' and o.parent==rig]
for track in rig.animation_data.nla_tracks:track.mute=True
walk=bpy.data.actions['Walk'];rig.animation_data.action=walk;rig.animation_data.action_slot=walk.slots[0]
scene.render.fps=24;scene.render.film_transparent=True;scene.render.resolution_x=512;scene.render.resolution_y=640;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True
scene.world=bpy.data.worlds.new('Neutral pilot world');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.68,.74,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
scene.view_settings.view_transform='Standard'
for pos,power,size in [((-3,-4,6),450,5),((4,-1,4),220,4),((0,4,5),300,3)]:
 bpy.ops.object.light_add(type='AREA',location=pos);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size
center=Vector((0,0,.85));bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=2.1;scene.camera=camera
camera.location=center+Vector((0,-8,8*.65/math.sqrt(1-.65**2)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
yaws={name:math.atan2(math.cos(i*math.pi/3),math.sin(i*math.pi/3)/.65) for i,name in enumerate(['e','se','sw','w','nw','ne'])};rig.rotation_mode='XYZ';rig.rotation_euler.z=yaws['e']
scene.frame_set(0);bpy.context.view_layer.update();anchor=world_to_camera_view(scene,camera,Vector((0,0,0)));anchorpx=[anchor.x*512,(1-anchor.y)*640]
source_hash=hashlib.sha256((OUT/'source/adventurer-original.gltf').read_bytes()).hexdigest()
def snapshot(frame):
 scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();points=[]
 for o in meshes:
  ev=o.evaluated_get(dg);me=ev.to_mesh();points.extend(ev.matrix_world@v.co for v in me.vertices);ev.to_mesh_clear()
 bones={n:list(rig.matrix_world@rig.pose.bones[n].head) for n in ['Hips','UpperLeg.L','LowerLeg.L','Foot.L','UpperLeg.R','LowerLeg.R','Foot.R']}
 return {'sourceFrame':frame,'bounds':[[min(v[k] for v in points),max(v[k] for v in points)]for k in range(3)],'pose':bones,'evaluatedMeshSha256':hashlib.sha256(repr([tuple(v)for v in points]).encode()).hexdigest()}
a=snapshot(0);b=snapshot(40);seam=max((Vector(a['pose'][n])-Vector(b['pose'][n])).length for n in a['pose'])
rows=[]
for i in range(24):
 frame=40*i/24;row=snapshot(frame);row['index']=i;rows.append(row)
contract={'status':'real-rig-walk-source-pilot-not-Ruta-likeness-approved','productionEnabled':False,'sourceSha256':source_hash,'sourceAction':'Walk','sourceRange':[0,40],'sourceFps':24,'cycleDurationMs':40/24*1000,'frameCount':24,'frameSize':[512,640],'footAnchor':anchorpx,'groundScale':.65,'orthographicScaleMeters':2.1,'orthographicWidthMeters':1.68,'nativeHorizontalPixelsPerMeter':640/2.1,'endpointEvaluatedMeshHashEqual':a['evaluatedMeshSha256']==b['evaluatedMeshSha256'],'cameraElevationRadians':math.asin(.65),'sixViewYawRadians':yaws,'renderedViews':['e'],'endpointBonePositionErrorMeters':seam,'rigBones':len(rig.data.bones),'meshes':[o.name for o in meshes],'frames':rows,'limitations':['stock adult low-poly Adventurer, not approved Ruta likeness','no bespoke wardrobe or satchel added','only E pilot rendered; no runtime installation','foot sliding/ground contacts measured, visual review pending']}
(OUT/'contract.json').write_text(json.dumps(contract,indent=2)+'\n');scene.frame_set(0);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'adventurer-walk-pilot.blend'))
indices=[0] if os.environ.get('READY_WALK_SINGLE')=='1' else range(24)
for i in indices:
 frame=40*i/24;scene.frame_set(int(frame),subframe=frame-int(frame));scene.render.filepath=str(FRAMES/f'{i:02}.png');bpy.ops.render.render(write_still=True)
