from pathlib import Path
import bpy,json,math
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;V=O/'v2-native-gutter-guard';V.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(O/'ruta-painted-garment-pilot.blend'))
def linear(c):return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4
# Measured raw beige background medians, sRGB bytes; material nodes evaluate linear RGB.
backgrounds={'mixed':[234,227,211],'trousers':[232,225,210]}
records=[]
for mat in bpy.data.materials:
 if not mat.name.startswith('Ruta painted garment '):continue
 original=mat.name[len('Ruta painted garment '):]
 if original in ['Ruta cream shirt','Ruta olive sleeveless vest']:continue
 nt=mat.node_tree;tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE');diff=next(n for n in nt.nodes if n.type=='BSDF_DIFFUSE');key='trousers'if original=='Ruta warm loose cargo cloth'else'mixed'
 bg=[linear(x/255)for x in backgrounds[key]];base=[linear(x/255)for x in ([127,80,46]if key=='trousers'else[141,77,35])]
 distance=nt.nodes.new('ShaderNodeVectorMath');distance.operation='DISTANCE';distance.label='Distance from immutable atlas beige in linear RGB';nt.links.new(tex.outputs['Color'],distance.inputs[0]);distance.inputs[1].default_value=bg
 mask=nt.nodes.new('ShaderNodeMapRange');mask.interpolation_type='SMOOTHERSTEP';mask.clamp=True;mask.inputs['From Min'].default_value=.30;mask.inputs['From Max'].default_value=.60;mask.inputs['To Min'].default_value=1;mask.inputs['To Max'].default_value=0;nt.links.new(distance.outputs['Value'],mask.inputs['Value'])
 mix=nt.nodes.new('ShaderNodeMixRGB');mix.blend_type='MIX';mix.label='Background-only gutter fallback, no bitmap changes';nt.links.new(mask.outputs['Result'],mix.inputs[0]);nt.links.new(tex.outputs['Color'],mix.inputs[1]);mix.inputs[2].default_value=(*base,1);color=mix.outputs[0]
 if key=='trousers':
  contrast=nt.nodes.new('ShaderNodeMixRGB');contrast.blend_type='MIX';contrast.label='Single constant 12% matte brown contrast restraint';contrast.inputs[0].default_value=.12;nt.links.new(color,contrast.inputs[1]);contrast.inputs[2].default_value=(*base,1);color=contrast.outputs[0]
 nt.links.new(color,diff.inputs['Color']);records.append({'material':mat.name,'texture':key,'backgroundSRGBBytes':backgrounds[key],'backgroundLinearRGB':bg,'baseLinearRGB':base,'distanceLinearRGB':{'fullGuardBelow':.30,'zeroGuardAbove':.60,'interpolation':'smootherstep'},'trousersConstantBaseMix':.12 if key=='trousers'else 0})
sc=bpy.context.scene;rig=next(o for o in sc.objects if o.type=='ARMATURE'and'Root'in o.data.bones);rest=Vector((0,-.050602056086063385,0));sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=32
for name,yaw,action in [('e-00',math.pi/2,'Walk_ProportionProposal'),('front-neutral',0,'Idle_Neutral_ProportionProposal')]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-rest);rig.animation_data.action=bpy.data.actions[action];sc.frame_set(0);bpy.context.view_layer.update();sc.render.filepath=str(V/(name+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(V/'ruta-garment-gutter-guard.blend'),compress=True);(V/'shader-contract.json').write_text(json.dumps({'rawImagesUnchanged':True,'UVUnchanged':True,'guardOnlyBrown':True,'records':records},indent=2));print('GUARD_PILOT_DONE',flush=True)
