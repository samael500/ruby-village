"""Deterministic native shader/outline study, immutable mesh/rig/actions; three poses only."""
from pathlib import Path
import bpy,json,hashlib,math
import numpy as np
from mathutils import Matrix
R=Path(__file__).resolve().parents[2];O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');expected='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';assert hashlib.sha256(P.read_bytes()).hexdigest()==expected;bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sc=bpy.context.scene

def invariant():
 rows={}
 for o in sc.objects:
  if o.type=='MESH':
   a=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',a);rows[o.name]={'positions':hashlib.sha256(a.tobytes()).hexdigest(),'polygons':hashlib.sha256(repr([list(p.vertices)for p in o.data.polygons]).encode()).hexdigest(),'weights':hashlib.sha256(repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]).encode()).hexdigest()}
 actions={a.name:hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()for a in bpy.data.actions}
 rig=bpy.data.objects['CharacterArmature'];bones=hashlib.sha256(repr([(b.name,list(b.head_local),list(b.tail_local),[list(v)for v in b.matrix_local])for b in rig.data.bones]).encode()).hexdigest();return {'meshes':rows,'actions':actions,'restBones':bones}
before=invariant();visible=[o for o in sc.objects if o.type=='MESH'and not o.hide_render];protected={m for o in visible if o.name.startswith('Ellie ready ')for m in o.data.materials if m};records=[]
# Rest-space coordinates are persistent attributes, never posed/world screen coordinates.
for o in visible:
 attr=o.data.attributes.get('RutaStudyRest')or o.data.attributes.new('RutaStudyRest','FLOAT_VECTOR','POINT');a=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',a);attr.data.foreach_set('vector',a)
for mat in {m for o in visible for m in o.data.materials if m}:
 if mat in protected:records.append({'material':mat.name,'policy':'native Ellie UV/alpha/eye/skin/hair shader preserved'});continue
 if not mat.use_nodes:continue
 nt=mat.node_tree;emissions=[n for n in nt.nodes if n.type=='EMISSION'];done=0
 for em in emissions:
  color=em.inputs['Color'];source=color.links[0].from_socket if color.is_linked else None;base=tuple(color.default_value)
  attr=nt.nodes.new('ShaderNodeAttribute');attr.attribute_name='RutaStudyRest';noise=nt.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=48;noise.inputs['Detail'].default_value=2;noise.inputs['Roughness'].default_value=.65;nt.links.new(attr.outputs['Vector'],noise.inputs['Vector']);grain=nt.nodes.new('ShaderNodeMapRange');grain.inputs['From Min'].default_value=0;grain.inputs['From Max'].default_value=1;grain.inputs['To Min'].default_value=.93;grain.inputs['To Max'].default_value=1.035;nt.links.new(noise.outputs['Fac'],grain.inputs['Value'])
  multiply=nt.nodes.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1;multiply.inputs[1].default_value=base
  if source:nt.links.new(source,multiply.inputs[1])
  nt.links.new(grain.outputs['Result'],multiply.inputs[2]);fres=nt.nodes.new('ShaderNodeFresnel');fres.inputs['IOR'].default_value=1.35;edge=nt.nodes.new('ShaderNodeValToRGB');edge.color_ramp.elements[0].position=.12;edge.color_ramp.elements[0].color=(1,1,1,1);edge.color_ramp.elements[1].position=.78;edge.color_ramp.elements[1].color=(.55,.39,.29,1);edge.color_ramp.interpolation='EASE';nt.links.new(fres.outputs['Fac'],edge.inputs['Fac']);ink=nt.nodes.new('ShaderNodeMixRGB');ink.blend_type='MULTIPLY';ink.inputs[0].default_value=.65;nt.links.new(multiply.outputs[0],ink.inputs[1]);nt.links.new(edge.outputs[0],ink.inputs[2]);nt.links.new(ink.outputs[0],color);done+=1
 records.append({'material':mat.name,'policy':'existing warm toon retained; subtle rest-bound pigment variation and warm facing-edge ink','emissionColorNodesModified':done})
# Deterministic one-native-pixel outside silhouette, Blender compositor only.
sc.use_nodes=True;nt=sc.node_tree;nt.nodes.clear();layers=nt.nodes.new('CompositorNodeRLayers');dilate=nt.nodes.new('CompositorNodeDilateErode');dilate.mode='DISTANCE';dilate.distance=1;nt.links.new(layers.outputs['Alpha'],dilate.inputs[0]);outline=nt.nodes.new('CompositorNodeSetAlpha');outline.inputs['Image'].default_value=(.095,.039,.016,1);nt.links.new(dilate.outputs[0],outline.inputs['Alpha']);over=nt.nodes.new('CompositorNodeAlphaOver');over.inputs[0].default_value=1;nt.links.new(outline.outputs[0],over.inputs[1]);nt.links.new(layers.outputs['Image'],over.inputs[2]);out=nt.nodes.new('CompositorNodeComposite');nt.links.new(over.outputs[0],out.inputs['Image'])
sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.view_settings.view_transform='Standard';sc.view_settings.look='Medium High Contrast';sc.view_settings.exposure=0;sc.view_settings.gamma=1
c=json.loads((R/'art/ruta-native-layered-walk48-v2/source-contract.json').read_text())['cameraVariants']['base']['fixedRenderCamera'];cam=bpy.data.objects.new('Native painted study camera',bpy.data.cameras.new('Native painted study camera'));sc.collection.objects.link(cam);cam.data.type='ORTHO';cam.data.ortho_scale=c['orthoScale'];cam.matrix_world=Matrix(c['matrixWorld']);sc.camera=cam;rig=bpy.data.objects['CharacterArmature'];rig.data.pose_position='POSE';a=bpy.data.actions['Walk_ProportionProposal'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
for t in rig.animation_data.nla_tracks:t.mute=True
root=rig.data.bones['Root'].head_local.copy();root.z=0;rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-root);sc.frame_set(0);after=invariant();assert before==after,'source geometry/action mutation';bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'native-painted-render-study.blend'),compress=True)
report={'status':'DETERMINISTIC-NATIVE-RENDER-FALLBACK-STUDY-NOT-ACCEPTED-STYLE-NOT-RUNTIME','sourceSha256':expected,'invariantsBefore':before,'invariantsAfter':after,'invariantsExactEqual':True,'allowedDataAddition':'POINT vector rest coordinate attribute only; no vertex/topology/weights/restbone/action edits','materials':records,'camera':c,'poses':[0,30,40],'cycleSeconds':40/24,'nativeHeadingYawRadians':math.pi/2,'outline':'Blender compositor1px warm outer silhouette; no PNG redraw/warp/per-frame offsets','limits':['native silhouette/face/view retained, not imagegen-painted redraw','three actual poses only, no whole-cycle approval','protected native face/eye/hair shading retained to avoid breaking UV/alpha; this may limit storybook match']};(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('SOURCE_CHECKPOINT_SAVED',flush=True)
for i in [0,30,40]:
 f=40*i/48;sc.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();sc.render.filepath=str(O/f'e-{i:02d}.png');print('RENDER_NATIVE_STUDY',i,flush=True);bpy.ops.render.render(write_still=True)
assert invariant()==before;assert hashlib.sha256(P.read_bytes()).hexdigest()==expected;print('THREE_POSES_DONE_SOURCE_UNCHANGED',flush=True)
