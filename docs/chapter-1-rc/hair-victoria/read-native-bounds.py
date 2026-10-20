import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(P/'sources/victoria.blend'));out={'sourceSha256':hashlib.sha256((P/'sources/victoria.blend').read_bytes()).hexdigest(),'space':'original native world meters, raw rest geometry; bone points are authored rig landmarks NOT measured scalp surface','hair':{},'headRestBoneLandmarks':{}}
for name in ['GEO-victoria_hair_main','GEO-victoria_hair_bangs']:
 o=bpy.data.objects[name];vs=[o.matrix_world@v.co for v in o.data.vertices];out['hair'][name]={'min':[min(v[i]for v in vs)for i in range(3)],'max':[max(v[i]for v in vs)for i in range(3)],'objectMatrix':[list(r)for r in o.matrix_world],'uvLayers':[x.name for x in o.data.uv_layers],'materials':[x.name for x in o.data.materials]}
for rigName,names in [('META-Victoria',['Head','Head_Top']),('RIG-Victoria',['ORG-Head','ORG-Head_Top'])]:
 o=bpy.data.objects[rigName]
 for name in names:
  b=o.data.bones[name];out['headRestBoneLandmarks'][rigName+'/'+name]={'head':list(o.matrix_world@b.head_local),'tail':list(o.matrix_world@b.tail_local)}
out['delivery']={'hairOnlyBlendSha256':hashlib.sha256((P/'victoria-hair-only-raw-rest.blend').read_bytes()).hexdigest(),'uvNote':'Both original meshes have zero UV layers; original materials/face material indices preserved, no UV invented.','noRig':True,'noModifiers':True,'noParents':True}
(P/'delivery-native-bounds.json').write_text(json.dumps(out,indent=2)+'\n')
