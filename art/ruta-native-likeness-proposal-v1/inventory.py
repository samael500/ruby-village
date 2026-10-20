from pathlib import Path
import bpy,json,numpy as np
from mathutils import Matrix
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath='/home/mskorokhod/life/ruby-village-36-uv-paint/art/ruta-native-uv-paint-pilot-v1/ruta-native-painted-hair-pilot.blend');rig=bpy.data.objects['CharacterArmature'];rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();rows=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH'and o.name.startswith('Ellie ready ')and not o.hide_render:
  p=np.array([list(o.matrix_world@v.co)for v in o.data.vertices]);rows.append({'name':o.name,'n':len(p),'bbox':[p.min(axis=0).tolist(),p.max(axis=0).tolist()],'basis':[list(x)for x in o.matrix_basis],'shapeKeys':list(o.data.shape_keys.key_blocks.keys())if o.data.shape_keys else[],'frontLowHairVertices':p[(p[:,1]<-.08)&(p[:,2]<1.56)].tolist()if o.name=='Ellie ready Loose cap'else None})
(O/'inventory.json').write_text(json.dumps({'headBone':[list(rig.data.bones['Head'].head_local),list(rig.data.bones['Head'].tail_local)],'rows':rows},indent=2)+'\n')
