"""Build/audit the gate geometry contract, independently of decorative models.
Run on gate-pilot.blend. Does not render or overwrite the art candidate.
"""
import hashlib
import html
import json
import math
from pathlib import Path
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/blender-chapter-1/geometry'
engine_path=OUT/'gate-engine.json'
engine=json.loads(engine_path.read_text())
assert engine['sceneId']=='gate'
scene=bpy.context.scene
camera=scene.camera
width,height=engine['resolution']
assert [scene.render.resolution_x,scene.render.resolution_y]==[width,height]
# Keep old art available for comparison, but hidden in this geometric source.
for col in scene.collection.children:
    col.hide_render=True
    col.hide_viewport=True
collection=bpy.data.collections.new('geometry_contract')
scene.collection.children.link(collection)

def world(point):
    # Fixed gate camera contract; projection audit below catches stale cameras.
    return ((point['x']-140)/100,(290-point['y'])/65,0)

def pixel(point):
    p=world_to_camera_view(scene,camera,Vector(point))
    return (p.x*width,(1-p.y)*height)

actual={}
for cell in engine['cells']:
    top=[world(p) for p in cell['polygon']]
    depth=.25 if cell['terrain'] else .08
    vertices=top+[(x,y,-depth) for x,y,z in top]
    faces=[tuple(reversed(range(6))),tuple(range(6,12))]+[(i,i+6,(i+1)%6+6,(i+1)%6) for i in range(6)]
    mesh=bpy.data.meshes.new('cell '+cell['id'])
    mesh.from_pydata(vertices,[],faces); mesh.update()
    obj=bpy.data.objects.new(('blocker ' if cell['terrain'] else 'playable ')+cell['id'],mesh)
    collection.objects.link(obj)
    obj['cellId']=cell['id']; obj['terrainRole']='blocker' if cell['terrain'] else 'playable'
    obj['terrain']=cell['terrain'] or ''
    obj.color=(.40,.25,.16,1) if cell['terrain'] else (.72,.77,.57,1)
    obj['capFace']=0
    actual[cell['id']]=obj
for name in ['start','goal']:
    obj=bpy.data.objects.new('contract '+name,None)
    collection.objects.link(obj); obj.location=world(engine[name]['pixel'])
    obj.empty_display_type='CIRCLE'; obj.empty_display_size=.3
    obj['role']='game ground anchor; not an artistic doorway'

bpy.context.view_layer.update()
polygons={}
for ident,obj in actual.items():
    cap=obj.data.polygons[obj['capFace']]
    polygons[ident]=[pixel(obj.matrix_world @ obj.data.vertices[index].co) for index in cap.vertices]

def signed_area(poly):
    return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(poly,poly[1:]+poly[:1]))/2 if poly else 0

def area(poly):return abs(signed_area(poly))

def intersection(subject,clip):
    """Sutherland-Hodgman: exact polygon areas, no pixel/interior sampling."""
    if signed_area(clip)<0:clip=list(reversed(clip))
    result=list(subject)
    for a,b in zip(clip,clip[1:]+clip[:1]):
        def side(p):return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])
        previous=result[-1] if result else None
        new=[]
        for point in result:
            before=side(previous); after=side(point)
            if (before>=0)!=(after>=0):
                t=before/(before-after)
                new.append((previous[0]+t*(point[0]-previous[0]),previous[1]+t*(point[1]-previous[1])))
            if after>=0:new.append(point)
            previous=point
        result=new
        if not result:break
    return result

blockers={ident:poly for ident,poly in polygons.items() if actual[ident]['terrainRole']=='blocker'}
expected_ids={c['id'] for c in engine['cells'] if c['terrain']}
assert set(blockers)==expected_ids
cells=[]; maximum_corner_error=0
for cell in engine['cells']:
    expected=[(p['x'],p['y']) for p in cell['polygon']]
    mesh_poly=polygons[cell['id']]
    maximum_corner_error=max(maximum_corner_error,max(min(math.dist(p,q) for q in mesh_poly) for p in expected))
    covered=sum(area(intersection(expected,poly)) for poly in blockers.values())
    desired=area(expected) if cell['terrain'] else 0
    cells.append({'id':cell['id'],'terrain':cell['terrain'],'areaPx2':area(expected),'blockedAreaPx2':covered,'areaErrorPx2':abs(covered-desired)})
maximum_area_error=max(c['areaErrorPx2'] for c in cells)
assert maximum_corner_error<.001,maximum_corner_error
assert maximum_area_error<.25,maximum_area_error
# Demonstrate the test is two-sided: missing one blocked cap must fail coverage.
missing=next(iter(blockers)); missing_expected=next(c for c in engine['cells'] if c['id']==missing)
expected=[(p['x'],p['y']) for p in missing_expected['polygon']]
missing_error=area(expected)-sum(area(intersection(expected,p)) for ident,p in blockers.items() if ident!=missing)
assert missing_error>8000,missing_error
# Moving a blocker onto a free cell must be detected as both a hole and a spill.
free=next(c for c in engine['cells'] if not c['terrain'])
dx=free['center']['x']-missing_expected['center']['x']; dy=free['center']['y']-missing_expected['center']['y']
moved=[(x+dx,y+dy) for x,y in blockers[missing]]
spill=area(intersection([(p['x'],p['y']) for p in free['polygon']],moved))
assert spill>8000,spill
# Old decorative entrances are measured, not relabelled as aligned by proxies.
step=scene.objects['threshold.001'].matrix_world.translation
step_px=pixel((step.x,step.y,0))
hinge=scene.objects['hinge gate_closed']
gate_mid=hinge.matrix_world @ Vector((0,math.sqrt(5)/2,0))
gate_px=pixel(gate_mid)
def distance(p,anchor):return math.dist(p,(anchor['pixel']['x'],anchor['pixel']['y']))
report={'sceneId':'gate','status':'geometry contract passes; decorative model registration pending','source':'art/blender/gate-geometry.blend','engineSha256':hashlib.sha256(engine_path.read_bytes()).hexdigest(),'method':'convex polygon intersection between actual Blender top faces and engine polygons, including full areas and boundaries','counts':{'board':len(cells),'blocked':len(blockers),'playable':len(cells)-len(blockers)},'maxCornerErrorPx':maximum_corner_error,'maxAreaErrorPx2':maximum_area_error,'areaTolerancePx2':.25,'mutationChecks':{'removedBlockerMissingAreaPx2':missing_error,'movedBlockerSpillAreaPx2':spill},'decorativeRegistration':{'status':'not aligned; contract anchors are not doorway claims','houseEntranceToStartPx':distance(step_px,engine['start']),'gateOpeningToGoalPx':distance(gate_px,engine['goal'])},'cells':cells}
(OUT/'gate-report.json').write_text(json.dumps(report,indent=2)+'\n')
# Vector diagnostic uses projected vertices from the .blend, NOT re-drawn engine fills.
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">','<rect width="100%" height="100%" fill="#faf4e6"/>','<g font-family="sans-serif" fill="#302b27">','<text x="60" y="75" font-size="34">Двор · геометрический контракт</text>','<text x="60" y="120" font-size="22">Заливка — грани из Blender. Синий контур — движок. Арт не проверяется этим листом.</text>']
solution={p['cellId'] for p in engine['solution']}
for cell in engine['cells']:
    ident=cell['id']; poly=polygons[ident]
    fill='#88684e' if cell['terrain'] else '#bba6d2' if ident in solution else '#e9e9cc'
    if ident==f"{engine['start']['q']},{engine['start']['r']}":fill='#94c5a5'
    if ident==f"{engine['goal']['q']},{engine['goal']['r']}":fill='#e5ad75'
    points=' '.join(f'{x:.5f},{y:.5f}' for x,y in poly)
    parts.append(f'<polygon points="{points}" fill="{fill}" stroke="#4c4237" stroke-width="1.5"/>')
    expected=' '.join(f"{p['x']:.5f},{p['y']:.5f}" for p in cell['polygon'])
    parts.append(f'<polygon points="{expected}" fill="none" stroke="#31658b" stroke-width="1" stroke-dasharray="5 3"/>')
    x=cell['center']['x']; y=cell['center']['y']
    label=html.escape(ident+(' · '+cell['terrain'] if cell['terrain'] else ''))
    parts.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="16" fill="{chr(35)}fff9eb"' + f'>{label}</text>' if cell['terrain'] else f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="16">{label}</text>')
parts+=['<text x="60" y="825" font-size="24">16 препятствий · 61 доступная клетка · 7 плит эталона</text>','<text x="60" y="870" font-size="22">Дом и калитка из первого арт-пилота пока не совмещены с этим контрактом.</text>','</g></svg>']
(OUT/'gate-contract.svg').write_text('\n'.join(parts)+'\n')
scene.render.engine='BLENDER_WORKBENCH'
scene.display.shading.color_type='OBJECT'; scene.display.shading.light='FLAT'
scene['geometryContract']='gate; full-cell masks from actual engine; decorative registration pending'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'art/blender/gate-geometry.blend'),compress=True)
print(json.dumps({k:v for k,v in report.items() if k!='cells'},indent=2))
