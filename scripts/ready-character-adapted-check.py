from pathlib import Path
import bpy,json,hashlib
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-adapted-v1'
def sha(x):return hashlib.sha256(repr(x).encode()).hexdigest()
def source_invariants():
 r=bpy.data.objects['CharacterArmature'];actions={}
 for a in bpy.data.actions:
  if a.name not in ['Death','Gun_Shoot','HitRecieve','HitRecieve_2','Idle','Idle_Gun','Idle_Gun_Pointing','Idle_Gun_Shoot','Idle_Neutral','Idle_Sword','Interact','Kick_Left','Kick_Right','Punch_Left','Punch_Right','Roll','Run','Run_Back','Run_Left','Run_Right','Run_Shoot','Sword_Slash','Walk','Wave']:continue
  actions[a.name]=sha([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])
 return {'rest':sha([(b.name,tuple(b.head_local),tuple(b.tail_local))for b in r.data.bones]),'actions':actions}
def geometry(o):return sha([(tuple(v.co),sorted((o.vertex_groups[g.group].name,g.weight)for g in v.groups))for v in o.data.vertices])
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/ready-character-walk-v1/adventurer-walk-pilot.blend'));baseline=source_invariants()
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/ready-character-walk-v1/source/casual-imported.blend'));pants=geometry(bpy.data.objects['Casual_Legs'])
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ruta-stock-adapted.blend'));current=source_invariants();assert baseline==current;assert pants==geometry(bpy.data.objects['Ruta stock long trousers'])
rig=bpy.data.objects['CharacterArmature'];names=['ONE hip satchel','Adventurer_Body','Ruta stock long trousers','Adventurer_Feet','Ruta CC0 ginger waves','Adventurer_Head'];pairs=[(0,1),(0,2),(2,3),(4,1),(4,5)];rows=[]
def tree(o):
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();m.calc_loop_triangles();t=BVHTree.FromPolygons([e.matrix_world@v.co for v in m.vertices],[tuple(t.vertices)for t in m.loop_triangles],all_triangles=True);e.to_mesh_clear();return t
for frame in [0,5,10,15,20,25,30,35,40]:
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();trees=[tree(bpy.data.objects[n])for n in names];rows.append({'frame':frame,'triangleIntersections':{names[a]+' / '+names[b]:len(trees[a].overlap(trees[b]))for a,b in pairs}})
(OUT/'assembly-checks.json').write_text(json.dumps({'status':'native-part-check-evidence-not-automatic-visual-approval','stockRestAndAll24OriginalActionsUnchanged':True,'nativeCasualTrousersGeometryWeightsUnchanged':True,'nativeInvariants':current,'trousersGeometryWeightsSha256':pants,'sourceRigCount':len(rig.data.bones),'oneSatchelBody':len([o for o in bpy.context.scene.objects if o.name=='ONE hip satchel']),'oneDiagonalStrap':len([o for o in bpy.context.scene.objects if o.name=='ONE diagonal satchel strap']),'samples':rows,'interpretation':'Counts distinguish garment-under-boot and hair-on-head contacts from bag/arm fit. Nonzero counts are disclosed, not converted into no-clipping claim. No motion action edits.'},indent=2)+'\n');print(rows)
