from pathlib import Path
import bpy,json,gzip,hashlib
O=Path(__file__).resolve().parent;B=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1');V=B/'v4-padded-accessories';h=lambda x:hashlib.sha256(repr(x).encode()).hexdigest()
def snap(p):
 bpy.ops.wm.open_mainfile(filepath=str(p));return {'geometry':{o.name:h(([(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices],[tuple(f.vertices)for f in o.data.polygons]))for o in bpy.data.objects if o.type=='MESH'},'rig':{o.name:h([(b.name,tuple(tuple(r)for r in b.matrix_local),b.parent.name if b.parent else None)for b in o.data.bones])for o in bpy.data.objects if o.type=='ARMATURE'},'actions':{a.name:h([(f.data_path,f.array_index,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right),k.interpolation)for k in f.keyframe_points])for f in a.fcurves])for a in bpy.data.actions},'pants':h(([[tuple(d.uv)for d in u.data]for u in bpy.data.objects['Ruta stock long trousers'].data.uv_layers],[s.material.name for s in bpy.data.objects['Ruta stock long trousers'].material_slots],[p.material_index for p in bpy.data.objects['Ruta stock long trousers'].data.polygons]))}
a=snap(B/'v3-padded-trousers/ruta-padded-trousers-pilot.blend');b=snap(V/'ruta-final-packed-garment-pilot.blend');assert a==b
manifest=json.loads((V/'garment-transfer-manifest.json').read_text());data=json.load(gzip.open(V/'garment-transfer-data.json.gz','rt'));assert hashlib.sha256((V/manifest['donorBlend']).read_bytes()).hexdigest()==manifest['donorSHA256'];assert len(data['objects'])==len(manifest['objects']);rows=[]
for entry in data['objects']:
 n=entry['object'];assert not n.startswith('Ellie ready ');ob=bpy.data.objects[n];assert ob.type=='MESH';shape=h(([tuple(v.co)for v in ob.data.vertices],[tuple(f.vertices)for f in ob.data.polygons]));assert shape==entry['restVertexTopologySHA256'];assert len(entry['polygonMaterialIndices'])==len(ob.data.polygons);assert len(ob.data.loops)==entry['loopCount'];assert entry['preserveOtherUVLayers'];skin=0
 for f,i in zip(ob.data.polygons,entry['polygonMaterialIndices']):
  if i>=0:assert i==f.material_index and str(i)in entry['usedMaterialSlots']and ob.material_slots[i].material.name==entry['usedMaterialSlots'][str(i)]
  if ob.material_slots[f.material_index].material.name=='Skin':assert i==-1;skin+=1
 for uv,coords in entry['usedPaintUVLayers'].items():assert uv.startswith('RutaPaint')and len(coords)==len(ob.data.loops)and coords==[list(d.uv)for d in ob.data.uv_layers[uv].data]
 summary=next(x for x in manifest['objects']if x['object']==n);assert summary['usedMaterialSlots']==entry['usedMaterialSlots'];assert summary['usedPaintUVLayerNames']==list(entry['usedPaintUVLayers']);rows.append({'object':n,'skinFacesPreserved':skin,'facesTransferred':sum(i>=0 for i in entry['polygonMaterialIndices'])})
faces=[];mats=set()
for ob in bpy.data.objects:
 if ob.type!='MESH':continue
 uv=ob.data.uv_layers.get('RutaPaintPaddedAccessories')
 if not uv:continue
 for f in ob.data.polygons:
  m=ob.material_slots[f.material_index].material
  if not m.name.startswith('Ruta v4 padded accessory '):continue
  mats.add(m.name);nt=m.node_tree;tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE');diff=next(n for n in nt.nodes if n.type=='BSDF_DIFFUSE');out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');assert tex.inputs['Vector'].links[0].from_node.uv_map==uv.name;assert diff.inputs['Color'].links[0].from_node==tex and out.inputs['Surface'].links[0].from_node==diff;assert abs(diff.inputs['Roughness'].default_value-.8)<1e-6;assert tex.image.colorspace_settings.name=='sRGB'and tex.interpolation=='Linear';assert hashlib.sha256(tex.image.packed_file.data).hexdigest()==manifest['textureSHA256'];faces.append({'uv':[list(uv.data[j].uv)for j in f.loop_indices]})
assert len(mats)==33
(O/'actual-new-UV-faces.json').write_text(json.dumps(faces));(O/'invariants.json').write_text(json.dumps({'status':'PASS-scoped-readback','donorSHA':manifest['donorSHA256'],'transferDataSHA':hashlib.sha256((V/'garment-transfer-data.json.gz').read_bytes()).hexdigest(),'manifestSHA':hashlib.sha256((V/'garment-transfer-manifest.json').read_bytes()).hexdigest(),'geometryRigActionsAndPantsV3Exact':True,'actions':len(b['actions']),'paintedMaterialCount':len(mats),'actualPaintedFaces':len(faces),'transferRows':rows,'limitations':'Transfer data/schema checked against donor, no target installer/import executed; -1 must preserve target and donor slot IDs must be remapped by name.'},indent=2)+'\n')
