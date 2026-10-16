"""Ray-test full hex interiors at a 4px lattice, plus all corners and edges.
This reports visible solid-mesh occlusion, not shadows, foliage motion or production hit-test.
"""
import json
import math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
scene=bpy.context.scene
for name in ['verification','ruta','stones','gate_open']:
    bpy.data.collections[name].hide_viewport=True
def check(state):
    bpy.data.collections['gate_open'].hide_viewport=state!='open'
    bpy.data.collections['gate_closed'].hide_viewport=state=='open'
    bpy.context.view_layer.update()
    deps=bpy.context.evaluated_depsgraph_get()
    # One world-space BVH avoids testing thousands of separate objects per ray.
    vertices=[]; polygons=[]; owners=[]
    ground_names={'continuous ground'}
    for obj in deps.objects:
        if obj.type not in ['MESH','CURVE'] or obj.hide_get():continue
        if obj.get('surfaceRole')=='walkable_ground':ground_names.add(obj.name)
        evaluated=obj.evaluated_get(deps)
        data=evaluated.to_mesh()
        offset=len(vertices)
        vertices.extend(obj.matrix_world @ v.co for v in data.vertices)
        polygons.extend(tuple(offset+i for i in face.vertices) for face in data.polygons)
        owners.extend([obj.name]*len(data.polygons))
        evaluated.to_mesh_clear()
    bvh=BVHTree.FromPolygons(vertices,polygons)
    print('BVH ready:',len(vertices),'vertices',flush=True)
    logic=json.loads((ROOT/'src/chapter-1.logical.json').read_text())['gate']
    direction=Vector((0,math.sqrt(1-.65**2),-.65))
    report=[]; total=0; cells=0
    for row in range(7):
        for col in range(11):
            q=col-row//2
            if f'{q},{row}' in logic['terrain']:continue
            cx=140+math.sqrt(3)*70*(q+row/2); cy=290+68.25*row
            points=[(cx,cy)]
            vertices=[(cx+70*math.cos(math.radians(30+i*60)),cy+.65*70*math.sin(math.radians(30+i*60))) for i in range(6)]
            for a,b in zip(vertices,vertices[1:]+vertices[:1]):
                points.extend((a[0]*(1-t/20)+b[0]*t/20,a[1]*(1-t/20)+b[1]*t/20) for t in range(21))
            def inside(x,y):
                crosses=[(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0]) for a,b in zip(vertices,vertices[1:]+vertices[:1])]
                return min(crosses)>=-.001 or max(crosses)<=.001
            for x in range(math.floor(cx-61),math.ceil(cx+61),4):
                for y in range(math.floor(cy-46),math.ceil(cy+46),4):
                    if inside(x,y):points.append((x,y))
            total+=len(points); cells+=1
            hits={}
            for px,py in points:
                floor=Vector(((px-140)/100,(290-py)/65,0))
                loc,normal,face,distance=bvh.ray_cast(floor-direction*40,direction,80)
                if face is not None and owners[face] not in ground_names:
                    name=owners[face]; hits[name]=hits.get(name,0)+1
            if hits: report.append({'cell':{'q':q,'r':row},'samples':len(points),'occludedSamples':sum(hits.values()),'objects':hits})
    return {'cellsWithOcclusion':report,'samples':total,'checkedCells':cells}
out={'method':'orthographic rays; 4px interior lattice + 20 subdivisions per edge; excludes Ruta and verification; not pixel-exact proof','states':{state:check(state) for state in ['closed','open']},'blockedCellsIgnored':True}
(ROOT/'docs/blender-chapter-1/geometry-report.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
assert all(not value['cellsWithOcclusion'] for value in out['states'].values()), 'Scenery overlaps playable cells'
