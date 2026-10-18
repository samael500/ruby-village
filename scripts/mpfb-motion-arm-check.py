"""Fresh saved-file arm/satchel triangle collision and elbow modulation audit."""
from pathlib import Path
import bpy,json,math
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))
body=bpy.data.objects['Ruta.MPFB.Body'];shirt=bpy.data.objects['Ruta.male_casualsuit01'];rig=bpy.data.objects['Ruta.MPFB.StandardRig']
for m in body.modifiers:
 if m.type=='MASK':m.show_viewport=False
for m in shirt.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels
sets={} # Subdivision topology and skin weights are pose-invariant.
records=[]
for frame in range(1,25):
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();verts=[];faces=[]
 for name in ['Ruta ONE satchel','Satchel flap','Satchel buckle']:
  o=bpy.data.objects[name];eo=o.evaluated_get(deps);offset=len(verts);verts.extend(eo.matrix_world@v.co for v in eo.data.vertices);faces.extend([i+offset for i in p.vertices]for p in eo.data.polygons)
 tree=BVHTree.FromPolygons(verts,faces);rec={'frame':frame,'intersections':{},'elbowDegrees':{},'evaluatedSelectedVertices':{}}
 for o in [body,shirt]:
  eo=o.evaluated_get(deps);ov=[eo.matrix_world@v.co for v in eo.data.vertices]
  for side in ['L','R']:
   for kind in ['hand','forearmHand']:
    cache_key=(o.name,side,kind)
    if cache_key not in sets:
     keys=['wrist','finger','thumb'] if kind=='hand' else ['lowerarm','wrist','finger','thumb'];groups={g.index for g in o.vertex_groups if g.name.endswith('.'+side)and any(k in g.name.lower()for k in keys)};selected={v.index for v in eo.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5};polys=[list(p.vertices)for p in eo.data.polygons if all(i in selected for i in p.vertices)];sets[cache_key]=(selected,polys)
    selected,polys=sets[cache_key];rec['evaluatedSelectedVertices'][o.name+'/'+side+'/'+kind]=len(selected);other=BVHTree.FromPolygons(ov,polys);rec['intersections'][o.name+'/'+side+'/'+kind]=len(tree.overlap(other))
 for side in ['L','R']:
  a=rig.pose.bones['upperarm01.'+side].head;b=rig.pose.bones['lowerarm01.'+side].head;c=rig.pose.bones['wrist.'+side].head;rec['elbowDegrees'][side]=180-math.degrees((a-b).angle(c-b))
 records.append(rec)
summary={'maxTrianglePairs':{k:max(r['intersections'][k]for r in records)for k in records[0]['intersections']},'elbowRangeDegrees':{side:[min(r['elbowDegrees'][side]for r in records),max(r['elbowDegrees'][side]for r in records)]for side in ['L','R']}}
(OUT/'arm-satchel-check.json').write_text(json.dumps({'method':'Fresh saved-file actual evaluated BVH triangle intersections against satchel+flap+buckle; native body MASK disabled and shirt actual render-level subdivision retained, membership from evaluated interpolated vertex groups; upper limb groups threshold>.5; source not saved','summary':summary,'records':records},indent=2)+'\n');print(json.dumps(summary,indent=2))
