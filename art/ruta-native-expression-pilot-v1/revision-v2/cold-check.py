from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[2];S=R/'art/ruta-native-hair-volume-study-v1/alpha-aware/cache/alpha-volume-baked.blend';D=O/'cache/ruta-expression-trial.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def actionhash(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for bag in s.channelbags for f in bag.fcurves]).encode()).hexdigest()
def snap(p):
 bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];meshes={}
 for o in sc.objects:
  if o.type!='MESH':continue
  coords=np.array([list(v.co)for v in o.data.vertices]);meshes[o.name]={'coords':coords,'topology':hashlib.sha256(repr([tuple(p.vertices)for p in o.data.polygons]).encode()).hexdigest(),'uv':{u.name:hashlib.sha256(np.array([tuple(v.uv)for v in u.data]).tobytes()).hexdigest()for u in o.data.uv_layers},'weights':hashlib.sha256(repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]).encode()).hexdigest(),'materials':[s.material.name if s.material else None for s in o.material_slots],'hideRender':o.hide_render}
 return meshes,{a.name:actionhash(a)for a in bpy.data.actions},{i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file},repr([(b.name,tuple(b.head_local),tuple(b.tail_local),tuple(tuple(r)for r in b.matrix_local),b.parent.name if b.parent else None)for b in rig.data.bones]),[list(r)for r in sc.camera.matrix_world],sc.camera.data.ortho_scale,[list(r)for r in rig.matrix_world]
a=snap(S);b=snap(D);assert a[1:]==b[1:];assert a[0].keys()==b[0].keys();parts=json.load(open(O/'derivation.json'))['parts'];allowed={'Ellie ready '+p['part']for p in parts if p['expressionChangedVertices']};rows=[]
for n,record in a[0].items():
 for k in record:
  if k!='coords':assert record[k]==b[0][n][k],(n,k)
  elif n not in allowed:assert np.array_equal(record[k],b[0][n][k]),n
 if n in allowed:
  v=record['coords'];delta=np.linalg.norm(v-b[0][n]['coords'],axis=1);protected=v[:,2]<=1.18;rows.append({'name':n,'changedVertices':int((delta>1e-8).sum()),'deltaMaxMeters':float(delta.max()),'protectedBelowZ1p18Count':int(protected.sum()),'protectedDeltaMaxMeters':float(delta[protected].max())if protected.any()else None});assert not protected.any()or delta[protected].max()==0
r={'sourceSha256':sha(S),'trialSha256':sha(D),'actionFullKeyHandlesHashesExact':len(a[1]),'boneRestRigMatrixCameraExact':True,'allPackedImagesExact':len(a[2]),'allMeshTopologyUVWeightsMaterialSlotsRenderVisibilityExact':True,'nonFacialCoordinatesIncludingCrownEyeGlobesAndHighlightsExact':True,'facialCoordinateDeltas':rows,'largeDeltaAcceptance':'UNCERTIFIED: native mouthparts up to33.13mm; mouth may overopen expression, require actualfront/closeup and futuremotionintersection review, not accepted'};(O/'cold-check.json').write_text(json.dumps(r,indent=2)+'\n');print('COLD_PASS_NO_RENDER')
