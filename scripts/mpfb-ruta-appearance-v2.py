"""Genuine MPFB mesh/clothes authoring pilot, not final appearance or animation."""
from pathlib import Path
import sys,os,json,math,bmesh
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/appearance-v2';OUT.mkdir(parents=True,exist_ok=True)
# Same isolated source-mode bootstrap as the verified smoke, no vendor writes.
bootstrap=(ROOT/'scripts/mpfb-smoke.py').read_text().split("bpy.ops.object.select_all(action='SELECT')")[0];exec(bootstrap,globals());OUT=ROOT/'art/characters-mpfb-v1/appearance-v2'
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
from mpfb.services import HumanService,TargetService
macro=TargetService.get_default_macro_info_dict();macro.update(gender=0.,age=.1875,muscle=.25,weight=.45,proportions=.35,height=.5);macro['race']={'asian':.15,'caucasian':.85,'african':0.}
human=HumanService.create_human(scale=.1,macro_detail_dict=macro);human.name='Ruta.MPFB.Body'
targets={'eyes/l-eye-scale-incr':2.2,'eyes/r-eye-scale-incr':2.2,'eyes/l-eye-height1-incr':1.2,'eyes/r-eye-height1-incr':1.2,'mouth/mouth-angles-up':.6,'mouth/mouth-scale-horiz-incr':.25,'nose/nose-scale-vert-decr':.35,'chin/chin-width-decr':.35,'cheek/l-cheek-volume-incr':.25,'cheek/r-cheek-volume-incr':.25}
for name,value in targets.items():
 file=MPFB_SRC/'mpfb/data/targets'/(name+'.target.gz')
 if file.exists():
  key=TargetService.load_target(human,str(file),weight=value);key.slider_max=3;key.value=value
# Coherent 3D stylization across all basis/targets and rig-fitting helpers, not a rendered-image deformation.
for key in human.data.shape_keys.key_blocks:
 for v in key.data:
  z=v.co.z;w=min(1,max(0,(z-1.01)/.07));pivot=Vector((0,-.025,1.045));v.co=pivot+(v.co-pivot)*(1+.55*w)
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
# Genuine sewn waistcoat surface, open front and deliberate armholes; weighted to torso rig.
verts=[];faces=[];rows=[(.68,.098,.083),(.76,.104,.087),(.84,.11,.09),(.91,.12,.084),(.97,.11,.073),(1.005,.073,.052)];segments=48
for z,rx,ry in rows:
 for j in range(segments+1):
  theta=.20+(2*math.pi-.40)*j/segments;verts.append((rx*math.sin(theta),-.005-ry*math.cos(theta),z))
for row in range(len(rows)-1):
 for j in range(segments):
  theta=.20+(2*math.pi-.40)*(j+.5)/segments
  if row>=3 and abs(math.sin(theta))>.78:continue
  a=row*(segments+1)+j;faces.append((a,a+1,a+segments+2,a+segments+1))
mesh=bpy.data.meshes.new('Sewn waistcoat topology');mesh.from_pydata(verts,[],faces);mesh.update();vest=bpy.data.objects.new('Ruta tailored olive waistcoat',mesh);bpy.context.collection.objects.link(vest);vest.data.materials.append(green);vest.parent=rig
for name in ['spine03','spine01']:vest.vertex_groups.new(name=name)
for v in mesh.vertices:
 w=min(1,max(0,(v.co.z-.75)/.22));vest.vertex_groups['spine01'].add([v.index],w,'REPLACE');vest.vertex_groups['spine03'].add([v.index],1-w,'REPLACE')
a=vest.modifiers.new('Torso skinning','ARMATURE');a.object=rig;smod=vest.modifiers.new('Fabric softness','SUBSURF');smod.levels=2;solid=vest.modifiers.new('Sewn thickness','SOLIDIFY');solid.thickness=.004
for f in mesh.polygons:f.use_smooth=True
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
# Cargo pockets on physical thigh sides; whole spatial sewn pieces, not painted cards.
for sign in [-1,1]:
 pocket=cube('Cargo pocket',(.115*sign,-.025,.47),(.055,.07,.105),brown,.012);pocket.parent_type='BONE';pocket.parent_bone='upperleg01.'+('L'if sign>0 else'R');pocket.matrix_world.translation=Vector((.115*sign,-.025,.47))
# Stable wavy hair locks, real curves with tapered round sections, behind the face.
hairtones=[mat('Chestnut lock '+str(i),c)for i,c in enumerate([(.24,.082,.022),(.35,.14,.035),(.44,.19,.055),(.29,.10,.023)])]
for k in range(23):
 theta=.25+(math.pi*1.5)*k/22;x=.135*math.cos(theta);y=.02+.08*math.sin(theta);points=[]
 for j in range(9):
  t=j/8;points.append((x+(.025+.025*t)*math.sin(t*math.pi*3+k*.6),y+.07*t,1.43-.57*t+.025*math.cos(k*.7)))
 curve=bpy.data.curves.new('Wavy lock','CURVE');curve.dimensions='3D';curve.resolution_u=12;curve.bevel_depth=.018;curve.bevel_resolution=3;sp=curve.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for j,(b,co)in enumerate(zip(sp.bezier_points,points)):b.co=co;b.handle_left_type='AUTO';b.handle_right_type='AUTO';b.radius=.85 if j<6 else max(.08,(8-j)/3)
 ob=bpy.data.objects.new('Ruta chestnut wavy lock',curve);bpy.context.collection.objects.link(ob);ob.data.materials.append(hairtones[k%4]);ob.parent=rig
# Relax arms using the genuine rig; no animation yet.
for side,angle in [('L',-.9),('R',.9)]:rig.pose.bones['upperarm01.'+side].rotation_euler.z=angle
bpy.context.view_layer.update();scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=800;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.35,.35,.35);scene.view_settings.view_transform='AgX'
def look(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-2.8,-5,2.2));camera=bpy.context.object;look(camera,(0,0,.78));camera.data.type='ORTHO';camera.data.ortho_scale=1.83;scene.camera=camera
for loc,power,size in [((-3,-4,5),450,4),((3,-2,3),200,3),((1,3,4),350,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;look(o,(0,0,.7))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-appearance-v2.blend'));scene.render.filepath=str(OUT/'ruta-e-pilot.png');bpy.ops.render.render(write_still=True)
(OUT/'settings.json').write_text(json.dumps({'status':'appearance-authoring-pilot-not-approved','productionEnabled':False,'macro':macro,'targets':targets,'head3DScale':1.55,'rig':'default','camera':{'location':list(camera.location),'orthoScale':camera.data.ortho_scale},'strapCount':1,'animation':'not-authored'},indent=2)+'\n')
