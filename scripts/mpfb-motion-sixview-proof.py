"""24-render genuine 3D camera proof after independent transition GO67450e0.

Two walking poses in each of six directions for BOTH accepted camera groups.
No full-cycle export, runtime activation, mirroring, or appearance acceptance.
"""
from pathlib import Path
import bpy,math,json,os,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
if os.environ.get('RUBY_MPFB_SIXVIEW_REVIEW_GO')!='1':raise RuntimeError('First E start/stop author + independent review GO required')
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/sixview-proof';OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend';transition=json.loads((source.parent/'manifest.json').read_text());source_hash=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source))
for object_name,action_name in transition['sourceActions'].items():bpy.data.objects[object_name].animation_data.action=bpy.data.actions[action_name]
scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera;shoe=bpy.data.objects['Ruta.shoes01']
scene.frame_set(1);bpy.context.view_layer.update();root_start=rig.matrix_world.translation.copy();scene.frame_set(25);bpy.context.view_layer.update();root_end=rig.matrix_world.translation.copy();measured_root_delta=root_end-root_start;assert abs(measured_root_delta.length-.5687545572916666)<1e-7
# A hidden measurement clone retains source sole IDs; visible boots stay render-level subdivided.
measure=shoe.copy();measure.data=shoe.data.copy();measure.name='PROOF MEASUREMENT ONLY source sole';scene.collection.objects.link(measure);measure.hide_render=True
for m in measure.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
markers={}
for side,sign in [('L',1),('R',-1)]:
 vertices=[v for v in measure.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vertices);sole=[v for v in vertices if v.co.z<z+.008];front=min(v.co.y for v in sole);back=max(v.co.y for v in sole)
 markers[side]={kind:[v.index for v in sole if(v.co.y<front+.025 if kind=='toe'else v.co.y>back-.025)]for kind in ['toe','heel']}
legacy_path=ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json';scene_path=ROOT/'src/scene-v8.json';legacy=json.loads(legacy_path.read_text());accepted=json.loads(scene_path.read_text());camera.data.ortho_scale=1.70
scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.cycles.samples=8;scene.cycles.use_denoising=True
manifest={'status':'TECHNICAL 24-frame camera proof ONLY; appearance rejected; no game activation','independentTransitionGo':'67450e0','source':'../transitions/mpfb-start-stop-technical.blend','sourceCommit':'35cddba','sourceCycleCommit':'5ca361b','sourceSha256':source_hash,'actualSourceRootDeltaNativeMeters':list(measured_root_delta),'actualSourceRootStartNativeMeters':list(root_start),'actualSourceRootEndNativeMeters':list(root_end),'actionBundle':transition['sourceActions'],'frameSize':[384,384],'orthoScaleMeters':1.70,'nativeHeightReferencePx':251,'displayHeightReferencePx':136,'physicalStrideMeters':.5687545572916666,'cycleMs':720,'renderedPhases':[0,.5],'renderedFrames':[1,13],'savedWalkInterpolation':'LINEAR at30ms; no exact C1 claim','arbitraryRouteAdapter':'PENDING; fixed clips/queued stop do not solve arbitrary route length; no root retiming, stride scaling or endpoint slide','calibrationReferences':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [legacy_path,scene_path]},'cameraVariants':{}}
def project(p):
 q=world_to_camera_view(scene,camera,p);return [384*q.x,384*(1-q.y)]
for group,spec in legacy['cameraVariants'].items():
 angle=spec['camera']['angle'];ground=spec['camera']['groundScale'];elev=math.asin(ground);scenes=[name for name,data in accepted.items()if abs(data['camera']['angle']-angle)<1e-12 and abs(data['camera']['groundScale']-ground)<1e-12];assert scenes
 result={'camera':spec['camera'],'acceptedSceneNames':scenes,'label':'base'if group=='base'else'tilted','directions':{}}
 for direction,data in spec['directions'].items():
  alpha=data['screenAngleRadians'];orbit=math.atan2(math.sin(alpha)/ground,math.cos(alpha));azimuth=-math.pi+orbit;records=[]
  for frame in [1,13]:
   scene.frame_set(frame);bpy.context.view_layer.update();center=rig.location+Vector((0,0,.68));camera.location=center+Vector((4*math.cos(elev)*math.cos(azimuth),4*math.cos(elev)*math.sin(azimuth),4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);es=measure.evaluated_get(deps)
   root=rig.matrix_world.translation;rec={'frame':frame,'phase':(frame-1)/24,'rigOriginWorld':list(root),'rootGroundAnchorPixels':project(root),'actualWorldFootBoneProjectionPixels':{side:project(er.matrix_world@er.pose.bones['foot.'+side].head)for side in ['L','R']},'actualSourceSoleMarkers':{}}
   for side in ['L','R']:
    rec['actualSourceSoleMarkers'][side]={}
    for kind,ids in markers[side].items():
     points=[es.matrix_world@es.data.vertices[i].co for i in ids];centerpoint=sum(points,Vector())/len(points);rec['actualSourceSoleMarkers'][side][kind]={'centerWorld':list(centerpoint),'projectedPixels':project(centerpoint),'minZ':min(p.z for p in points),'sourceVertexIndices':ids}
   # Direct forward projection in the actual camera, not a copied legacy stride.
   start=project(root);end=project(root+measured_root_delta);delta=[b-a for a,b in zip(start,end)];observed=math.atan2(delta[1],delta[0]);error=math.atan2(math.sin(observed-alpha),math.cos(observed-alpha));assert abs(error)<1e-5,(group,direction,error)
   rec['actualProjectedStridePixels']=delta;rec['actualProjectedStrideScenePixels']=[v*136/251 for v in delta];rec['actualProjectedAngleErrorRadians']=error;records.append(rec);scene.render.filepath=str(OUT/group/direction/f'{frame:02}.png');bpy.ops.render.render(write_still=True)
  result['directions'][direction]={'screenAngleRadians':alpha,'actorWorldHeadingRadians':orbit-angle,'nativeCameraAzimuthRadians':azimuth,'mirror':False,'frames':records}
 manifest['cameraVariants'][group]=result
manifest['sourceSha256After']=hashlib.sha256(source.read_bytes()).hexdigest();assert manifest['sourceSha256After']==source_hash
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('PROOF_COMPLETE actual24PNG, source unchanged, base+tilted, no full export')
