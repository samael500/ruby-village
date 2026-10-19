"""Two read-only-pose NPR material studies. No garment, rig or action fitting."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1];O=R/'art/ready-character-npr-v1';O.mkdir(exist_ok=True);S=R/'art/ready-character-adapted-v1/ruta-stock-adapted.blend'
bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature']
def actionhash():return hashlib.sha256(repr([(a.name,[(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])for a in bpy.data.actions]).encode()).hexdigest()
def geometryhash():return hashlib.sha256(repr([(o.name,[(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices])for o in sc.objects if o.type=='MESH']).encode()).hexdigest()
ah=actionhash();gh=geometryhash();changes=[]
for o in sc.objects:
 if o.type=='MESH':
  for p in o.data.polygons:p.use_smooth=True
  # Stock disconnected coincident vertices need shared custom normals, not welding.
  normals={}
  for poly in o.data.polygons:
   for vi in poly.vertices:
    key=tuple(round(c,6)for c in o.data.vertices[vi].co)
    normals[key]=normals.get(key,Vector())+poly.normal*poly.area
  o.data.normals_split_custom_set_from_vertices([normals[tuple(round(c,6)for c in v.co)].normalized()for v in o.data.vertices])
for m in list(bpy.data.materials):
 if not m.use_nodes:continue
 nt=m.node_tree;bs=next((n for n in nt.nodes if n.type=='BSDF_PRINCIPLED'),None)
 if not bs:continue
 base=bs.inputs['Base Color'];color=base.default_value[:];base_link=base.links[0].from_socket if base.is_linked else None
 alpha=bs.inputs['Alpha'];av=alpha.default_value;alink=alpha.links[0].from_socket if alpha.is_linked else None
 diffuse=nt.nodes.new('ShaderNodeBsdfDiffuse');diffuse.inputs['Color'].default_value=(.8,.8,.8,1);diffuse.inputs['Roughness'].default_value=.85
 rgb=nt.nodes.new('ShaderNodeShaderToRGB');nt.links.new(diffuse.outputs[0],rgb.inputs[0]);ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='EASE'
 ramp.color_ramp.elements[0].position=.1;ramp.color_ramp.elements[0].color=(.37,.27,.24,1);ramp.color_ramp.elements[1].position=.75;ramp.color_ramp.elements[1].color=(1,.96,.84,1)
 e=ramp.color_ramp.elements.new(.40);e.color=(.74,.66,.55,1);nt.links.new(rgb.outputs[0],ramp.inputs[0])
 mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[1].default_value=color
 if base_link:nt.links.new(base_link,mul.inputs[1])
 nt.links.new(ramp.outputs[0],mul.inputs[2]);em=nt.nodes.new('ShaderNodeEmission');nt.links.new(mul.outputs[0],em.inputs[0]);em.inputs[1].default_value=1
 trans=nt.nodes.new('ShaderNodeBsdfTransparent');mix=nt.nodes.new('ShaderNodeMixShader');mix.inputs[0].default_value=av
 if alink:nt.links.new(alink,mix.inputs[0])
 nt.links.new(trans.outputs[0],mix.inputs[1]);nt.links.new(em.outputs[0],mix.inputs[2]);out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');nt.links.new(mix.outputs[0],out.inputs['Surface']);changes.append(m.name)
sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=768;sc.render.resolution_y=960;sc.render.resolution_percentage=100;sc.render.film_transparent=True
# Native render compositor: soft image-gradient ink, alpha retained exactly.
sc.use_nodes=True;nt=sc.node_tree;nt.nodes.clear();rl=nt.nodes.new('CompositorNodeRLayers');edge=nt.nodes.new('CompositorNodeFilter');edge.filter_type='SOBEL';nt.links.new(rl.outputs['Image'],edge.inputs['Image']);inv=nt.nodes.new('CompositorNodeInvert');nt.links.new(edge.outputs[0],inv.inputs['Color']);mix=nt.nodes.new('CompositorNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.25;nt.links.new(rl.outputs['Image'],mix.inputs[1]);nt.links.new(inv.outputs[0],mix.inputs[2]);alpha=nt.nodes.new('CompositorNodeSetAlpha');nt.links.new(mix.outputs[0],alpha.inputs['Image']);nt.links.new(rl.outputs['Alpha'],alpha.inputs['Alpha']);out=nt.nodes.new('CompositorNodeComposite');nt.links.new(alpha.outputs[0],out.inputs[0])
sc.view_settings.view_transform='Standard';sc.view_settings.look='Medium High Contrast';sc.view_settings.exposure=0;sc.view_settings.gamma=1
for t in rig.animation_data.nla_tracks:t.mute=True
a=bpy.data.actions['Walk'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0];sc.frame_set(0)
p=rig.data.bones['Root'].head_local.copy();p.z=0;rows=[]
for name,yaw in [('e',math.pi/2),('front',0)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-p);bpy.context.view_layer.update();q=world_to_camera_view(sc,sc.camera,rig.matrix_world@rig.pose.bones['Root'].head)
 rows.append({'view':name,'yaw':yaw,'rootPx':[q.x*768,(1-q.y)*960]});sc.render.filepath=str(O/(name+'-00.png'));bpy.ops.render.render(write_still=True)
assert ah==actionhash();assert gh==geometryhash()
bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-stock-npr.blend'))
(O/'checks.json').write_text(json.dumps({'status':'NPR-source-study-not-approved-Ruta','sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'actionsHash':ah,'geometryAndWeightsHash':gh,'actionsGeometryWeightsUnchanged':True,'changes':['smooth shared-position custom normals only; no vertex welding','native compositor subtle gradient contour, source render alpha retained','warm three-stop Eevee lighting ramp multiplying existing materials, source alpha retained'],'materials':changes,'views':rows,'limitations':['stock head/body/boot geometry and adult proportions unchanged','soft compositor gradient ink, not hand-drawn illustration','no bow/garment fitting or pose changes','not a painted sprite replacement; style and game acceptance pending']},indent=2)+'\n')
