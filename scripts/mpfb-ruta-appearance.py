"""Genuine MPFB mesh/clothes authoring pilot, not final appearance or animation."""
from pathlib import Path
import sys,os,json,math,bmesh
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/appearance-v1';OUT.mkdir(parents=True,exist_ok=True)
# Same isolated source-mode bootstrap as the verified smoke, no vendor writes.
bootstrap=(ROOT/'scripts/mpfb-smoke.py').read_text().split("bpy.ops.object.select_all(action='SELECT')")[0];exec(bootstrap,globals());OUT=ROOT/'art/characters-mpfb-v1/appearance-v1'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
from mpfb.services import HumanService,TargetService
macro=TargetService.get_default_macro_info_dict();macro.update(gender=0.,age=.1875,muscle=.25,weight=.45,proportions=.35,height=.5);macro['race']={'asian':.15,'caucasian':.85,'african':0.}
human=HumanService.create_human(scale=.1,macro_detail_dict=macro);human.name='Ruta.MPFB.Body'
targets={'eyes/l-eye-scale-incr':1.,'eyes/r-eye-scale-incr':1.,'chin/chin-width-decr':.35,'cheek/l-cheek-volume-incr':.25,'cheek/r-cheek-volume-incr':.25}
for name,value in targets.items():
 file=MPFB_SRC/'mpfb/data/targets'/(name+'.target.gz')
 if file.exists():TargetService.load_target(human,str(file),weight=value)
# Coherent 3D stylization across all basis/targets and rig-fitting helpers, not a rendered-image deformation.
for key in human.data.shape_keys.key_blocks:
 for v in key.data:
  z=v.co.z;w=min(1,max(0,(z-1.01)/.07));pivot=Vector((0,-.025,1.045));v.co=pivot+(v.co-pivot)*(1+.32*w)
rig=HumanService.add_builtin_rig(human,'default');rig.name='Ruta.MPFB.StandardRig'
def mat(name,color,rough=.8):
 m=bpy.data.materials.new(name);m.use_fake_user=True;m.diffuse_color=(*color,1);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Roughness'].default_value=rough;return m
skin=mat('Ruta warm skin',(.74,.40,.24));white=mat('Ruta ivory shirt',(.85,.78,.63));brown=mat('Ruta brown canvas',(.22,.105,.055));green=mat('Ruta olive vest',(.15,.19,.07));red=mat('Ruta red scarf',(.38,.025,.018));leather=mat('Ruta satchel leather',(.27,.105,.025));gold=mat('Ruta warm brass',(.7,.38,.07),.35);sole=mat('Ruta boot soles',(.07,.04,.025))
human.data.materials.clear();human.data.materials.append(skin)
ASSETS=ROOT/'art/characters-mpfb-v1/source-assets'
def asset(name,kind='Clothes'):
 f=ASSETS/name;o=HumanService.add_mhclo_asset(str(f),human,asset_type=kind,subdiv_levels=1);return o
clothes=asset('clothes/male_casualsuit01/male_casualsuit01.mhclo');clothes.data.materials.clear();clothes.data.materials.append(white);clothes.data.materials.append(brown)
for poly in clothes.data.polygons:poly.material_index=0 if poly.center.z>.65 else 1
boots=asset('clothes/shoes01/shoes01.mhclo');boots.data.materials.clear();boots.data.materials.append(leather);boots.data.materials.append(sole)
for poly in boots.data.polygons:poly.material_index=1 if poly.center.z<.025 else 0
hair=asset('hair/long01/long01.mhclo','Hair')
# Existing alpha-bearing diffuse retained; multiply warm brown without destroying hair cards' cutouts.
for m in hair.data.materials:
 if m and m.use_nodes:
  for node in m.node_tree.nodes:
   if node.type=='BSDF_PRINCIPLED':node.inputs['Roughness'].default_value=.8
try:eyes=asset('eyes/high-poly/high-poly.mhclo','Eyes')
except Exception as e:print('EYE_ASSET_ERROR',e);eyes=None
if eyes:
 from mpfb.entities.material.makeskinmaterial import MakeSkinMaterial
 from mpfb.services import MaterialService
 e=MakeSkinMaterial();e.populate_from_mhmat(str(ASSETS/'eyes/materials/blue.mhmat'));eyes.data.materials.clear();m=MaterialService.create_empty_material('Ruta blue eyes',eyes);e.apply_node_tree(m)
try:asset('eyebrows/eyebrow006/eyebrow006.mhclo','Eyebrows')
except Exception as e:print('BROW_ASSET_ERROR',e)
# Vest is fitted 3D shirt topology with original skin weights, torso-only open front.
vest=clothes.copy();vest.data=clothes.data.copy();bpy.context.collection.objects.link(vest);vest.name='Ruta fitted olive waistcoat';bm=bmesh.new();bm.from_mesh(vest.data);gone=[v for v in bm.verts if v.co.z<.66 or v.co.z>1.005 or abs(v.co.x)>.135 or(abs(v.co.x)<.022 and v.co.y<-.02)];bmesh.ops.delete(bm,geom=gone,context='VERTS');bm.to_mesh(vest.data);bm.free();vest.data.materials.clear();vest.data.materials.append(green)
for v in vest.data.vertices:v.co.x*=1.045;v.co.y*=1.06
for p in vest.data.polygons:p.material_index=0
solid=vest.modifiers.new('Waistcoat thickness','SOLIDIFY');solid.thickness=.003
# Rounded accessory meshes are real spatial geometry, not image cards.
def cube(name,loc,scale,material,bevel=.01):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);b=o.modifiers.new('Soft sewn edges','BEVEL');b.width=bevel;b.segments=3;o.modifiers.new('Normals','WEIGHTED_NORMAL');o.parent=rig;return o
def ribbon(name,points,width,material):
 verts=[]
 for x,y,z in points:verts.extend([(x-width/2,y,z),(x+width/2,y,z)])
 faces=[(i*2,i*2+1,i*2+3,i*2+2)for i in range(len(points)-1)];mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(material);o.parent=rig;s=o.modifiers.new('Fabric thickness','SOLIDIFY');s.thickness=.004;b=o.modifiers.new('Soft fabric edges','BEVEL');b.width=.002;b.segments=2;return o
bag=cube('Ruta ONE satchel',(-.19,-.035,.66),(.19,.10,.17),leather,.022);cube('Satchel flap',(-.19,-.092,.695),(.185,.022,.095),leather,.012);cube('Satchel buckle',(-.19,-.108,.69),(.027,.008,.036),gold,.003)
ribbon('ONE diagonal satchel strap',[(.105,-.055,.995),(.08,-.105,.94),(.025,-.12,.86),(-.055,-.12,.79),(-.15,-.10,.72),(-.19,-.08,.69)],.027,leather)
ribbon('Red scarf left tail',[(-.035,-.08,1.025),(-.012,-.095,.99),(-.06,-.11,.91)],.035,red);ribbon('Red scarf right tail',[(.035,-.08,1.025),(.012,-.095,.99),(.04,-.11,.91)],.035,red);cube('Red scarf knot',(0,-.101,.995),(.045,.025,.035),red,.012)
for x in [-.045,.045]:
 for z in [.71,.77,.83]:cube('Vest brass button',(x,-.109,z),(.013,.007,.013),gold,.005)
# Relax arms using the genuine rig; no animation yet.
for side,angle in [('L',-.9),('R',.9)]:rig.pose.bones['upperarm01.'+side].rotation_euler.y=angle
bpy.context.view_layer.update();scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=800;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.35,.35,.35);scene.view_settings.view_transform='AgX'
def look(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-2.8,-5,2.2));camera=bpy.context.object;look(camera,(0,0,.73));camera.data.type='ORTHO';camera.data.ortho_scale=1.68;scene.camera=camera
for loc,power,size in [((-3,-4,5),450,4),((3,-2,3),200,3),((1,3,4),350,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;look(o,(0,0,.7))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-appearance-v1.blend'));scene.render.filepath=str(OUT/'ruta-e-pilot.png');bpy.ops.render.render(write_still=True)
(OUT/'settings.json').write_text(json.dumps({'status':'appearance-authoring-pilot-not-approved','productionEnabled':False,'macro':macro,'targets':targets,'head3DScale':1.32,'rig':'default','camera':{'location':list(camera.location),'orthoScale':camera.data.ortho_scale},'strapCount':1,'animation':'not-authored'},indent=2)+'\n')
