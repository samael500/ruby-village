"""Native MPFB head sculpt on BAKED macro result, fitted eyes/eyelids, three orthographic views."""
from pathlib import Path
import bpy,json,math,os
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];exec((ROOT/'scripts/mpfb-smoke.py').read_text().split("bpy.ops.object.select_all(action='SELECT')")[0],globals());variant=int(os.environ.get('RUBY_MPFB_HEAD_STUDY','1'));OUT=ROOT/f'art/characters-mpfb-v1/head-study-{variant}';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
from mpfb.services import HumanService,TargetService,MaterialService
from mpfb.entities.material.makeskinmaterial import MakeSkinMaterial
macro=TargetService.get_default_macro_info_dict();macro.update(gender=0.,age=.1875,muscle=.25,weight=.5,proportions=.4,height=.5);macro['race']={'asian':.15,'caucasian':.85,'african':0.}
h=HumanService.create_human(scale=.1,macro_detail_dict=macro);h.name='Ruta native MPFB head study body'
targets={'eyes/l-eye-scale-incr':.65,'eyes/r-eye-scale-incr':.65,'eyes/l-eye-height1-incr':.35,'eyes/r-eye-height1-incr':.35,'cheek/l-cheek-volume-incr':.45,'cheek/r-cheek-volume-incr':.45,'chin/chin-width-decr':.2,'nose/nose-scale-vert-decr':.35,'nose/nose-scale-depth-decr':.25,'mouth/mouth-angles-up':.45,'mouth/mouth-scale-horiz-incr':.2}
if variant==2:
 targets.update({'eyes/l-eye-scale-incr':1.15,'eyes/r-eye-scale-incr':1.15,'eyes/l-eye-height1-incr':.65,'eyes/r-eye-height1-incr':.65,'nose/nose-scale-vert-decr':.55,'nose/nose-scale-depth-decr':.60,'nose/nose-scale-horiz-decr':.3,'mouth/mouth-angles-up':.85,'mouth/mouth-upperlip-middle-up':.20,'mouth/mouth-lowerlip-middle-down':.22})
for name,value in targets.items():
 f=MPFB_SRC/'mpfb/data/targets'/(name+'.target.gz')
 if f.exists():
  k=TargetService.load_target(h,str(f),weight=value);k.slider_max=2;k.value=value
# Bake actual child macro mix before ANY nonlinear stylization. Separate author key preserves edited native topology.
TargetService.bake_targets(h);h.shape_key_add(name='Basis');key=h.shape_key_add(name='Ruta coherent child head sculpt');key.value=1
for v in key.data:
 x,y,z=v.co;w=min(1,max(0,(z-1.015)/.06));w=w*w*(3-2*w);pivot=Vector((0,-.025,1.045));d=Vector((x,y,z))-pivot
 # Larger whole head, broad soft cheeks; no independent orbital radial warp.
 factors=Vector((1+.65*w,1+.50*w,1+.55*w));v.co=pivot+Vector((d.x*factors.x,d.y*factors.y,d.z*factors.z))
rig=HumanService.add_builtin_rig(h,'default');rig.name='Ruta native head rig'
def mat(name,color):
 m=bpy.data.materials.new(name);m.use_fake_user=True;m.use_nodes=True;m.diffuse_color=(*color,1);n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Roughness'].default_value=.8;return m
skin=mat('Warm peach skin',(.72,.34,.18));h.data.materials.clear();h.data.materials.append(skin)
assets=ROOT/'art/characters-mpfb-v1/source-assets'
def add(path,kind):return HumanService.add_mhclo_asset(str(assets/path),h,asset_type=kind,subdiv_levels=1)
eyes=add('eyes/high-poly/high-poly.mhclo','Eyes');e=MakeSkinMaterial();e.populate_from_mhmat(str(assets/'eyes/materials/blue.mhmat'));eyes.data.materials.clear();em=MaterialService.create_empty_material('Blue native fitted eyes',eyes);e.apply_node_tree(em)
brows=add('eyebrows/eyebrow006/eyebrow006.mhclo','Eyebrows')
if variant==2:
 teeth=add('teeth/teeth_base/teeth_base.mhclo','Teeth')
 teeth.data.materials.clear();teeth.data.materials.append(mat('Warm ivory teeth',(.9,.85,.72)))
 rig.pose.bones['jaw'].rotation_euler.x=.045
 for side,sign in [('L',1),('R',-1)]:
  b=rig.pose.bones['oris03.'+side];b.location=b.bone.matrix_local.to_3x3().inverted()@Vector((sign*.002,0,.004))
# Head-only anatomy frame; original hair source is optional framing reference, not new hair authoring.
hair=add('hair/long01/long01.mhclo','Hair')
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=800;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.25,.25,.25);scene.view_settings.view_transform='AgX'
def look(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
# Locate camera from ACTUAL postsculpt native bones, not pre-bake assumed landmarks.
head=rig.data.bones['head'];center=(head.head_local+head.tail_local)/2;center.z+=.015
bpy.ops.object.camera_add();camera=bpy.context.object;camera.data.type='ORTHO';camera.data.ortho_scale=.56;scene.camera=camera
for loc,power,size in [((-2,-3,4),130,3),((3,-1,2),50,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=size;look(o,center)
records=[]
for name,angle in [('front',0),('three-quarter',-.52),('profile',-math.pi/2)]:
 camera.location=center+Vector((math.sin(angle)*3,-math.cos(angle)*3,.15));look(camera,center);scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True);records.append({'name':name,'camera':list(camera.location),'orthoScale':camera.data.ortho_scale})
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-head.blend'));(OUT/'settings.json').write_text(json.dumps({'status':'head-only anatomy study not approved likeness','productionEnabled':False,'macro':macro,'targets':targets,'macroBakedBeforeSculpt':True,'nativeVertexCount':len(h.data.vertices),'authorShapeKey':key.name,'rig':'default','nativeEyesFittedAfterSculpt':True,'headBone':[list(head.head_local),list(head.tail_local)],'views':records,'hair':'originalstraightreferenceonly-not-final'},indent=2)+'\n')
