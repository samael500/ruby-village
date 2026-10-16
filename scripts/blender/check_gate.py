"""Validate the real gate mesh, every sweep pose, full hex areas and export crop.
Load gate-pilot.blend. --render creates fast, explicitly labelled Workbench evidence.
"""
import argparse
import json
import math
import runpy
import sys
from pathlib import Path
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(); p.add_argument('--render',action='store_true')
args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
OUT=ROOT/'docs/blender-chapter-1/gate-fix'; OUT.mkdir(exist_ok=True)
maths=runpy.run_path(str(ROOT/'scripts/blender/gate_layout.py'))
area,overlap,bounds=maths['area'],maths['overlap'],maths['bounds']
engine=json.loads((ROOT/'docs/blender-chapter-1/geometry/gate-engine.json').read_text())
layout=json.loads(bpy.context.scene['gate_layout_json'])
scene=bpy.context.scene; camera=scene.camera
free=[]
for cell in engine['cells']:
    if cell['terrain']:continue
    polygon=[(p['x'],p['y']) for p in cell['polygon']]
    free.append((cell['id'],polygon,bounds(polygon)))
hinge=bpy.data.objects['hinge gate_closed']
col=bpy.data.collections['gate_closed']

def pixel(point):
    p=world_to_camera_view(scene,camera,point); return (p.x*1672,(1-p.y)*941)

def triangles():
    bpy.context.view_layer.update(); deps=bpy.context.evaluated_depsgraph_get()
    result=[]
    for obj in col.objects:
        if obj.type!='MESH':continue
        evaluated=obj.evaluated_get(deps); mesh=evaluated.to_mesh(); mesh.calc_loop_triangles()
        result.extend([[obj.matrix_world @ mesh.vertices[i].co for i in tri.vertices] for tri in mesh.loop_triangles])
        evaluated.to_mesh_clear()
    return result

def intersections(tris,ground=False):
    tested=[]
    for tri in tris:
        poly=[pixel(Vector((v.x,v.y,0)) if ground else v) for v in tri]
        if area(poly)>.001:tested.append((poly,bounds(poly)))
    hits=set(); maximum=0
    for ident,cell,cb in free:
        for poly,pb in tested:
            if pb[0]>=cb[2] or cb[0]>=pb[2] or pb[1]>=cb[3] or cb[1]>=pb[3]:continue
            intersection=overlap(poly,cell); maximum=max(maximum,intersection)
            if intersection>.1:hits.add(ident)
    return sorted(hits),maximum

poses=[]; minimum_crop_margin=10000
for step in range(20):
    fraction=step/19; hinge.rotation_euler[2]=layout['closedAngle']+fraction*(layout['openAngle']-layout['closedAngle'])
    tris=triangles()
    visible,max_visible=intersections(tris)
    ground,max_ground=intersections(tris,ground=True)
    margin=min(min(x,y,1672-x,941-y) for tri in tris for x,y in [pixel(v) for v in tri])
    minimum_crop_margin=min(minimum_crop_margin,margin)
    assert not visible and not ground,(step,visible,ground)
    assert margin>1,(step,margin)
    poses.append({'fraction':fraction,'visibleCellIntersections':visible,'groundCellIntersections':ground,'maxVisibleIntersectionPx2':max_visible,'maxGroundIntersectionPx2':max_ground,'cropMarginPx':margin})
# A deliberately wrong move back into the board must fail the actual-mesh check.
saved_location=hinge.location.copy(); hinge.rotation_euler[2]=layout['closedAngle']
hinge.location-=Vector((*layout['incomingDirection'],0))*.85
mutated_visible,_=intersections(triangles())
assert mutated_visible,'The actual-mesh checker did not detect the misplaced gate'
hinge.location=saved_location
# In the open pose the whole hex-width corridor remains free, not just Ruta's centre.
hinge.rotation_euler[2]=layout['openAngle']; tris=triangles()
center=Vector((*layout['openingCenter'],0)); normal=Vector((*layout['normal'],0))
leaf_min=min((v-center).dot(normal) for tri in tris for v in tri)
left_inner=-layout['width']/2+.11; right_inner=layout['width']/2-.11
clear_width=min(right_inner,leaf_min)-left_inner
assert clear_width>=1.4,(clear_width,leaf_min)
arrival=bpy.data.objects['gate arrival court']
arrival_pixel=pixel(arrival.matrix_world @ arrival.data.vertices[arrival['goalArrivalVertex']].co)
goal_pixel=engine['goal']['pixel']; arrival_error=math.dist(arrival_pixel,(goal_pixel['x'],goal_pixel['y']))
assert arrival_error<.001,arrival_error
hinge.rotation_euler[2]=layout['closedAngle']; bpy.context.view_layer.update()
opening=hinge.matrix_world @ Vector((0,layout['width']/2,0))
perpendicular=abs(Vector((*layout['incomingDirection'],0)).dot(Vector((*layout['normal'],0))))
assert perpendicular<1e-9
report={'sceneId':'gate','source':'art/blender/gate-pilot.blend','status':'pass','method':'actual evaluated bevelled mesh triangles intersected with full engine cell polygons; 20 sweep poses; ground footprints and projected silhouettes checked separately','rendererForProof':'Blender Workbench; technical evidence, not final art','poses':poses,'minimumCropMarginPx':minimum_crop_margin,'arrivalAnchorErrorPx':arrival_error,'openClearWidthWorld':clear_width,'requiredHexWidthWorld':1.4,'closedOpeningToGoalPx':math.dist(pixel(opening),(goal_pixel['x'],goal_pixel['y'])),'approachLengthWorld':layout['approachLengthWorld'],'planePerpendicularError':perpendicular,'negativeCheckMisplacedGateCells':mutated_visible,'logicalDataChanged':False}
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='poses'},indent=2),flush=True)
if args.render:
    scene.render.engine='BLENDER_WORKBENCH'
    scene.render.film_transparent=False
    scene.display.shading.color_type='MATERIAL'; scene.display.shading.light='STUDIO'
    scene.display.shading.show_shadows=False; scene.display.shading.show_cavity=True
    scene.display.shading.cavity_type='BOTH'
    scene.display.shading.background_type='WORLD'; scene.world.color=(.65,.70,.50)
    scene.render.resolution_x=1672; scene.render.resolution_y=941
    saved_loc=camera.location.copy(); saved_rot=camera.rotation_euler.copy(); saved_scale=camera.data.ortho_scale
    for state in ['closed','open']:
        bpy.data.collections['gate_closed'].hide_render=state!='closed'
        bpy.data.collections['gate_open'].hide_render=state!='open'
        for check in [False,True]:
            bpy.data.collections['verification'].hide_render=not check
            scene.render.filepath=str(OUT/f'{state}-{"check" if check else "clean"}.png')
            bpy.ops.render.render(write_still=True)
        bpy.data.collections['verification'].hide_render=True
        scene.render.resolution_x=960; scene.render.resolution_y=640; camera.data.ortho_scale=5.2
        goal=Vector((*layout['goal'],0)); target=(goal+opening)/2+Vector((0,0,.25))
        camera.location=target+Vector((0,-math.sqrt(1-.65**2)*30,.65*30))
        camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(OUT/f'{state}-detail.png'); bpy.ops.render.render(write_still=True)
        camera.location=saved_loc; camera.rotation_euler=saved_rot; camera.data.ortho_scale=saved_scale
        scene.render.resolution_x=1672; scene.render.resolution_y=941
