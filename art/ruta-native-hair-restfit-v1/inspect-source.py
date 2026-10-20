from pathlib import Path
import bpy,json
from mathutils import Matrix
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');bpy.ops.wm.open_mainfile(filepath=str(P));rig=next(o for o in bpy.context.scene.objects if o.type=='ARMATURE'and'Root'in o.data.bones);rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();rows=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH'and not o.hide_render and o.name.startswith('Ellie ready '):
  ps=[o.matrix_world@v.co for v in o.data.vertices];rows.append({'object':o.name,'vertices':len(ps),'bounds':[[min(p[k]for p in ps)for k in[0,1,2]],[max(p[k]for p in ps)for k in[0,1,2]]],'materials':[s.material.name if s.material else None for s in o.material_slots]})
(O/'source-inventory.json').write_text(json.dumps({'objects':rows,'HeadRest':[list(rig.data.bones['Head'].head_local),list(rig.data.bones['Head'].tail_local)]},indent=2));print(json.dumps(rows,indent=2))
