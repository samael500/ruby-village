from pathlib import Path
from collections import Counter,deque
import bpy,bmesh,json,hashlib,numpy as np,time
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';assert sha(S)==expected;bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;hair=bpy.data.objects['Ellie ready Daisy CC-BY hair'];rig=bpy.data.objects['CharacterArmature'];rig.data.pose_position='REST';bpy.context.view_layer.update()
def stats(o):
 me=o.data;adj=[[]for _ in me.vertices]
 for e in me.edges:a,b=e.vertices;adj[a].append(b);adj[b].append(a)
 seen=set();components=[]
 for i in range(len(adj)):
  if i in seen:continue
  pending=[i];seen.add(i);count=0
  while pending:
   j=pending.pop();count+=1
   for k in adj[j]:
    if k not in seen:seen.add(k);pending.append(k)
  components.append(count)
 bm=bmesh.new();bm.from_mesh(me);world=np.array([list(o.matrix_world@v.co)for v in me.vertices]);r={'vertices':len(me.vertices),'faces':len(me.polygons),'components':len(components),'componentVertexCountsDescending':sorted(components,reverse=True),'boundaryEdges':sum(e.is_boundary for e in bm.edges),'nonManifoldEdges':sum(not e.is_manifold for e in bm.edges),'worldBounds':[world.min(0).tolist(),world.max(0).tolist()]};bm.free();return r
source=stats(hair);candidate=hair.copy();candidate.data=hair.data.copy();candidate.name='Daisy solid-volume feasibility NOT FINAL';sc.collection.objects.link(candidate)
# This exploratory union uses native curved mesh surfaces; original opacity cutouts are NOT incorporated.
# Therefore success would require a separate original-alpha clipping/surface reconstruction stage, not direct promotion.
for m in list(candidate.modifiers):candidate.modifiers.remove(m)
bpy.context.view_layer.objects.active=candidate;candidate.select_set(True);solid=candidate.modifiers.new('Technical sheet thickness4mm','SOLIDIFY');solid.thickness=.004;solid.offset=0;solid.use_even_offset=True;bpy.ops.object.modifier_apply(modifier=solid.name);thick=stats(candidate);remesh=candidate.modifiers.new('Technical voxel union3mm','REMESH');remesh.mode='VOXEL';remesh.voxel_size=.003;remesh.use_smooth_shade=True;start=time.monotonic();bpy.ops.object.modifier_apply(modifier=remesh.name);union=stats(candidate);r={'sourceSha256':expected,'source':source,'solidify4mm':thick,'voxelUnion3mm':union,'remeshSeconds':time.monotonic()-start,'criticalLimitation':'Probe unions full original card triangles, not alpha-clipped hair. Native alpha contours must be reconstructed before this could be faithful. ExistingUV destroyed by remesh; not secretly reusing invalidUV.','proposedRGBTransfer':'Only after acceptable geometry: native originalUV closest-surface colour bake to newUV; hair-only fixed image, no perframeimageediting. Ambiguous occluded cards/alpha holes need explicit checks.'};(O/'geometry-probe.json').write_text(json.dumps(r,indent=2)+'\n');cache=O/'cache';cache.mkdir(exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(cache/'technical-volume-probe.blend'),compress=True);assert sha(S)==expected;print(json.dumps({'sourceComponents':source['components'],'unionComponents':union['components'],'unionBoundary':union['boundaryEdges'],'unionNonManifold':union['nonManifoldEdges'],'vertices':union['vertices']},indent=2))
