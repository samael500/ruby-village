from pathlib import Path
import bpy,json,hashlib
O=Path(__file__).resolve().parent;source=O.parent/'ruta-native-uv-paint-pilot-v1/ruta-native-painted-hair-pilot.blend';derivative=O/'v4-padded-accessories/ruta-accessories-newUV-source.blend'
def digest(x):return hashlib.sha256(repr(x).encode()).hexdigest()
def inventory():
 return {'meshRestTopologyWeights':{o.name:digest(([(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices],[tuple(p.vertices)for p in o.data.polygons]))for o in bpy.data.objects if o.type=='MESH'},'rigRest':{o.name:digest([(b.name,tuple(b.head_local),tuple(b.tail_local),b.parent.name if b.parent else None)for b in o.data.bones])for o in bpy.data.objects if o.type=='ARMATURE'},'actions':{a.name:digest([(fc.data_path,fc.array_index,[(tuple(k.co),k.interpolation)for k in fc.keyframe_points])for fc in a.fcurves])for a in bpy.data.actions},'protectedHeadHairUVMaterials':{o.name:digest(([[tuple(l.uv)for l in u.data]for u in o.data.uv_layers],[s.material.name if s.material else None for s in o.material_slots]))for o in bpy.data.objects if o.type=='MESH'and o.name.startswith('Ellie ready ')}}
bpy.ops.wm.open_mainfile(filepath=str(source));a=inventory();bpy.ops.wm.open_mainfile(filepath=str(derivative));b=inventory();assert a==b;assert all(x.use_fake_user for x in bpy.data.actions)
contract=json.load(open(O/'partial-reuse-contract.json'))
report={'status':'cold-open-source-invariants-PASS-not-art-quality','sourceSHA256':hashlib.sha256(source.read_bytes()).hexdigest(),'derivativeSHA256':hashlib.sha256(derivative.read_bytes()).hexdigest(),'restPositionsTopologyWeightsEqual':True,'rigRestEqual':True,'allActionsEqual':True,'actionCount':len(b['actions']),'headHairUVMaterialsUnchanged':True,'explicitRutaPaintBindingsChecked':'pre-generation placeholders; not applied','allActionsFakeUser':True,'renderEngine':bpy.context.scene.render.engine}
(O/'v4-padded-accessories/cold-open-check.json').write_text(json.dumps(report,indent=2));print('COLD_OPEN_PASS',flush=True)

def pants():
 ob=bpy.data.objects['Ruta stock long trousers'];return digest(([[tuple(l.uv)for l in u.data]for u in ob.data.uv_layers],[s.material.name if s.material else None for s in ob.material_slots],[p.material_index for p in ob.data.polygons]))
p=pants();bpy.ops.wm.open_mainfile(filepath=str(O/'v3-padded-trousers/ruta-padded-trousers-pilot.blend'));assert p==pants();report['pantsV3AllUVAndMaterialAssignmentsEqual']=True;(O/'v4-padded-accessories/cold-open-check.json').write_text(json.dumps(report,indent=2));print('PANTS_FROZEN_PASS')
