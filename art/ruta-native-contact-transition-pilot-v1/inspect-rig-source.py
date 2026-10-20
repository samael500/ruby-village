from pathlib import Path
import bpy,json
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath='/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');r=bpy.data.objects['CharacterArmature'];a=bpy.data.actions['Walk_ProportionProposal'];r.animation_data.action=a;bpy.context.scene.frame_set(5);bpy.context.view_layer.update();print([(n,r.pose.bones[n].rotation_mode,list(r.pose.bones[n].location),r.pose.bones[n].length,r.pose.bones[n].parent.name if r.pose.bones[n].parent else None)for n in ['Root','Hips','UpperLeg.L','LowerLeg.L','Foot.L','UpperLeg.R','LowerLeg.R','Foot.R']])
for n in ['UpperLeg.L','LowerLeg.L','Foot.L','UpperLeg.R','LowerLeg.R','Foot.R']:
 p=r.pose.bones[n];print(n,'head',list(p.head),'tail',list(p.tail),'constraints',[(c.name,c.type,c.influence,c.target.name if hasattr(c,'target')and c.target else None,getattr(c,'subtarget',None),getattr(c,'chain_count',None))for c in p.constraints])
