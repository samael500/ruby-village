"""Fixed-camera whole-canvas technical E24 render. Stock appearance, NOT final art."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Matrix
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent/'e24';O.mkdir(exist_ok=True);P=R/'art/ruta-native-proportions-study-v2/b-neutral/ruta-proportion-proposal.blend';h=hashlib.sha256(P.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(P));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];a=bpy.data.actions['Walk_ProportionProposal'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
for t in rig.animation_data.nla_tracks:t.mute=True
p=rig.data.bones['Root'].head_local.copy();p.z=0;rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-p);sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_percentage=50;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True;rows=[]
for i in range(24):
 frame=40*i/24;sc.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();q=world_to_camera_view(sc,sc.camera,rig.matrix_world@rig.pose.bones['Root'].head);sc.render.filepath=str(O/f'phase-{i:02}.png');bpy.ops.render.render(write_still=True);rows.append({'index':i,'frame':frame,'rootPx':[q.x*256,(1-q.y)*320],'cameraMatrixWorld':[list(r)for r in sc.camera.matrix_world],'orthoScale':sc.camera.data.ortho_scale,'rgbaSha256':hashlib.sha256(Path(sc.render.filepath).read_bytes()).hexdigest()})
assert hashlib.sha256(P.read_bytes()).hexdigest()==h;(O/'render.json').write_text(json.dumps({'sourceCommit':'e6ab193','sourceSha256':h,'action':'Walk_ProportionProposal','frameCount':24,'frameSampling':'0..40 excluded repeated endpoint; frame=40*i/24','cycleMs':40/24*1000,'imageSize':[256,320],'uniformCameraResolutionPercentage':50,'perFrameCropOrScale':False,'sourceWrite':False,'scope':'Technical stock B native retarget proof; NOT Ruta art acceptance, gameplay or no-slip certificate','frames':rows},indent=2)+'\n')
