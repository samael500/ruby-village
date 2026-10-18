"""Fresh actual root path/forward/sole projections for the single-camera proof."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/turn-study';meta=json.loads((OUT/'manifest.json').read_text());result=json.loads((OUT/'raster-path-metadata.json').read_text());source=OUT/'mpfb-native60-turn-technical.blend';before=hashlib.sha256(source.read_bytes()).hexdigest();assert before==result['sourceSha256Before'];bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera;shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();measure.hide_render=True;scene.collection.objects.link(measure)
for mod in measure.modifiers:
 if mod.type=='SUBSURF':mod.show_viewport=False
for name,action in meta['turnActions'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
markers={}
for side,sign in [('L',1),('R',-1)]:
 vs=[v for v in measure.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vs);sole=[v for v in vs if v.co.z<z+.008];front=min(v.co.y for v in sole);back=max(v.co.y for v in sole);markers[side]={k:[v.index for v in sole if(v.co.y<front+.025 if k=='toe'else v.co.y>back-.025)]for k in ['toe','heel']}
def set_frame(value):scene.frame_set(int(value),subframe=value-int(value));bpy.context.view_layer.update()
def cam(root):
 elev=math.asin(.65);center=root+Vector((0,0,.68));camera.data.ortho_scale=1.70;camera.location=center+Vector((-4*math.cos(elev),0,4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
def project(point):
 q=world_to_camera_view(scene,camera,point);return [384*q.x,384*(1-q.y)]
cam(Vector());origin=project(Vector())
for point in result['actualPath']:
 set_frame(point['frame']);pixel=project(rig.matrix_world.translation);point['actualFixedCameraProjectedRootDeltaPixels']=[b-a for a,b in zip(origin,pixel)];point['actualFixedCameraProjectedRootDeltaScenePixels']=[v*136/251 for v in point['actualFixedCameraProjectedRootDeltaPixels']]
for rec in result['renderedFrames']:
 set_frame(rec['frame']);root=rig.matrix_world.translation;cam(root);start=project(root);end=project(root+rig.matrix_world.to_3x3()@Vector((0,-1,0)));forward=[b-a for a,b in zip(start,end)];rec['actualProjectedForwardVectorPixels']=forward;rec['actualScreenHeadingRadians']=math.atan2(forward[1],forward[0]);rec['baseGridHeadingRadians']=-rig.rotation_euler.z;deps=bpy.context.evaluated_depsgraph_get();es=measure.evaluated_get(deps);rec['actualSourceSoleMarkers']={}
 for side in ['L','R']:
  rec['actualSourceSoleMarkers'][side]={}
  for kind,ids in markers[side].items():
   points=[es.matrix_world@es.data.vertices[i].co for i in ids];world=sum(points,Vector())/len(points);rec['actualSourceSoleMarkers'][side][kind]={'centerWorldMeters':list(world),'projectedPixels':project(world),'sourceVertexIndices':ids}
 assert math.dist(start,rec['rootGroundAnchorPixels'])<.001
result['coordinateContract']={'nativeForward':[0,-1,0],'nativePositiveYaw':'left turn, world+Z rotation','baseGridHeadingChangeRadians':-meta['angleRadians'],'baseGridGroundXYFromNativeXY':[[0,-1],[-1,0]],'baseScreenGroundDirectionFromNativeXY':[[0,-1],[-.65,0]],'note':'Coordinate basis mapping is not an image mirror; camera rotations/rig remain proper3D transforms. Other scene calibrations must use their actual camera projection.'};result['actualProjectedRootPathLengthScenePixels']=sum(math.dist(a['actualFixedCameraProjectedRootDeltaScenePixels'],b['actualFixedCameraProjectedRootDeltaScenePixels'])for a,b in zip(result['actualPath'],result['actualPath'][1:]));result['sourceSha256AfterFreshProjection']=hashlib.sha256(source.read_bytes()).hexdigest();assert result['sourceSha256AfterFreshProjection']==before;(OUT/'raster-path-metadata.json').write_text(json.dumps(result,indent=2)+'\n');print('FRESH_TURN_PROJECTIONS12 source unchanged, native+60 maps base-grid-60')
