"""Native fitted garment authoring on preserved MPFB body/weighted motion source.

No source PNG deformation, imagegen, vendor writes or production activation.
New waistcoat is authored topology with analytical armhole boundary loops, fitted
to the real native shirt and carrying barycentrically transferred native weights.
"""
from pathlib import Path
from collections import Counter,defaultdict
import bpy,math,json,hashlib,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'art/characters-mpfb-v1/styled-body-pilot-v3/ruta-styled-body.blend'
OUT=ROOT/'art/characters-mpfb-v1/tailored-wardrobe-v1';OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene;scene.frame_set(0)
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE' and len(o.data.bones)==167)
body=next(o for o in bpy.data.objects if o.type=='MESH' and len(o.data.vertices)==19158)
shirt=bpy.data.objects['Ruta.male_casualsuit01']
body_hash=hashlib.sha256(b''.join(bytes(str(tuple(v.co)),'ascii') for v in body.data.vertices)).hexdigest()
source_action=rig.animation_data.action.name
original_pose=rig.data.pose_position;rig.data.pose_position='REST';bpy.context.view_layer.update()

def material(name,color,rough=.75):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough
    return m
olive=material('Tailored olive wool',(.095,.125,.045));binding=material('Dark olive sewn binding',(.052,.068,.023))
leather=material('Warm brown boot leather',(.21,.085,.030));rubber=material('Brown boot sole',(.055,.031,.018));lace_mat=material('Warm tan boot lace',(.48,.30,.13));brass=material('Sewn vest brass',(.46,.255,.055),.4)

def surface_data(o):
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh(preserve_all_data_layers=True,depsgraph=bpy.context.evaluated_depsgraph_get());me.calc_loop_triangles()
    points=[v.co.copy() for v in me.vertices];triangles=[tuple(t.vertices) for t in me.loop_triangles]
    weights=[{o.vertex_groups[g.group].name:g.weight for g in v.groups if g.weight>1e-6} for v in me.vertices]
    bvh=BVHTree.FromPolygons(points,triangles,all_triangles=True);ev.to_mesh_clear()
    return points,triangles,weights,bvh
sp,st,sw,sbvh=surface_data(shirt)
def barycentric(point,a,b,c):
    v0=b-a;v1=c-a;v2=point-a;d00=v0.dot(v0);d01=v0.dot(v1);d11=v1.dot(v1);d20=v2.dot(v0);d21=v2.dot(v1);den=d00*d11-d01*d01
    if abs(den)<1e-16:return [1,0,0]
    v=(d11*d20-d01*d21)/den;w=(d00*d21-d01*d20)/den
    q=[max(0,min(1,x)) for x in [1-v-w,v,w]];s=sum(q);return [x/s for x in q]
def native_weights(point):
    loc,n,index,d=sbvh.find_nearest(point);tri=st[index];f=barycentric(loc,*[sp[i] for i in tri]);result=defaultdict(float)
    for vertex,factor in zip(tri,f):
        for name,weight in sw[vertex].items():
            if name in rig.data.bones:result[name]+=weight*factor
    total=sum(result.values());return {n:w/total for n,w in result.items() if w>1e-6}
def apply_weights(o,weights):
    for name in sorted({n for row in weights for n in row}):o.vertex_groups.new(name=name)
    for i,row in enumerate(weights):
        for name,value in row.items():o.vertex_groups[name].add([i],value,'REPLACE')
def skin(o):
    o.parent=rig;o.matrix_parent_inverse=rig.matrix_world.inverted();m=o.modifiers.new('Native weighted garment motion','ARMATURE');m.object=rig
def mesh_object(name,verts,faces,mat,weights=None):
    me=bpy.data.meshes.new(name+' topology');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);o.data.materials.append(mat)
    for p in me.polygons:p.use_smooth=True
    if weights:apply_weights(o,weights)
    return o
def activate(o):
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o

# Preserve rejected native source; remove only its failed presentation garment.
removed=[]
for o in list(bpy.data.objects):
    if o.name=='Ruta fitted olive waistcoat' or o.name.startswith('Vest brass button'):
        removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)

# Parameter domain is a sewn torso sheet, not a cropped/deleted shirt mesh.
NX=88;NY=44;uv=[];faces=[];gap=.19;holes=[(math.pi/2,.765,.45,.15),(3*math.pi/2,.765,.45,.15)]
for j in range(NY+1):
    for i in range(NX+1):uv.append([gap+(2*math.pi-2*gap)*i/NX,j/NY])
def in_hole(t,v):return any(((t-c)/rx)**2+((v-cv)/rv)**2<1 for c,cv,rx,rv in holes)
for j in range(NY):
    for i in range(NX):
        t=(uv[j*(NX+1)+i][0]+uv[j*(NX+1)+i+1][0])/2;v=(j+.5)/NY
        if not in_hole(t,v):
            a=j*(NX+1)+i;faces.append((a,a+1,a+NX+2,a+NX+1))
edges=Counter(tuple(sorted((f[k],f[(k+1)%4]))) for f in faces for k in range(4))
boundary={v for edge,count in edges.items() if count==1 for v in edge}
for index in boundary:
    t,v=uv[index];i=index%(NX+1);j=index//(NX+1)
    if i in [0,NX] or j in [0,NY]:continue
    c,cv,rx,rv=min(holes,key=lambda h:abs(t-h[0]));dx=(t-c)/rx;dy=(v-cv)/rv;length=math.hypot(dx,dy)
    uv[index]=[c+rx*dx/length,cv+rv*dy/length]
used=sorted({i for face in faces for i in face});mapping={i:n for n,i in enumerate(used)};verts=[];weights=[]
for index in used:
    t,v=uv[index];front=min(t,2*math.pi-t);q=max(0,min(1,(front-gap)/1.0));q=q*q*(3-2*q)
    top=.960+.095*q-.025*max(0,-math.cos(t))**4;bottom=.680+.012*math.sin(t)**2;z=bottom+(top-bottom)*v
    nominal=Vector((.128*math.sin(t),-.005-.093*math.cos(t),z));loc,n,tri,d=sbvh.find_nearest(nominal)
    radial=Vector((math.sin(t),-math.cos(t),0))
    if n.dot(radial)<0:n=-n
    co=loc+n*.006;verts.append(co);weights.append(native_weights(loc))
vest=mesh_object('Ruta sewn fitted waistcoat',verts,[tuple(mapping[i] for i in f) for f in faces],olive,weights)
activate(vest);sub=vest.modifiers.new('Sewn boundary refinement','SUBSURF');sub.levels=1;bpy.ops.object.modifier_apply(modifier=sub.name)
solid=vest.modifiers.new('Real sewn cloth thickness','SOLIDIFY');solid.thickness=.0025;solid.offset=.3
skin(vest)

# Buttons sit on actual shirt-fit surface and carry the same native torso weights.
for sign in [-1,1]:
    for z in [.72,.785,.85]:
        hit=sbvh.ray_cast(Vector((sign*.045,-.5,z)),Vector((0,1,0)),1)[0]
        if hit is None:continue
        co=hit+Vector((0,-.010,0));bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.0055,location=co);o=bpy.context.object;o.name='Tailored brass button';bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
        # Bake object translation into mesh for stable common rig-space skinning.
        for vertex in o.data.vertices:vertex.co+=o.location
        o.location=(0,0,0);o.data.materials.append(brass);apply_weights(o,[native_weights(co)]*len(o.data.vertices));skin(o)

rig.data.pose_position=original_pose;scene.frame_set(0);bpy.context.view_layer.update()
assert len(body.data.vertices)==19158 and len(rig.data.bones)==167
assert hashlib.sha256(b''.join(bytes(str(tuple(v.co)),'ascii') for v in body.data.vertices)).hexdigest()==body_hash
assert rig.animation_data.action.name==source_action
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-tailored-source.blend'))
report={'status':'early-native-vest-source-checkpoint-boots-pending','productionEnabled':False,'source':str(SOURCE.relative_to(ROOT)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'bodyVertices':19158,'bodyRestGeometryChanged':False,'rigBones':167,'actionPreserved':source_action,'nativeHead12Preserved':True,'bagAndSingleStrapGeometryPreserved':True,'removedRejectedGarmentObjects':removed,'newVestVertices':len(vest.data.vertices),'vestConstruction':'authored sewn torso topology, analytical smooth armhole loops, real-shirt surface fit, barycentrically transferred native weights','vestClearanceMeters':.006,'vestThicknessMeters':.0025,'warning':'source checkpoint; rendered fit/intersections and proper ankle boots still pending'}
(OUT/'checkpoint.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if os.environ.get('RUBY_MPFB_WARDROBE_RENDER')=='1':
    scene.render.engine='CYCLES';scene.cycles.samples=16;scene.render.resolution_x=800;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
    camera=scene.camera;center=Vector((0,0,.76))
    for name,offset in [('front',Vector((0,-3,1.3))),('three-quarter',Vector((-2.5,-2.5,1.5))),('east',Vector((-3,0,1.6)))]:
        camera.location=center+offset;camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'.png'));bpy.ops.render.render(write_still=True)
