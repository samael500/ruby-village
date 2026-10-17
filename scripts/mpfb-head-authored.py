"""Reproducible native MPFB post-bake authored orbital sculpt and flattened wavy locks.
Starts from preserved study 1. No source image planes or disconnected surface eyes.
"""
from pathlib import Path
import bpy, math, os, json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
V=int(os.environ.get('RUBY_MPFB_HEAD_STUDY','3')); OUT=ROOT/f'art/characters-mpfb-v1/head-study-{V}';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'art/characters-mpfb-v1/head-study-1/ruta-head.blend'))
h=next(o for o in bpy.data.objects if o.type=='MESH' and 'study body' in o.name and '.' not in o.name)
eyes=next(o for o in bpy.data.objects if 'high-poly' in o.name)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a))); return t*t*(3-2*t)
centers=[Vector((s*.042355,-.125694,1.232388)) for s in [-1,1]]
def sculpt(p):
 q=p.copy()
 # Broad orbital support moves actual lids, surrounding face and fitted eyeballs together.
 for c in centers:
  d=p-c;r=math.sqrt((d.x/.072)**2+(d.z/.070)**2)
  w=(1-smooth(.35,1,r))*(1-smooth(.045,.095,abs(d.y)))
  q.x+=d.x*(.53 if V==3 else .67)*w
  q.z+=d.z*(.60 if V==3 else .72)*w
 # Small upturned nasal tip with intact native nostrils.
 w=math.exp(-((p.x/.023)**2+((p.z-1.191)/.032)**2))* (1-smooth(-.17,-.12,p.y))
 q.y+=.011*w;q.z+=.004*w
 # Widen and lift mouth corners continuously into cheeks, keeping native mouth topology.
 w=math.exp(-((p.z-1.160)/.023)**2)* (1-smooth(-.145,-.09,p.y))
 q.x+=p.x*.19*w;q.z+=.008*(min(1,abs(p.x)/.032)**1.7)*w
 return q
key=h.shape_key_add(name=f'Ruta authored orbital cheek smile study {V}');key.value=1
if V>=4:key.relative_key=h.data.shape_keys.key_blocks['Ruta coherent child head sculpt']
for v in key.data:v.co=sculpt(v.co)
for ob in [eyes]+[o for o in bpy.data.objects if 'eyebrow' in o.name]:
 for v in ob.data.vertices:v.co=sculpt(v.co)
# Subtle warm skin, brighter than prior realistic brown study.
skin=h.data.materials[0];skin.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.80,.43,.26,1)
def mat(name,c):
 m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*c,1);n.inputs['Roughness'].default_value=.72;return m
copper=[mat('Copper lock '+str(i),c) for i,c in enumerate([(.43,.13,.035),(.60,.23,.065),(.76,.34,.105),(.53,.18,.045)])]
old=next(o for o in bpy.data.objects if 'long01' in o.name);old.hide_render=True;old.hide_viewport=True
# Overlapping flattened elliptical sections, changing breadth and taper; no cylinder primitives.
def lock(name,points,width,phase,index):
 verts=[];faces=[];N=48;K=10
 for j in range(N):
  t=j/(N-1);u=t*(len(points)-1);k=min(len(points)-2,int(u));f=u-k;c=Vector(points[k]).lerp(Vector(points[k+1]),f)
  c.x+=math.sin(t*math.pi*3+phase)*.010*math.sin(math.pi*t);c.y+=math.sin(t*math.pi*4+phase)*.009*math.sin(math.pi*t)
  tangent=Vector(points[k+1])-Vector(points[k]);a=Vector((1,0,0));b=tangent.cross(a).normalized();a=b.cross(tangent).normalized()
  breadth=width*(.35+.65*math.sin(math.pi*(.08+.86*t)))*max(.03,(1-t)**.35)
  for n in range(K):
   angle=2*math.pi*n/K;verts.append(c+a*math.cos(angle)*breadth+b*math.sin(angle)*breadth*.22)
 for j in range(N-1):
  for n in range(K):faces.append((j*K+n,j*K+(n+1)%K,(j+1)*K+(n+1)%K,(j+1)*K+n))
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(copper[index%4])
 for p in mesh.polygons:p.use_smooth=True
 mod=ob.modifiers.new('Smooth sculpted lock','SUBSURF');mod.levels=1
# Back and side crown masses wrap the head, with asymmetric overlapping roots.
for i in range(19):
 a=-math.pi*.03+i/18*math.pi*1.06;x=.137*math.cos(a);y=.028+.115*math.sin(a)
 lock('Authored back wave %02d'%i,[(x*.28,y*.35,1.370),(x*.90,y,1.315),(x*1.04,y*1.04,1.205),(x*1.10,y*.92,1.09),(x*.94,y*.75,1.005+(.018*math.sin(i)))],.028, i*.8,i)
# Front swept fringe frames forehead, leaving eyes clear; broad tapered sections.
for s in [-1,1]:
 for j in range(4):
  lock('Swept fringe '+str((s,j)),[(.025-j*.012,-.006,1.372),(s*(.055+j*.015),-.088,1.345),(s*(.105+j*.010),-.113,1.290),(s*(.137+j*.005),-.081,1.205),(s*(.143+j*.004),-.060,1.09)],.027-j*.002,j*.7+2,j+1)
scene=bpy.context.scene;scene.cycles.samples=24;scene.render.resolution_x=800;scene.render.resolution_y=800
# Frontal studio fill reveals actual surface anatomy.
for ob in bpy.data.objects:
 if ob.type=='LIGHT':ob.data.energy*=1.65
center=Vector((0,-.02564,1.28330));camera=scene.camera
for name,angle in [('front',0),('three-quarter',-.52),('profile',-math.pi/2)]:
 camera.location=center+Vector((math.sin(angle)*3,-math.cos(angle)*3,.08));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-head.blend'))
(OUT/'settings.json').write_text(json.dumps({'study':V,'status':'authored head study, not approved','productionEnabled':False,'nativeVertices':len(h.data.vertices),'nativeEyeLidDeformation':'shared smooth orbital field','hair':'authored flattened tapered elliptical-section wave meshes','base':'head-study-1/ruta-head.blend','orbitalScale':[.53,.60] if V==3 else [.67,.72]},indent=2)+'\n')
