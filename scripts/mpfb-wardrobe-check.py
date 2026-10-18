"""Read-only native source invariants and evaluated 3D collision evidence."""
from pathlib import Path
from collections import Counter,defaultdict
import bpy,json,hashlib,os
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1]
VERSION=os.environ.get('RUBY_MPFB_WARDROBE_VERSION','v3')
OUT=ROOT/f'art/characters-mpfb-v1/tailored-wardrobe-{VERSION}'
SOURCE=ROOT/'art/characters-mpfb-v1/styled-body-pilot-v3/ruta-styled-body.blend'
def digest(value):return hashlib.sha256(repr(value).encode()).hexdigest()
def invariants():
    rig=next(o for o in bpy.data.objects if o.type=='ARMATURE' and len(o.data.bones)==167)
    body=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
    assets={}
    for name in ['Ruta ONE satchel','Satchel flap','Satchel buckle','ONE diagonal satchel strap']:
        o=bpy.data.objects[name];assets[name]=digest(([(tuple(v.co),[(g.group,g.weight) for g in v.groups]) for v in o.data.vertices],tuple(tuple(row) for row in o.matrix_basis)))
    action=rig.animation_data.action
    channels=[]
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                channels.extend([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation) for k in f.keyframe_points]) for f in bag.fcurves])
    return {'bodyRest':digest([tuple(v.co) for v in body.data.vertices]),'bodyWeights':digest([[(g.group,g.weight) for g in v.groups] for v in body.data.vertices]),'rigRest':digest([(b.name,tuple(b.head_local),tuple(b.tail_local),b.parent.name if b.parent else None) for b in rig.data.bones]),'motionAction':digest(channels),'actionName':action.name,'actionFrameRange':list(action.frame_range),'preservedAccessories':assets}
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));baseline=invariants()
bpy.ops.wm.open_mainfile(filepath=str(OUT/'ruta-tailored-source.blend'));current=invariants()
assert baseline==current,'native source invariant changed'
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE' and len(o.data.bones)==167)
body=bpy.data.objects['Ruta.MPFB.Body'];vest=bpy.data.objects['Ruta sewn fitted waistcoat']
edges=Counter(tuple(sorted(edge)) for p in vest.data.polygons for edge in p.edge_keys)
adj=defaultdict(set)
for (a,b),count in edges.items():
    if count==1:adj[a].add(b);adj[b].add(a)
components=0;seen=set()
for a in adj:
    if a in seen:continue
    components+=1;todo=[a];seen.add(a)
    while todo:
        for b in adj[todo.pop()]:
            if b not in seen:seen.add(b);todo.append(b)
weight_sums=[sum(g.weight for g in v.groups) for v in vest.data.vertices]
def world_bvh(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles();points=[ev.matrix_world@v.co for v in me.vertices];triangles=[tuple(t.vertices) for t in me.loop_triangles]
    tree=BVHTree.FromPolygons(points,triangles,all_triangles=True);ev.to_mesh_clear();return tree
frames=[f for f in [0,12,24,36,48,60] if baseline['actionFrameRange'][0]<=f<=baseline['actionFrameRange'][1]]
rows=[]
for frame in frames:
    bpy.context.scene.frame_set(frame);bpy.context.view_layer.update()
    objects={n:bpy.data.objects[n] for n in ['Ruta sewn fitted waistcoat','Ruta.male_casualsuit01','Ruta.MPFB.Body','Ruta ONE satchel','ONE diagonal satchel strap','Ruta.shoes01','Cream ankle cuff L','Cream ankle cuff R']}
    trees={n:world_bvh(o) for n,o in objects.items()}
    pairs=[('Ruta sewn fitted waistcoat','Ruta.male_casualsuit01'),('Ruta sewn fitted waistcoat','Ruta.MPFB.Body'),('Ruta sewn fitted waistcoat','Ruta ONE satchel'),('Ruta sewn fitted waistcoat','ONE diagonal satchel strap'),('Ruta.shoes01','Ruta.male_casualsuit01'),('Cream ankle cuff L','Ruta.MPFB.Body'),('Cream ankle cuff R','Ruta.MPFB.Body')]
    rows.append({'frame':frame,'evaluatedTriangleIntersectionPairs':{a+' / '+b:len(trees[a].overlap(trees[b])) for a,b in pairs}})
# Expose underlying native skin for a separate physical-fit check; never save it.
for mod in body.modifiers:
    if mod.name.startswith('Delete.'):mod.show_viewport=False
bpy.context.scene.frame_set(0);bpy.context.view_layer.update();bare=world_bvh(body)
physical={n:len(world_bvh(bpy.data.objects[n]).overlap(bare)) for n in ['Ruta sewn fitted waistcoat','Ruta.shoes01','Cream ankle cuff L','Cream ankle cuff R']}
report={'status':'source-check-evidence-not-automatic-art-approval','version':VERSION,'nativeInvariantsUnchanged':True,'invariants':current,'vestBaseBoundaryLoops':components,'expectedBaseBoundaryLoops':3,'vestWeightSumRange':[min(weight_sums),max(weight_sums)],'vestModifierOrder':[(m.name,m.type) for m in vest.modifiers],'samples':rows,'underlyingSkinFrame0Intersections':physical,'interpretation':'Triangle intersections reported directly; contacts/hidden native garment skin require visual interpretation. No candidate is declared passing on numeric counts alone.'}
(OUT/'geometry-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
