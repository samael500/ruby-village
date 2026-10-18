"""Actual render-level left/right boot intersections during compact stepping pivot."""
from pathlib import Path
import os
import bpy,json,hashlib
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('RUBY_MPFB_PIVOT_VARIANT','right60');assert VARIANT in ['right60','left120','right120'];OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-variants'/VARIANT;meta=json.loads((OUT/'manifest.json').read_text());source=OUT/'mpfb-compact-pivot-technical.blend';before=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source));shoe=bpy.data.objects['Ruta.shoes01'];scene=bpy.context.scene
for n,a in meta['turnActions'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels
regions={};records=[]
for i in range(400*meta.get('segments',1)+1):
 p=i/400;f=1+40*p;scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();o=shoe.evaluated_get(deps);vertices=[o.matrix_world@v.co for v in o.data.vertices];trees={}
 for side in ['L','R']:
  if side not in regions:
   groups={g.index for g in shoe.vertex_groups if g.name.endswith('.'+side)};ids={v.index for v in o.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5};faces=[list(face.vertices) for face in o.data.polygons if all(v in ids for v in face.vertices)];regions[side]={'vertices':len(ids),'polygons':faces};assert ids and faces
  trees[side]=BVHTree.FromPolygons(vertices,regions[side]['polygons'])
 pairs=trees['L'].overlap(trees['R']);records.append({'phase':p,'timeMs':p*1200,'renderBootTriangleIntersections':len(pairs)})
result={'status':'ACTUAL RENDER-LEVEL BOOT BVH; NO PATH CLEARANCE CLAIM','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(source.read_bytes()).hexdigest(),'samples':len(records),'maximumBootIntersectionPairs':max(r['renderBootTriangleIntersections'] for r in records),'intersectingSamples':sum(r['renderBootTriangleIntersections']>0 for r in records),'selectedVertices':{s:r['vertices'] for s,r in regions.items()},'records':records};assert result['sourceSha256After']==before;(OUT/'boot-surface-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
