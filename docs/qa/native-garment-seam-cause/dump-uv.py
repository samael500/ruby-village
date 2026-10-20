from pathlib import Path
import bpy,json,hashlib
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-garment-paint/art/ruta-native-garment-paint-pilot-v1/ruta-painted-garment-pilot.blend');bpy.ops.wm.open_mainfile(filepath=str(S));a=[]
for name in ['Ruta stock long trousers','Adventurer_Feet']:
 ob=bpy.data.objects[name];uv=ob.data.uv_layers['RutaPaint']
 a.append({'object':name,'faces':[{'material':ob.material_slots[f.material_index].material.name,'uv':[list(uv.data[j].uv)for j in f.loop_indices]}for f in ob.data.polygons]})
images=[{'name':im.name,'packedSha256':hashlib.sha256(im.packed_file.data).hexdigest(),'externalSha256':hashlib.sha256(Path(im.filepath).read_bytes()).hexdigest(),'alphaUsedInNodes':[n.name for m in bpy.data.materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE'and n.image==im and n.outputs['Alpha'].is_linked]}for im in bpy.data.images if im.packed_file and im.name.startswith('painted-')and'garment'in im.name or im.packed_file and im.name.startswith('painted-trousers')]
(O/'actual-uv.json').write_text(json.dumps({'objects':a,'packedImages':images}))
