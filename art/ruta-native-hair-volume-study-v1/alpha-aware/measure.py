from pathlib import Path
import bpy,numpy as np,json,hashlib
from mathutils import Vector
from mathutils.bvhtree import BVHTree
O=Path(__file__).resolve().parent;C=O/'cache';bpy.ops.wm.open_mainfile(filepath=str(C/'alpha-volume-geometry.blend'));obj=bpy.data.objects['Daisy alpha-aware volume candidate'];data=np.load(C/'clipped-surface.npz');bvh=BVHTree.FromPolygons([Vector(p)for p in data['vertices']],data['faces'].tolist(),all_triangles=True);ids=np.unique(np.linspace(0,len(obj.data.vertices)-1,min(20000,len(obj.data.vertices)),dtype=int));dist=[bvh.find_nearest(obj.data.vertices[int(i)].co)[3]for i in ids];adj=[[]for _ in obj.data.vertices]
for e in obj.data.edges:a,b=e.vertices;adj[a].append(b);adj[b].append(a)
seen=set();comps=[]
for i in range(len(adj)):
 if i in seen:continue
 pending=[i];seen.add(i);n=0
 while pending:
  j=pending.pop();n+=1
  for k in adj[j]:
   if k not in seen:seen.add(k);pending.append(k)
 comps.append(n)
r={'sampleCount':len(ids),'samplePolicy':'deterministic evenlyspaced voxelvertices to originalalpha-clipped surface BVH','distanceMeters':{'median':float(np.median(dist)),'p95':float(np.percentile(dist,95)),'p99':float(np.percentile(dist,99)),'max':max(dist)},'componentCount':len(comps),'componentVertexCountsDescending':sorted(comps,reverse=True),'noSmoothingOrDecimation':True,'limitations':'one-sided sampled surface distance, not Hausdorff or exactopaque silhouette; inward4mmthickness+3mmvoxel introduces bounded-design geometric variation, no guaranteedallpointsbound'};(O/'geometry-measurements.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
