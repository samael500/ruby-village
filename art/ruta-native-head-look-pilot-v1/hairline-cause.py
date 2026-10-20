from pathlib import Path
import bpy,json,numpy as np
from collections import Counter
from mathutils import Vector
O=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(O/'pitch-up20/ruta-head-look.blend'));sc=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();cam=sc.camera;head=bpy.data.objects['Ellie ready head'];edges=Counter()
for p in head.data.polygons:
 f=list(p.vertices)
 for a,b in zip(f,f[1:]+f[:1]):edges[tuple(sorted((a,b)))]+=1
boundary=[k for k,v in edges.items()if v==1];top=[]
for a,b in boundary:
 pa=head.data.vertices[a].co;pb=head.data.vertices[b].co
 if pa.z>1.35 and pb.z>1.35:top.append({'indices':[a,b],'a':list(pa),'b':list(pb)})
frame=cam.data.view_frame(scene=sc);xmin,xmax=frame[2].x,frame[1].x;ymin,ymax=frame[1].y,frame[0].y;direction=(cam.matrix_world.to_3x3()@Vector((0,0,-1))).normalized();rays=[]
for px,py in [(250,162),(240,159),(260,165),(250,174),(250,150)]:
 u=(px+.5)/512;v=1-(py+.5)/640;origin=cam.matrix_world@Vector((xmin+u*(xmax-xmin),ymin+v*(ymax-ymin),-cam.data.clip_start));hits=[]
 obj=head; ev=head.evaluated_get(dg); inv=ev.matrix_world.inverted(); localDirection=(inv.to_3x3()@direction).normalized()
 for step in range(8):
  hit,localLoc,localNormal,index=ev.ray_cast(inv@origin,localDirection); loc=ev.matrix_world@localLoc; normal=(ev.matrix_world.to_3x3()@localNormal).normalized()
  if not hit:break
  ev=obj.evaluated_get(dg);me=ev.to_mesh();poly=me.polygons[index]if 0<=index<len(me.polygons)else None;mi=poly.material_index if poly else None;material=obj.material_slots[mi].material.name if mi is not None and mi<len(obj.material_slots)and obj.material_slots[mi].material else None;hits.append({'object':obj.name,'polygon':index,'materialIndex':mi,'material':material,'location':list(loc),'worldNormal':list(normal),'normalDotRay':normal.dot(direction),'polygonVertexCount':len(poly.vertices)if poly else None});ev.to_mesh_clear();origin=loc+direction*.00005
 rays.append({'pixel':[px,py],'hitsGeometryNotAlphaAware':hits})
report={'scope':'head-only evaluated-object rays through saved front diagnostic; hidden old hair excluded; not shader-alpha-aware','headMaterials':[m.material.name if m.material else None for m in head.material_slots],'headVertexCount':len(head.data.vertices),'headFaceCount':len(head.data.polygons),'headBoundaryEdgeCount':len(boundary),'headUpperBoundaryEdgesZAbove1p35':top,'pixels':rays};(O/'hairline-geometry-cause.json').write_text(json.dumps(report,indent=2)+'\n');print('BOUNDARY',len(boundary),'UPPER',len(top));print('HEADMATS',report['headMaterials']);print(json.dumps(rays,indent=2))
