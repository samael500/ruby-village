from pathlib import Path
import bpy,json,numpy as np
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'cache/alpha-volume-baked.blend'));sc=bpy.context.scene;obj=bpy.data.objects['Daisy alpha-aware volume candidate'];adj=[[]for _ in obj.data.vertices]
for e in obj.data.edges:a,b=e.vertices;adj[a].append(b);adj[b].append(a)
seen=set();small=[];large=[]
for i in range(len(adj)):
 if i in seen:continue
 todo=[i];seen.add(i);ids=[]
 while todo:
  j=todo.pop();ids.append(j)
  for k in adj[j]:
   if k not in seen:seen.add(k);todo.append(k)
 (small if len(ids)<100 else large).append(ids)
ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();rows=[]
for ids in small:
 p=[]
 for i in ids:
  q=world_to_camera_view(sc,sc.camera,ev.matrix_world@me.vertices[i].co);p.append([q.x*512,(1-q.y)*640])
 p=np.array(p);rows.append({'vertexCount':len(ids),'projectedEWalk0BoxPx':[p.min(0).tolist(),p.max(0).tolist()],'projectedSizePx':(p.max(0)-p.min(0)).tolist()})
ev.to_mesh_clear();r={'polygonSmoothCount':sum(p.use_smooth for p in obj.data.polygons),'polygonCount':len(obj.data.polygons),'smallComponents':rows,'largestComponentVertexCount':max(map(len,large)),'definition':'actual saved EWalk0 evaluatedvertices, fixedcamera; tinycomponents NOTdeleted'};(O/'fragment-projections.json').write_text(json.dumps(r,indent=2)+'\n')
