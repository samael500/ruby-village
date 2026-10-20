"""Kitbash six authored Ellie pony islands with immutable per-part similarity transforms."""
from pathlib import Path
import bpy,bmesh,json,math,hashlib
import numpy as np
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];H=R/'art/ruta-ellie-head-v1';O=H/'loose-locks-pilot';O.mkdir(exist_ok=True)
inv=json.loads((H/'material-adaptation/native-hair-components.json').read_text());entry=next(x for x in inv['objects']if x['object']=='GEO-ellie_hair');locks=[p for p in entry['parts']if p['worldBBox'][0][0]<-.25 and p['worldBBox'][2][1]>1.45];assert len(locks)==6
bpy.ops.wm.open_mainfile(filepath=str(H/'source/ellie-original.blend'),use_scripts=False);src=bpy.data.objects['GEO-ellie_hair'];allids=set(range(len(src.data.vertices)));lockids=set(i for p in locks for i in p['vertexIndices']);parts=[]
for idx,ids in enumerate([sorted(allids-lockids)]+[p['vertexIndices']for p in locks]):
 mesh=src.data.copy();bm=bmesh.new();bm.from_mesh(mesh);bm.verts.ensure_lookup_table();keep=set(ids);bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.index not in keep],context='VERTS');bm.to_mesh(mesh);bm.free();mesh.transform(src.matrix_world);mesh.materials.clear();o=bpy.data.objects.new('Ellie raw loose '+str(idx),mesh);parts.append(o)
lib=O/'native-seven-parts.blend';bpy.data.libraries.write(str(lib),set(parts),fake_user=True,compress=True);print('EXTRACTED_NATIVE7',flush=True)
bpy.ops.wm.open_mainfile(filepath=str(H/'color-handoff/ruta-b-ellie-blue-copper-temporary.blend'),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];mat=bpy.data.objects['Ellie ready hair_cut'].data.materials[0]
for n in ['Ellie ready hair_cut','Ellie ready CC0 Cortu waves']:bpy.data.objects[n].hide_render=True
with bpy.data.libraries.load(str(lib),link=False)as(a,b):b.objects=sorted(a.objects)
parts=sorted(b.objects,key=lambda o:int(o.name.rsplit(' ',1)[1]));fit=json.loads((H/'friendly-pilot/pilot-manifest.json').read_text())['uniformHeadFit'];S=fit['scale'];off=Vector(fit['offset']);pivot=Vector((0,-.001293765,1.012899637));cap=Matrix.Translation(off)@Matrix.Scale(S,4)@Matrix.Translation(pivot)@Matrix.Scale(1.075,4)@Matrix.Translation(-pivot)
placements=[((-.075,.10,1.48),(-.18,.15,.95)),((-.145,.055,1.47),(-.28,.02,.98)),((-.17,-.02,1.43),(-.25,-.05,1.07)),((.075,.10,1.48),(.18,.15,.95)),((.145,.055,1.47),(.28,.02,.98)),((.17,-.02,1.43),(.25,-.05,1.07))];records=[]
for idx,o in enumerate(parts):
 sc.collection.objects.link(o);p=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',p);p=p.reshape((-1,3));sourcehash=hashlib.sha256(p.tobytes()).hexdigest()
 if idx==0:M=cap;definition={'capScaleAboutNativeHead':1.075,'sourceHeadPivot':list(pivot),'headFit':fit}
 else:
  root=Vector(p[p[:,0]>=p[:,0].max()-.02].mean(axis=0));tip=Vector(p[p[:,0]<=p[:,0].min()+.03].mean(axis=0));a,c=map(Vector,placements[idx-1]);old=tip-root;new=c-a;rot=old.rotation_difference(new);scale=new.length/old.length;M=Matrix.Translation(a)@rot.to_matrix().to_4x4()@Matrix.Scale(scale,4)@Matrix.Translation(-root);definition={'sourceRootProxy':list(root),'sourceTipProxy':list(tip),'sourceDefinition':'mean of existing extreme-X terminal vertices; hair attachment proxies, not anatomy','targetRoot':list(a),'targetTip':list(c),'uniformScale':scale,'rotationQuaternion':list(rot)}
 o.name='Ellie ready Loose '+('cap'if idx==0 else'wave '+str(idx));o.data.transform(M);o.data.update();o.data.materials.append(mat)
 for poly in o.data.polygons:poly.use_smooth=True
 o.parent=rig;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4);o.vertex_groups.clear();g=o.vertex_groups.new(name='Head');g.add(list(range(len(o.data.vertices))),1.,'REPLACE');mod=o.modifiers.new('Rigid native Head binding','ARMATURE');mod.object=rig;sub=o.modifiers.new('Native hair surface subdivision','SUBSURF');sub.levels=1;sub.render_levels=2
 records.append({'name':o.name,'baseVertices':len(o.data.vertices),'baseFaces':len(o.data.polygons),'UVLayers':len(o.data.uv_layers),'sourceGeometrySha256':sourcehash,'matrix':[list(row)for row in M],'definition':definition})
print('SEVEN_PARTS_BOUND',flush=True)
root=rig.data.bones['Root'].head_local.copy();root.z=0;whole=sc.camera;face=bpy.data.objects['Ellie native face proof camera'];views=[]
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root);bpy.context.view_layer.update()
 for kind,cam in [('whole',whole),('face',face)]:
  sc.camera=cam;sc.render.filepath=str(O/(name+'-'+kind+'.png'));print('LOOSE_RENDER',name,kind,flush=True);bpy.ops.render.render(write_still=True);views.append(name+'-'+kind+'.png')
sc.camera=whole;rig.matrix_world=Matrix.Translation(-root);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-b-ellie-loose-locks.blend'),compress=True)
def ah(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()
report={'status':'ONE-native-six-authored-lock-kitbash-art-review-pending-NOT-final-Ruta','source':'Blender Studio Ellie CC-BY4.0; upstream original retained in ../source','sourceSha256':hashlib.sha256((H/'source/ellie-original.blend').read_bytes()).hexdigest(),'parts':records,'baseVerticesTotal':sum(x['baseVertices']for x in records),'definition':'Original full hair split along existing disconnected islands:21 scalp/fringe islands plus6 long locks. Each whole part one constant rest similarity matrix, no mirrored geometry, new strands, sculpt or per-frame adjustment. Existing authored topology/UV/material preserved.','actions':{n:ah(bpy.data.actions[n])for n in ['Walk_ProportionProposal','Idle_Neutral_ProportionProposal']},'views':views,'materialProtection':'ASCII Ellie ready prefix: preserve native shaders/normals/UV/alpha. Honor hide_render for rejected hair.','limitations':['one rest kitbash for actual visual review, not accepted Ruta likeness','rigid Head binding; shoulder/wardrobe intersections need actual-motion review','no no-slip/contact claim; actions unchanged by hair assembly']};assert report['baseVerticesTotal']==7364;(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('LOOSE_READY',flush=True)
