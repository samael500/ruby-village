from pathlib import Path
import bpy,json,math,hashlib,numpy as np
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;B=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1');sources={'original':B/'ruta-painted-garment-pilot.blend','guard':B/'v2-native-gutter-guard/ruta-garment-gutter-guard.blend'};records={}
def setup(src):
 bpy.ops.wm.open_mainfile(filepath=str(src));sc=bpy.context.scene;rig=next(o for o in sc.objects if o.type=='ARMATURE' and 'Root'in o.data.bones);rig.matrix_world=Matrix.Translation(Vector((0,.050602056086063385,0)));rig.animation_data.action=bpy.data.actions['Idle_Neutral_ProportionProposal'];sc.frame_set(0);bpy.context.view_layer.update();sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=16;sc.render.resolution_percentage=100;return sc
for mode in ['original-albedo','guard-albedo','uv-id','no-underbody']:
 sc=setup(sources['guard'if mode=='guard-albedo'else'original']);mats=sorted([m for m in bpy.data.materials if m.name.startswith('Ruta painted garment ')and'shirt'not in m.name and'vest'not in m.name],key=lambda m:m.name)
 if mode=='no-underbody':bpy.data.objects['Adventurer_Body'].hide_render=True
 else:
  for idx,m in enumerate(mats):
   nt=m.node_tree;diff=next(n for n in nt.nodes if n.type=='BSDF_DIFFUSE');out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');em=nt.nodes.new('ShaderNodeEmission')
   if mode=='uv-id':
    uv=next(n for n in nt.nodes if n.type=='UVMAP');sep=nt.nodes.new('ShaderNodeSeparateXYZ');comb=nt.nodes.new('ShaderNodeCombineXYZ');nt.links.new(uv.outputs[0],sep.inputs[0]);nt.links.new(sep.outputs['X'],comb.inputs['X']);nt.links.new(sep.outputs['Y'],comb.inputs['Y']);comb.inputs['Z'].default_value=(idx+1)/100;nt.links.new(comb.outputs[0],em.inputs['Color'])
   else:
    inp=diff.inputs['Color'];nt.links.new(inp.links[0].from_socket,em.inputs['Color']) if inp.is_linked else None
   nt.links.new(em.outputs[0],out.inputs['Surface'])
 sc.render.image_settings.file_format='OPEN_EXR';sc.render.image_settings.color_mode='RGBA';sc.render.image_settings.color_depth='32';sc.render.filepath=str(O/(mode+'.exr'));bpy.ops.render.render(write_still=True);im=bpy.data.images.load(sc.render.filepath,check_existing=False);pix=np.empty(len(im.pixels),dtype=np.float32);im.pixels.foreach_get(pix);np.save(O/(mode+'.npy'),pix.reshape((640,512,4)));records[mode]={'materials':[m.name for m in mats],'sourceSha256':hashlib.sha256(sources['guard'if mode=='guard-albedo'else'original'].read_bytes()).hexdigest()};sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_depth='8';sc.render.filepath=str(O/(mode+'.png'));bpy.data.images['Render Result'].save_render(sc.render.filepath,scene=sc)
(O/'albedo-contract.json').write_text(json.dumps(records,indent=2))
