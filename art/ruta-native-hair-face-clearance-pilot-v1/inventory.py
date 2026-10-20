from pathlib import Path
import bpy,json,hashlib,numpy as np
from mathutils import Matrix
O=Path(__file__).resolve().parent;S=O.parents[1]/'art/ruta-native-hair-tone-pilot-v1/cache/ruta-hair-tone-trial.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(S)=='159298a6225fa24c174af5562c7a14113e93bbbc5e463ac3e0968b0f15bb81f9';bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);rig=bpy.data.objects['CharacterArmature'];rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();rows=[]
for name in ['Ellie ready head','Ellie ready eye.L','Ellie ready eye.R','Daisy alpha-aware volume candidate']:
 o=bpy.data.objects[name];p=np.array([list(o.matrix_world@v.co)for v in o.data.vertices]);rows.append({'name':name,'bounds':[p.min(0).tolist(),p.max(0).tolist()],'centerMean':p.mean(0).tolist(),'frontMinYPoint':p[p[:,1].argmin()].tolist()})
(O/'inventory.json').write_text(json.dumps({'sourceSha256':sha(S),'restParts':rows,'coordinateDefinition':'nativeZup/front−Y/cameraEunchanged, no physicalirislandmarkclaims'},indent=2)+'\n');print(json.dumps(rows,indent=2))
