from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent
S=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1/ruta-painted-garment-pilot.blend')
bpy.ops.wm.open_mainfile(filepath=str(S))
sc=bpy.context.scene;rig=next(o for o in sc.objects if o.type=='ARMATURE' and 'Root'in o.data.bones);rig.matrix_world=Matrix.Translation(Vector((0,.050602056086063385,0)));rig.animation_data.action=bpy.data.actions['Idle_Neutral_ProportionProposal'];sc.frame_set(0);bpy.context.view_layer.update();sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=16;sc.render.resolution_percentage=100;sc.render.threads_mode='FIXED';sc.render.threads=2
rows=[]
for ob in sc.objects:
 if ob.type!='MESH':continue
 slots=[]
 for slot in ob.material_slots:
  m=slot.material
  if m:slots.append({'name':m.name,'polygons':sum(p.material_index==slot.slot_index for p in ob.data.polygons),'nodes':[{'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None,'uv':n.uv_map if n.type=='UVMAP' else None}for n in m.node_tree.nodes]if m.use_nodes else []})
 rows.append({'name':ob.name,'hideRender':ob.hide_render,'materials':slots,'uvLayers':[u.name for u in ob.data.uv_layers],'modifiers':[m.type for m in ob.modifiers]})
images=[{'name':im.name,'size':list(im.size),'colorspace':im.colorspace_settings.name,'alphaMode':im.alpha_mode,'packed':bool(im.packed_file),'filepath':im.filepath}for im in bpy.data.images]
(O/'inventory.json').write_text(json.dumps({'source':str(S),'sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'objects':rows,'images':images},indent=2))
for mode in ['baseline','constant-painted']:
 if mode=='constant-painted':
  for m in bpy.data.materials:
   if not m.name.startswith('Ruta painted garment '):continue
   if 'shirt'in m.name or 'vest'in m.name:continue
   diff=next(n for n in m.node_tree.nodes if n.type=='BSDF_DIFFUSE');inp=diff.inputs['Color']
   for l in list(inp.links):m.node_tree.links.remove(l)
   inp.default_value=(.23,.09,.035,1)
 sc.render.filepath=str(O/(mode+'-front.png'));bpy.ops.render.render(write_still=True)
print('DONE',flush=True)
