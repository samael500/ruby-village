"""Export review layers and four Ruta views from the saved pilot without rebuilding."""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(); p.add_argument('--samples',type=int,default=12)
p.add_argument('--resume',action='store_true')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
scene=bpy.context.scene; scene.cycles.samples=args.samples
camera=scene.camera
OUT=ROOT/'docs/blender-chapter-1/candidates'
collections={k:bpy.data.collections[k] for k in ['background','foreground','gate_closed','gate_open','ruta','stones','verification']}
manifest=json.loads((OUT.parent/'manifest.json').read_text())
logical=json.loads((ROOT/'src/chapter-1.logical.json').read_text())['gate']
def render(name):
    target=OUT/(name+'.png')
    if args.resume and target.exists(): return
    scene.cycles.use_denoising=name in ['layer-background','gate-detail','gate-wide']
    scene.render.filepath=str(target); bpy.ops.render.render(write_still=True)
scene.render.film_transparent=True
layers={}
for layer in ['background','foreground','gate_closed','gate_open','ruta','stones']:
    for name,col in collections.items(): col.hide_render=name!=layer
    render('layer-'+layer)
    layers[layer]={'file':'candidates/layer-'+layer+'.png','origin':[0,0],'sourceRect':[0,0,1672,941],'alpha':'straight','state':layer.removeprefix('gate_') if layer.startswith('gate_') else None,'shadowContract':'self-shadow only; cross-layer shadow pass pending'}
for name,col in collections.items(): col.hide_render=name!='ruta'
saved_location=camera.location.copy(); saved_rotation=camera.rotation_euler.copy(); saved_scale=camera.data.ortho_scale
scene.render.resolution_x=600; scene.render.resolution_y=800
camera.data.ortho_scale=1.6
sx,sy,_=manifest['camera']['anchors']['start']['world']
target=Vector((sx,sy,.62))
for name,direction in [('front',(0,-1,.05)),('side',(1,0,.05)),('back',(0,1,.05)),('game',(0,-.76,.65))]:
    camera.location=target+Vector(direction)*8
    camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    render('ruta-'+name)
camera.location=saved_location; camera.rotation_euler=saved_rotation; camera.data.ortho_scale=saved_scale
scene.render.resolution_x=1672; scene.render.resolution_y=941
maximum=0.0; samples=0
bpy.context.view_layer.update()
for row in range(7):
    for col in range(11):
        q=col-row//2; x=math.sqrt(3)*.7*(q+row/2); y=-1.05*row
        for dx,dy in [(0,0)]+[(.7*math.cos(math.radians(30+i*60)),.7*math.sin(math.radians(30+i*60))) for i in range(6)]:
            v=world_to_camera_view(scene,camera,Vector((x+dx,y+dy,0)))
            maximum=max(maximum,math.hypot(v.x*1672-(140+100*(x+dx)),(1-v.y)*941-(290-65*(y+dy))))
            samples+=1
assert maximum<.01,maximum
# Dedicated true 3D details, without changing the source scene.
for name,col in collections.items(): col.hide_render=name in ['verification','gate_open','ruta','stones']
scene.render.film_transparent=False
scene.render.resolution_x=800; scene.render.resolution_y=600
camera.data.ortho_scale=3.8
for name,point in [('gate-detail',(14,-5.25,.5)),('stone-detail',(6,-8.7,0))]:
    if name=='stone-detail':
        for key,col in collections.items(): col.hide_render=key!='stones'
        scene.render.film_transparent=True
        camera.data.ortho_scale=2.2
    center=Vector(point); camera.location=center+Vector((0,-math.sqrt(1-.65**2)*30,.65*30))
    camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    render(name)
# Actual side scenery from the same geometry, with the original camera center.
camera.location=saved_location; camera.rotation_euler=saved_rotation
camera.data.ortho_scale=32.72
scene.render.resolution_x=3272; scene.render.resolution_y=1200
scene.render.film_transparent=False
for name,col in collections.items(): col.hide_render=name in ['verification','gate_open']
render('gate-wide')
manifest['extendedCanvas']={'file':'candidates/gate-wide.png','resolution':[3272,1200],'originalRect':[800,129.5,1672,941],'method':'same camera center; wider orthographic frustum; real geometry'}
manifest['layers']=layers
manifest['inputSha256']['scripts/blender/courtyard.py']=hashlib.sha256((ROOT/'scripts/blender/courtyard.py').read_bytes()).hexdigest()
manifest['projectionCheck']={'points':samples,'maxErrorPx':maximum,'includes':'77 centers + 462 corners'}
manifest['exportSamples']=args.samples
manifest['exportCommand']='blender --background --threads 8 art/blender/gate-pilot.blend --python-exit-code 1 --python scripts/blender/export.py -- --samples '+str(args.samples)
(OUT.parent/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
