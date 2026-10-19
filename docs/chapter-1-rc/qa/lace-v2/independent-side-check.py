import bpy,json,hashlib
from pathlib import Path
from mathutils import Matrix
from mathutils.bvhtree import BVHTree
P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');bpy.ops.wm.open_mainfile(filepath=str(P));s=bpy.context.scene;r=bpy.data.objects['CharacterArmature'];r.matrix_world=Matrix.Identity(4);r.data.pose_position='POSE';a=bpy.data.actions['Walk_ProportionProposal'];r.animation_data.action=a;r.animation_data.action_slot=a.slots[0]
for t in r.animation_data.nla_tracks:t.mute=True
boots=bpy.data.objects['Adventurer_Feet'];rows=[]
def geom(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();v=[ev.matrix_world@x.co for x in m.vertices];tri=[tuple(x.vertices)for x in m.loop_triangles];ev.to_mesh_clear();return v,tri
for i in range(48):
 frame=40*i/48;s.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();v,tri=geom(boots)
 for side,sign in [('L',1),('R',-1)]:
  ids=[t for t in tri if sum(boots.data.vertices[j].co.x for j in t)*sign>0];tree=BVHTree.FromPolygons(v,ids,all_triangles=True);lace=bpy.data.objects['Ankle boot lace '+side];coords,faces=geom(lace);used=sorted({j for t in faces for j in t});dist=[];signed=[]
  for j in used:
   p,n,idx,d=tree.find_nearest(coords[j]);dist.append(d);signed.append((coords[j]-p).dot(n))
  rows.append({'phase':i,'side':side,'usedVertices':len(used),'maxSameSideDistanceM':max(dist),'minSignedDistanceM':min(signed),'maxSignedDistanceM':max(signed)})
weights={}
for side in ['L','R']:
 o=bpy.data.objects['Ankle boot lace '+side];groups={g.name:0 for g in o.vertex_groups}
 for v in o.data.vertices:
  for g in v.groups:groups[o.vertex_groups[g.group].name]+=g.weight
 weights[side]={k:v/len(o.data.vertices)for k,v in groups.items()if v>0}
out={'sourceSha256':hashlib.sha256(P.read_bytes()).hexdigest(),'sameSideMaxDistanceM':max(x['maxSameSideDistanceM']for x in rows),'minSignedDistanceM':min(x['minSignedDistanceM']for x in rows),'maxSignedDistanceM':max(x['maxSignedDistanceM']for x in rows),'averageVertexSkinWeights':weights,'rows':rows,'scope':'48sampledposes ownsideunsignedandsignedsurfaceproximity, not continuouscollision or visualacceptance'};Path('/tmp/ruby-export-pack-qa/docs/chapter-1-rc/qa/lace-v2/independent-side-report.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items()if k!='rows'})
