"""Kitbash six authored Ellie pony islands with immutable per-part similarity transforms."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
import numpy as np
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];H=R/'art/ruta-ellie-head-v1';O=H/'layered-locks-pilot';O.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(H/'loose-locks-pilot/ruta-b-ellie-loose-locks.blend'),use_scripts=False)
sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];mat=bpy.data.objects['Ellie ready Loose cap'].data.materials[0]
for o in list(sc.objects):
 if o.name.startswith('Ellie ready Loose wave '):bpy.data.objects.remove(o,do_unlink=True)
S=H/'loose-locks-pilot/native-seven-parts.blend'
with bpy.data.libraries.load(str(S),link=False)as(a,b):b.objects=sorted(n for n in a.objects if n!='Ellie raw loose 0')
raw=sorted(b.objects,key=lambda o:int(o.name.rsplit(' ',1)[1]));assert len(raw)==6
records=[]
for i in range(18):
 donor=raw[i%6];o=donor.copy();o.data=donor.data.copy();sc.collection.objects.link(o);o.name='Ellie ready Layered wave '+str(i+1)
 p=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',p);p=p.reshape((-1,3));a=Vector(p[p[:,0]>=p[:,0].max()-.02].mean(axis=0));c=Vector(p[p[:,0]<=p[:,0].min()+.03].mean(axis=0));old=c-a
 layer=i//6;theta=math.radians(-105+42*(i%6)+(-7 if layer==1 else 7 if layer==2 else 0));radius=[.145,.13,.11][layer];root=Vector((math.sin(theta)*radius,math.cos(theta)*.105,1.475+layer*.025));tip=Vector((math.sin(theta)*[.255,.23,.205][layer],math.cos(theta)*[.16,.185,.21][layer],.98+layer*.025+.025*math.cos(theta*2)))
 new=tip-root;u=np.array(old.normalized());thickness=1.45;A=thickness*np.eye(3)+(1-thickness)*np.outer(u,u);T=Matrix(A.tolist()).to_4x4();M=Matrix.Translation(root)@old.rotation_difference(new).to_matrix().to_4x4()@Matrix.Scale(new.length/old.length,4)@T@Matrix.Translation(-a)
 o.data.transform(M);o.data.update();o.data.materials.clear();o.data.materials.append(mat)
 for poly in o.data.polygons:poly.use_smooth=True
 o.parent=rig;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4);o.vertex_groups.clear();g=o.vertex_groups.new(name='Head');g.add(list(range(len(o.data.vertices))),1.,'REPLACE');m=o.modifiers.new('Rigid Head binding','ARMATURE');m.object=rig;sub=o.modifiers.new('Native hair surface subdivision','SUBSURF');sub.levels=2;sub.render_levels=2
 records.append({'name':o.name,'donor':donor.name,'baseVertices':len(o.data.vertices),'baseFaces':len(o.data.polygons),'UVLayers':len(o.data.uv_layers),'sourceRootProxy':list(a),'sourceTipProxy':list(c),'targetRoot':list(root),'targetTip':list(tip),'crossSectionRestScale':thickness,'matrix':[list(row)for row in M]})
for obj in sc.objects:
 if not obj.hide_render:
  obj.hide_viewport=False;obj.hide_set(False)
  for mod in obj.modifiers:
   if mod.type=='SUBSURF':mod.levels=mod.render_levels
   mod.show_viewport=mod.show_render
print('18_NATIVE_LOCKS_BOUND',flush=True)
root=rig.data.bones['Root'].head_local.copy();root.z=0;whole=sc.camera;face=bpy.data.objects['Ellie native face proof camera'];views=[]
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root);bpy.context.view_layer.update()
 for kind,cam in [('whole',whole),('face',face)]:
  sc.camera=cam;sc.render.filepath=str(O/(name+'-'+kind+'.png'));print('LOOSE_RENDER',name,kind,flush=True);bpy.ops.render.render(write_still=True);views.append(name+'-'+kind+'.png')
sc.camera=whole;rig.matrix_world=Matrix.Translation(-root);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-b-ellie-layered-locks.blend'),compress=True)
def ah(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()
report={'status':'ONE-native-18-lock-layered-kitbash-art-review-pending-NOT-final-Ruta','source':'Blender Studio Ellie CC-BY4.0; upstream original retained in ../source','sourceSha256':hashlib.sha256((H/'source/ellie-original.blend').read_bytes()).hexdigest(),'parts':records,'baseVerticesTotal':sum(x['baseVertices']for x in records),'definition':'Original scalp/fringe retained. Six authored native pony lock islands each duplicated into three layers:18whole locks. Fixed per-lock rest affine matrix including1.45cross-section thickness; no new primitive/strand topology, mirroring or per-frame changes. Native UV/material retained.','actions':{n:ah(bpy.data.actions[n])for n in ['Walk_ProportionProposal','Idle_Neutral_ProportionProposal']},'views':views,'materialProtection':'ASCII Ellie ready prefix: preserve native shaders/normals/UV/alpha. Honor hide_render for rejected hair.','limitations':['one rest kitbash for actual visual review, not accepted Ruta likeness','rigid Head binding; shoulder/wardrobe intersections need actual-motion review','no no-slip/contact claim; actions unchanged by hair assembly']};(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('LOOSE_READY',flush=True)
