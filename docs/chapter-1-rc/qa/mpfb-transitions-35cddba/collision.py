"""Independent actual render-level mesh intersections over217 subframes."""
import bpy,json,sys,math
from pathlib import Path
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend'));scene=bpy.context.scene;body=bpy.data.objects['Ruta.MPFB.Body'];shirt=bpy.data.objects['Ruta.male_casualsuit01']
for m in body.modifiers:
 if m.type=='MASK':m.show_viewport=False
for m in shirt.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels
cache={};records=[]

lead=sys.argv[-1];assert lead in ['L','R'];manifest=json.loads((ROOT/'art/characters-mpfb-v1/motion/transitions/manifest.json').read_text());bundle=manifest['demos'][lead]['actionBundle'];assert len(bundle)==3
for objectName,actionName in bundle.items():bpy.data.objects[objectName].animation_data.action=bpy.data.actions[actionName]
for i in range(217):
 f=1+i/4;scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();bagverts=[];bagpolys=[];parts={}
 for name in ['Ruta ONE satchel','Satchel flap','Satchel buckle']:
  ob=bpy.data.objects[name].evaluated_get(deps);offset=len(bagverts);vs=[ob.matrix_world@v.co for v in ob.data.vertices];ps=[[v+offset for v in p.vertices]for p in ob.data.polygons];assert vs and ps;bagverts.extend(vs);bagpolys.extend(ps);parts[name]={'vertices':len(vs),'polygons':len(ps)}
 bag=BVHTree.FromPolygons(bagverts,bagpolys);r={'frame':f,'intersections':{},'counts':{}}
 for obj,kinds in [(body,['hand','forearmHand']),(shirt,['forearmHand'])]:
  ob=obj.evaluated_get(deps);verts=[ob.matrix_world@v.co for v in ob.data.vertices]
  for side in ['L','R']:
   for kind in kinds:
    name=obj.name+'/'+side+'/'+kind
    if name not in cache:
     words=['wrist','finger','thumb'] if kind=='hand' else ['lowerarm','wrist','finger','thumb'];groups={g.index for g in obj.vertex_groups if g.name.endswith('.'+side)and any(w in g.name for w in words)};selected={v.index for v in ob.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5};polys=[list(p.vertices)for p in ob.data.polygons if all(v in selected for v in p.vertices)];assert groups and selected and polys,(name,len(groups),len(selected),len(polys));cache[name]={'groups':groups,'selected':selected,'polys':polys}
    item=cache[name];assert max(item['selected'])<len(verts);tree=BVHTree.FromPolygons(verts,item['polys']);r['intersections'][name]=len(bag.overlap(tree));r['counts'][name]={'selectedVertices':len(item['selected']),'selectedPolygons':len(item['polys'])}
 records.append(r)
summary={name:{'maxTrianglePairs':max(r['intersections'][name] for r in records),'intersectingSamples':sum(r['intersections'][name]>0 for r in records),'actualVertices':records[0]['counts'][name]['selectedVertices'],'actualPolygons':records[0]['counts'][name]['selectedPolygons']}for name in cache}
(OUT/(f'collision-{lead}.json')).write_text(json.dumps({'method':'Independent fresh Blender reopen; 97 quarter-frame actual evaluated mesh samples; body MASK disabled only for stable limb weights; shirt render-level1; satchel+flap+buckle retained. All six tested limb sets explicitly nonempty with actual faces. No empty shirt-hand test counted as a pass. Source not saved.','bagParts':parts,'summary':summary,'records':records},indent=2)+'\n');print(json.dumps(summary,indent=2))
