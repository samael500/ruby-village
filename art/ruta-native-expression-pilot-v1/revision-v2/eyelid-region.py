from pathlib import Path
import bpy,json,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[2];bpy.ops.wm.open_mainfile(filepath=str(R/'art/ruta-ellie-head-v1/source/ellie-original.blend'),use_scripts=False);o=bpy.data.objects['GEO-ellie_head']
if o.animation_data:
 for d in o.animation_data.drivers:
  if 'levels'in d.data_path:d.mute=True
for m in o.modifiers:
 if m.type=='SUBSURF':m.show_viewport=True;m.levels=max(1,min(2,m.render_levels))
bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();groups={g.index:g.name for g in o.vertex_groups if 'eyelid'in g.name.lower()};ids=[v.index for v in me.vertices if sum(g.weight for g in v.groups if g.group in groups)>.05];delta=np.load(O/'cache/native-expression-delta.npz')['head'];assert len(me.vertices)==len(delta);d=np.linalg.norm(delta[ids],axis=1)if ids else np.array([]);r={'nativeEyelidWeightGroupNames':list(groups.values()),'thresholdTotalWeight':.05,'evaluatedVertexCount':len(me.vertices),'eyelidRegionVertexCount':len(ids),'nativeExpressionDeltaMaxMeters':float(d.max())if len(d)else None,'nativeExpressionChangedCountAbove1eMinus7':int((d>1e-7).sum())if len(d)else None,'definition':'actual original evaluated head skinning-group region, not bitmap landmark'};
weights=np.array([sum(g.weight for g in v.groups if g.group in groups)for v in me.vertices]);r['weightThresholdDetails']=[{'threshold':float(t),'vertexCount':int((weights>t).sum()),'deltaMaxNativeMeters':float(np.linalg.norm(delta[weights>t],axis=1).max())if (weights>t).any()else None}for t in [.25,.5,.8,.95]]
from collections import Counter
edges=Counter(tuple(sorted((a,b)))for p in me.polygons for a,b in zip(list(p.vertices),list(p.vertices)[1:]+list(p.vertices)[:1]));boundary={i for e,n in edges.items()if n==1 for i in e};rim=sorted(i for i in boundary if weights[i]>.05);r['verifiedBoundaryEyelidRegionVertexCount']=len(rim);r['rimDeltaMaxNativeMeters']=float(np.linalg.norm(delta[rim],axis=1).max())if rim else None
r['strictZeroRegionGuard']='FAILED, explicitly relaxedbyroot: smallbrowskininfluenceallowed, no longerclaimexactlidskinpreservation'
r['anatomicalOpeningLimitation']='Openingboundary only if native meshboundary intersects eyelidgroups, not projectedfullskinbbox'
ev.to_mesh_clear();(O/'eyelid-region.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));assert len(ids)>0
