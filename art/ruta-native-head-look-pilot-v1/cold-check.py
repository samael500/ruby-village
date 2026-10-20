from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent
exec((O/'prepare.py').read_text().split('reports=[]')[0])
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];records={o.name:mesh_record(o)for o in sc.objects if o.type=='MESH'};acts={a.name:ah(a)for a in bpy.data.actions};images={i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file};cam=([list(r)for r in sc.camera.matrix_world],sc.camera.data.ortho_scale,sc.render.resolution_x,sc.render.resolution_y);head=bpy.data.objects['Ellie ready head'];ids=[v.index for v in head.data.vertices if v.co.z<=1.18];evals={}
 for f in [0,40]:
  sc.frame_set(f);bpy.context.view_layer.update();ev=head.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();evals[f]=np.array([list(ev.matrix_world@me.vertices[i].co)for i in ids]);ev.to_mesh_clear()
 return records,acts,images,cam,ids,evals
s=snapshot(SOURCE);c=snapshot(O/'ruta-head-look-chosen.blend');changed={x['name']for x in json.load(open(O/'pitch-up20/contract.json'))['changedObjects']}
for n in s[0]:
 for k in s[0][n]:
  if n in changed and k=='coordsSha256':continue
  assert s[0][n][k]==c[0][n][k],(n,k)
assert s[1]==c[1] and s[2]==c[2] and s[3]==c[3] and s[4]==c[4]
seam={f:float(np.linalg.norm(s[5][f]-c[5][f],axis=1).max())for f in s[5]};assert max(seam.values())==0
r={'sourceSha256':sha(SOURCE),'chosenSha256':sha(O/'ruta-head-look-chosen.blend'),'actionCountExact':len(s[1]),'packedImageCountExact':len(s[2]),'cameraCanvasExact':True,'allMeshTopologyUVWeightsModifiersMaterialSlotsExact':True,'nonHeadMeshCoordinatesExact':True,'protectedNeckVertexCount':len(s[4]),'evaluatedProtectedNeckMaxDeltaMetersAtFrames':seam,'scope':'cold-open source and final saved E Walk blend, no 48-phase/global art certificate'};(O/'cold-check.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
