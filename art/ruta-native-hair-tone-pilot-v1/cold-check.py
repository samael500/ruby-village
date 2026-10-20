from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
 bpy.ops.wm.open_mainfile(filepath=str(p));sc=bpy.context.scene
 meshes={o.name:{'coords':hashlib.sha256(np.array([list(v.co)for v in o.data.vertices]).tobytes()).hexdigest(),'topology':repr([tuple(p.vertices)for p in o.data.polygons]),'uv':{u.name:hashlib.sha256(np.array([tuple(v.uv)for v in u.data]).tobytes()).hexdigest()for u in o.data.uv_layers},'weights':repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]),'slots':[s.material.name if s.material else None for s in o.material_slots]}for o in sc.objects if o.type=='MESH'}
 actions={a.name:repr([(f.data_path,f.array_index,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])for a in bpy.data.actions}
 old=bpy.data.materials['ellie.head_hair'].node_tree.nodes['Principled BSDF'];original=[list(old.inputs['Base Color'].default_value),old.inputs['Roughness'].default_value,old.inputs['Alpha'].default_value]
 rig=bpy.data.objects['CharacterArmature'];rigproof=repr(([(b.name,tuple(b.head_local),tuple(b.tail_local),tuple(tuple(r)for r in b.matrix_local),b.parent.name if b.parent else None)for b in rig.data.bones],tuple(tuple(r)for r in rig.matrix_world)))
 return meshes,actions,{i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file},[list(r)for r in sc.camera.matrix_world],original,rigproof
S=O.parents[1]/'art/ruta-native-expression-pilot-v1/revision-v2/cache/ruta-expression-trial.blend';s=record(S);d=record(O/'cache/ruta-hair-tone-trial.blend');changes=[]
for name in s[0]:
 for k in s[0][name]:
  if s[0][name][k]!=d[0][name][k]:changes.append([name,k,s[0][name][k],d[0][name][k]])
assert len(changes)==1 and changes[0][:2]==['Daisy alpha-aware volume candidate','slots'];assert s[1:]==d[1:];(O/'cold-check.json').write_text(json.dumps({'geometryTopologyUVWeightsExact':True,'actionsExact':len(s[1]),'packedImagesExact':len(s[2]),'cameraBoneRestRigMatrixExact':True,'originalScalpMaterialUnchanged':True,'onlyMeshRecordChange':changes,'sourceSha256':sha(S),'outputSha256':sha(O/'cache/ruta-hair-tone-trial.blend')},indent=2)+'\n');print('PASS')
