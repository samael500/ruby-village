"""Source-only appearance assembly: native MPFB head study on the measured rig.
No runtime asset activation and no mutation of the source motion .blend.
"""
from pathlib import Path
import bpy,json,math,os,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];variant=int(os.environ.get('RUBY_MPFB_STYLE_VARIANT','1'));OUT=ROOT/('art/characters-mpfb-v1/styled-body-pilot' if variant==1 else f'art/characters-mpfb-v1/styled-body-pilot-v{variant}');OUT.mkdir(parents=True,exist_ok=True)
source=Path('/home/mskorokhod/life/ruby-village-36-mpfb-motion/art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend');style=ROOT/'art/characters-mpfb-v1/native-target-study-8/ruta-head.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(0)
body=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158);rig=next(o for o in bpy.data.objects if o.type=='ARMATURE' and len(o.data.bones)>160)
old_assets=[o for o in bpy.data.objects if o.type=='MESH' and any(k in o.name.lower() for k in ['.long01','.high-poly','.eyebrow006','.eyelashes01'])]
def shape_coords(o):
 states=[(m,m.show_viewport) for m in o.modifiers]
 for m,_ in states:m.show_viewport=False
 bpy.context.view_layer.update();coords=[v.co.copy() for v in o.evaluated_get(bpy.context.evaluated_depsgraph_get()).data.vertices]
 for m,on in states:m.show_viewport=on
 bpy.context.view_layer.update();return coords
old=shape_coords(body);old_asset_names=[o.name for o in old_assets]
with bpy.data.libraries.load(str(style),link=False) as (a,b):b.objects=[n for n in a.objects if n.startswith('Ruta native')]
appended=[o for o in b.objects if o]
for o in appended:scene.collection.objects.link(o)
style_body=next(o for o in appended if o.type=='MESH' and len(o.data.vertices)==19158);styled=shape_coords(style_body);assert len(styled)==len(old)==19158
body.shape_key_clear();changed=0
for i,v in enumerate(body.data.vertices):
 z=styled[i].z;w=max(0,min(1,(z-1.00)/.055));w=w*w*(3-2*w);v.co=old[i].lerp(styled[i],w)
 if w>0:changed+=1
body.data.materials.clear()
for mat in style_body.data.materials:body.data.materials.append(mat)
for o in old_assets:bpy.data.objects.remove(o,do_unlink=True)
new_assets=[]
for o in appended:
 if o.type!='MESH' or o==style_body:continue
 world=o.matrix_world.copy();o.parent=rig;o.matrix_parent_inverse=rig.matrix_world.inverted();o.matrix_world=world
 for mod in o.modifiers:
  if mod.type=='ARMATURE':mod.object=rig
 new_assets.append(o.name)
for o in appended:
 if o==style_body or o.type=='ARMATURE':bpy.data.objects.remove(o,do_unlink=True)
body.data.update();bpy.context.view_layer.update()
if variant>=2:
 import bmesh
 hair=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.endswith('.long01'))
 for v in hair.data.vertices:
  if v.co.z<1.21:
   t=min(1,max(0,(1.21-v.co.z)/.16));v.co.z-=.12*t*t*(3-2*t);v.co.x+=.012*t*math.sin(v.co.z*32+v.co.x*10);v.co.y+=.012*t
 vest=next(o for o in bpy.data.objects if o.name=='Ruta fitted olive waistcoat');bm=bmesh.new();bm.from_mesh(vest.data)
 boundary=[v for v in bm.verts if any(e.is_boundary for e in v.link_edges)]
 for _ in range(10):
  targets={v:sum((e.other_vert(v).co for e in v.link_edges if e.is_boundary),Vector())/sum(e.is_boundary for e in v.link_edges) for v in boundary}
  for v,target in targets.items():v.co=v.co.lerp(target,.55)
 bm.to_mesh(vest.data);bm.free();vest.data.update()
 suit=next(o for o in bpy.data.objects if o.type=='MESH' and '.male_casualsuit01' in o.name);smooth=suit.modifiers.new('Gentle fabric smoothing','SMOOTH');smooth.factor=.45;smooth.iterations=3
 skin=body.data.materials[0];nodes=skin.node_tree.nodes;links=skin.node_tree.links;tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load('/home/mskorokhod/life/_tools/mpfb2-v2.0.18/src/mpfb/data/textures/mpfb_lips.jpg');tex.image.colorspace_settings.name='Non-Color';strength=nodes.new('ShaderNodeMath');strength.operation='MULTIPLY';strength.inputs[1].default_value=.45;links.new(tex.outputs['Color'],strength.inputs[0]);mix=nodes.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(.95,.62,.38,1);mix.inputs[2].default_value=(.60,.17,.12,1);links.new(strength.outputs[0],mix.inputs[0]);links.new(mix.outputs[0],nodes.get('Principled BSDF').inputs['Base Color'])
 for name,color in [('Ruta red scarf',(.40,.015,.022,1)),('Ruta olive vest',(.16,.24,.045,1))]:
  m=bpy.data.materials.get(name)
  if m and m.use_nodes:m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color
 shoes=next(o for o in bpy.data.objects if o.type=='MESH' and '.shoes01' in o.name)
 lace_mat=bpy.data.materials.new('Cream boot laces');lace_mat.diffuse_color=(.72,.60,.40,1)
 for side in ['L','R']:
  bone=rig.data.bones['foot.'+side];a,b=bone.head_local,bone.tail_local;direction=(b-a);direction.z=0;direction.normalize();cross=Vector((-direction.y,direction.x,0));sgn=1 if a.x>0 else -1
  def top(p):
   near=[v.co.z for v in shoes.data.vertices if v.co.x*sgn>0 and (v.co.xy-p.xy).length<.018]
   return max(near) if near else a.z+.025
  for row,t in enumerate([.25,.43,.61]):
   mid=a.lerp(b,t);left=mid-cross*.019;right=mid+cross*.019+direction*.006
   for p in [left,mid,right]:p.z=top(p)+.002
   cu=bpy.data.curves.new('Lace curve','CURVE');cu.dimensions='3D';cu.bevel_depth=.0015;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(2)
   for point,p in zip(sp.points,[left,mid,right]):point.co=(*p,1)
   bpy.ops.object.select_all(action='DESELECT');o=bpy.data.objects.new('Boot lace '+side+str(row),cu);scene.collection.objects.link(o);o.data.materials.append(lace_mat);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o=bpy.context.object;vg=o.vertex_groups.new(name='foot.'+side);vg.add(list(range(len(o.data.vertices))),1,'REPLACE');m=o.modifiers.new('Weighted foot motion','ARMATURE');m.object=rig;o.parent=rig;o.matrix_parent_inverse=rig.matrix_world.inverted();o.select_set(False)

for o in list(bpy.data.objects):
 if o.type in ['LIGHT','CAMERA']:bpy.data.objects.remove(o,do_unlink=True)
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.render.resolution_x=800;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.view_settings.view_transform='AgX';scene.world.use_nodes=True;bg=scene.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.7,.7,.7,1);bg.inputs['Strength'].default_value=.5
root=rig.matrix_world@rig.pose.bones['root'].head;center=Vector((root.x,root.y,.76))
def look(o,p):o.rotation_euler=(p-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=1.85;scene.camera=camera
for loc,power,size in [((-2,-3,4),220,3),((3,-1,2),90,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;look(o,center)
for name,offset in [('front',Vector((0,-3,1.3))),('three-quarter',Vector((-2.5,-2.5,1.5))),('east',Vector((-3,0,1.6)))]:
 camera.location=center+offset;look(camera,center);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-styled-body.blend'))
(OUT/'assembly.json').write_text(json.dumps({'status':'source-only full-body appearance assembly, not approved likeness or validated motion','sourceMotion':str(source),'sourceHead':str(style),'vertexTopology':19158,'restHeadVertexBlendCount':changed,'restNeckTransition':[1.,1.055],'oldHeadAssetsRemoved':old_asset_names,'sourceMotionSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceHeadSha256':hashlib.sha256(style.read_bytes()).hexdigest(),'newNativeHeadAssets':new_assets,'motionRigBones':len(rig.data.bones),'poseFrame':0,'warning':'Head/eye/hair assembly changes require fresh fit/animation review; original motion and current production are unchanged'},indent=2)+'\n')
