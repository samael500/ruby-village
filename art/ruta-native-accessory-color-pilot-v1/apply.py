from pathlib import Path
import bpy,hashlib,json,math
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';assert sha(S)==expected;bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;changes=[];copies={};images={i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file}
for o in sc.objects:
 if o.type!='MESH'or o.hide_render:continue
 for slot in o.material_slots:
  old=slot.material
  if not old or not old.name.startswith('Ruta v4 padded accessory '):continue
  if old.name not in copies:
   old.use_fake_user=True;m=old.copy();m.name=old.name+' medium brown mix25';tree=m.node_tree;d=next(n for n in tree.nodes if n.type=='BSDF_DIFFUSE');link=d.inputs['Color'].links[0];src=link.from_socket;tree.links.remove(link);mix=tree.nodes.new('ShaderNodeMixRGB');mix.name='ONE global leather brown mix25';mix.blend_type='MIX';mix.inputs[0].default_value=.25;mix.inputs[2].default_value=(.16,.07,.028,1);tree.links.new(src,mix.inputs[1]);tree.links.new(mix.outputs['Color'],d.inputs['Color']);copies[old.name]=m;changes.append({'original':old.name,'copy':m.name})
  slot.material=copies[old.name]
assert copies;out=O/'ruta-accessory-brown25.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);r={'sourceSha256':expected,'outputSha256':sha(out),'changes':changes,'mix':'75% ORIGINAL padded texture +25% medium brown linearRGB(.16,.07,.028)','unchangedPackedImageHashes':images,'geometryUVPaddingGaitHeadHairCameraUnchanged':True};rig=bpy.data.objects['CharacterArmature']
for view,yaw,action in [('e',math.pi/2,'Walk_ProportionProposal'),('front',0,'Idle_Neutral_ProportionProposal')]:
 rig.animation_data.action=bpy.data.actions[action];rig.animation_data.action_slot=rig.animation_data.action.slots[0];rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(Vector((0,.050602056086063385,0)));sc.frame_set(0);bpy.context.view_layer.update();sc.render.filepath=str(O/(view+'.png'));bpy.ops.render.render(write_still=True)
assert sha(S)==expected;assert images=={i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file};(O/'contract.json').write_text(json.dumps(r,indent=2)+'\n')
