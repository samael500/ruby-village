"""Appearance v3 whole 3D authoring candidate. Genuine MPFB basis, no raster pose generation."""
from pathlib import Path
import bpy,math,json
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
# Reuse preserved model recipe up to pose/render, leaving v1/v2 evidence intact.
exec((ROOT/'scripts/mpfb-ruta-appearance-v2.py').read_text().split('# Relax arms')[0],globals())
OUT=ROOT/'art/characters-mpfb-v1/appearance-v3';OUT.mkdir(parents=True,exist_ok=True)
for o in list(bpy.data.objects):
 if o.name.startswith('Ruta chestnut wavy lock')or o.name.startswith('Cargo pocket'):bpy.data.objects.remove(o,do_unlink=True)
# Skin mesh is still full MPFB topology; custom features are real 3D surfaces weighted to its head.
def weighted(o,bone):
 bpy.ops.object.select_all(action='DESELECT');bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.context.view_layer.update()
 if o.type!='MESH':bpy.ops.object.convert(target='MESH');o=bpy.context.object
 bpy.context.view_layer.update();matrix=o.matrix_world.copy()
 for v in o.data.vertices:v.co=matrix@v.co
 o.matrix_world=Matrix.Identity(4);o.parent=rig;g=o.vertex_groups.new(name=bone);g.add(list(range(len(o.data.vertices))),1,'REPLACE');a=o.modifiers.new('Semantic bone skinning','ARMATURE');a.object=rig;return o
def sphere(name,loc,scale,material,bone='head'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(material)
 for f in o.data.polygons:f.use_smooth=True
 return weighted(o,bone)
def curve3(name,points,radius,material,bone='head',radii=None):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=20;c.bevel_depth=radius;c.bevel_resolution=4;s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for i,(b,co)in enumerate(zip(s.bezier_points,points)):b.co=co;b.handle_left_type='AUTO';b.handle_right_type='AUTO';b.radius=(radii[i]if radii else 1)
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(material);return weighted(o,bone)
# Fitted upper garment needs clearance over the base shirt; preserve its sewn 3D topology.
for v in vest.data.vertices:v.co.x*=1.17;v.co.y*=1.58
# Relax both actual upperarms down around their correct local axis.
for side,angle in [('L',-.68),('R',.68)]:rig.pose.bones['upperarm01.'+side].rotation_euler.z=angle
# Softened base fabric folds rather than realistic harsh wrinkling.
c=clothes.modifiers.new('Gentle cloth smoothing','CORRECTIVE_SMOOTH');c.factor=.45;c.iterations=5
# Large expressive eyes / eyelids use actual modeled geometry; original fitted eyes retained hidden as source.
if eyes:eyes.hide_render=True
ivory=mat('Eye ivory',(1,.95,.84),.35);blue=mat('Clear warm blue iris',(.025,.23,.45),.3);dark=mat('Deep pupil',(.009,.018,.023),.25);shine=mat('Eye catchlight',(1,1,.92),.15);hairdark=mat('Warm chestnut brows',(.13,.042,.011));lip=mat('Warm lip outline',(.43,.095,.058));mouth=mat('Smile interior',(.105,.014,.016));tooth=mat('Smile ivory teeth',(.94,.87,.69))
for sign,side in [(1,'L'),(-1,'R')]:
 x=sign*.047;z=1.235
 sphere('Ruta expressive sclera '+side,(x,-.137,z),(.032,.025,.038),ivory)
 sphere('Ruta blue iris '+side,(x+sign*.002,-.160,z),(.020,.005,.026),blue)
 sphere('Ruta pupil '+side,(x+sign*.002,-.164,z),(.010,.003,.018),dark)
 sphere('Ruta eye glint '+side,(x-.006,-.168,z+.011),(.005,.002,.006),shine)
 points=[(x-.031,-.146,z+.009),(x-.020,-.159,z+.034),(x+.010,-.161,z+.038),(x+.031,-.145,z+.014)]
 curve3('Ruta upper eyelid '+side,points,.0045,hairdark)
 curve3('Ruta warm lower eyelid '+side,[(x-.029,-.145,z-.014),(x,-.16,z-.034),(x+.027,-.146,z-.015)],.003,skin)
 curve3('Ruta expressive brow '+side,[(x-.031,-.14,z+.055),(x-.006,-.145,z+.068),(x+.026,-.136,z+.058)],.006,hairdark,radii=[.55,1,.3])
# Friendly smile modeled on the front facial surface.
sphere('Ruta smile',(0,-.166,1.16),(.034,.007,.015),mouth)
sphere('Ruta visible smile teeth',(0,-.173,1.166),(.029,.002,.005),tooth)
curve3('Ruta smiling lower lip',[(-.031,-.168,1.165),(0,-.174,1.147),(.031,-.168,1.165)],.0035,lip,radii=[.5,1,.5])
# Volumetric copper-brown wavy locks originate at scalp; roots taper into existing fitted cap.
hairtones=[mat('Copper wave '+str(i),c)for i,c in enumerate([(.28,.085,.016),(.39,.135,.028),(.48,.19,.05),(.34,.105,.02)])]
for k in range(26):
 theta=.05+math.pi*1.95*k/25;x=.125*math.cos(theta);y=.025+.075*math.sin(theta);top=1.34-.045*abs(math.cos(theta));pts=[]
 for j in range(10):
  t=j/9;pts.append((x*(1+.28*t)+.022*math.sin(t*math.pi*3+k*.7),y+.09*t,top-.53*t))
 curve3('Ruta copper sculpted wave',pts,.022,hairtones[k%4],radii=[.1,.65,1,1,1,.95,.9,.7,.4,.04])
# Cargo pockets weighted to actual physical thighs and softly rounded in 3D.
for side,sign in [('L',1),('R',-1)]:
 o=cube('Ruta canvas cargo pocket',(.116*sign,-.035,.48),(.055,.076,.10),brown,.014);weighted(o,'upperleg01.'+side)
# Boots have dark tread thickness and real lacing, not just a flat color swap.
for side,sign in [('L',1),('R',-1)]:
 x=.138*sign
 for j in range(4):
  z=.10-j*.014;y=-.04-j*.014;curve3('Boot lace '+side,[(x-.026,y,z),(x+.025,y-.006,z-.008)],.003,white,bone='foot.'+side)
# Bag has a softly puffed leather panel and stitched edge over the retained source shape.
for o in bpy.data.objects:
 if o.name=='Ruta ONE satchel':
  for m in o.modifiers:
   if m.type=='BEVEL':m.width=.04;m.segments=6
curve3('Satchel sewn border',[(-.27,-.102,.73),(-.27,-.107,.59),(-.12,-.107,.59),(-.105,-.102,.73)],.002,gold,bone='spine05')
# Render genuine whole model; transparent source PNG, with comparison composed separately.
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=800;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.film_transparent=True;scene.world.color=(.25,.25,.25);scene.view_settings.view_transform='AgX'
def look(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(-2.8,-5,2.2));camera=bpy.context.object;look(camera,(0,0,.74));camera.data.type='ORTHO';camera.data.ortho_scale=1.73;scene.camera=camera
for loc,power,size in [((-3,-4,5),400,4),((3,-2,3),130,3),((1,3,4),250,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;look(o,(0,0,.7))
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-appearance-v3.blend'));scene.render.filepath=str(OUT/'ruta-e-pilot.png');bpy.ops.render.render(write_still=True)
(OUT/'settings.json').write_text(json.dumps({'status':'appearance-authoring-candidate-needs-review','productionEnabled':False,'meshBasis':'MPFB2.0.18 child plus coherent3Dheadsculpt','rig':'default','largeEyes':'genuine3Dsurfaces weighted head','hair':'sculptedcurves weighted head plus original fittedcap','strapCount':1,'animation':'not-authored'},indent=2)+'\n')
