"""Fixed world camera and checker ground: actual skinned 3D contact diagnostics."""
from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))
stride=json.loads((OUT/'measurements.json').read_text())['strideMeters'];scene=bpy.context.scene;cam=scene.camera
center=Vector((0,-stride*.5,.68));elevation=math.asin(.65);cam.location=center+Vector((-4*math.cos(elevation),0,4*math.sin(elevation)));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.9
bpy.ops.mesh.primitive_plane_add(size=4,location=(0,-stride*.5,0));floor=bpy.context.object;floor.name='Diagnostic fixed world ground 10cm checker'
mat=bpy.data.materials.new('World anchored checker');mat.use_nodes=True;floor.data.materials.append(mat);nodes=mat.node_tree.nodes;links=mat.node_tree.links;geo=nodes.new('ShaderNodeNewGeometry');check=nodes.new('ShaderNodeTexChecker');check.inputs['Scale'].default_value=10;check.inputs['Color1'].default_value=(.38,.4,.36,1);check.inputs['Color2'].default_value=(.46,.48,.43,1);links.new(geo.outputs['Position'],check.inputs['Vector']);links.new(check.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color']);nodes.get('Principled BSDF').inputs['Roughness'].default_value=1
for f in [1,5,9,13,17,21]:
 scene.frame_set(f);scene.render.filepath=str(OUT/'fixed-world'/f'{f:02}.png');bpy.ops.render.render(write_still=True)
