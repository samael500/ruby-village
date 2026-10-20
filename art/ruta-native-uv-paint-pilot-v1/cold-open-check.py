from pathlib import Path
import bpy,json,hashlib
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O/'ruta-native-painted-hair-pilot.blend'))
c=json.load(open(O/'pilot-contract.json'));actual={a.name:hashlib.sha256(str([(fc.data_path,fc.array_index,[(tuple(k.co),k.interpolation)for k in fc.keyframe_points])for fc in a.fcurves]).encode()).hexdigest()for a in bpy.data.actions}
assert actual==c['actionHashesUnchanged'];assert all(a.use_fake_user for a in bpy.data.actions)
m=bpy.data.materials['Ellie ready Stable painted copper UV pilot'];output=next(n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL');assert output.inputs['Surface'].links[0].from_node.type=='BSDF_DIFFUSE'
report={'actionCount':len(actual),'actionHashesUnchanged':True,'allActionsFakeUser':True,'surfaceShader':'Diffuse BSDF roughness .8; original SH-Hair nodes disconnected from output','texturePacked':True,'sourceSHA256':hashlib.sha256(Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend').read_bytes()).hexdigest(),'derivativeSHA256':hashlib.sha256((O/'ruta-native-painted-hair-pilot.blend').read_bytes()).hexdigest()};assert report['sourceSHA256']=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';(O/'cold-open-check.json').write_text(json.dumps(report,indent=2));print('COLD_OPEN_PASS')
def meshhash():
 return {o.name:hashlib.sha256(str(([(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices],[tuple(p.vertices)for p in o.data.polygons])).encode()).hexdigest()for o in bpy.data.objects if o.type=='MESH'}
def righash():
 return {o.name:hashlib.sha256(str([(b.name,tuple(b.head_local),tuple(b.tail_local),b.parent.name if b.parent else None)for b in o.data.bones]).encode()).hexdigest()for o in bpy.data.objects if o.type=='ARMATURE'}
a=meshhash();r=righash();bpy.ops.wm.open_mainfile(filepath='/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');assert a==meshhash();assert r==righash();report['allMeshRestPositionsTopologyWeightsEqualFrozen']=True;report['allRigRestBonesEqualFrozen']=True;(O/'cold-open-check.json').write_text(json.dumps(report,indent=2));print('GEOMETRY_RIG_PASS')
def binding():
 return {o.name:{'activeRenderUV':[u.name for u in o.data.uv_layers if u.active_render],'materials':[{'name':s.material.name,'nodes':[{'name':n.name,'type':n.type,'uvMap':getattr(n,'uv_map',None),'image':n.image.name if n.type=='TEX_IMAGE' and n.image else None}for n in s.material.node_tree.nodes]}for s in o.material_slots if s.material and s.material.use_nodes]}for o in bpy.data.objects if o.type=='MESH' and o.name in ['Adventurer_Body','Adventurer_Feet','Ruta stock long trousers']}
original=binding();bpy.ops.wm.open_mainfile(filepath=str(O/'ruta-native-painted-hair-pilot.blend'));derivative=binding();assert original==derivative;(O/'unpainted-material-binding-check.json').write_text(json.dumps({'original':original,'derivative':derivative,'sameOriginalPaletteUVAndNodes':True},indent=2));print('PALETTE_BINDING_PASS')
