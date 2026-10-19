from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-six-v1'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/ready-character-adapted-v1/ruta-stock-adapted.blend'));rig=bpy.data.objects['CharacterArmature'];p=rig.data.bones['Root'].head_local.copy();p.z=0;rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-p);meshes=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.parent==rig]
def snap(frame):
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();result={}
 for o in meshes:
  e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();result[o.name]=[e.matrix_world@v.co for v in m.vertices];e.to_mesh_clear()
 return result
rows={}
for name,end in [('Walk',40),('Idle_Neutral',50)]:
 action=bpy.data.actions[name];rig.animation_data.action=action;rig.animation_data.action_slot=action.slots[0];a=snap(0);b=snap(end);dist=[(v-w).length for n in a for v,w in zip(a[n],b[n])];maximum=max(dist);assert maximum<1e-4,(name,maximum)
 rows[name]={'sourceRange':[0,end],'evaluatedVertexCount':len(dist),'maximumEndpointVertexDistanceMeters':maximum,'rmsEndpointVertexDistanceMeters':math.sqrt(sum(d*d for d in dist)/len(dist)),'sourceActionUnchanged':True}
(OUT/'loop-seam-checks.json').write_text(json.dumps({'status':'whole-native-mesh-loop-endpoints-measured','actions':rows,'interpretation':'Endpoint closure is separate from stance no-slide; measured source gait residual remains disclosed. Last repeated endpoint is excluded from24 exported phases.'},indent=2)+'\n');print(rows)
