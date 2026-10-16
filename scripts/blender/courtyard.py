"""Blender 4.5.3: reproducible, review-only courtyard. No production writes."""
import argparse
import hashlib
import json
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector
from bpy_extras.object_utils import world_to_camera_view

ROOT = Path(__file__).resolve().parents[2]
args = argparse.ArgumentParser()
args.add_argument('--output', type=Path, default=ROOT / 'docs/blender-chapter-1/candidates')
args.add_argument('--samples', type=int, default=12)
args.add_argument('--only', choices=['all', 'clean', 'check', 'build'], default='all')
opt = args.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
opt.output.mkdir(parents=True, exist_ok=True)
random.seed(40)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = opt.samples
scene.render.use_file_extension = True
scene.cycles.use_denoising = True
scene.render.threads_mode = 'FIXED'
scene.render.threads = 8
scene.render.resolution_x = 1672
scene.render.resolution_y = 941
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.view_settings.view_transform = 'Standard'
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(.77,.84,1,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
collections = {}
for name in ['background', 'foreground', 'gate_closed', 'gate_open', 'ruta', 'stones', 'verification']:
    col = bpy.data.collections.new(name)
    scene.collection.children.link(col)
    collections[name] = col
current = 'background'

def put(obj, name, mat=None):
    obj.name = name
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collections[current].objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    return obj

def material(name, color, noise=0, scale=7):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1)
    m.use_nodes = True
    n, l = m.node_tree.nodes, m.node_tree.links
    bs = n.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*color, 1)
    bs.inputs['Roughness'].default_value = .94
    bs.inputs['Specular IOR Level'].default_value = .03
    if noise:
        tex = n.new('ShaderNodeTexNoise')
        tex.inputs['Scale'].default_value = scale
        tex.inputs['Detail'].default_value = 3
        ramp = n.new('ShaderNodeValToRGB')
        ramp.color_ramp.elements[0].color = (*(v * (1-noise) for v in color), 1)
        ramp.color_ramp.elements[1].color = (*(min(1, v*(1+noise)) for v in color), 1)
        l.new(tex.outputs['Fac'], ramp.inputs[0])
        l.new(ramp.outputs[0], bs.inputs['Base Color'])
        bump = n.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = .14
        bump.inputs['Distance'].default_value = .03
        l.new(tex.outputs['Fac'], bump.inputs['Height'])
        l.new(bump.outputs[0], bs.inputs['Normal'])
    return m

cream = material('warm lime plaster', (.78,.62,.35), .14)
wood = material('honey oak grain', (.32,.14,.045), .28, 11)
trim = material('dark brown contour', (.12,.065,.024))
roofm = [material('terracotta %s'%i, (.52+i*.027,.10+i*.012,.035+i*.006), .16) for i in range(5)]
leafm = [material('sage leaf %s'%i, (.12+i*.025,.23+i*.026,.045+i*.009), .22) for i in range(5)]
ground = material('quiet moss and ochre soil', (.46,.48,.18), .3, 2.3)
stone = material('warm limestone', (.59,.54,.39), .2)
white = material('cream petals', (.98,.89,.65))
pink = material('rose petals', (.70,.22,.31))
gold = material('pollen and brass', (.85,.49,.055))

# Bevels catch soft light; every prop is mesh geometry, never a reference plane.
# Cache unit spheres; avoid a dependency-graph rebuild per leaf.
sphere_meshes = {}
for segments in [8,12,16]:
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=8)
    temp=bpy.context.object
    sphere_meshes[segments]=temp.data
    for polygon in temp.data.polygons: polygon.use_smooth=True
    bpy.data.objects.remove(temp,do_unlink=True)

def box(name, loc, scale, mat, bevel=.04):
    vertices=[(x*scale[0]/2,y*scale[1]/2,z*scale[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
    data=bpy.data.meshes.new(name)
    data.from_pydata(vertices,[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
    data.materials.append(mat)
    o=bpy.data.objects.new(name,data); collections[current].objects.link(o); o.location=loc
    if bevel:
        b=o.modifiers.new('soft hand-shaped edges','BEVEL'); b.width=bevel; b.segments=2
        o.modifiers.new('weighted normals','WEIGHTED_NORMAL')
    return o

def ball(name, loc, size, mat, segments=16):
    o=bpy.data.objects.new(name,sphere_meshes[segments]); collections[current].objects.link(o)
    o.location=loc; o.scale=size
    if not o.data.materials: o.data.materials.append(mat)
    o.material_slots[0].link='OBJECT'; o.material_slots[0].material=mat
    return o

def line(name, points, radius, mat):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.bevel_depth=radius; c.bevel_resolution=2
    s=c.splines.new('POLY'); s.points.add(len(points)-1)
    for p,co in zip(s.points,points): p.co=(*co,1)
    o=bpy.data.objects.new(name,c); collections[current].objects.link(o); c.materials.append(mat)
    return o

def beam(name,a,b,width,mat):
    o=box(name,(Vector(a)+Vector(b))/2,(width,width,(Vector(b)-Vector(a)).length),mat,width*.2)
    o.rotation_euler=(Vector(b)-Vector(a)).to_track_quat('Z','Y').to_euler()
    return o

def mesh(name, verts, faces, mat):
    m=bpy.data.meshes.new(name); m.from_pydata(verts,[],faces); m.update()
    o=bpy.data.objects.new(name,m); collections[current].objects.link(o); m.materials.append(mat)
    return o

box('continuous ground', (7,-3,-.16),(38,32,.3),ground)
# Compact house with pitched roof, separate overlapping tiles and stonework.
box('cottage walls',(.45,.9,1.45),(4.05,3.8,2.9),cream)
mesh('gable', [(-1.575,-1,2.9),(2.475,-1,2.9),(.45,-1,3.95),(-1.575,2.8,2.9),(2.475,2.8,2.9),(.45,2.8,3.95)],[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],cream)
for side in [-1,1]:
    for row in range(7):
        t=(row+.5)/7
        for col in range(10):
            o=box('individual curved clay roof tile',(.45+side*t*2.28,-1.25+col*.45,4.05-t*1.12),(.47,.51,.13),random.choice(roofm),.075)
            o.rotation_euler[1]=side*math.atan(1.12/2.28)
for y in range(10): ball('ridge cap',(.45,-1.22+y*.46,4.07),(.16,.27,.14),roofm[1])
box('chimney',(-.6,1.7,3.6),(.55,.55,1.55),stone)
box('chimney lip',(-.6,1.7,4.43),(.69,.69,.16),roofm[2])
box('chimney dark opening',(-.6,1.7,4.52),(.4,.4,.015),trim)
# Door on right wall, facing east; threshold approaches immutable start.
box('door surround',(2.51,-.22,1.03),(.17,1.22,2.15),trim)
for j in range(6): box('door plank',(2.62,-.75+j*.19,1.02),(.10,.175,1.99),wood,.025)
ball('door brass knob',(2.72,-.55,1.02),(.07,.07,.07),gold)
for x,z,w in [(2.7,.16,.55),(2.95,.07,.95)]: box('threshold',(x,-.25,z),(w,1.45,.16),stone)
for x in [-.7,1.35]:
    box('window dark inset',(x,-1.025,1.65),(.9,.12,1.12),trim)
    box('window amber light',(x,-1.1,1.65),(.7,.08,.92),gold)
    box('window mullion',(x,-1.17,1.65),(.055,.08,1),wood)
    box('window crossbar',(x,-1.17,1.65),(.76,.08,.055),wood)
    for s in [-1,1]: box('sage shutters',(x+s*.57,-1.13,1.65),(.29,.12,1.15),leafm[1])
    box('flower box',(x,-1.28,.99),(1.15,.36,.29),wood)
for i in range(28):
    x=random.uniform(-1.5,2.3); z=random.uniform(.2,2.8)
    box('plaster stone detail',(x,-1.012,z),(.22,.025,.11),stone,.03)
beam('weather vane',(.45,.8,4.1),(.45,.8,4.75),.04,trim)
beam('weather arrow',(.03,.8,4.6),(.87,.8,4.6),.035,trim)
# Bring the threshold to the immutable start without moving any game cell.
bpy.context.view_layer.update()
house_transform = Matrix.Translation((2.5,-1.6,0)) @ Matrix.Rotation(-math.pi/4,4,'Z') @ Matrix.Diagonal((.70,.75,.72,1)) @ Matrix.Translation((-2.5,0,0))
house_transform = Matrix.Translation((1.4,-.077,0)) @ Matrix.Diagonal((.72,.72,.72,1)) @ Matrix.Translation((-2,1,0)) @ house_transform
for obj in collections['background'].objects:
    if obj.name != 'continuous ground':
        obj.matrix_world = house_transform @ obj.matrix_world

# Fences stay beyond the full playable cell footprints. Gate is east of goal.
def fence_post(x,y):
    box('fence post',(x,y,.61),(.19,.21,1.22),wood)
    ball('post cap',(x,y,1.26),(.14,.15,.10),gold)

def fence(a,b):
    dist=(Vector(b)-Vector(a)).length
    count=max(1,round(dist/1.3))
    for i in range(count+1):
        p=Vector(a).lerp(Vector(b),i/count); fence_post(p.x,p.y)
    for z in [.4,.86]: beam('fence rail',(*a,z),(*b,z),.12,wood)

fence((-2,3.7),(17,3.7))
fence((14.0,3.7),(14.0,-4.25))
fence((14.0,-6.25),(14.0,-10.0))
current='foreground'
fence((-3,-9.5),(10.5,-9.5))
# A diagonal gate reveals its boards while leaving the whole goal cell clear.
for state,angle in [('gate_closed',-math.atan2(1.0,2.0)),('gate_open',math.radians(-150))]:
    current=state
    hinge=bpy.data.objects.new('hinge '+state,None); collections[current].objects.link(hinge)
    hinge.location=(13.5,-6.25,0)
    for i in range(10):
        t=(i+.5)/10; height=.96+.20*math.sin(t*math.pi)
        o=box('gate vertical plank',(0,t*math.sqrt(5),height/2),(.12,.215,height),wood,.035)
        o.parent=hinge
    for z in [.22,.76]:
        o=beam('gate cross rail',(.08,0,z),(.08,math.sqrt(5),z),.10,trim); o.parent=hinge
    o=ball('gate brass latch',(-.10,1.95,.65),(.07,.07,.07),gold); o.parent=hinge
    hinge.rotation_euler[2]=angle
current='background'
fence((14,-6.25),(13.5,-6.25))
fence((14,-4.25),(14.5,-4.25))
collections['gate_open'].hide_render=True
current='background'
# Clustered leaves and flowers at the perimeter, with sparse garden floor.
def plant(x,y,size=.5,flowers=False):
    for k in range(7):
        a=k*2.4; dx=math.cos(a)*size*.46; dy=math.sin(a)*size*.46
        o=ball('leaf cluster',(x+dx,y+dy,size*.4+random.random()*.17),(size*.45,size*.22,size*.24),random.choice(leafm),12)
        o.rotation_euler[2]=a
    if flowers:
        for k in range(3):
            fx=x+random.uniform(-size,size)*.5; fy=y+random.uniform(-size,size)*.5; z=size+.12
            beam('flower stem',(fx,fy,.05),(fx,fy,z),.018,leafm[0])
            for p in range(5):
                a=p*math.tau/5
                ball('flower petal',(fx+.065*math.cos(a),fy+.065*math.sin(a),z),(.07,.045,.028),white if k%2 else pink,8)
            ball('pollen',(fx,fy,z+.03),(.033,.033,.028),gold,8)

for i in range(100):
    x=random.uniform(-5,19); y=random.choice([random.uniform(1.8,3.5),random.uniform(-11,-8.55)])
    plant(x,y,random.uniform(.32,.65),i%3==0)
for i in range(26): plant(random.uniform(14.1,17),random.uniform(-7,4),random.uniform(.3,.65),i%2==0)
for i in range(38): plant(random.uniform(-1.5,.8),random.uniform(-7,-3.4),random.uniform(.35,.65),i%2==0)
for i in range(14): plant(random.uniform(-2.9,-1.9),random.uniform(-4,3),.45,True)
for x in [-.7,1.35]: plant(x,-1.35,.30,True)
for x,y in [(-2,2.8),(5,2.8),(11,2.8),(17,2.8),(-4,-7),(16,-9)]:
    beam('tree trunk',(x,y,0),(x+.13,y,3.6),.25,wood)
    for j in range(13):
        a=j*2.4; r=random.uniform(.3,1.25)
        ball('tree canopy',(x+math.cos(a)*r,y+math.sin(a)*r,3.3+random.random()*1.2),(.9,.75,.65),random.choice(leafm))
for i in range(20):
    x=random.uniform(-3,18); y=random.choice([3.0,-9.0])
    ball('mossy rock',(x,y,.2),(.3,.22,.25),stone,12)
# Stylised individual Ruta study: geometry, asymmetrical bag, flowing hair, blue eyes.
current='ruta'
skin=material('Ruta warm skin',(.87,.52,.29),.07)
hair=material('chestnut hair',(.31,.115,.035),.22,12)
shirt=material('linen shirt',(.91,.82,.64),.08)
vest=material('olive waistcoat',(.20,.27,.10),.15)
red=material('red neck scarf',(.55,.045,.035),.12)
blue=material('blue eyes',(.035,.26,.48))
logical=json.loads((ROOT/'src/chapter-1.logical.json').read_text())['gate']
solutions=json.loads((ROOT/'src/art-solutions.json').read_text())['gate']
metadata=json.loads((ROOT/'src/scene-v8.json').read_text())['gate']
R=metadata['camera']['radius']/100

def hexworld(h): return (math.sqrt(3)*R*(h['q']+h['r']/2),-1.5*R*h['r'],0)
sx,sy,_=hexworld(logical['start'])
def rp(x,y,z): return (sx+x,sy+y,z)
for s in [-1,1]:
    ball('boots',rp(s*.12,-.065,.10),(.105,.18,.1),wood)
    ball('trousers',rp(s*.12,0,.40),(.12,.12,.31),wood)
ball('shirt torso',rp(0,0,.89),(.24,.15,.31),shirt)
for s in [-1,1]:
    ball('vest panel',rp(s*.13,-.11,.91),(.11,.065,.28),vest)
    beam('sleeve',rp(s*.21,0,1.07),rp(s*.32,-.025,.79),.14,shirt)
    beam('forearm',rp(s*.32,-.025,.79),rp(s*.29,-.12,.63),.10,skin)
    ball('hand',rp(s*.29,-.12,.64),(.065,.065,.075),skin)
ball('long hair back',rp(0,.095,1.16),(.29,.16,.48),hair)
ball('head',rp(0,-.01,1.40),(.235,.18,.275),skin)
for s in [-1,1]:
    ball('ear',rp(s*.232,0,1.40),(.055,.05,.08),skin)
    ball('eye white',rp(s*.085,-.174,1.44),(.060,.023,.067),white)
    ball('blue iris',rp(s*.085,-.195,1.44),(.032,.014,.045),blue)
    ball('pupil',rp(s*.085,-.207,1.44),(.014,.008,.030),trim)
    ball('eye highlight',rp(s*.075,-.213,1.46),(.009,.005,.012),white)
    line('eyebrow',[rp(s*.04,-.185,1.54),rp(s*.11,-.185,1.55),rp(s*.15,-.17,1.53)],.012,hair)
ball('nose',rp(0,-.19,1.37),(.035,.04,.04),skin)
line('smile',[rp(-.06,-.175,1.29),rp(0,-.194,1.275),rp(.06,-.175,1.29)],.009,red)
# Locks descend behind face, without a braid or head scarf.
for j in range(11):
    a=j/10*math.pi
    x=math.cos(a)*.24
    line('flowing hair lock',[rp(x,.03,1.56),rp(x*1.13,.08,1.31),rp(x*1.28,.12,1.0),rp(x*1.18,.07,.85)],.055,hair)
for s in [-1,1]:
    line('fringe',[rp(0,-.03,1.67),rp(s*.15,-.13,1.61),rp(s*.21,-.13,1.45)],.065,hair)
ball('scarf knot',rp(0,-.17,1.13),(.07,.045,.07),red)
for s in [-1,1]:
    mesh('scarf tail',[rp(0,-.18,1.13),rp(s*.13,-.19,.90),rp(s*.055,-.20,.86)],[(0,1,2)],red)
line('single diagonal bag strap',[rp(.17,-.16,1.11),rp(0,-.18,.91),rp(-.25,-.13,.65)],.025,wood)
box('satchel',rp(-.30,0,.63),(.23,.14,.29),wood)
box('satchel flap',rp(-.30,-.083,.69),(.25,.025,.13),hair)
box('satchel buckle',rp(-.30,-.107,.65),(.055,.02,.06),gold)
bpy.context.view_layer.update()
ruta_transform=Matrix.Translation((sx,sy,0)) @ Matrix.Diagonal((.72,.72,.72,1)) @ Matrix.Translation((-sx,-sy,0))
for obj in collections['ruta'].objects:
    obj.matrix_world=ruta_transform @ obj.matrix_world

# Separate mathematical hex slab, not baked into courtyard.
current='stones'
charoite=material('charoite with irregular mineral veins',(.29,.095,.45),.35,9)
n=charoite.node_tree.nodes; l=charoite.node_tree.links
tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=4; tex.inputs['Distortion'].default_value=3
wave=n.new('ShaderNodeTexVoronoi'); wave.feature='DISTANCE_TO_EDGE'; wave.inputs['Scale'].default_value=7
l.new(tex.outputs['Color'],wave.inputs['Vector'])
ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.015; ramp.color_ramp.elements[0].color=(.68,.49,.77,1)
ramp.color_ramp.elements[1].position=.065; ramp.color_ramp.elements[1].color=(.23,.06,.36,1)
l.new(wave.outputs['Distance'],ramp.inputs[0]); l.new(ramp.outputs[0],n.get('Principled BSDF').inputs['Base Color'])

def slab(name,x,y,mat,r=R):
    # Surface lies on z=0: its camera silhouette is the exact game hex mask.
    vs=[(x+r*math.cos(math.radians(30+i*60)),y+r*math.sin(math.radians(30+i*60)),0) for i in range(6)]
    return mesh(name,vs,[tuple(range(6))],mat)
slab('separate stone candidate',6,-8.7,charoite)
# Accurate verification uses real game grid/endpoints and reference placements.
current='verification'
checkmat=material('verification line',(.12,.30,.30))
startmat=material('start marker',(.10,.55,.24)); goalmat=material('goal marker',(.85,.23,.03))
for row in range(7):
    for col in range(11):
        h={'q':col-row//2,'r':row}; x,y,_=hexworld(h)
        points=[(x+R*math.cos(math.radians(30+i*60)),y+R*math.sin(math.radians(30+i*60)),0) for i in range(7)]
        blocked=f"{h['q']},{h['r']}" in logical['terrain']
        line('blocked hex' if blocked else 'playable hex',points,.008,red if blocked else checkmat)
for name,mat in [('start',startmat),('goal',goalmat)]:
    x,y,_=hexworld(logical[name]); slab(name,x,y,mat)
for ident,placement in solutions.items():
    assert placement['turns']==0, 'gate pilot expects single-cell stones'
    x,y,_=hexworld(placement['anchor']); slab('solution '+ident,x,y,charoite)
collections['verification'].hide_render=True
# Camera solves affine yScale exactly: elevation asin(.65), orthographic.
current='background'
bpy.ops.object.camera_add(); camera=put(bpy.context.object,'game affine camera')
scene.camera=camera; camera.data.type='ORTHO'; camera.data.ortho_scale=16.72
center=Vector(((836-140)/100,-(470.5-290)/65,0))
camera.location=center+Vector((0,-math.sqrt(1-.65**2)*30,.65*30))
camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.light_add(type='AREA', location=(-3,-1,12)); light=put(bpy.context.object,'large warm sky light')
collections['background'].objects.unlink(light)
scene.collection.objects.link(light)
light.data.energy=2200; light.data.shape='DISK'; light.data.size=8
light.rotation_euler=(Vector((6,-2,0))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.context.view_layer.update()
errors=[]; anchors={}
for name,h in [('start',logical['start']),('goal',logical['goal'])]:
    p=world_to_camera_view(scene,camera,Vector(hexworld(h)))
    px=[p.x*1672,(1-p.y)*941]; expected=metadata['groundAnchors'][name]
    err=math.hypot(px[0]-expected['x'],px[1]-expected['y']); errors.append(err)
    anchors[name]={'pixel':px,'world':hexworld(h),'expected':expected,'errorPx':err}
assert max(errors)<.01, anchors
scene.render.image_settings.color_mode = 'RGBA'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/blender/gate-pilot.blend'),compress=True)

def render(name):
    scene.render.filepath=str(opt.output/(name+'.png')); bpy.ops.render.render(write_still=True)

if opt.only in ['all','clean']: render('gate-clean')
if opt.only in ['all','check']:
    collections['verification'].hide_render=False; render('gate-check'); collections['verification'].hide_render=True
manifest={'status':'candidate — awaiting Maksim art review; not production', 'scene':'gate','blender':bpy.app.version_string,'seed':40,'source':'art/blender/gate-pilot.blend','command':'blender --background --factory-startup --threads 8 --python-exit-code 1 --python scripts/blender/courtyard.py -- --samples 16', 'samples':opt.samples,'resolution':[1672,941],'sourceRect':[0,0,1672,941],'camera':{'type':'orthographic','elevationDegrees':math.degrees(math.asin(.65)),'worldToPixel':[[100,0,0,140],[0,-65,-100*math.sqrt(1-.65**2),290]],'groundPixelToWorld':[[.01,0,-1.4],[0,-1/65,290/65]],'anchors':anchors},'collections':list(collections),'productionChanged':False}
manifest['inputSha256']={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [ROOT/'src/scene-v8.json',ROOT/'src/chapter-1.logical.json',ROOT/'src/art-solutions.json',Path(__file__).resolve()]}
(opt.output.parent/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
