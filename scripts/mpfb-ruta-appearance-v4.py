"""Native MPFB face/eye and hair sculpt study; no attached cartoon eyeball replacement."""
from pathlib import Path
import bpy,math,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
exec((ROOT/'scripts/mpfb-ruta-appearance-v2.py').read_text().split('# Relax arms')[0],globals())
OUT=ROOT/'art/characters-mpfb-v1/appearance-v4';OUT.mkdir(parents=True,exist_ok=True)
for o in list(bpy.data.objects):
 if o.name.startswith('Ruta chestnut wavy lock')or o.name.startswith('Cargo pocket'):bpy.data.objects.remove(o,do_unlink=True)
def face_sculpt(co):
 x,y,z=co;sign=1 if x>=0 else -1
 if y<-.06 and 1.17<z<1.31:
  dx=abs(x)-.0397;dz=z-1.2313;w=max(0,1-(dx/.060)**2-(dz/.065)**2);x=sign*(.0397+dx*(1+.65*w));z=1.2313+dz*(1+.65*w)
 if y<-.105 and 1.13<z<1.19 and abs(x)<.06:
  w=max(0,1-((z-1.165)/.032)**2);z+=.014*min(1,abs(x)/.032)*w
 return (x,y,z)
# Same continuous 3D sculpt is applied to head target stack, existing fitted eyeballs and brows.
for key in human.data.shape_keys.key_blocks:
 for v in key.data:v.co=face_sculpt(v.co)
for o in [eyes]+[o for o in bpy.data.objects if 'eyebrow' in o.name]:
 if o:
  for v in o.data.vertices:v.co=face_sculpt(v.co)
# Long fitted hair cards acquire coherent spatial waves and length; original UV/alpha stays intact.
for v in hair.data.vertices:
 x,y,z=v.co
 if y>-.055 or abs(x)>.11:
  t=min(1,max(0,(1.25-z)/.22));v.co.z-=.23*t;v.co.x=x*(1+.25*t)+.020*math.sin(t*math.pi*3+x*30)*t;v.co.y+=.055*t
for m in hair.data.materials:
 if m and m.use_nodes:
  n=m.node_tree.nodes.get('diffuseIntensity')
  if n:n.inputs[0].default_value=1;n.inputs[2].default_value=(1.,.62,.25,1)
for v in vest.data.vertices:v.co.x*=1.20;v.co.y*=1.75
# Tuck lower shirt into trousers; preserve pants and limbs as actual original garment geometry.
for v in clothes.data.vertices:
 if .63<v.co.z<.74:
  w=max(0,1-abs(v.co.z-.68)/.06);v.co.x*=1-.10*w;v.co.y*=1-.20*w
c=clothes.modifiers.new('Soft cloth polish','CORRECTIVE_SMOOTH');c.factor=.7;c.iterations=12
# Relaxed upperarms, genuine rig. No walk yet.
for side,angle in [('L',-.62),('R',.62)]:rig.pose.bones['upperarm01.'+side].rotation_euler.z=angle
# Existing single sling must sit outside the outer fitted waistcoat.
strap=bpy.data.objects.get('ONE diagonal satchel strap')
if strap:
 for v in strap.data.vertices:
  if v.co.z<.99:v.co.y-=.055
# Warm skin and cloth lighting study, not a claimed likeness pass.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=800;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.22,.22,.22);scene.view_settings.view_transform='AgX'
def look(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-2.8,-5,2.2));camera=bpy.context.object;look(camera,(0,0,.74));camera.data.type='ORTHO';camera.data.ortho_scale=1.73;scene.camera=camera
for loc,power,size in [((-3,-4,5),400,4),((3,-2,3),130,3),((1,3,4),250,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;look(o,(0,0,.7))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-appearance-v4.blend'));scene.render.filepath=str(OUT/'ruta-e-pilot.png');bpy.ops.render.render(write_still=True)
(OUT/'settings.json').write_text(json.dumps({'status':'native-3D-appearance-study-not-approved','productionEnabled':False,'meshBasis':'MPFB2.0.18 child plus native3Dsculpt','eyes':'original fitted meshes plus identical continuous local face sculpt','hair':'original alpha/UV preserved, actual mesh length and spatial waves authored','strapCount':1,'animation':'not-authored'},indent=2)+'\n')
