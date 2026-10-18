"""Native MPFB head sculpt on BAKED macro result, fitted eyes/eyelids, three orthographic views."""
from pathlib import Path
import bpy,json,math,os
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];exec((ROOT/'scripts/mpfb-smoke.py').read_text().split("bpy.ops.object.select_all(action='SELECT')")[0],globals());variant=int(os.environ.get('RUBY_MPFB_HEAD_STUDY','1'));OUT=ROOT/f'art/characters-mpfb-v1/native-target-study-{variant}';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
from mpfb.services import HumanService,TargetService,MaterialService
from mpfb.entities.material.makeskinmaterial import MakeSkinMaterial
macro=TargetService.get_default_macro_info_dict();macro.update(gender=0.,age=.1875,muscle=.25,weight=.5,proportions=.4,height=.5);macro['race']={'asian':.15,'caucasian':.85,'african':0.}
h=HumanService.create_human(scale=.1,macro_detail_dict=macro);h.name='Ruta native MPFB head study body'
targets={'eyes/l-eye-scale-incr':.65,'eyes/r-eye-scale-incr':.65,'eyes/l-eye-height1-incr':.35,'eyes/r-eye-height1-incr':.35,'cheek/l-cheek-volume-incr':.45,'cheek/r-cheek-volume-incr':.45,'chin/chin-width-decr':.2,'nose/nose-scale-vert-decr':.35,'nose/nose-scale-depth-decr':.25,'mouth/mouth-angles-up':.45,'mouth/mouth-scale-horiz-incr':.2}
if variant==2:
 targets.update({'eyes/l-eye-scale-incr':1.15,'eyes/r-eye-scale-incr':1.15,'eyes/l-eye-height1-incr':.65,'eyes/r-eye-height1-incr':.65,'nose/nose-scale-vert-decr':.55,'nose/nose-scale-depth-decr':.60,'nose/nose-scale-horiz-decr':.3,'mouth/mouth-angles-up':.85,'mouth/mouth-upperlip-middle-up':.20,'mouth/mouth-lowerlip-middle-down':.22})
# Coordinator experiment: native topology targets only, no orbital warp.
strength=float(os.environ.get('RUBY_MPFB_NATIVE_EYE','3'))
targets.update({'eyes/l-eye-scale-incr':strength,'eyes/r-eye-scale-incr':strength,'eyes/l-eye-height1-incr':1.2,'eyes/r-eye-height1-incr':1.2,'cheek/l-cheek-volume-incr':.65,'cheek/r-cheek-volume-incr':.65,'nose/nose-scale-vert-decr':.8,'nose/nose-scale-depth-decr':.8,'mouth/mouth-angles-up':float(os.environ.get('RUBY_MPFB_SMILE','1.1')),'mouth/mouth-scale-horiz-incr':.55,'nose/nose-scale-horiz-decr':.6,'mouth/mouth-scale-depth-decr':.45})
for name,value in targets.items():
 f=MPFB_SRC/'mpfb/data/targets'/(name+'.target.gz')
 if f.exists():
  k=TargetService.load_target(h,str(f),weight=value);k.slider_max=6;k.value=value
# Bake actual child macro mix before ANY nonlinear stylization. Separate author key preserves edited native topology.
TargetService.bake_targets(h);h.shape_key_add(name='Basis');key=h.shape_key_add(name='Ruta coherent child head sculpt');key.value=1
for v in key.data:
 x,y,z=v.co;w=min(1,max(0,(z-1.015)/.06));w=w*w*(3-2*w);pivot=Vector((0,-.025,1.045));d=Vector((x,y,z))-pivot
 # Larger whole head, broad soft cheeks; no independent orbital radial warp.
 factors=Vector((1+.65*w,1+.50*w,1+.55*w));v.co=pivot+Vector((d.x*factors.x,d.y*factors.y,d.z*factors.z))
rig=HumanService.add_builtin_rig(h,'default');rig.name='Ruta native head rig'
def mat(name,color):
 m=bpy.data.materials.new(name);m.use_fake_user=True;m.use_nodes=True;m.diffuse_color=(*color,1);n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Roughness'].default_value=.8;return m
skin=mat('Warm peach skin',(.95,.62,.38));h.data.materials.clear();h.data.materials.append(skin)
assets=ROOT/'art/characters-mpfb-v1/source-assets'
def add(path,kind):return HumanService.add_mhclo_asset(str(assets/path),h,asset_type=kind,subdiv_levels=1)
eyes=add('eyes/high-poly/high-poly.mhclo','Eyes');e=MakeSkinMaterial();e.populate_from_mhmat(str(assets/'eyes/materials/blue.mhmat'));eyes.data.materials.clear();em=MaterialService.create_empty_material('Blue native fitted eyes',eyes);e.apply_node_tree(em)
# Study6: native globe topology, procedural UV iris colour (not extra eyes).
if variant>=6:
 em.node_tree.nodes.clear();nodes=em.node_tree.nodes;links=em.node_tree.links;out=nodes.new('ShaderNodeOutputMaterial');bs=nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.20;links.new(bs.outputs['BSDF'],out.inputs['Surface']);uv=nodes.new('ShaderNodeTexCoord');ds=[]
 for center in [(.294,.297,0),(.705,.703,0)]:
  sub=nodes.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=center;links.new(uv.outputs['UV'],sub.inputs[0]);length=nodes.new('ShaderNodeVectorMath');length.operation='LENGTH';links.new(sub.outputs['Vector'],length.inputs[0]);ds.append(length)
 minimum=nodes.new('ShaderNodeMath');minimum.operation='MINIMUM';links.new(ds[0].outputs['Value'],minimum.inputs[0]);links.new(ds[1].outputs['Value'],minimum.inputs[1]);ramp=nodes.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='LINEAR';palette=[(0,(.005,.012,.02,1)),(.048,(.005,.012,.02,1)),(.055,(.02,.30,.62,1)),(.125,(.04,.48,.86,1)),(.145,(.008,.04,.08,1)),(.155,(.008,.04,.08,1)),(.165,(.98,.98,.95,1)),(1,(.98,.98,.95,1))]
 for el in list(ramp.color_ramp.elements)[2:]:ramp.color_ramp.elements.remove(el)
 for index,(pos,color) in enumerate(palette):
  el=ramp.color_ramp.elements[index] if index<2 else ramp.color_ramp.elements.new(pos);el.position=pos;el.color=color
 links.new(minimum.outputs[0],ramp.inputs['Fac']);links.new(ramp.outputs['Color'],bs.inputs['Base Color'])
 alpha=nodes.new('ShaderNodeTexImage');alpha.image=bpy.data.images.load(str(assets/'eyes/materials/blue_eye.png'));links.new(alpha.outputs['Alpha'],bs.inputs['Alpha'])
 lashes=add('eyelashes/eyelashes01/eyelashes01.mhclo','Eyelashes');lm=MakeSkinMaterial();lm.populate_from_mhmat(str(assets/'eyelashes/eyelashes01/eyelashes01.mhmat'));lashes.data.materials.clear();lmat=MaterialService.create_empty_material('Native upper lashes',lashes);lm.apply_node_tree(lmat)

brows=add('eyebrows/eyebrow006/eyebrow006.mhclo','Eyebrows')
if variant==2:
 teeth=add('teeth/teeth_base/teeth_base.mhclo','Teeth')
 teeth.data.materials.clear();teeth.data.materials.append(mat('Warm ivory teeth',(.9,.85,.72)))
 rig.pose.bones['jaw'].rotation_euler.x=.045
 for side,sign in [('L',1),('R',-1)]:
  b=rig.pose.bones['oris03.'+side];b.location=b.bone.matrix_local.to_3x3().inverted()@Vector((sign*.002,0,.004))
# Head-only anatomy frame; original hair source is optional framing reference, not new hair authoring.
hair=add('hair/cortu_strawberry_cloud_hair/cortu_strawberry_cloud_hair.mhclo' if variant>=9 else 'hair/long01/long01.mhclo','Hair');hair.data.materials.clear();hair.data.materials.append(mat('Copper native cap reference only',(.42,.115,.025)))
if variant>=8:
 # Preserve the native alpha-card scalp/strand edges rather than opaque helmet.
 hm=hair.data.materials[0];hn=hm.node_tree.nodes;hl=hm.node_tree.links;tex=hn.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(assets/('hair/cortu_strawberry_cloud_hair/strawberry_cloud_diff.png' if variant>=9 else 'hair/long01/long01_diffuse.png')));ramp=hn.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.10,.018,.004,1);ramp.color_ramp.elements[1].color=(.94,.46,.12,1);ramp.color_ramp.elements[1].position=.36;middle=ramp.color_ramp.elements.new(.12);middle.color=(.48,.115,.022,1);hl.new(tex.outputs['Color'],ramp.inputs['Fac']);hl.new(ramp.outputs['Color'],hn.get('Principled BSDF').inputs['Base Color']);hl.new(tex.outputs['Alpha'],hn.get('Principled BSDF').inputs['Alpha'])
 zmin=min(v.co.z for v in hair.data.vertices);zmax=max(v.co.z for v in hair.data.vertices);span=zmax-zmin
 for v in ([] if variant>=9 else hair.data.vertices):
  x,y,z=v.co;t=max(0,min(1,(zmax-z)/span));weight=max(0,min(1,(t-.22)/.35));weight=weight*weight*(3-2*weight)
  v.co.x+=.020*weight*math.sin((z-zmin)*32+x*7)
  v.co.y+=.009*weight*math.sin((z-zmin)*36+x*10+.7)
 # Native upper lashes only: no doll-like lower false-lash fringe.
 import bmesh
 bm=bmesh.new();bm.from_mesh(lashes.data);cutoff=sum(v.co.z for v in eyes.data.vertices)/len(eyes.data.vertices);lower=[f for f in bm.faces if f.calc_center_median().z<cutoff];bmesh.ops.delete(bm,geom=lower,context='FACES');bm.to_mesh(lashes.data);bm.free()

if variant>=12:
 ramp.color_ramp.elements[0].color=(.08,.010,.002,1)
 middle.color=(.32,.055,.008,1);middle.position=.35
 ramp.color_ramp.elements[-1].color=(.65,.19,.025,1);ramp.color_ramp.elements[-1].position=.95

# Study11: correct the fitted curly scalp clearance on its own native cards.
# Keep low locks untouched; no second hairstyle or opaque shell.
if variant>=11:
 for v in hair.data.vertices:
  w=max(0,min(1,(v.co.z-1.29)/.045));w=w*w*(3-2*w)
  d=v.co-Vector((0,-.025,1.23))
  if d.length:v.co+=d.normalized()*.010*w

# Study10: original fitted native scalp underlay beneath the separate curly cards.
# The CC0 curly asset exposes scalp at exaggerated child-head targets; preserve
# its complete locks and add only the crown of the system native hair mesh.
if variant==10:
 cap=add('hair/long01/long01.mhclo','Hair');cap.name='Ruta native scalp underlay'
 import bmesh
 bm=bmesh.new();bm.from_mesh(cap.data);zmax=max(v.co.z for v in bm.verts)
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_center_median().z<zmax-.10],context='FACES')
 bm.to_mesh(cap.data);bm.free()
 cm=mat('Copper scalp underlay',(.42,.115,.025));cap.data.materials.clear();cap.data.materials.append(cm)
 cn=cm.node_tree.nodes;cl=cm.node_tree.links;t=cn.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(assets/'hair/long01/long01_diffuse.png'));r=cn.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.10,.018,.004,1);r.color_ramp.elements[1].color=(.70,.29,.065,1);r.color_ramp.elements[1].position=.36;cl.new(t.outputs['Color'],r.inputs['Fac']);cl.new(r.outputs['Color'],cn.get('Principled BSDF').inputs['Base Color']);cl.new(t.outputs['Alpha'],cn.get('Principled BSDF').inputs['Alpha'])

scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=12;scene.render.resolution_x=800;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.6,.6,.6);scene.view_settings.view_transform='AgX'
def look(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
# Locate camera from ACTUAL postsculpt native bones, not pre-bake assumed landmarks.
head=rig.data.bones['head'];center=(head.head_local+head.tail_local)/2;center.z+=.015
bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=.56;scene.camera=camera
for loc,power,size in [((-2,-3,4),130,3),((3,-1,2),50,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;look(o,center)
records=[]
for name,angle in [('front',0),('three-quarter',-.52),('profile',-math.pi/2)]:
 camera.location=center+Vector((math.sin(angle)*3,-math.cos(angle)*3,.15));look(camera,center);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True);records.append({'name':name,'camera':list(camera.location),'orthoScale':camera.data.ortho_scale})
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-head.blend'));(OUT/'settings.json').write_text(json.dumps({'status':'native target exaggeration experiment; head-only, not approved likeness','productionEnabled':False,'macro':macro,'targets':targets,'macroBakedBeforeSculpt':True,'nativeVertexCount':len(h.data.vertices),'authorShapeKey':key.name,'rig':'default','nativeEyesFittedAfterSculpt':True,'headBone':[list(head.head_local),list(head.tail_local)],'views':records,'hair':'CC0 cortu strawberry cloud native fitted study' if variant>=9 else 'originalstraightreferenceonly-not-final'},indent=2)+'\n')
