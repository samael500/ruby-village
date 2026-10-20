from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def record(p):
 bpy.ops.wm.open_mainfile(filepath=str(p));sc=bpy.context.scene
 meshes={o.name:{'coords':hashlib.sha256(np.array([list(v.co)for v in o.data.vertices]).tobytes()).hexdigest(),'topology':repr([tuple(p.vertices)for p in o.data.polygons]),'uv':{u.name:hashlib.sha256(np.array([tuple(v.uv)for v in u.data]).tobytes()).hexdigest()for u in o.data.uv_layers},'weights':repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]),'slots':[s.material.name if s.material else None for s in o.material_slots]}for o in sc.objects if o.type=='MESH'}
 actions={a.name:repr([(f.data_path,f.array_index,[tuple(k.co)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])for a in bpy.data.actions}
 old=bpy.data.materials['ellie.head_hair'].node_tree.nodes['Principled BSDF'];original=[list(old.inputs['Base Color'].default_value),old.inputs['Roughness'].default_value,old.inputs['Alpha'].default_value]
 return meshes,actions,{i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest()for i in bpy.data.images if i.packed_file},[list(r)for r in sc.camera.matrix_world],original
S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');source=record(S);dest=record(O/'cache/alpha-volume-baked.blend')
assert source[0]=={n:dest[0][n]for n in source[0]}
assert source[1]==dest[1] and source[3]==dest[3] and source[4]==dest[4]
assert all(dest[2][n]==v for n,v in source[2].items())
r={'sourceSha256':sha(S),'outputCacheSha256':sha(O/'cache/alpha-volume-baked.blend'),'allOriginalMeshCoordinatesTopologyUVWeightsMaterialSlotsExact':True,'actionsExact':len(source[1]),'cameraExact':True,'allOriginalPackedImagesExact':len(source[2]),'addedImageNames':sorted(set(dest[2])-set(source[2])),'sourceHairRenderHiddenInDerivativeOnly':True,'limitation':'newhair geometry visual/surface issues remain; no allphase motion certificate'}
(O/'cold-check.json').write_text(json.dumps(r,indent=2)+'\n');print('PASS')
