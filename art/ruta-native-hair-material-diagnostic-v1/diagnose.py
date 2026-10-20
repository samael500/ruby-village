from pathlib import Path
import bpy,hashlib,json,math
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';assert sha(S)==expected;report={'sourceSha256':expected,'variants':[]}
for variant in ['normal-zero','uniform-copper-normal-zero']:
 bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];hair=bpy.data.objects['Ellie ready Daisy CC-BY hair'];mat=hair.material_slots[0].material.copy();hair.material_slots[0].material=mat;changes=[]
 for n in mat.node_tree.nodes:
  if n.type=='NORMAL_MAP':
   changes.append({'node':n.name,'parameter':'Strength','before':n.inputs['Strength'].default_value,'after':0});n.inputs['Strength'].default_value=0
 if variant.startswith('uniform'):
  diffuse=next(n for n in mat.node_tree.nodes if n.type=='BSDF_DIFFUSE');links=list(diffuse.inputs['Color'].links);linknames=[(l.from_node.name,l.from_socket.name)for l in links]
  for l in links:mat.node_tree.links.remove(l)
  diffuse.inputs['Color'].default_value=(.32,.095,.035,1);changes.append({'node':diffuse.name,'parameter':'Color','afterLinearRGBA':[.32,.095,.035,1],'removedColorLinks':linknames})
 for view,yaw,action in [('e',math.pi/2,'Walk_ProportionProposal'),('front',0,'Idle_Neutral_ProportionProposal')]:
  rig.animation_data.action=bpy.data.actions[action];rig.animation_data.action_slot=rig.animation_data.action.slots[0];rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(Vector((0,.050602056086063385,0)));sc.frame_set(0);bpy.context.view_layer.update();sc.render.filepath=str(O/(variant+'-'+view+'.png'));
  if not Path(sc.render.filepath).exists():bpy.ops.render.render(write_still=True)
 report['variants'].append({'name':variant,'changes':changes,'originalAlphaLinksUnchanged':True,'geometryUVActionCameraUnchanged':True})
assert sha(S)==expected;report['sourceHashAfter']=sha(S);(O/'diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print('DONE')
