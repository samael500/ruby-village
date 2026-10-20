from pathlib import Path
import bpy,numpy as np,json,hashlib
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(S)=='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';bpy.ops.wm.open_mainfile(filepath=str(S));h=bpy.data.objects['Ellie ready Daisy CC-BY hair'];im=bpy.data.images['daisyhair1.png'];px=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);uv=h.data.uv_layers['UVMap'];total=opaque=0.;triangles=count=0
for p in h.data.polygons:
 ls=list(p.loop_indices)
 for j in range(1,len(ls)-1):
  tr=[ls[0],ls[j],ls[j+1]];v=np.array([list(h.data.vertices[h.data.loops[k].vertex_index].co)for k in tr]);u=np.array([list(uv.data[k].uv)for k in tr]);area=np.linalg.norm(np.cross(v[1]-v[0],v[2]-v[0]))/2;flags=[]
  # Equal-area stratified barycentric samples via square-root mapping.
  for a in range(8):
   for b in range(8):
    r=np.sqrt((a+.5)/8);s=(b+.5)/8;w=np.array([1-r,r*(1-s),r*s]);q=w@u;x=int(q[0]*im.size[0])%im.size[0];y=int(q[1]*im.size[1])%im.size[1];flags.append(px[y,x,3]>.5)
  total+=area;opaque+=area*np.mean(flags);count+=len(flags);triangles+=1
r={'sourceSha256':sha(S),'nativeAlphaImage':'daisyhair1.png','threshold':.5,'originalMeshTriangleCount':triangles,'sampleCount':count,'method':'64equal-area-stratified samples pertriangle; approximate area coverage, not exact isocontour trim','opaqueSurfaceAreaFraction':opaque/total,'transparentSurfaceAreaFraction':1-opaque/total,'rawCardUnionFillsTransparentRegions':True};(O/'alpha-area.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
