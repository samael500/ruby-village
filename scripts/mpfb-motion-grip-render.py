"""Actual close views of the same rigged hand and the existing ONE strap."""
from pathlib import Path
import bpy
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pilot/grip-close';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT.parent/'mpfb-walk-technical.blend'));scene=bpy.context.scene;cam=scene.camera;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];scene.render.resolution_x=600;scene.render.resolution_y=600;cam.data.ortho_scale=.55
for frame in [1,13]:
 scene.frame_set(frame);target=Vector((0,-.08,.88))+rig.location
 for view,offset in [('front',Vector((0,-3,.72))),('three-quarter',Vector((-1.5,-3,.72)))]:
  cam.location=target+offset;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/f'{view}-{frame:02}.png');bpy.ops.render.render(write_still=True)
