"""One material-only stock study; retains real geometry, weights and source walk."""
from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'art/ready-character-walk-v1/adventurer-walk-pilot.blend';OUT=ROOT/'art/ready-character-colour-v1';OUT.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene
palette={'White':(.84,.77,.63),'Hair_Brown':(.27,.075,.025),'Green':(.105,.135,.052),'LightGreen':(.18,.20,.09),'Brown2':(.21,.095,.040),'Brown_02':(.16,.075,.032),'Brown':(.14,.065,.025)}
changes={}
for name,rgb in palette.items():
 m=bpy.data.materials.get(name)
 if not m:continue
 changes[name]={'oldDiffuse':list(m.diffuse_color),'newLinearRgb':list(rgb)};m.diffuse_color=(*rgb,1)
 if m.use_nodes:
  for n in m.node_tree.nodes:
   if n.type=='BSDF_PRINCIPLED':n.inputs['Base Color'].default_value=(*rgb,1)
scene.frame_set(0);scene.render.filepath=str(OUT/'e-phase00.png');bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'adventurer-colour-study.blend'));bpy.ops.render.render(write_still=True)
(OUT/'study.json').write_text(json.dumps({'status':'material-only-study-not-approved-Ruta','source':str(SOURCE.relative_to(ROOT)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'changes':changes,'geometryWeightsActionsEdited':False,'bag':'stock backpack retained; no single-satchel claim','limitations':['stock short hair, shorts, short sleeves and backpack remain','palette cannot replace approved Ruta likeness/outfit','one E pose only; no new direction batch']},indent=2)+'\n')
