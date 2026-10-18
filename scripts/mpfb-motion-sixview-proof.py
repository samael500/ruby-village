"""Gated 12-render genuine 3D proof. Run only after transition pilot review GO."""
from pathlib import Path
import bpy,math,json,os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
if os.environ.get('RUBY_MPFB_SIXVIEW_REVIEW_GO')!='1':raise RuntimeError('First E start/stop author + independent review GO required')
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/sixview-proof';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/characters-mpfb-v1/motion/pilot/mpfb-walk-technical.blend'))
scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera
legacy=json.loads((ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json').read_text());spec=legacy['cameraVariants']['base'];ground=spec['camera']['groundScale'];elev=math.asin(ground);camera.data.ortho_scale=1.70
scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.cycles.samples=8;scene.cycles.use_denoising=True
manifest={'status':'TECHNICAL 12 actual frame camera proof; appearance rejected; no game activation','source':'../pilot/mpfb-walk-technical.blend','sourceCycleCommit':'5ca361b','frameSize':[384,384],'orthoScaleMeters':1.70,'nativeHeightReferencePx':251,'displayHeightReferencePx':136,'groundScale':ground,'directions':{}}
def project(p):
 q=world_to_camera_view(scene,camera,p);return [384*q.x,384*(1-q.y)]
for direction,data in spec['directions'].items():
 alpha=data['screenAngleRadians'];azimuth=-math.pi+math.atan2(math.sin(alpha)/ground,math.cos(alpha));records=[]
 for frame in range(1,25):
  scene.frame_set(frame);bpy.context.view_layer.update();center=rig.location+Vector((0,0,.68));camera.location=center+Vector((4*math.cos(elev)*math.cos(azimuth),4*math.cos(elev)*math.sin(azimuth),4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update()
  rec={'frame':frame,'rigOriginWorld':list(rig.matrix_world.translation),'rootGroundAnchorPixels':project(rig.matrix_world.translation),'actualWorldFootBoneProjectionPixels':{side:project(rig.matrix_world@rig.pose.bones['foot.'+side].head)for side in ['L','R']}}
  records.append(rec)
  if frame in [1,13]:scene.render.filepath=str(OUT/direction/f'{frame:02}.png');bpy.ops.render.render(write_still=True)
 # Native forward travel projection, with the current fixed camera orientation.
 a=Vector(rig.matrix_world.translation);b=a+Vector((0,-.5687545572916666,0));pa=project(a);pb=project(b)
 manifest['directions'][direction]={'screenAngleRadians':alpha,'cameraAzimuthRadians':azimuth,'actualProjectedStridePixels':[pb[0]-pa[0],pb[1]-pa[1]],'frames':records,'renderedFrames':[1,13],'mirror':False}
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
