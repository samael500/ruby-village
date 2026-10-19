"""Bind whole ready native Ellie head to corrected B rig; no gait edits, sculpt or raster manipulation."""
from pathlib import Path
import bpy,json,hashlib,math,os
import numpy as np
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[1];HEADROOT=R/'art/ruta-ellie-head-v1';O=HEADROOT/os.environ.get('ELLIE_PILOT_DIR','.');O.mkdir(exist_ok=True);LIB=HEADROOT/os.environ.get('ELLIE_PARTS_FILE','ellie-native-head-parts.blend');EX=HEADROOT/os.environ.get('ELLIE_EXTRACTION_FILE','extraction.json');B=Path(os.environ['ELLIE_BODY_SOURCE']);C=Path(os.environ['ELLIE_BODY_CONTRACT']);print('STAGE readingbody',str(B),flush=True);contract=json.loads(C.read_text());ex=json.loads(EX.read_text());bpy.ops.wm.open_mainfile(filepath=str(B),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature']
def ah(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()
assert all(n in bpy.data.actions for n in ['Walk_ProportionProposal','Idle_Neutral_ProportionProposal']),'corrected B required; copied actions missing'
hashes={n:ah(bpy.data.actions[n])for n in ['Walk_ProportionProposal','Idle_Neutral_ProportionProposal']}
for n in hashes:bpy.data.actions[n].use_fake_user=True
for t in rig.animation_data.nla_tracks:t.mute=True
# Preserve original B meshes and hide replaced ready stock head/hair only.
for n in ['Adventurer_Head','Ruta CC0 ginger waves']:bpy.data.objects[n].hide_render=True
with bpy.data.libraries.load(str(LIB),link=False)as(src,dst):dst.objects=[n for n in src.objects if n.startswith('Ellie ready ')]
parts=dst.objects;print('STAGE loadedparts',len(parts),flush=True)
for o in parts:sc.collection.objects.link(o)
source_crown=max(v.co.z for o in parts if o.name=='Ellie ready hair_cut'for v in o.data.vertices);source_chin=ex['sourceMarkersWorld']['DEF-Chin'][2];target_chin=contract['restMeshBoundsAfter']['headMesh'][2][0];target_crown=contract['restMeshBoundsAfter']['body'][2][1];s=(target_crown-target_chin)/(source_crown-source_chin);srcpivot=Vector(ex['sourceMarkersWorld']['ORG-Head']);srcpivot.z=source_chin;dstpivot=rig.data.bones['Head'].head_local.copy();dstpivot.z=target_chin;offset=dstpivot-srcpivot*s;records=[]
for o in parts:
 coords=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',coords);coords=coords.reshape((-1,3))*s+np.array(offset);o.data.vertices.foreach_set('co',coords.astype(np.float32).ravel());print('STAGE fit',o.name,len(o.data.vertices),flush=True)
 o.parent=rig;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4);o.vertex_groups.clear();group=o.vertex_groups.new(name='Head');print('STAGE weights',o.name,flush=True);group.add(list(range(len(o.data.vertices))),1.,'REPLACE');print('STAGE weights-done',o.name,flush=True);m=o.modifiers.new('Rigid native Head binding','ARMATURE');m.object=rig;o.hide_render=False
 records.append({'name':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'binding':'Head weight1 native Armature','materials':[m.name for m in o.data.materials if m]})
assert len([o for o in sc.objects if o.type=='ARMATURE'])==1
active=bpy.data.actions['Idle_Neutral_ProportionProposal'];rig.animation_data.action=active;rig.animation_data.action_slot=active.slots[0];sc.frame_set(0);root=rig.data.bones['Root'].head_local.copy();root.z=0
sc.render.engine=os.environ.get('ELLIE_RENDER_ENGINE','BLENDER_EEVEE_NEXT')
if sc.render.engine=='CYCLES':
 sc.cycles.samples=8;sc.cycles.use_denoising=True
sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.render.film_transparent=True;source_camera=sc.camera;views=[]
close_data=source_camera.data.copy();close=bpy.data.objects.new('Ellie native face proof camera',close_data);sc.collection.objects.link(close);close_data.ortho_scale=.78;face_target=Vector((0,-.01,(target_chin+target_crown)/2));close.location=face_target+Vector((0,-8,8*.65/math.sqrt(1-.65**2)));close.rotation_euler=(face_target-close.location).to_track_quat('-Z','Y').to_euler()
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root);bpy.context.view_layer.update();q=world_to_camera_view(sc,source_camera,rig.matrix_world@rig.pose.bones['Root'].head)
 for crop,cam in [('whole',source_camera),('face',close)]:
  sc.camera=cam;sc.render.filepath=str(O/(name+'-'+crop+'.png'));print('STAGE render',name,crop,sc.render.engine,flush=True);bpy.ops.render.render(write_still=True);views.append({'view':name,'proof':crop,'sourceFrame':0,'headExpression':ex.get('appliedNativePoseAssets',[]),'action':active.name,'yaw':yaw,'file':name+'-'+crop+'.png','rootPxWholeCamera':[q.x*512,(1-q.y)*640]})
sc.camera=source_camera;rig.matrix_world=Matrix.Translation(-root);assert all(ah(bpy.data.actions[n])==h for n,h in hashes.items());print('STAGE pack-save',flush=True);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-b-ellie-head-pilot.blend'),compress=True)
report={'status':'internal-ready-native-head-pilot-NOT-approved-Ruta-or-runtime','bodySource':str(B),'bodySourceSha256':hashlib.sha256(B.read_bytes()).hexdigest(),'bodyContractSha256':hashlib.sha256(C.read_bytes()).hexdigest(),'originalEllieSourceSha256':ex['sourceSha256'],'headPartsLibrarySha256':hashlib.sha256(LIB.read_bytes()).hexdigest(),'uniformHeadFit':{'scale':s,'offset':list(offset),'sourceChinBoneZ':source_chin,'sourceHaircutCrownZ':source_crown,'targetOldBHeadMeshLowerProxyZ':target_chin,'targetOldBHairCrownZ':target_crown,'definition':'single3Drest similarity transform preserving native facial/eye/brow/mouth geometry; proxies not anatomical equivalence'},'bodyAndActions':'B body/rest/action curves unchanged; only original stock head/hair render visibility disabled and ready native head parts added','actionHashesUnchangedByHeadBinding':hashes,'parts':records,'views':views,'limitations':['short dark native Ellie haircut not accepted Ruta chestnut waves','static authored source expression, original complete facial rig retained separately','chin proxy and neck/collar fit need visual review','simple B stock garments unchanged; detailed root styling separate','no Walking/contact/no-slip proof from neutral pilot','no per-frame/image deformation or camera compensation']};(O/'pilot-manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('ELLIE_HEAD_BIND_PILOT_READY',len(parts),s,flush=True)
