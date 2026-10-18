"""Fresh saved-source root endpoint + world-skin projection readback, no rendering."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/sixview-proof';manifest=json.loads((OUT/'manifest.json').read_text());source=OUT/manifest['source'];before=hashlib.sha256(source.read_bytes()).hexdigest();assert before==manifest['sourceSha256'];bpy.ops.wm.open_mainfile(filepath=str(source))
for name,action in manifest['actionBundle'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera;shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();scene.collection.objects.link(measure);measure.hide_render=True
for m in measure.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels
scene.frame_set(1);bpy.context.view_layer.update();start=rig.matrix_world.translation.copy();scene.frame_set(25);bpy.context.view_layer.update();end=rig.matrix_world.translation.copy();delta=end-start
manifest['actualSourceRootStartNativeMeters']=list(start);manifest['actualSourceRootEndNativeMeters']=list(end);manifest['actualSourceRootDeltaNativeMeters']=list(delta);records=[]
def project(point):
 q=world_to_camera_view(scene,camera,point);return [384*q.x,384*(1-q.y)]
for group,spec in manifest['cameraVariants'].items():
 elev=math.asin(spec['camera']['groundScale'])
 for direction,data in spec['directions'].items():
  azimuth=data['nativeCameraAzimuthRadians']
  for record in data['frames']:
   scene.frame_set(record['frame']);bpy.context.view_layer.update();center=rig.location+Vector((0,0,.68));camera.data.ortho_scale=1.70;camera.location=center+Vector((4*math.cos(elev)*math.cos(azimuth),4*math.cos(elev)*math.sin(azimuth),4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();es=measure.evaluated_get(deps);er=rig.evaluated_get(deps);boot=shoe.evaluated_get(deps);root=rig.matrix_world.translation;freshdelta=[b-a for a,b in zip(project(root),project(root+delta))];markererrors=[]
   for side,markers in record['actualSourceSoleMarkers'].items():
    for kind,marker in markers.items():
     points=[es.matrix_world@es.data.vertices[i].co for i in marker['sourceVertexIndices']];world=sum(points,Vector())/len(points);markererrors.append((world-Vector(marker['centerWorld'])).length)
   rec={'cameraVariant':group,'direction':direction,'frame':record['frame'],'maxSourceSkinWorldReadbackErrorMeters':max(markererrors),'rootProjectionReadbackErrorPixels':math.dist(project(root),record['rootGroundAnchorPixels']),'priorConfiguredDeltaProjectionErrorPixels':math.dist(freshdelta,record['actualProjectedStridePixels']),'actualNativeFootBoneWorld':{side:list(er.matrix_world@er.pose.bones['foot.'+side].head)for side in ['L','R']},'minActualFullRenderLevelBootZ':min((boot.matrix_world@v.co).z for v in boot.data.vertices),'actualMeasuredEndpointDeltaProjectionPixels':freshdelta};records.append(rec);record['actualProjectedStridePixels']=freshdelta;record['actualProjectedStrideScenePixels']=[v*136/251 for v in freshdelta];record['actualProjectedAngleErrorRadians']=math.atan2(math.sin(math.atan2(freshdelta[1],freshdelta[0])-data['screenAngleRadians']),math.cos(math.atan2(freshdelta[1],freshdelta[0])-data['screenAngleRadians']))
assert max(r['maxSourceSkinWorldReadbackErrorMeters']for r in records)<1e-6
assert max(r['rootProjectionReadbackErrorPixels']for r in records)<.001
assert max(r['priorConfiguredDeltaProjectionErrorPixels']for r in records)<.001
check={'status':'FRESH AUTHOR SOURCE READBACK; independent proof review pending','rootDeltaMethod':'Actual saved source actions frame25 rig world translation minus frame1; project measured vector through each actual camera','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(source.read_bytes()).hexdigest(),'actualNativeRootDeltaMeters':list(delta),'records':records};assert check['sourceSha256Before']==check['sourceSha256After'];(OUT/'fresh-source-check.json').write_text(json.dumps(check,indent=2)+'\n');(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('FRESH_CAMERA_CHECK',len(records),'source unchanged, measured native root delta',list(delta))
