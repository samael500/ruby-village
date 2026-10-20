from pathlib import Path
import bpy,json,hashlib,gzip
O=Path(__file__).resolve().parent;B=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1');paths=[B/'ruta-painted-garment-pilot.blend',B/'v3-padded-trousers/ruta-padded-trousers-pilot.blend']
h=lambda v:hashlib.sha256(repr(v).encode()).hexdigest()
def snap(P):
 bpy.ops.wm.open_mainfile(filepath=str(P));meshes={}
 for o in bpy.data.objects:
  if o.type=='MESH':meshes[o.name]={'rest':h([(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices]+[tuple(f.vertices)for f in o.data.polygons]),'UV':{u.name:h([tuple(d.uv)for d in u.data])for u in o.data.uv_layers},'materials':[s.material.name if s.material else None for s in o.material_slots]}
 rigs={o.name:h([(b.name,tuple(tuple(r)for r in b.matrix_local),b.parent.name if b.parent else None)for b in o.data.bones])for o in bpy.data.objects if o.type=='ARMATURE'};actions={a.name:h([(fc.data_path,fc.array_index,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right),k.interpolation)for k in fc.keyframe_points])for fc in a.fcurves])for a in bpy.data.actions}
 return {'sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'meshes':meshes,'rigs':rigs,'actions':actions}
a=snap(paths[0]);b=snap(paths[1]);assert a['rigs']==b['rigs']and a['actions']==b['actions'];assert set(a['meshes'])==set(b['meshes'])
for n,v in a['meshes'].items():
 assert v['rest']==b['meshes'][n]['rest']
 for uv,hh in v['UV'].items():assert b['meshes'][n]['UV'][uv]==hh
 if n!='Ruta stock long trousers':assert v['materials']==b['meshes'][n]['materials']
ob=bpy.data.objects['Ruta stock long trousers'];uv=ob.data.uv_layers['RutaPaintPaddedTrousers'];faces=[];mapping={}
for f in ob.data.polygons:
 m=ob.material_slots[f.material_index].material;mapping.setdefault(m.name,[]).append(f.index)
 if m.use_nodes and any(n.type=='UVMAP'and n.uv_map==uv.name for n in m.node_tree.nodes):
  tex=next(n for n in m.node_tree.nodes if n.type=='TEX_IMAGE');assert hashlib.sha256(tex.image.packed_file.data).hexdigest()=='b61be8876856d1463b9a8dfa7afecf60c95333f45792180a0e717fd08a107179';assert tex.image.colorspace_settings.name=='sRGB';assert tex.interpolation=='Linear';assert tex.inputs['Vector'].links[0].from_node.type=='UVMAP' and tex.inputs['Vector'].links[0].from_node.uv_map==uv.name;diff=next(n for n in m.node_tree.nodes if n.type=='BSDF_DIFFUSE');assert diff.inputs['Color'].links[0].from_node==tex and abs(diff.inputs['Roughness'].default_value-.8)<1e-6;out=next(n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL');assert out.inputs['Surface'].links[0].from_node==diff;faces.append({'index':f.index,'uv':[list(uv.data[j].uv)for j in f.loop_indices]})
meta=json.loads((B/'v3-padded-trousers/padding-contract.json').read_text());selected={i for c in meta['selectedCharts']for i in c['sourceFaceIndices']};assert {f['index']for f in faces}==selected;assert len(selected)==meta['selectedFaces'];assert set(range(len(ob.data.polygons)))-selected==set(meta['tinyUnpaintedFaces'])
(O/'actual-new-UV-faces.json').write_text(json.dumps(faces));(O/'invariants.json').write_text(json.dumps({'status':'PASS','baseSha256':a['sha256'],'candidateSha256':b['sha256'],'meshesRestTopologyWeightsEqual':len(a['meshes']),'rigsEqual':a['rigs'],'actionsEqual':len(a['actions']),'oldUVLayersAllPreserved':True,'otherObjectMaterialSlotsPreserved':True,'selectedFaceCount':len(selected),'tinyPlainFaces':len(meta['tinyUnpaintedFaces']),'actualMaterialFaceMapping':mapping,'texturePackedHash':'b61be8876856d1463b9a8dfa7afecf60c95333f45792180a0e717fd08a107179'},indent=2)+'\n')
