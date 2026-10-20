from pathlib import Path
import bpy,bmesh,numpy as np,json,hashlib,time,math
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
O=Path(__file__).resolve().parent;CACHE=O/'cache';CACHE.mkdir(exist_ok=True);S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();expected='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';assert sha(S)==expected;bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];saved=rig.matrix_world.copy();rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();hair=bpy.data.objects['Ellie ready Daisy CC-BY hair'];origpos=np.array([list(hair.matrix_world@v.co)for v in hair.data.vertices]);uv=hair.data.uv_layers['UVMap'];im=bpy.data.images['daisyhair1.png'];pixels=np.array(im.pixels[:]).reshape(im.size[1],im.size[0],4);IH,IW=pixels.shape[:2];vs=[];fs=[];origtri=[];origuv=[];counts={'leaf':0,'subdivided':0,'opaqueLeaves':0,'transparentLeaves':0,'crossingLeaves':0,'maxDepth':0};start=time.monotonic()
def alpha(u):
 x=(u[0]%1)*IW-.5;y=(u[1]%1)*IH-.5;ix=math.floor(x);iy=math.floor(y);fx=x-ix;fy=y-iy
 return float((pixels[iy%IH,ix%IW,3]*(1-fx)+pixels[iy%IH,(ix+1)%IW,3]*fx)*(1-fy)+(pixels[(iy+1)%IH,ix%IW,3]*(1-fx)+pixels[(iy+1)%IH,(ix+1)%IW,3]*fx)*fy)
def emit(p,u,a):
 poly=[]
 for j in range(3):
  prev=(j-1)%3;inside=a[j]>.5;old=a[prev]>.5
  if inside!=old:
   t=(.5-a[prev])/(a[j]-a[prev]);poly.append(p[prev]+t*(p[j]-p[prev]))
  if inside:poly.append(p[j])
 if len(poly)<3:return
 base=len(vs);vs.extend(poly)
 for j in range(1,len(poly)-1):fs.append((base,base+j,base+j+1))
def rec(p,u,depth=0):
 a=[alpha(x)for x in u];m=[(u[0]+u[1])/2,(u[1]+u[2])/2,(u[2]+u[0])/2];probes=a+[alpha(x)for x in m]+[alpha(u.mean(0))];mixed=min(probes)<=.5<max(probes);uvspan=max(np.linalg.norm((u[j]-u[(j+1)%3])*[IW,IH])for j in range(3));worldedge=max(np.linalg.norm(p[j]-p[(j+1)%3])for j in range(3));# base samples prevent missing large internal holes, boundary refines subpixel/world4mm
 split=depth<6 and ((mixed and(uvspan>2 or worldedge>.003))or(depth<2 and uvspan>12))
 if split:
  counts['subdivided']+=1;pm=[(p[0]+p[1])/2,(p[1]+p[2])/2,(p[2]+p[0])/2]
  for pp,uu in [([p[0],pm[0],pm[2]],[u[0],m[0],m[2]]),([pm[0],p[1],pm[1]],[m[0],u[1],m[1]]),([pm[2],pm[1],p[2]],[m[2],m[1],u[2]]),([pm[0],pm[1],pm[2]],[m[0],m[1],m[2]])]:rec(np.array(pp),np.array(uu),depth+1)
 else:
  counts['leaf']+=1;counts['maxDepth']=max(counts['maxDepth'],depth);counts['crossingLeaves'if mixed else'opaqueLeaves'if max(probes)>.5 else'transparentLeaves']+=1;emit(p,u,a)
for poly in hair.data.polygons:
 ls=list(poly.loop_indices)
 for j in range(1,len(ls)-1):
  tri=[ls[0],ls[j],ls[j+1]];pp=np.array([origpos[hair.data.loops[k].vertex_index]for k in tri]);uu=np.array([list(uv.data[k].uv)for k in tri]);origtri.append(pp);origuv.append(uu);rec(pp,uu)
print('CLIPPED',counts,len(vs),len(fs),'seconds',time.monotonic()-start,flush=True);mesh=bpy.data.meshes.new('Native alpha iso clipped surfaces');mesh.from_pydata(vs,[],fs);mesh.update();obj=bpy.data.objects.new('Daisy alpha-aware volume candidate',mesh);sc.collection.objects.link(obj);bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.to_mesh(mesh);bm.free();bpy.context.view_layer.objects.active=obj
for o in bpy.context.selected_objects:o.select_set(False)
obj.select_set(True);pre={'vertices':len(mesh.vertices),'faces':len(mesh.polygons)};solid=obj.modifiers.new('4mm native inward shell','SOLIDIFY');solid.thickness=.004;solid.offset=-1;solid.use_even_offset=True;bpy.ops.object.modifier_apply(modifier=solid.name);rem=obj.modifiers.new('3mm native volume union','REMESH');rem.mode='VOXEL';rem.voxel_size=.003;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name);bm=bmesh.new();bm.from_mesh(obj.data);boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free();candidate=np.array([list(v.co)for v in obj.data.vertices]);r={'sourceSha256':expected,'originalHairWorldRestBounds':[origpos.min(0).tolist(),origpos.max(0).tolist()],'alphaSampling':'native original bilinearalpha>.5; base2subdivisions forUVspan>12px, boundary recursion maxdepth6, targetUVedge2px/world3mm; approximation not exactcontour','counts':counts,'clippedMesh':pre,'voxelMesh':{'vertices':len(obj.data.vertices),'faces':len(obj.data.polygons),'boundaryEdges':boundary,'nonManifoldEdges':nonmanifold,'bounds':[candidate.min(0).tolist(),candidate.max(0).tolist()]},'noSmoothingOrDecimation':True,'geometrySeconds':time.monotonic()-start};assert boundary==0 and nonmanifold==0;hair.hide_render=True
# Native fixed3D source-triangle RGB correspondence; no per-frame semantic image processing.
source_vertices=[];source_faces=[]
for p in origtri:
 n=len(source_vertices);source_vertices.extend(p);source_faces.append((n,n+1,n+2))
bvh=BVHTree.FromPolygons([Vector(p)for p in source_vertices],source_faces,all_triangles=True);np.savez(CACHE/'source-correspondence.npz',triangles=np.array(origtri),uv=np.array(origuv));np.savez(CACHE/'clipped-surface.npz',vertices=np.array(vs),faces=np.array(fs));obj['candidate_status']='alpha-aware geometry candidate, bake pending';rig.data.pose_position='POSE';rig.matrix_world=saved;sc.frame_set(0);bpy.context.view_layer.update();# bind AFTER coordinates built in rig identity rest
obj.parent=rig;g=obj.vertex_groups.new(name='Head');g.add(list(range(len(obj.data.vertices))),1,'REPLACE');mod=obj.modifiers.new('Native Head','ARMATURE');mod.object=rig
bpy.ops.wm.save_as_mainfile(filepath=str(CACHE/'alpha-volume-geometry.blend'),compress=True);assert sha(S)==expected;(O/'geometry-contract.json').write_text(json.dumps(r,indent=2)+'\n');print('VOLUME_GEOMETRY_READY',r['voxelMesh'],flush=True)
