import bpy,json
from pathlib import Path
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/characters-mpfb-v1/motion/pilot/mpfb-walk-technical.blend'));body=bpy.data.objects['Ruta.MPFB.Body'];bag=bpy.data.objects['Ruta ONE satchel'];scene=bpy.context.scene
# Temporarily retain source indices; no save, no author asset modification.
for m in body.modifiers:
 if m.type=='MASK':m.show_viewport=False
selected={}
for side in ['L','R']:
 groups={g.index for g in body.vertex_groups if g.name.endswith('.'+side) and any(k in g.name.lower() for k in ['lowerarm','wrist','finger','thumb'])};selected[side]={v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5}
records=[]
for f in range(1,25):
 scene.frame_set(f);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();eb=body.evaluated_get(deps);ea=bag.evaluated_get(deps);av=[ea.matrix_world@v.co for v in ea.data.vertices];ap=[list(p.vertices)for p in ea.data.polygons];tree=BVHTree.FromPolygons(av,ap);item={'frame':f,'bagForearmSurfaceIntersections':{}}
 for side in ['L','R']:
  polys=[list(p.vertices) for p in eb.data.polygons if all(i in selected[side]for i in p.vertices)];verts=[eb.matrix_world@v.co for v in eb.data.vertices];other=BVHTree.FromPolygons(verts,polys);item['bagForearmSurfaceIntersections'][side]=len(tree.overlap(other))
 records.append(item)
(OUT/'accessory-check.json').write_text(json.dumps({'method':'actual evaluated meshes; body MASK disabled in measurement process for source vertex groups; no source saved. BVH surface intersection of satchel and vertices >.5 weighted to lowerarm/wrist/finger/thumb. Does not cover all garment/body collisions.','selectedBodyVertexCount':{s:len(v)for s,v in selected.items()},'records':records},indent=2)+'\n');print(records)
