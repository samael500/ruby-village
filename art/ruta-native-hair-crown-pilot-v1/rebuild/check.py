from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
 bpy.ops.wm.open_mainfile(filepath=str(p));sc=bpy.context.scene
 meshes={o.name:{'coords':hashlib.sha256(np.array([list(v.co)for v in o.data.vertices]).tobytes()).hexdigest(),'topology':repr([tuple(p.vertices)for p in o.data.polygons]),'uv':{u.name:hashlib.sha256(np.array([tuple(v.uv)for v in u.data]).tobytes()).hexdigest()for u in o.data.uv_layers},'weights':repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]),'slots':[s.material.name if s.material else None for s in o.material_slots]}for o in sc.objects if o.type=='MESH'}
 actions={a.name:repr([(f.data_path,f.array_index,[tuple(k.co)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])for a in bpy.data.actions}
 old=bpy.data.materials['ellie.head_hair'].node_tree.nodes['Principled BSDF'];original=[list(old.inputs['Base Color'].default_value),old.inputs['Roughness'].default_value,old.inputs['Alpha'].default_value]
 return meshes,actions,{i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file},[list(r)for r in sc.camera.matrix_world],original
S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');s=record(S);d=record(O/'ruta-continuous-crown.blend');changes=[]
for name in s[0]:
 for k in s[0][name]:
  if s[0][name][k]!=d[0][name][k]:changes.append([name,k,s[0][name][k],d[0][name][k]])
assert len(changes)==1 and changes[0][:2]==['Ellie ready Daisy CC-BY hair','coords'];assert s[1:]==d[1:];(O/'cold-check.json').write_text(json.dumps({'allExistingGeometryExactExceptDaisyRootCoordinates':True,'actionsExact':len(s[1]),'packedImagesExact':len(s[2]),'cameraExact':True,'originalScalpMaterialUnchanged':True,'sourceMeshRecordChanges':changes,'sourceSha256':sha(S),'outputSha256':sha(O/'ruta-continuous-crown.blend')},indent=2)+'\n');print('PASS')
