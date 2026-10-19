"""Minimal stock-part assembly, not garment sewing or retargeted replacement motion."""
from pathlib import Path
from collections import defaultdict
import bpy,bmesh,json,hashlib,math,os
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-adapted-v1';OUT.mkdir(exist_ok=True)
HAIR_SOURCE=Path('/home/mskorokhod/life/ruby-village-36-mpfb/art/characters-mpfb-v1/styled-body-pilot-v3/ruta-styled-body.blend')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/ready-character-colour-v1/adventurer-colour-study.blend'));scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.data.pose_position='REST';bpy.context.view_layer.update()
def digest(x):return hashlib.sha256(repr(x).encode()).hexdigest()
def action_hash():
 a=bpy.data.actions['Walk'];return digest([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])
walk_hash=action_hash();bones_hash=digest([(b.name,tuple(b.head_local),tuple(b.tail_local))for b in rig.data.bones])
def bind(o,weights):
 o.parent=rig;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4)
 o.vertex_groups.clear()
 for name in set(n for row in weights for n in row):o.vertex_groups.new(name=name)
 for i,row in enumerate(weights):
  for n,w in row.items():o.vertex_groups[n].add([i],w,'REPLACE')
 for mod in list(o.modifiers):o.modifiers.remove(mod)
 mod=o.modifiers.new('Native stock armature','ARMATURE');mod.object=rig
# Identify complete disconnected accessory pieces without cutting any garment faces.
body=bpy.data.objects['Adventurer_Body'];keys=[tuple(round(c,5)for c in v.co)for v in body.data.vertices];adj=defaultdict(set)
for e in body.data.edges:
 a,b=(keys[i]for i in e.vertices);adj[a].add(b);adj[b].add(a)
seen=set();components=[]
for key in adj:
 if key in seen:continue
 todo=[key];seen.add(key);group=set()
 while todo:
  a=todo.pop();group.add(a)
  for b in adj[a]:
   if b not in seen:seen.add(b);todo.append(b)
 components.append(group)
keep=max(components,key=len);bm=bmesh.new();bm.from_mesh(body.data);gone=[v for v in bm.verts if tuple(round(c,5)for c in v.co)not in keep];removed=len(gone);bmesh.ops.delete(bm,geom=gone,context='VERTS');bm.to_mesh(body.data);bm.free()
# Swap ready-made long trousers from the identical native rig (zero rest-bone difference).
with bpy.data.libraries.load(str(ROOT/'art/ready-character-walk-v1/source/casual-imported.blend'),link=False)as(src,dst):dst.objects=['Casual_Legs']
pants=dst.objects[0];scene.collection.objects.link(pants);pants.name='Ruta stock long trousers'
for mod in pants.modifiers:
 if mod.type=='ARMATURE':mod.object=rig
pants.parent=rig;pants.matrix_parent_inverse=Matrix.Identity(4);pants.matrix_basis=Matrix.Identity(4)
oldlegs=bpy.data.objects['Adventurer_Legs'];bpy.data.objects.remove(oldlegs,do_unlink=True)
# Cream shirt and brown trousers use ready geometry, not a new vest mesh.
def mat(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1);bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.8;return m
brown=mat('Adapted warm brown leather',(.20,.085,.03));canvas=mat('Adapted brown trousers',(.18,.095,.052));gold=mat('Adapted warm brass',(.45,.25,.05))
pants.data.materials.clear();pants.data.materials.append(canvas)
# Remove only stock short-hair polygons, preserving actual head/face vertices and weights.
head=bpy.data.objects['Adventurer_Head'];bm=bmesh.new();bm.from_mesh(head.data);gone=[f for f in bm.faces if head.data.materials[f.material_index].name.startswith('Hair_')];bmesh.ops.delete(bm,geom=gone,context='FACES');bm.to_mesh(head.data);bm.free()
HAIR_CACHE=OUT/'source/ginger-native-part.blend'
load_source=HAIR_CACHE if HAIR_CACHE.exists() else HAIR_SOURCE
with bpy.data.libraries.load(str(load_source),link=False)as(src,dst):dst.objects=[n for n in src.objects if '.cortu_strawberry_cloud_hair' in n]
hair=dst.objects[0];scene.collection.objects.link(hair)
if not HAIR_CACHE.exists():
 hair.parent=None
 for mod in list(hair.modifiers):hair.modifiers.remove(mod)
 bpy.data.libraries.write(str(HAIR_CACHE),{hair},fake_user=True)
hair.name='Ruta CC0 ginger waves'
for v in hair.data.vertices:
 v.co.x=(v.co.x-.026)*.72;v.co.y=(v.co.y+.010)*.72-.070;v.co.z=1.81+(v.co.z-1.4145)*.62
 if v.co.z<1.72:v.co.z-=(1.72-v.co.z)
bind(hair,[{'Head':1.}for v in hair.data.vertices])
# One genuine 3D satchel, rigidly weighted to Hips; single diagonal strap blends torso/hips.
def cube(name,center,size,material,bone='Hips'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=center);o=bpy.context.object;o.name=name;o.dimensions=size;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True);o.data.materials.append(material)
 bevel=o.modifiers.new('Soft leather edge','BEVEL');bevel.width=.012;bevel.segments=2;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=bevel.name)
 bind(o,[{bone:1.}for v in o.data.vertices]);return o
bag=cube('ONE hip satchel',(-.235,-.020,1.005),(.22,.12,.22),brown)
cube('Satchel flap',(-.235,-.087,1.052),(.225,.023,.105),brown)
cube('Satchel buckle',(-.235,-.104,1.040),(.035,.010,.040),gold)
curve=bpy.data.curves.new('Single diagonal strap path','CURVE');curve.dimensions='3D';curve.bevel_depth=.014;curve.bevel_resolution=2;spline=curve.splines.new('BEZIER');spline.bezier_points.add(3)
for p,co in zip(spline.bezier_points,[(.12,-.115,1.49),(.035,-.175,1.34),(-.115,-.16,1.18),(-.235,-.09,1.11)]):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
strap=bpy.data.objects.new('ONE diagonal satchel strap',curve);scene.collection.objects.link(strap);strap.data.materials.append(brown);bpy.ops.object.select_all(action='DESELECT');strap.select_set(True);bpy.context.view_layer.objects.active=strap;bpy.ops.object.convert(target='MESH');strap=bpy.context.object
weights=[]
for v in strap.data.vertices:
 w=max(0,min(1,(v.co.z-1.1)/.35));weights.append({'Chest':w,'Hips':1-w})
bind(strap,weights)
rig.data.pose_position='POSE';scene.frame_set(0);bpy.context.view_layer.update();assert walk_hash==action_hash();assert bones_hash==digest([(b.name,tuple(b.head_local),tuple(b.tail_local))for b in rig.data.bones])
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-stock-adapted.blend'))
report={'status':'minimal-stock-parts-pilot-not-approved-Ruta','rigBones':len(rig.data.bones),'walkActionSha256':walk_hash,'stockBoneRestSha256':bones_hash,'sourceActionsAndBoneRestUnchanged':True,'removedAccessoryVertices':removed,'removedAccessories':'all disconnected backpack/bedroll/strap/buckle pieces; main shirt+arms component preserved without face cuts','trousers':'Casual_Legs, same CC0 pack, identical62-bone rest skeleton measured restdiff0m, original weights preserved','hair':{'source':str(HAIR_SOURCE),'sourceSha256':hashlib.sha256(HAIR_SOURCE.read_bytes()).hexdigest(),'part':'Cortu Johnstone strawberry_cloud, CC0 official hair01 pack; stale OBJheader documented','fit':'scalp xy.72/z.62, lower wave length extended, native mesh Head1','physics':'rigid head-bound; no extra hair motion authored'},'satchel':'one native beveled rigid Hips-weighted bag with flap/buckle; one Chest/Hips blended diagonal strap','limitations':['adult stock proportions and low-poly likeness remain','no new vest; source green shirt retained','hair/boot/trouser/bag intersections require three-view and loop review','no production or six-direction batch']}
(OUT/'assembly.json').write_text(json.dumps(report,indent=2)+'\n')
if os.environ.get('ADAPTED_RENDER')=='1':
 for name,yaw in [('front',0),('three-quarter',math.pi/4),('e',math.pi/2)]:
  rig.rotation_euler.z=yaw;scene.frame_set(0);scene.render.filepath=str(OUT/(name+'-00.png'));bpy.ops.render.render(write_still=True)
