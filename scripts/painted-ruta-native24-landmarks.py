"""Read-only native skeletal/sole feature projection for manual sprite registration."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1];O=R/'art/painted-ruta-registration24-v1';O.mkdir(exist_ok=True);S=R/'art/ready-character-adapted-v1/ruta-stock-adapted.blend';bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];feet=bpy.data.objects['Adventurer_Feet']
for t in rig.animation_data.nla_tracks:t.mute=True
a=bpy.data.actions['Walk'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0];p=rig.data.bones['Root'].head_local.copy();p.z=0;rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-p)
# Sole markers use actual source vertices, selected once in native rest geometry.
sole={}
for side in ['L','R']:
 names={g.index:g.name for g in feet.vertex_groups};ids=[v.index for v in feet.data.vertices if any(names[g.group]=='Foot.'+side and g.weight>=.5 for g in v.groups)];assert ids
 zmin=min(feet.data.vertices[i].co.z for i in ids);ids=[i for i in ids if feet.data.vertices[i].co.z<=zmin+.012];ys=[feet.data.vertices[i].co.y for i in ids];span=max(ys)-min(ys)
 sole[side]={'soleRestRegion':ids,'toe': [i for i in ids if feet.data.vertices[i].co.y<=min(ys)+span*.15],'heel':[i for i in ids if feet.data.vertices[i].co.y>=max(ys)-span*.15]}
def marker(w):
 q=world_to_camera_view(sc,sc.camera,w);return {'worldMeters':list(w),'guideDeliveryPx':[q.x*256,(1-q.y)*320]}
rows=[]
for i in range(24):
 f=40*i/24;sc.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();marks={name:marker(rig.matrix_world@rig.pose.bones[bone].head)for name,bone in {'root':'Root','hip':'Hips','ankleL':'Foot.L','ankleR':'Foot.R'}.items()};ev=feet.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
 for side,regions in sole.items():
  for feature,ids in regions.items():
   w=sum((ev.matrix_world@mesh.vertices[j].co for j in ids),Vector())/len(ids);marks[feature+side]=marker(w)
 ev.to_mesh_clear();rows.append({'index':i,'sourceFrame':f,'markers':marks})
(O/'native-landmarks24.json').write_text(json.dumps({'source':str(S.relative_to(R)),'sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'rootWorld':[0,0,0],'rootRestGround':list(p),'yawRadians':math.pi/2,'frameSize':[256,320],'joints':'pose bone heads; anatomical L/R; hip=Hips head','soleDefinition':'actual boot vertices with Foot.side weight>=.5, restZ<=minimum+.012m; toe/heel extreme15% nativeY of this region; marker=mean evaluated vertex positions, NOT inferred contact or bbox bottom','soleSourceVertexIndices':sole,'uncertainty':'sole region features are geometric references, not verified stance contacts; source in-place foot slide is retained','frames':rows},indent=2)+'\n');print('NATIVE24_OK')
