from pathlib import Path
import bpy,numpy as np,json,hashlib
from mathutils import Matrix
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(S)=='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();hair=bpy.data.objects['Ellie ready Daisy CC-BY hair'];mat=hair.material_slots[0].material;im=next(n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE'and n.image and n.image.name=='daisyhair1.png');px=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);uv=hair.data.uv_layers['UVMap'];samples=[]
# Barycentric face interior samples include actual opaque texture coverage, not merely transparent vertices.
for p in hair.data.polygons:
 loops=list(p.loop_indices)
 for j in range(1,len(loops)-1):
  tri=[loops[0],loops[j],loops[j+1]];vs=np.array([list(hair.matrix_world@hair.data.vertices[hair.data.loops[k].vertex_index].co)for k in tri]);us=np.array([list(uv.data[k].uv)for k in tri])
  for a in range(7):
   for b in range(7-a):
    w=np.array([a/6,b/6,1-(a+b)/6]);q=w@us;alpha=px[min(int(q[1]*im.size[1]),im.size[1]-1)%im.size[1],min(int(q[0]*im.size[0]),im.size[0]-1)%im.size[0],3]
    if alpha>.5:samples.append((float((w@vs)[2]),p.index,(w@vs).tolist(),q.tolist(),float(alpha)))
samples.sort(reverse=True);h=bpy.data.objects['Ellie ready head'];ids={i for p in h.data.polygons if h.material_slots[p.material_index].material.name=='Ellie copper scalp root material diagnostic'for i in p.vertices};top=max((h.matrix_world@h.data.vertices[i].co).z for i in ids);r={'sourceSha256':sha(S),'definition':'REST native-alpha>.5 barycentric6-subdivision triangle samples; approximate surface sampling, not exact contour','opaqueSampleCount':len(samples),'scalpTopZ':top,'highestOpaqueSamples':samples[:12],'highestOpaqueMinusScalpTopMeters':samples[0][0]-top};(O/'opaque-crown.json').write_text(json.dumps(r,indent=2)+'\n');print('OPAQUE TOP GAP',r['highestOpaqueMinusScalpTopMeters'])
