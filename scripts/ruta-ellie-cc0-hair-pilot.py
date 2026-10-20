"""One global native ready CC0 wave-hair rest fit; original alpha/UV material retained."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[1];H=R/'art/ruta-ellie-head-v1';O=H/'cc0-wave-hair-pilot';O.mkdir(exist_ok=True);CACHE=R/'art/ready-character-adapted-v1/source/ginger-native-part.blend';B=H/'material-adaptation/ruta-b-ellie-native-color.blend';bpy.ops.wm.open_mainfile(filepath=str(B),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];contract=json.loads((H/'source/body-b-corrected-contract.json').read_text())
# Correct native haircut color parameter directly; no geometry/texture changes. It stays hidden in this long-hair study.
m=bpy.data.materials['ellie.hair_mesh'];node=m.node_tree.nodes['Group.009'];socket=node.inputs['Base Color'];original_link=[{'from':l.from_node.name+':'+l.from_socket.name,'to':l.to_socket.identifier}for l in socket.links]
for l in list(socket.links):m.node_tree.links.remove(l)
socket.default_value=(.27,.075,.018,1)
for o in sc.objects:
 if o.name=='Ellie ready hair_cut':o.hide_render=True
with bpy.data.libraries.load(str(CACHE),link=False)as(src,dst):dst.objects=[n for n in src.objects if '.cortu_strawberry_cloud_hair'in n]
hair=dst.objects[0];sc.collection.objects.link(hair);hair.name='Ellie ready CC0 Cortu waves';source_coords=[tuple(v.co)for v in hair.data.vertices];source_anchor=Vector((.026,-.010,1.4145387411117554));target=rig.data.bones['Head'].head_local.copy();target.y-=.025;target.z=contract['restMeshBoundsAfter']['body'][2][1];scales=Vector((1.55,1.55,1.90));T=Matrix.Translation(target)@Matrix.Diagonal((*scales,1))@Matrix.Translation(-source_anchor);hair.data.transform(T)
for p in hair.data.polygons:p.use_smooth=True
hair.parent=rig;hair.matrix_parent_inverse=Matrix.Identity(4);hair.matrix_basis=Matrix.Identity(4);hair.vertex_groups.clear();g=hair.vertex_groups.new(name='Head');g.add(list(range(len(hair.data.vertices))),1.,'REPLACE')
for m in list(hair.modifiers):hair.modifiers.remove(m)
a=hair.modifiers.new('Rigid native Head binding','ARMATURE');a.object=rig;hair.hide_render=False;alpha=[]
for m in hair.data.materials:
 if hasattr(m,'surface_render_method'):m.surface_render_method='DITHERED'
 for n in m.node_tree.nodes:
  if n.type=='BSDF_PRINCIPLED':alpha.extend([{'material':m.name,'from':l.from_node.name+':'+l.from_socket.name,'to':'Principled Alpha'}for l in n.inputs['Alpha'].links])
assert alpha,'native hair alpha link must survive'
root=rig.data.bones['Root'].head_local.copy();root.z=0;bodycam=sc.camera;facecam=bpy.data.objects['Ellie native face proof camera'];views=[]
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root);bpy.context.view_layer.update()
 for kind,cam in [('whole',bodycam),('face',facecam)]:
  sc.camera=cam;sc.render.filepath=str(O/(name+'-'+kind+'.png'));print('CC0_HAIR_RENDER',name,kind,flush=True);bpy.ops.render.render(write_still=True);views.append(name+'-'+kind+'.png')
sc.camera=bodycam;rig.matrix_world=Matrix.Translation(-root);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-b-ellie-cc0-waves.blend'),compress=True)
report={'status':'ONE-native-CC0-hair-restfit-study-not-accepted-Ruta','hairObjectName':hair.name,'rootMaterialProtection':'ASCII prefix Ellie ready ; preserve all native hair alpha/UV/normals/shader','rawHairSource':str(CACHE.relative_to(R)),'rawHairSha256':hashlib.sha256(CACHE.read_bytes()).hexdigest(),'license':'Cortu Johnstone strawberry_cloud CC0, official hair01 table and author mhclo retained in ready-character-adapted-v1/source; stale generic OBJ AGPL header documented in inherited provenance','sourceVertices':len(source_coords),'sourceGeometrySha256':hashlib.sha256(repr(source_coords).encode()).hexdigest(),'restFit':{'sourceAnchor':list(source_anchor),'targetAnchor':list(target),'scaleXYZ':list(scales),'matrixRows':[list(r)for r in T],'definition':'one global3Drest affine fit; no old lower extension, no per-strand or per-frame changes'},'nativeAlphaLinks':alpha,'nativeUVLayers':[u.name for u in hair.data.uv_layers],'existingCutHairMaterialParameterFix':{'socket':'ellie.hair_mesh / Group.009 SH-Hair Base Color','oldLink':original_link,'newNativeBaseColor':[.27,.075,.018,1],'note':'previous palette selection looked pale; corrected direct native author parameter, haircut hidden in this study'},'views':views,'limitations':['479vertex ready card mesh may show flat cards/triangular silhouette; inspect actual two views before selecting','rest X/Y1.55 Z1.90 may distort source waves; no resemblance/fit/no-slip PASS claimed','body/style and gait curves unchanged by this hair rest fit','no procedural cap or generated/new sculpt hair']};(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('CC0_HAIR_ONE_FIT_READY',flush=True)
