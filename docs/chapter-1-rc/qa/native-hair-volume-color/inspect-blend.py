from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent;A=Path('/tmp/ruby-combined-loop/art/ruta-native-hair-volume-study-v1/alpha-aware');P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');r={}
def inventory(path,label):
 bpy.ops.wm.open_mainfile(filepath=str(path));rows=[]
 for m in bpy.data.materials:
  if not m.use_nodes:continue
  if not any(n.type=='TEX_IMAGE'and n.image and n.image.name in ['painted-daisy-rgb-v1.png','Fixed native 3D volume RGB bake']for n in m.node_tree.nodes):continue
  rows.append({'material':m.name,'nodes':[{'name':n.name,'type':n.type,'image':n.image.name if n.type=='TEX_IMAGE'and n.image else None,'uv':getattr(n,'uv_map',None),'operation':getattr(n,'operation',None),'inputs':{s.name:list(s.default_value)if hasattr(s.default_value,'__len__')else s.default_value for s in n.inputs if hasattr(s,'default_value')and isinstance(s.default_value,(int,float))or hasattr(s,'default_value')and s.type in ['RGBA','VECTOR']}}for n in m.node_tree.nodes],'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name)for l in m.node_tree.links]})
 images=[]
 for im in bpy.data.images:
  if im.name not in ['painted-daisy-rgb-v1.png','Fixed native 3D volume RGB bake']:continue
  images.append({'name':im.name,'colorspace':im.colorspace_settings.name,'isFloat':im.is_float,'source':im.source,'size':list(im.size),'packedSHA':hashlib.sha256(im.packed_file.data).hexdigest()if im.packed_file else None,'filepath':im.filepath,'alphaMode':im.alpha_mode})
 r[label]={'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'materials':rows,'images':images}
 if label=='volume':
  ob=bpy.data.objects['Daisy alpha-aware volume candidate'];uvs={}
  for name in ['NativeSourceUV','VolumeBakeUV']:
   x=np.empty(len(ob.data.uv_layers[name].data)*2,dtype=np.float32);ob.data.uv_layers[name].data.foreach_get('uv',x);uvs[name]=x.reshape(-1,2)
  # Uniform deterministic face-centroid samples, no source-frame pixel changes.
  indices=np.linspace(0,len(ob.data.polygons)-1,10000,dtype=int);src=[];dst=[]
  for i in indices:
   f=ob.data.polygons[int(i)];src.append(uvs['NativeSourceUV'][list(f.loop_indices)].mean(axis=0));dst.append(uvs['VolumeBakeUV'][list(f.loop_indices)].mean(axis=0))
  np.savez_compressed(O/'uv-centroids.npz',source=np.array(src),target=np.array(dst));r[label]['mesh']={'vertices':len(ob.data.vertices),'faces':len(ob.data.polygons),'uvSamples':len(indices)}
  for im in bpy.data.images:
   if im.name=='painted-daisy-rgb-v1.png'and im.packed_file:(O/'original-painted-daisy-rgb.png').write_bytes(im.packed_file.data)
inventory(P,'parent');inventory(A/'cache/alpha-volume-baked.blend','volume');(O/'material-inventory.json').write_text(json.dumps(r,indent=2)+'\n')
