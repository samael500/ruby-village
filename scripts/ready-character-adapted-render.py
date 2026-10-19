from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-adapted-v1';FRAMES=OUT/'e';FRAMES.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ruta-stock-adapted.blend'));scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.rotation_euler.z=math.pi/2
meshes=[o for o in scene.objects if o.type=='MESH' and o.parent==rig];rows=[]
for i in range(24):
 f=40*i/24;scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();points=[]
 for o in meshes:
  ev=o.evaluated_get(dg);m=ev.to_mesh();points.extend(ev.matrix_world@v.co for v in m.vertices);ev.to_mesh_clear()
 rows.append({'index':i,'sourceFrame':f,'bounds':[[min(v[k]for v in points),max(v[k]for v in points)]for k in range(3)]})
 scene.render.filepath=str(FRAMES/f'{i:02}.png');bpy.ops.render.render(write_still=True)
contract=json.loads((ROOT/'art/ready-character-walk-v1/contract.json').read_text());contract.update(status='adapted-ready-parts-walk-pilot-not-approved-Ruta',frames=rows,source='../ready-character-walk-v1/source/adventurer-original.gltf',sourceAction='Walk',meshes=[o.name for o in meshes],limitations=['stock adult proportions, green shirt rather than approved vest','head-bound CC0 hair; no hair physics','single new satchel, native pants swap','actual game review and intersection checks remain separate'])
(OUT/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
