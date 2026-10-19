from pathlib import Path
import bpy,json,math
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-six-v1'
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/ready-character-adapted-v1/ruta-stock-adapted.blend'));scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.rotation_mode='XYZ';p=rig.data.bones['Root'].head_local.copy();p.z=0
rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-p);rig.data.pose_position='REST';bpy.context.view_layer.update();points=[]
for o in scene.objects:
 if o.type!='MESH' or o.parent!=rig:continue
 e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();points.extend(e.matrix_world@v.co for v in m.vertices);e.to_mesh_clear()
zmin=min(v.z for v in points);zmax=max(v.z for v in points);a=world_to_camera_view(scene,scene.camera,Vector());x=world_to_camera_view(scene,scene.camera,Vector((1,0,0)));z=world_to_camera_view(scene,scene.camera,Vector((0,0,1)));ppm_x=(x.x-a.x)*512;ppm_z=(z.y-a.y)*640
reference={'method':'evaluated REST native world Z bbox including hair/boots, multiplied by measured camera projection of1m vertical Z','worldZBoundsMeters':[zmin,zmax],'worldHeightMeters':zmax-zmin,'nativeHorizontalPixelsPerMeter':ppm_x,'nativeVerticalZPixelsPerMeter':ppm_z,'nativeHeightPx':(zmax-zmin)*abs(ppm_z),'deliveryScale':.5,'deliveryNativeHeightPx':(zmax-zmin)*abs(ppm_z)*.5,'orthographicScaleMeters':scene.camera.data.ortho_scale,'actualViewportWidthMeters':512/ppm_x,'frameCanvasHeightIsNotBodyHeight':True}
rig.data.pose_position='POSE'
cal=json.loads((ROOT/'art/ready-character-walk-v1/heading-contract.json').read_text());origin=world_to_camera_view(scene,scene.camera,Vector());anchor=[origin.x*512,(1-origin.y)*640];rows=[]
for variant,v in cal['variants'].items():
 for name,h in v['directions'].items():
  yaw=h['stockForwardMinusYBlenderYawRadians'];rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-p)
  samples=[]
  for action_name,end in [('Walk',40),('Idle_Neutral',50)]:
   a=bpy.data.actions[action_name];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
   for frame in [0,end/2,end]:
    scene.frame_set(int(frame));bpy.context.view_layer.update();world=rig.matrix_world@rig.pose.bones['Root'].head;screen=world_to_camera_view(scene,scene.camera,world);px=[screen.x*512,(1-screen.y)*640];error=math.hypot(px[0]-anchor[0],px[1]-anchor[1]);assert error<.0001,(variant,name,action_name,frame,error)
    samples.append({'action':action_name,'frame':frame,'actualPosedRootWorld':list(world),'projectedRootPixel':px,'anchorErrorPixels':error})
  forward=rig.matrix_world.to_3x3()@Vector((0,-1,0));screen_angle=math.atan2(-.65*forward.y,forward.x);error=math.atan2(math.sin(screen_angle-h['acceptedScreenAngleRadians']),math.cos(screen_angle-h['acceptedScreenAngleRadians']));assert abs(error)<1e-6
  rows.append({'variant':variant,'direction':name,'yaw':yaw,'forwardReprojectionErrorRadians':error,'samples':samples})
(OUT/'static-origin-checks.json').write_text(json.dumps({'status':'12-headings-native-rest-origin-and-pose-root-projection-verified','nativeRootRestGround':list(p),'commonFootAnchor':anchor,'bodyReference':reference,'worldTransform':'Rz(yaw) @ T(-native Root rest ground)','samples':rows,'maximumAnchorErrorPixels':max(s['anchorErrorPixels']for r in rows for s in r['samples']),'noSourceLocalGeometryWeightsRestOrActionsEdited':True},indent=2)+'\n')
