"""Fresh source/action/marker readback for every full-export receipt, no renders."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/full-cycle-technical';manifest=json.loads((OUT/'manifest.json').read_text());source=ROOT/manifest['sourceBlend'];before=hashlib.sha256(source.read_bytes()).hexdigest();assert before==manifest['sourceSha256'];bpy.ops.wm.open_mainfile(filepath=str(source))
for name,action in manifest['sourceActionBundle'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera;shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();measure.hide_render=True;scene.collection.objects.link(measure)
for mod in measure.modifiers:
 if mod.type=='SUBSURF':mod.show_viewport=False
for mod in shoe.modifiers:
 if mod.type=='SUBSURF':mod.levels=mod.render_levels
scene.frame_set(1);bpy.context.view_layer.update();start=rig.matrix_world.translation.copy();initial={b.name:b.matrix.copy()for b in rig.pose.bones};scene.frame_set(25);bpy.context.view_layer.update();delta=rig.matrix_world.translation-start;looperror=max(abs(rig.pose.bones[n].matrix[i][j]-matrix[i][j])for n,matrix in initial.items()for i in range(4)for j in range(4));records=[]
def project(point):
 q=world_to_camera_view(scene,camera,point);return [384*q.x,384*(1-q.y)]
for group,variant in manifest['cameraVariants'].items():
 elev=math.asin(variant['camera']['groundScale'])
 for direction,entry in variant['directions'].items():
  receipt=json.loads((OUT/entry['receipt']).read_text());azimuth=receipt['nativeCameraAzimuthRadians']
  for frame in receipt['frames']:
   scene.frame_set(frame['frame']);bpy.context.view_layer.update();center=rig.location+Vector((0,0,.68));camera.data.ortho_scale=1.70;camera.location=center+Vector((4*math.cos(elev)*math.cos(azimuth),4*math.cos(elev)*math.sin(azimuth),4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();es=measure.evaluated_get(deps);er=rig.evaluated_get(deps);errors=[];boneerrors=[]
   for side,foot in frame['feet'].items():
    boneerrors.append((er.matrix_world@er.pose.bones['foot.'+side].head-Vector(foot['actualBoneWorldMeters'])).length)
    for kind,marker in foot['sourceSole'].items():
     points=[es.matrix_world@es.data.vertices[i].co for i in marker['sourceVertexIndices']];centerpoint=sum(points,Vector())/len(points);errors.append((centerpoint-Vector(marker['centerWorldMeters'])).length)
   records.append({'cameraVariant':group,'direction':direction,'frame':frame['frame'],'actualSourceSkinReadbackMaxErrorMeters':max(errors),'actualBoneReadbackMaxErrorMeters':max(boneerrors),'actualRootReadbackErrorMeters':(rig.matrix_world.translation-Vector(frame['rootNativeWorldMeters'])).length,'rootProjectionReadbackErrorPixels':math.dist(project(rig.matrix_world.translation),frame['rootGroundAnchorPixels']),'cameraRotationDeterminant':camera.rotation_euler.to_matrix().determinant(),'rigWorldDeterminant':rig.matrix_world.determinant(),'orthoScaleMeters':camera.data.ortho_scale})
summary={'recordCount':len(records),'maxActualSourceSkinReadbackErrorMeters':max(r['actualSourceSkinReadbackMaxErrorMeters']for r in records),'maxActualBoneReadbackErrorMeters':max(r['actualBoneReadbackMaxErrorMeters']for r in records),'maxActualRootReadbackErrorMeters':max(r['actualRootReadbackErrorMeters']for r in records),'maxRootProjectionReadbackErrorPixels':max(r['rootProjectionReadbackErrorPixels']for r in records),'nativeRootDeltaMeters':list(delta),'nativeRootRelativeBoneLoopMaxElementError':looperror,'minimumCameraRotationDeterminant':min(r['cameraRotationDeterminant']for r in records)}
assert len(records)==288 and summary['maxActualSourceSkinReadbackErrorMeters']<1e-6 and summary['maxActualBoneReadbackErrorMeters']<1e-6 and summary['maxRootProjectionReadbackErrorPixels']<.001 and looperror<1e-5
result={'status':'FRESH AUTHOR SAVED-SOURCE READBACK; INDEPENDENT FULL EXPORT REVIEW PENDING','method':'Reopen immutable packed source, activate named three-object actions, evaluate every actual exported frame; stable source skin indices and actual evaluated foot bones in world coordinates; proper camera rotations and constant ortho scale','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(source.read_bytes()).hexdigest(),'summary':summary,'records':records};assert result['sourceSha256Before']==result['sourceSha256After'];(OUT/'fresh-source-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
