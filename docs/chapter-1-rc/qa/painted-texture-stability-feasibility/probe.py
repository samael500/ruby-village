"""Read-only cold-open inventory; never save the source or render."""
import bpy,json,hashlib
from pathlib import Path
source=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend')
before=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source),use_scripts=False)
report={'sourceSha256':before,'meshes':[{'name':o.name,'vertices':len(o.data.vertices),'uvs':[u.name for u in o.data.uv_layers],'materials':[m.name for m in o.data.materials if m]} for o in bpy.context.scene.objects if o.type=='MESH' and not o.hide_render], 'images':[{'name':i.name,'size':list(i.size),'packed':bool(i.packed_file)} for i in bpy.data.images if i.type=='IMAGE']}
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
report['sourceUnchanged']=True
Path(__file__).with_name('inventory.json').write_text(json.dumps(report,indent=2)+'\n')
