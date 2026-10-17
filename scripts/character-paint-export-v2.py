"""Six-view painted cutout export driven by ONE original IK action, not phase generation.
blender -b art/blender/characters/ruta-motion-prototype.blend -t 2 --python scripts/character-paint-export-v2.py -- --directions e,se,sw,w,nw,ne
"""
import bpy,math,json,sys,argparse
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--directions',default='e,se,sw,w,nw,ne');parser.add_argument('--camera-variant',default='all');parser.add_argument('--parts-root',default='art/characters-walk-v1/clean-parts-v2');parser.add_argument('--output',default='art/characters-walk-v1/export-v2');parser.add_argument('--no-render',action='store_true');parser.add_argument('--samples',type=int,default=24);args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
directions=args.directions.split(',');out=root/args.output;out.mkdir(parents=True,exist_ok=True)
scene=bpy.context.scene;projection_camera=scene.camera;rig=next(o for o in scene.objects if o.type=='ARMATURE');source_manifest=json.loads((root/'art/blender/characters/manifest.json').read_text());source_anchor=Vector(source_manifest['footAnchor']);scale=224/210;offset=Vector((160,256))-source_anchor*scale
# Derive view variants from EACH actual scene camera; source paint stays the same six views.
scene_cameras=json.loads((root/'src/scene-v8.json').read_text());groups={}
for scene_id,metadata in scene_cameras.items():
 camera_contract=metadata['camera'];key=(camera_contract['groundScale'],camera_contract['angle']);groups.setdefault(key,{'camera':camera_contract,'scenes':[]})['scenes'].append(scene_id)
variant_specs={};screen_angles={};projection_yaws={};view_direction={};view_variant={};requested=directions[:];directions=[]
for variant_index,(key,group) in enumerate(sorted(groups.items())):
 variant='base' if variant_index==0 else f'calibrated-{variant_index}'
 if args.camera_variant not in ['all',variant]:continue
 variant_specs[variant]=group
 for index,d in enumerate(['e','se','sw','w','nw','ne']):
  if d not in requested:continue
  view=d if variant=='base' else f'{variant}-{d}';directions.append(view);view_direction[view]=d;view_variant[view]=variant
  angle=index*math.pi/3+group['camera']['angle'];screen=math.atan2(group['camera']['groundScale']*math.sin(angle),math.cos(angle));screen_angles[view]=screen;projection_yaws[view]=math.atan2(math.cos(screen),math.sin(screen)/math.sin(math.atan2(3.8,8)))
bones=['root','head','thigh.L','shin.L','foot.L','thigh.R','shin.R','foot.R','arm.L','forearm.L','arm.R','forearm.R']
# Refine the one original action: contact body low, passing high; keep exact foot controls/stride.
# Original .blend is not overwritten. Locked straight contact knees in prototype are not final gait.
for frame in range(1,18):
 scene.frame_set(frame);phase=(frame-1)/16;rootbone=rig.pose.bones['root'];rootbone.location=(0,-.02-.012*math.cos(phase*math.tau*2),0);rootbone.keyframe_insert('location',frame=frame)
# Append idle and start/stop states to that same action.
for index in range(17):
 t=index/16;frame=101+index
 rig.pose.bones['root'].location=(0,-.008+.004*math.sin(t*math.tau),0);rig.pose.bones['root'].keyframe_insert('location',frame=frame)
 for side,phase in [('L',0),('R',math.pi)]:
  foot=rig.pose.bones['foot.'+side];foot.location=(0,0,0);foot.keyframe_insert('location',frame=frame)
  arm=rig.pose.bones['arm.'+side];arm.rotation_euler.x=.025*math.sin(t*math.tau+phase);arm.keyframe_insert('rotation_euler',frame=frame)
 head=rig.pose.bones['head'];head.rotation_euler.z=.005*math.sin(t*math.tau);head.keyframe_insert('rotation_euler',frame=frame)
# Natural half-step start: planted R cancels actor translation; L swings forward. End velocity matches walk.
# Stop variants begin on L/R contact, plant that foot, bring trailing foot to neutral; actor decelerates to zero.
for state,base,contact in [('start',201,'R'),('stop-L',301,'L'),('stop-R',401,'R')]:
 for index in range(9):
  t=index/8;s=t*t if state=='start' else 2*t-t*t;frame=base+index
  for side in ['L','R']:
   if state=='start':y=(-.18 if side=='L' else .18)*s;z=.09*math.sin(math.pi*t) if side=='L' else 0
   else:
    y=(-.18 if side==contact else .18)*(1-s);z=.09*math.sin(math.pi*t) if side!=contact else 0
   foot=rig.pose.bones['foot.'+side];foot.location=(0,-y,z);foot.keyframe_insert('location',frame=frame)
   arm=rig.pose.bones['arm.'+side];arm.rotation_euler.x=.05*math.sin(math.pi*t)*(1 if side=='L' else -1);arm.keyframe_insert('rotation_euler',frame=frame)
  rootbone=rig.pose.bones['root'];rootbone.location=(0,-.008-.024*s if state=='start' else -.032+.024*s,0);rootbone.keyframe_insert('location',frame=frame)
  head=rig.pose.bones['head'];head.rotation_euler.z=0;head.keyframe_insert('rotation_euler',frame=frame)
for curve in rig.animation_data.action.fcurves:
 for key in curve.keyframe_points:key.interpolation='LINEAR'
clips={'walk':{'frames':list(range(1,17)),'durationMs':50,'loop':True},'idle':{'frames':list(range(101,117)),'durationMs':200,'loop':True},'start':{'frames':list(range(201,210)),'durationMs':50,'loop':False},'stop-L':{'frames':list(range(301,310)),'durationMs':50,'loop':False},'stop-R':{'frames':list(range(401,410)),'durationMs':50,'loop':False}}
all_frames=sorted({frame for clip in clips.values() for frame in clip['frames']});poses={}
for direction in directions:
 rig.rotation_euler.z=projection_yaws[direction];poses[direction]={}
 for frame in all_frames:
  scene.frame_set(frame);bpy.context.view_layer.update();poses[direction][frame]={}
  for name in bones:
   bone=rig.pose.bones[name];points=[]
   for point in [bone.head,bone.tail]:
    q=world_to_camera_view(scene,projection_camera,rig.matrix_world@point);points.append([q.x*256,(1-q.y)*256])
   poses[direction][frame][name]=points
(out/'evaluated-joints.json').write_text(json.dumps(poses,indent=2)+'\n')
# Hidden original geometry remains in .blend for audit; one orthographic camera renders all painted views.
for obj in scene.objects:
 if obj.type=='MESH':obj.hide_render=True
camera_data=bpy.data.cameras.new('PaintedExportCamera');camera=bpy.data.objects.new('PaintedExportCamera',camera_data);scene.collection.objects.link(camera);camera.location=(160,160,1000);camera_data.type='ORTHO';camera_data.ortho_scale=320;scene.camera=camera
scene.render.resolution_x=320;scene.render.resolution_y=320;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.fps=20
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
for attr in ['taa_render_samples','taa_samples']:
 if hasattr(scene.eevee,attr):setattr(scene.eevee,attr,args.samples)
objects={};blink_nodes={};source_contracts={}
for direction in directions:
 folder=root/args.parts_root/view_direction[direction];spec=json.loads((folder/'parts.json').read_text());source_contracts[direction]=spec
 collection=bpy.data.collections.new('Painted_'+direction);scene.collection.children.link(collection);objects[direction]=[];items=dict(spec['parts'])
 if 'body' not in items:items={'body':{'file':'body.png','bone':'root','a':[160,170],'b':[160,120],'z':.2},**items}
 for index,(name,item) in enumerate(items.items()):
  image=bpy.data.images.load(str(folder/item.get('file',name+'.png')),check_existing=True);mat=bpy.data.materials.new(direction+'-'+name);mat.use_nodes=True;
  if hasattr(mat,'surface_render_method'):mat.surface_render_method='BLENDED'
  nodes=mat.node_tree.nodes;nodes.clear();output=nodes.new('ShaderNodeOutputMaterial');transparent=nodes.new('ShaderNodeBsdfTransparent');emission=nodes.new('ShaderNodeEmission');texture=nodes.new('ShaderNodeTexImage');texture.image=image;mix=nodes.new('ShaderNodeMixShader');links=mat.node_tree.links
  links.new(texture.outputs['Color'],emission.inputs['Color']);links.new(texture.outputs['Alpha'],mix.inputs[0]);links.new(transparent.outputs[0],mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
  step=16 if item['bone']=='root' else 320;points=320//step+1
  verts=[(x,320-y,float(item.get('z',.2 if name=='body' else index*.01))) for y in range(0,321,step) for x in range(0,321,step)];faces=[]
  for row in range(points-1):
   for col in range(points-1):a=row*points+col;faces.append((a,a+1,a+points+1,a+points))
  mesh=bpy.data.meshes.new(direction+'-'+name);mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new(direction+'-'+name,mesh);collection.objects.link(obj);obj.data.materials.append(mat);objects[direction].append(obj);uv=mesh.uv_layers.new()
  for polygon in mesh.polygons:
   for li in polygon.loop_indices:
    v=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(v.x/320,v.y/320)
  obj.shape_key_add(name='Basis');a=Vector(item['a']);b=Vector(item['b']);u=b-a;length=max(u.length,1);perp=Vector((-u.y,u.x))/length;bone=item['bone'];rest=poses[direction][1][bone]
  for frame in all_frames:
   key=obj.shape_key_add(name=f'rig-{frame:03}');current=poses[direction][frame][bone]
   if bone=='root':A=a+(Vector(current[0])-Vector(rest[0]))*scale;B=b+(Vector(current[1])-Vector(rest[1]))*scale
   else:A=Vector(current[0])*scale+offset;B=Vector(current[1])*scale+offset
   v=B-A;
   if bone.startswith('foot.'):v=v.normalized()*length
   newperp=Vector((-v.y,v.x))/max(v.length,1)
   for vertex,original in zip(key.data,verts):
    P=Vector((original[0],320-original[1]));rel=P-a;target=A+rel.dot(u)/(length*length)*v+rel.dot(perp)*newperp
    if bone=='root':
     # Localized sleeve/forearm skin movement; face and satchel are not regenerated.
     for side in ['L','R']:
      center=Vector(poses[direction][1]['forearm.'+side][1])*scale+offset;delta=(Vector(poses[direction][frame]['forearm.'+side][1])-Vector(poses[direction][1]['forearm.'+side][1]))*scale
      weight=math.exp(-((P.x-center.x)/17)**2-((P.y-center.y)/25)**2)*max(0,min(1,(P.y-115)/20));target+=delta*weight
    vertex.co=(target.x,320-target.y,original[2])
   for at,value in [(max(1,frame-1),0),(frame,1),(frame+1,0)]:key.value=value;key.keyframe_insert('value',frame=at)
  if name=='body' and (folder/'body-blink.png').exists():blink_nodes[direction]=(texture,image,bpy.data.images.load(str(folder/'body-blink.png'),check_existing=True))
# Portable .blend stores every source texture and original/evaluated action for all directions.
for direction,parts in objects.items():
 for obj in parts:obj.hide_render=direction!=directions[0]
scene.frame_set(1);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'ruta-painted-six-view.blend'))
manifest={'schemaVersion':2,'status':'candidate-needs-visual-validation','productionEnabled':False,'frameSize':[320,320],'footAnchor':[160,256],'nativeHeightPx':224,'targetDisplayHeightPx':136,'cycleDurationMs':800,'strideWorldUnits':.72,'sourceRig':'art/blender/characters/ruta-motion-prototype.blend','screenDirectionAnglesRadians':screen_angles,'sourceYawRadians':projection_yaws,'projectionReference':{'file':'src/scene-v8.json','note':'all distinct scene calibrations export their own six retargeted limb directions; body identity and original camera are preserved'},'sourceActionRefinement':{'walkRootLocalY':'-.02-.012*cos(4*pi*phase)','reason':'soft contact knees, body rises in passing; foot controls and stride unchanged','idleRootLocalY':'-.008+.004*sin(2*pi*phase)'},'sourceContracts':source_contracts,'directions':{}}
for direction in directions:
 for d,parts in objects.items():
  for obj in parts:obj.hide_render=d!=direction
 manifest['directions'][direction]={'screenAngleRadians':screen_angles[direction],'sourceYawRadians':projection_yaws[direction],'projectedStridePixels':.72*256/2.65*(136/210)*math.hypot(math.sin(projection_yaws[direction]),math.cos(projection_yaws[direction])*math.sin(math.atan2(3.8,8))),'clips':{}}
 for state,clip in clips.items():
  folder=out/'renders'/direction/state;folder.mkdir(parents=True,exist_ok=True);outputframes=[]
  for index,frame in enumerate(clip['frames']):
   scene.frame_set(frame);scene.render.filepath=str(folder/f'{index:02}.png');
   if not args.no_render:bpy.ops.render.render(write_still=True)
   entry={'file':str(Path(scene.render.filepath).relative_to(root)),'sourceRect':[0,0,320,320],'frameSize':[320,320],'footAnchor':[160,256],'durationMs':clip['durationMs']}
   if state=='walk' and index in [0,8]:entry['contact']='left' if index==0 else 'right'
   if state in ['start','stop-L','stop-R'] and index==8:
    entry['durationMs']=1;entry['contact']='left' if state in ['start','stop-R'] else 'right'
   if state in ['start','stop-L','stop-R']:entry['motionFraction']=((index/8)**2 if state=='start' else 2*(index/8)-(index/8)**2)
   if state=='idle' and index==8 and direction in blink_nodes:
    entry['durationMs']=60;outputframes.append(entry);node,open_image,closed_image=blink_nodes[direction];node.image=closed_image;blinkfile=folder/'08-blink.png';scene.render.filepath=str(blinkfile);
    if not args.no_render:bpy.ops.render.render(write_still=True)
    node.image=open_image;outputframes.append({**entry,'file':str(blinkfile.relative_to(root)),'durationMs':80,'blink':True});entry={**entry,'durationMs':60}
   outputframes.append(entry)
  manifest['directions'][direction]['clips'][state]={'loop':clip['loop'],'frames':outputframes,'actorWorldDistance':.18 if state in ['start','stop-L','stop-R'] else None}
raw_directions=manifest['directions'];manifest['cameraVariants']={variant:{**group,'directions':{view_direction[view]:raw_directions[view] for view in directions if view_variant[view]==variant}} for variant,group in variant_specs.items()};manifest['sceneCameraVariant']={scene_id:variant for variant,group in variant_specs.items() for scene_id in group['scenes']};manifest['directions']=manifest['cameraVariants'][next(iter(variant_specs))]['directions'];manifest['rigidBootTextures']=True
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Painted rig export complete; artistic/runtime validation still required')
