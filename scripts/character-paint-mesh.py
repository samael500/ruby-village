"""Blender headless: one painted cutout driven by projected joints from the existing IK action.
/tmp/blender-4.5.3-linux-x64/blender -b art/blender/characters/ruta-motion-prototype.blend -t 2 --python scripts/character-paint-mesh.py
"""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
root=Path(__file__).resolve().parents[1];out=root/'art/characters-walk-v1/mesh-pilot';frames=out/'renders';frames.mkdir(exist_ok=True);spec=json.loads((out/'parts.json').read_text());scene=bpy.context.scene;camera=scene.camera;rig=next(o for o in scene.objects if o.type=='ARMATURE');rig.rotation_euler.z=math.pi/2
# Preserve/export the actual evaluated IK joint coordinates before hiding technical meshes.
poses={}
for frame in range(1,17):
 scene.frame_set(frame);bpy.context.view_layer.update();poses[frame]={}
 for name in ['root','thigh.L','shin.L','foot.L','thigh.R','shin.R','foot.R','arm.R','forearm.R']:
  bone=rig.pose.bones[name]
  points=[]
  for p in [bone.head,bone.tail]:
   q=world_to_camera_view(scene,camera,rig.matrix_world@p);points.append([q.x*256,(1-q.y)*256])
  poses[frame][name]=points
(out/'evaluated-rig-joints.json').write_text(json.dumps(poses,indent=2)+'\n')
for o in list(scene.objects):
 if o.type=='MESH':o.hide_render=True
# Reuse original rig/action, add a 2D orthographic export camera facing the cutout plane.
camera.data.type='ORTHO';camera.data.ortho_scale=320;camera.location=(160,160,1000);camera.rotation_euler=(0,0,0);scene.render.resolution_x=320;scene.render.resolution_y=320;scene.render.resolution_percentage=100;scene.render.film_transparent=True
scene.view_settings.view_transform='Standard';scene.view_settings.look='Medium High Contrast' if 'Medium High Contrast' in [i.name for i in []] else 'None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
for index,(name,item) in enumerate([('body',{'bone':'root','a':[160,170],'b':[160,120]})]+list(spec['parts'].items())):
 image=bpy.data.images.load(str(out/f'{name}.png'),check_existing=True);material=bpy.data.materials.new('painted-'+name);material.use_nodes=True;nodes=material.node_tree.nodes;nodes.clear();output=nodes.new('ShaderNodeOutputMaterial');transparent=nodes.new('ShaderNodeBsdfTransparent');emission=nodes.new('ShaderNodeEmission');texture=nodes.new('ShaderNodeTexImage');texture.image=image;mix=nodes.new('ShaderNodeMixShader');links=material.node_tree.links;links.new(texture.outputs['Color'],emission.inputs['Color']);links.new(texture.outputs['Alpha'],mix.inputs[0]);links.new(transparent.outputs[0],mix.inputs[1]);links.new(emission.outputs[0],mix.inputs[2]);links.new(mix.outputs[0],output.inputs['Surface'])
 # Dense grid stores a continuous 2D skin, bones drive phase-specific positions. No phase repainting.
 verts=[(x,320-y,index*.01) for y in range(0,321,16) for x in range(0,321,16)];faces=[]
 for row in range(20):
  for col in range(20):a=row*21+col;faces.append((a,a+1,a+22,a+21))
 mesh=bpy.data.meshes.new('skin-'+name);mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new('painted-'+name,mesh);scene.collection.objects.link(obj);obj.data.materials.append(material);uv=mesh.uv_layers.new()
 for poly in mesh.polygons:
  for li in poly.loop_indices:
   v=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(v.x/320,v.y/320)
 obj.shape_key_add(name='Basis');a=Vector(item['a']);b=Vector(item['b']);rest=poses[1][item['bone']];scale=224/210
 for frame in range(1,17):
  key=obj.shape_key_add(name=f'phase-{frame:02}');current=poses[frame][item['bone']]
  da=Vector(current[0])-Vector(rest[0]);db=Vector(current[1])-Vector(rest[1]);
  if name=='body':A=a+da*scale;B=b+db*scale
  else:
   projectedOffset=Vector((160-128*scale,256-215.26*scale));A=Vector(current[0])*scale+projectedOffset;B=Vector(current[1])*scale+projectedOffset
  u=b-a;v=B-A;length=max(u.length,1);perp=Vector((-u.y,u.x))/length;newperp=Vector((-v.y,v.x))/max(v.length,1)
  for vertex,original in zip(key.data,verts):
   P=Vector((original[0],320-original[1]));rel=P-a;t=rel.dot(u)/(length*length);side=rel.dot(perp);target=A+t*v+side*newperp;
   if name=='body':
    armDelta=(Vector(poses[frame]['forearm.R'][1])-Vector(poses[1]['forearm.R'][1]))*(224/210);weight=math.exp(-((P.x-163)/17)**2-((P.y-155)/32)**2)*max(0,min(1,(P.y-108)/20));target+=armDelta*weight
   vertex.co=(target.x,320-target.y,original[2])
  for at,value in [(max(1,frame-1),0),(frame,1),(min(17,frame+1),0)]:key.value=value;key.keyframe_insert('value',frame=at)
 # Body above legs at hip seam; back/front layers preserve original physical side, no mirror.
 if name=='body':obj.location.z=.2
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.engine='BLENDER_EEVEE_NEXT';scene.render.fps=20
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'painted-cutout-driven-by-rig.blend'))
for frame in range(1,17):scene.frame_set(frame);scene.render.filepath=str(frames/f'e-{frame:02}.png');bpy.ops.render.render(write_still=True)
print('16 phases from one IK action exported; experimental not final')
