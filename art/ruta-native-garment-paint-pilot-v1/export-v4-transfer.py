from pathlib import Path
import bpy,json,gzip,hashlib
O=Path(__file__).resolve().parent/'v4-padded-accessories';bpy.ops.wm.open_mainfile(filepath=str(O/'ruta-final-packed-garment-pilot.blend'));sc=bpy.context.scene;validation=json.load(open(O/'generated-padding-validation.json'))
transfer=[]
for ob in sc.objects:
 if ob.type!='MESH' or ob.name.startswith('Ellie ready '):continue
 used=sorted(set(f.material_index for f in ob.data.polygons));slots={i:ob.data.materials[i]for i in used if i<len(ob.data.materials)and ob.data.materials[i] and (ob.data.materials[i].name.startswith(('Ruta painted garment ','Ruta v3 padded ','Ruta v4 padded ')) or ob.name in ['Adventurer_Feet','ONE diagonal satchel strap','ONE rounded right hip satchel','Single rounded satchel flap','Ruta stock long trousers','Cargo side pocket L','Cargo side pocket R'])}
 if not slots:continue
 layers=set()
 for mat in slots.values():
  if mat.use_nodes:
   layers.update(n.uv_map for n in mat.node_tree.nodes if n.type=='UVMAP'and n.uv_map.startswith('RutaPaint'))
 if not layers and ob.name not in ['Cargo side pocket L','Cargo side pocket R']:continue
 shape=hashlib.sha256(repr(([tuple(v.co)for v in ob.data.vertices],[tuple(f.vertices)for f in ob.data.polygons])).encode()).hexdigest()
 transfer.append({'object':ob.name,'restVertexTopologySHA256':shape,'vertexCount':len(ob.data.vertices),'polygonCount':len(ob.data.polygons),'loopCount':len(ob.data.loops),'usedMaterialSlots':{str(k):v.name for k,v in slots.items()},'polygonMaterialIndices':[f.material_index if f.material_index in slots else -1 for f in ob.data.polygons],'usedPaintUVLayers':{name:[list(l.uv)for l in ob.data.uv_layers[name].data]for name in sorted(layers)},'preserveOtherUVLayers':True})
with gzip.open(O/'garment-transfer-data.json.gz','wt')as z:json.dump({'status':'garmentUVMaterialOnly-not-rig-head-hair-transfer','objects':transfer},z)

summary={'donorBlend':'ruta-final-packed-garment-pilot.blend','donorSHA256':hashlib.sha256((O/'ruta-final-packed-garment-pilot.blend').read_bytes()).hexdigest(),'textureSHA256':validation['rawSHA256'],'rawImageUnchanged':True,'noBackgroundGuardOrContrastHack':True,'transferScope':'Only specified garment objects: copy used material datablocks, named usedPaintUVLayers per loop, then polygon material indices with slot remap (-1 preserves target face material); NOT original source slot numbering directly; verify restVertexTopologySHA256 first. Do not copy rig/geometry/actions/head/hair. Keep target native palette UV and unrelated UVs.','objects':[{k:v for k,v in row.items()if k not in ['polygonMaterialIndices','usedPaintUVLayers']}|{'usedPaintUVLayerNames':list(row['usedPaintUVLayers'])}for row in transfer]};(O/'garment-transfer-manifest.json').write_text(json.dumps(summary,indent=2));print('V4_PACKED_ACTUAL_DONE',flush=True)
