from pathlib import Path
import bpy,json,gzip,hashlib
R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style');O=Path(__file__).resolve().parent;H=R/'art/ruta-native-head-look-pilot-v1/scalp-copper-material/ruta-copper-scalp.blend';C=R/'art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend';D=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1/v4-padded-accessories');h=lambda x:hashlib.sha256(repr(x).encode()).hexdigest()
def val(v):
 if isinstance(v,(int,float,str,bool)):return v
 try:return list(v)
 except:return str(type(v))
def graph(m):
 if not m:return None
 if not m.use_nodes:return h((m.name,tuple(m.diffuse_color)))
 nodes=[]
 for n in m.node_tree.nodes:
  image=getattr(n,'image',None);ih=hashlib.sha256(image.packed_file.data).hexdigest()if image and image.packed_file else image.filepath if image else None
  nodes.append((n.name,n.type,[(p.name,val(p.default_value))for p in n.inputs if hasattr(p,'default_value')],ih,getattr(n,'uv_map',None),getattr(n,'operation',None),getattr(n,'blend_type',None)))
 return h((nodes,[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name)for l in m.node_tree.links]))
def snap(p):
 bpy.ops.wm.open_mainfile(filepath=str(p));out={'geometry':{},'UV':{},'faces':{},'graphs':{}}
 for ob in bpy.data.objects:
  if ob.type=='MESH':
   out['geometry'][ob.name]=h(([(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in ob.data.vertices],[tuple(f.vertices)for f in ob.data.polygons]));out['UV'][ob.name]={u.name:h([tuple(d.uv)for d in u.data])for u in ob.data.uv_layers};materials=[s.material for s in ob.material_slots];graphs=[graph(m) for m in materials];out['faces'][ob.name]=[materials[f.material_index].name if f.material_index<len(materials)and materials[f.material_index]else None for f in ob.data.polygons];out['graphs'][ob.name]=[graphs[f.material_index]if f.material_index<len(graphs)else None for f in ob.data.polygons]
 out['rig']={o.name:h([(b.name,tuple(tuple(r)for r in b.matrix_local),b.parent.name if b.parent else None)for b in o.data.bones])for o in bpy.data.objects if o.type=='ARMATURE'};out['actions']={a.name:h([(f.data_path,f.array_index,[(tuple(k.co),tuple(k.handle_left),tuple(k.handle_right),k.interpolation)for k in f.keyframe_points])for f in a.fcurves])for a in bpy.data.actions};return out
assert hashlib.sha256(H.read_bytes()).hexdigest()=='f9376819c54d8136f8a56d6eaae875c9fbc0535a02f1509bb2d5cae07e622ceb';assert hashlib.sha256(C.read_bytes()).hexdigest()=='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7'
a=snap(H);b=snap(C);assert a['geometry']==b['geometry']and a['rig']==b['rig']and a['actions']==b['actions'];t=json.load(gzip.open(D/'garment-transfer-data.json.gz','rt'));by={e['object']:e for e in t['objects']};assembly=json.loads((R/'art/ruta-native-painted-combined-v1/assembly-contract.json').read_text());assemblyBy={r['object']:r for r in assembly['transfers']};skin=0;preserve=0;head=0
for name,uv in a['UV'].items():
 allow=set(assemblyBy[name]['paintUVs'])if name in assemblyBy else set()
 for u in allow:assert b['UV'][name][u]==assemblyBy[name]['sourceUVHashes'][u]
 for u,hh in uv.items():
  if u not in allow:assert b['UV'][name][u]==hh,(name,u,hh,b['UV'][name][u])
 if name not in by:
  assert a['faces'][name]==b['faces'][name]and a['graphs'][name]==b['graphs'][name]
  if name.startswith('Ellie ready '):head+=1
  continue
 entry=by[name]
 for u,coords in entry['usedPaintUVLayers'].items():assert b['UV'][name][u]==h([tuple(v)for v in coords])
 for i,slot in enumerate(entry['polygonMaterialIndices']):
  if slot==-1:assert a['faces'][name][i]==b['faces'][name][i]and a['graphs'][name][i]==b['graphs'][name][i];preserve+=1
  else:assert b['faces'][name][i]==entry['usedMaterialSlots'][str(slot)]
  if a['faces'][name][i]=='Skin':assert slot==-1 and b['graphs'][name][i]==a['graphs'][name][i];skin+=1
(O/'results.json').write_text(json.dumps({'status':'PASS-scoped-independent-cold-open','headSourceSHA256':hashlib.sha256(H.read_bytes()).hexdigest(),'combinedSHA256':hashlib.sha256(C.read_bytes()).hexdigest(),'meshRestTopologyWeightCountExact':len(a['geometry']),'rigBonesRestHashesExact':a['rig'],'actionsExactIncludingHandles':len(a['actions']),'skinFacesGraphAndAssignmentPreserved':skin,'allMinusOneFacesGraphAndAssignmentPreserved':preserve,'headHairObjectUVGraphsAndFacesExact':head,'nativePaletteAndNonPaintNamespaceUVLayersPreserved':True,'scopeWarning':'Assembler copies PAINT_UVS referenced by all donor slots, including unused old RutaPaint on feet; broader than transfer manifest actually-used layers. Extra unused paint-layer overwrite is not native UVMap overwrite.','allNamedTransferredUVLoopsExact':True,'allTransferredFaceMaterialNamesExact':True,'limits':'No render, animation evaluation, target installer execution, new combined loop or visual/game/no-slip acceptance.'},indent=2)+'\n')
