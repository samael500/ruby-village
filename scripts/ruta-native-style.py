"""Deterministic whole-mesh Ruta appearance study; no pose or PNG manipulation.

RUTA_STYLE_INPUT may point at the proportion author's committed blend.
RUTA_REST_MAP points at the matching old/new rest-bone transform JSON.
This script owns only art/ruta-native-style-v1. Never edits its input.
"""
from pathlib import Path
import bpy, bmesh, json, os, math, hashlib
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / os.environ.get('RUTA_STYLE_OUTPUT_DIR','art/ruta-native-style-v1')
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = Path(os.environ.get('RUTA_STYLE_INPUT', str(ROOT / 'art/ruta-native-proportions-study-v2/b-neutral/ruta-proportion-proposal.blend')))
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
scene = bpy.context.scene
rig = bpy.data.objects['CharacterArmature']
rig.matrix_world = Matrix.Identity(4)
rig.data.pose_position = 'REST'
bpy.context.view_layer.update()
rest_map_path = os.environ.get('RUTA_REST_MAP',str(ROOT/'art/ruta-native-proportions-study-v2/b-neutral/rest-transform-contract.json'))
rest_map = json.loads(Path(rest_map_path).read_text()) if rest_map_path else None

def action_hash():
    values = [(a.name, [(f.data_path, f.array_index, [(tuple(k.co), k.interpolation) for k in f.keyframe_points]) for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]) for a in bpy.data.actions]
    return hashlib.sha256(repr(values).encode()).hexdigest()

before_actions = action_hash()
added = []

def transform_source_point(point, bone):
    """Single rest-space transform, not a per-frame correction."""
    if not rest_map:
        return Vector(point)
    rows = rest_map.get('bones', rest_map)
    row = rows[bone]
    return Vector(row['newHead']) + float(row['scale']) * (Vector(point) - Vector(row['oldHead']))

def original_weighted_position(obj, vertex):
    if not rest_map:
        return vertex.co.copy()
    offset=Vector()
    scale=0.0
    total=sum(g.weight for g in vertex.groups)
    for g in vertex.groups:
        row=rest_map['bones'][obj.vertex_groups[g.group].name]
        w=g.weight/total
        s=float(row['scale'])
        offset+=w*(Vector(row['newHead'])-s*Vector(row['oldHead']))
        scale+=w*s
    return (vertex.co-offset)/scale

def material(name, rgb):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*rgb, 1)
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (*rgb, 1)
    bs.inputs['Roughness'].default_value = .85
    return m

cream = material('Ruta cream shirt', (.86, .77, .58))
olive = material('Ruta olive sleeveless vest', (.20, .24, .075))
brass = material('Ruta warm brass detail', (.63, .36, .065))
red = material('Ruta burgundy neck bow', (.36, .035, .032))
leather = material('Ruta satchel warm leather', (.25, .105, .032))
skin = material('Ruta warm round face', (.79, .49, .29))
hair_copper = material('Ruta chestnut copper hair', (.38, .115, .027))
hair_gold = material('Ruta warm copper hair highlights', (.52, .205, .055))
white = material('Ruta ivory eyes', (.99, .96, .85))
blue = material('Ruta blue iris', (.025, .30, .58))
pupil = material('Ruta warm black pupils', (.018, .012, .009))
cheek = material('Ruta subtle warm cheeks', (.66, .27, .17))

def bind_created(o, bone, mat):
    # Apply local construction transforms while still in original rest coordinates.
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    for v in o.data.vertices:
        v.co = transform_source_point(v.co, bone)
    o.parent = rig
    o.matrix_parent_inverse = Matrix.Identity(4)
    o.matrix_basis = Matrix.Identity(4)
    g = o.vertex_groups.new(name=bone)
    g.add(list(range(len(o.data.vertices))), 1, 'REPLACE')
    arm = o.modifiers.new('Same whole-body armature', 'ARMATURE')
    arm.object = rig
    o.data.materials.append(mat)
    for p in o.data.polygons:
        p.use_smooth = True
    added.append({'object': o.name, 'bone': bone, 'vertices': len(o.data.vertices)})
    return o

def ellipsoid(name, center, radius, mat, bone='Head'):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=1, location=center)
    o = bpy.context.object
    o.name = name
    o.scale = radius
    return bind_created(o, bone, mat)

def patch(name, vertices, faces, mat, bone='Chest'):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    scene.collection.objects.link(o)
    return bind_created(o, bone, mat)

def path(name, points, thickness, mat, bone, radii=None):
    curve = bpy.data.curves.new(name, 'CURVE')
    curve.dimensions = '3D'
    curve.bevel_depth = thickness
    curve.bevel_resolution = 3
    sp = curve.splines.new('BEZIER')
    sp.bezier_points.add(len(points)-1)
    for i,(p, co) in enumerate(zip(sp.bezier_points, points)):
        p.co = co
        p.handle_left_type = p.handle_right_type = 'AUTO'
        if radii:
            p.radius = radii[i]
    o = bpy.data.objects.new(name, curve)
    scene.collection.objects.link(o)
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target='MESH')
    return bind_created(bpy.context.object, bone, mat)

# Existing shoulder fabric becomes cream; the torso remains a separate olive vest.
body = bpy.data.objects.get('Adventurer_Body')
if body:
    for i, m in enumerate(body.data.materials):
        if m and m.name == 'Green':
            body.data.materials[i] = cream
        elif m and m.name == 'LightGreen':
            body.data.materials[i] = olive
    if cream.name not in body.data.materials:
        body.data.materials.append(cream)
    cream_index=next(i for i,m in enumerate(body.data.materials)if m==cream)
    source_positions=[original_weighted_position(body,v)for v in body.data.vertices]
    skin_index=next(i for i,m in enumerate(body.data.materials)if m and m.name=='Skin')
    hand_groups={g.index for g in body.vertex_groups if g.name.startswith(('Wrist.','Index','Middle','Ring','Pinky','Thumb'))}
    for polygon in body.data.polygons:
        center=sum((source_positions[i]for i in polygon.vertices),Vector())/len(polygon.vertices)
        hand_weight=sum(sum(g.weight for g in body.data.vertices[i].groups if g.group in hand_groups) for i in polygon.vertices)/len(polygon.vertices)
        if hand_weight>.25:
            polygon.material_index=skin_index
        elif abs(center.x)>.145 and center.z>1.39:
            polygon.material_index=cream_index

# Real 3D details follow the same rest transform and armature in every frame.
patch('Cream shirt V inside vest', [(-.059,-.199,1.513),(.059,-.199,1.513),(0,-.207,1.358)], [(0,1,2)], cream)
for i,z in enumerate([1.363,1.294,1.226]):
    ellipsoid(f'Vest brass button {i+1}', (-.026,-.198,z), (.010,.006,.010), brass, 'Chest')
patch('Left burgundy bow loop', [(0,-.221,1.481),(-.057,-.218,1.505),(-.050,-.229,1.453)], [(0,1,2)], red)
patch('Right burgundy bow loop', [(0,-.222,1.481),(.050,-.224,1.506),(.058,-.219,1.453)], [(0,1,2)], red)
ellipsoid('Burgundy bow knot', (0,-.229,1.480), (.015,.009,.016), red, 'Chest')
patch('Two burgundy bow tails', [(-.008,-.225,1.477),(-.033,-.218,1.415),(-.009,-.220,1.428),(.009,-.226,1.477),(.032,-.219,1.420),(.011,-.222,1.429)], [(0,1,2),(3,4,5)], red)

# Source mode preserves a ready artistic head supplied by the head owner.
head_mode=os.environ.get('RUTA_HEAD_MODE','procedural-study')
if head_mode!='source':
    # New whole 3D head/hair study. The old stock polygon face is not a painted likeness.
    # Replace the stock head as one part, rather than cutting a deformed face by a
    # height threshold from a different rest space.
    import bmesh
    head = bpy.data.objects.get('Adventurer_Head')
    if head:
        bpy.data.objects.remove(head,do_unlink=True)
    for o in list(scene.objects):
        if o.name == 'Ruta CC0 ginger waves':
            bpy.data.objects.remove(o,do_unlink=True)
    ellipsoid('Soft full neck join',(0,-.044,1.533),(.045,.044,.063),skin,'Neck')
    head_object=ellipsoid('Whole round storybook head', (0,-.066,1.661), (.109,.113,.125), skin)
    nose_object=ellipsoid('Small rounded nose', (0,-.183,1.652), (.014,.014,.017), skin)

    # One painted face texture on genuine 3D head geometry, shared by every pose.
    # Rest-space UVs and mask are fixed before animation; no screen-space face cards.
    face_texture=OUT/'textures/ruta-face-front-v1.png'
    if face_texture.exists():
        image=bpy.data.images.load(str(face_texture),check_existing=True)
        for obj in [head_object,nose_object]:
            uv=obj.data.uv_layers.new(name='Fixed front face projection')
            mask=obj.data.color_attributes.new(name='FaceFrontMask',type='FLOAT_COLOR',domain='POINT')
            row=rest_map['bones']['Head'] if rest_map else None
            old_positions=[]
            for v in obj.data.vertices:
                p=Vector(row['oldHead'])+(v.co-Vector(row['newHead']))/row['scale'] if row else v.co.copy()
                old_positions.append(p)
                amount=max(0,min(1,(-p.y-.060)/.052))
                mask.data[v.index].color=(amount,amount,amount,1)
            for loop in obj.data.loops:
                p=old_positions[loop.vertex_index]
                uv.data[loop.index].uv=((p.x+.110)/.220,(p.z-1.540)/.250)
        nt=skin.node_tree
        tex=nt.nodes.new('ShaderNodeTexImage')
        tex.image=image
        tex.extension='EXTEND'
        uv_node=nt.nodes.new('ShaderNodeUVMap')
        uv_node.uv_map='Fixed front face projection'
        nt.links.new(uv_node.outputs['UV'],tex.inputs['Vector'])
        attr=nt.nodes.new('ShaderNodeVertexColor')
        attr.layer_name='FaceFrontMask'
        mix=nt.nodes.new('ShaderNodeMixRGB')
        mix.inputs[1].default_value=(.79,.49,.29,1)
        nt.links.new(attr.outputs['Color'],mix.inputs[0])
        nt.links.new(tex.outputs['Color'],mix.inputs[2])
        nt.links.new(mix.outputs[0],nt.nodes.get('Principled BSDF').inputs['Base Color'])

    # Curved scalp surface and complete tapered wave meshes, fixed in head rest space.
    verts=[]
    faces=[]
    columns=64
    rings=16
    for j in range(rings+1):
        for i in range(columns):
            phi=2*math.pi*i/columns
            front=max(0,-math.sin(phi))
            limit=2.50-1.34*front**2
            theta=max(.002,limit*j/rings)
            ripple=1+.018*math.sin(phi*7+theta*2)
            verts.append((.124*math.sin(theta)*math.cos(phi)*ripple,-.061+.127*math.sin(theta)*math.sin(phi),1.668+.143*math.cos(theta)))
            if j:
                a=(j-1)*columns+i
                b=(j-1)*columns+(i+1)%columns
                c=j*columns+(i+1)%columns
                d=j*columns+i
                faces.append((a,b,c,d))
    patch('Soft copper hair crown',verts,faces,hair_copper,'Head')
    for side in [-1,1]:
        for layer in range(4):
            x=side*(.102+.009*layer)
            y=-.028+.025*layer
            points=[(side*.075,y,1.71),(x,y-.015,1.672),(x+side*.014,y+.008,1.59),(x-side*.007,y-.009,1.522),(x+side*.018,y+.018,1.463),(x+side*.004,y+.012,1.420+layer*.009)]
            path(f'Copper whole wave {side} {layer}',points,.025,hair_copper,'Head',[.75,1,1,.9,.65,.04])
            accent=[(p[0]+side*.008,p[1]-.018,p[2]+.002) for p in points]
            path(f'Copper wave fine highlight {side} {layer}',accent,.0028,hair_gold,'Head',[.1,.8,.8,.7,.4,.02])
    for i in range(4):
        path(f'Swept copper fringe {i}',[(-.052+i*.012,-.120,1.791),(.005+i*.015,-.166,1.766),(.074+i*.008,-.158,1.714),(.110+i*.003,-.112,1.663)],.013,hair_copper,'Head',[.7,1,1,.04])

    # Deliberate sparse crown strands instead of a woodgrain/noise pattern.
    for i in range(28):
        phi=2*math.pi*i/28
        front=max(0,-math.sin(phi))
        limit=2.50-1.34*front**2
        points=[]
        for j in range(7):
            theta=.20+(limit-.20)*j/6
            points.append((.125*math.sin(theta)*math.cos(phi),-.061+.128*math.sin(theta)*math.sin(phi),1.668+.144*math.cos(theta)))
        path(f'Fine crown strand {i}',points,.0009,hair_gold,'Head',[.04,.6,.8,.8,.7,.5,.04])

    # Procedural eye fallback is only for absent texture; final study uses a shared
    # painted UV texture instead of oversized separate eyeballs.
    for side in ([] if face_texture.exists() else [-1,1]):
        x = side*.050
        ellipsoid(f'Ivory eye {side}', (x,-.171,1.686), (.031,.016,.027), white)
        ellipsoid(f'Blue iris {side}', (x,-.186,1.686), (.016,.006,.020), blue)
        ellipsoid(f'Pupil {side}', (x,-.192,1.686), (.007,.003,.012), pupil)
        ellipsoid(f'Eye highlight {side}', (x-.005,-.195,1.693), (.004,.002,.005), white)
        path(f'Soft upper eyelid {side}', [(x-.028,-.174,1.692),(x,-.188,1.713),(x+.028,-.174,1.692)], .0028, leather, 'Head')
        path(f'Soft eyebrow {side}',[(x-.025,-.163,1.721),(x,-.172,1.729),(x+.024,-.163,1.723)],.003,hair_copper,'Head')
    if not face_texture.exists():
        path('Friendly small smile', [(-.025,-.162,1.618),(0,-.174,1.611),(.025,-.162,1.618)], .002, leather, 'Head')

for name in ['ONE hip satchel','Satchel flap','Satchel buckle']:
    o=bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o,do_unlink=True)
def rounded_box(name,center,size,radius,mat,bone='Hips'):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center)
    o=bpy.context.object
    o.name=name
    o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    bevel=o.modifiers.new('Rounded leather silhouette','BEVEL')
    bevel.width=radius
    bevel.segments=5
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    return bind_created(o,bone,mat)
rounded_box('ONE rounded right hip satchel',(-.225,-.004,.985),(.205,.12,.195),.042,leather)
rounded_box('Single rounded satchel flap',(-.225,-.073,1.026),(.207,.024,.113),.025,leather)
rounded_box('Satchel warm brass clasp',(-.225,-.090,1.006),(.029,.012,.034),.005,brass)

# The approved outfit has loose cargo trousers and ankle boots, not knee boots.
trousers=bpy.data.objects.get('Ruta stock long trousers')
if trousers:
    trouser_mat=material('Ruta warm loose cargo cloth',(.28,.16,.079))
    trousers.data.materials.clear()
    trousers.data.materials.append(trouser_mat)
    for v in trousers.data.vertices:
        weights={trousers.vertex_groups[g.group].name:g.weight for g in v.groups}
        leg=max(((n,w)for n,w in weights.items()if n.startswith(('UpperLeg.','LowerLeg.'))),key=lambda x:x[1],default=None)
        if leg:
            bone=rig.data.bones[leg[0]]
            axis=bone.tail_local-bone.head_local
            center=bone.head_local+axis*((v.co-bone.head_local).dot(axis)/axis.length_squared)
            radial=v.co-center
            # Rest-mesh tailoring only; weights, animation and all rendered poses stay native.
            v.co=center+Vector((radial.x*1.40,radial.y*1.25,radial.z))
boots=bpy.data.objects.get('Adventurer_Feet')
if boots:
    cut=transform_source_point((0,0,.315),'Foot.L').z
    bm=bmesh.new()
    bm.from_mesh(boots.data)
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=.000001)
    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),plane_co=(0,0,cut),plane_no=(0,0,1),dist=.000001,clear_outer=True,clear_inner=False)
    cap_edges=[e for e in bm.edges if e.is_boundary and all(abs(v.co.z-cut)<.00001 for v in e.verts)]
    if cap_edges:
        bmesh.ops.holes_fill(bm,edges=cap_edges,sides=0)
    bm.to_mesh(boots.data)
    bm.free()
    for v in boots.data.vertices:
        side='L' if v.co.x>0 else 'R'
        center=rig.data.bones[f'Foot.{side}'].head_local.x
        v.co.x=center+(v.co.x-center)*1.3
for side,label in [(-1,'R'),(1,'L')]:
    center=side*.110
    # One continuous tied lace on each whole native 3D boot.
    points=[]
    for j in range(5):
        z=.275-j*.035
        y=[-.101,-.102,-.103,-.108,-.130][j]
        points.append((center+(-.025 if j%2 else .025),y,z))
    path(f'Ankle boot lace {label}',points,.0018,cream,f'Foot.{label}')
    cuff_vertices=[]
    cuff_faces=[]
    for j,z in enumerate([.315,.338]):
        for k in range(24):
            a=2*math.pi*k/24
            cuff_vertices.append((center+.050*math.cos(a),-.036+.064*math.sin(a),z))
            if j:
                cuff_faces.append((k,(k+1)%24,24+(k+1)%24,24+k))
    patch(f'Cream sock cuff {label}',cuff_vertices,cuff_faces,cream,f'LowerLeg.{label}')
    pocket_mat=material(f'Cargo pocket cloth {label}',(.25,.135,.064))
    rounded_box(f'Cargo side pocket {label}',(side*.170,-.035,.745),(.046,.116,.153),.012,pocket_mat,f'UpperLeg.{label}')

# A fixed rest-space head attitude exposes the young face to the map camera.
# This is one mesh construction transform, not an animation or frame adjustment.
head_tilt_degrees=0.0 if head_mode=='source' else float(os.environ.get('RUTA_HEAD_REST_TILT_DEG','10'))
pivot=rig.data.bones['Head'].head_local.copy()
head_rotation=Matrix.Rotation(math.radians(-head_tilt_degrees),3,'X')
for row in added:
    if row['bone']=='Head':
        for v in bpy.data.objects[row['object']].data.vertices:
            v.co=pivot+head_rotation@(v.co-pivot)

# Smooth shared-position normals without welding, preserving the deformation weights.
for o in scene.objects:
    if o.type != 'MESH' or o.parent != rig:
        continue
    if head_mode=='source' and o.name.startswith('Ellie ready '):
        continue
    o.data.update()
    normals = {}
    for p in o.data.polygons:
        p.use_smooth = True
        for i in p.vertices:
            key = tuple(round(c,6) for c in o.data.vertices[i].co)
            normals[key] = normals.get(key,Vector()) + p.normal*p.area
    o.data.normals_split_custom_set_from_vertices([normals[tuple(round(c,6) for c in v.co)].normalized() for v in o.data.vertices])

# Eevee toon shading keeps source texture/alpha links, including actual hair alpha.
source_head_materials={m for o in scene.objects if head_mode=='source' and o.name.startswith('Ellie ready ') for m in o.data.materials if m}
for m in list(bpy.data.materials):
    if m in source_head_materials:
        continue
    if not m.use_nodes:
        continue
    nt = m.node_tree
    bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if not bs:
        continue
    base = bs.inputs['Base Color']
    color = tuple(base.default_value)
    base_link = base.links[0].from_socket if base.is_linked else None
    alpha = bs.inputs['Alpha']
    opacity = alpha.default_value
    alpha_link = alpha.links[0].from_socket if alpha.is_linked else None
    diffuse = nt.nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.inputs['Color'].default_value = (.8,.8,.8,1)
    rgb = nt.nodes.new('ShaderNodeShaderToRGB')
    nt.links.new(diffuse.outputs[0],rgb.inputs[0])
    lighting_scale=nt.nodes.new('ShaderNodeMath')
    lighting_scale.operation='MULTIPLY'
    lighting_scale.inputs[1].default_value=.55
    nt.links.new(rgb.outputs[0],lighting_scale.inputs[0])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.interpolation = 'EASE'
    ramp.color_ramp.elements[0].position = .1
    ramp.color_ramp.elements[0].color = (.46,.34,.28,1)
    ramp.color_ramp.elements[1].position = .78
    ramp.color_ramp.elements[1].color = (1,.97,.88,1)
    e = ramp.color_ramp.elements.new(.43)
    e.color = (.79,.71,.59,1)
    nt.links.new(lighting_scale.outputs[0],ramp.inputs[0])
    mul = nt.nodes.new('ShaderNodeMixRGB')
    mul.blend_type = 'MULTIPLY'
    mul.inputs[0].default_value = 1
    mul.inputs[1].default_value = color
    if base_link:
        nt.links.new(base_link,mul.inputs[1])
    nt.links.new(ramp.outputs[0],mul.inputs[2])
    emission = nt.nodes.new('ShaderNodeEmission')
    nt.links.new(mul.outputs[0],emission.inputs[0])
    trans = nt.nodes.new('ShaderNodeBsdfTransparent')
    mix = nt.nodes.new('ShaderNodeMixShader')
    mix.inputs[0].default_value = opacity
    if alpha_link:
        nt.links.new(alpha_link,mix.inputs[0])
    nt.links.new(trans.outputs[0],mix.inputs[1])
    nt.links.new(emission.outputs[0],mix.inputs[2])
    output = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL')
    nt.links.new(mix.outputs[0],output.inputs['Surface'])

scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 768
scene.render.resolution_y = 960
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.view_settings.view_transform = 'Standard'
scene.view_settings.look = 'Medium High Contrast'
scene.view_settings.exposure = 0
scene.view_settings.gamma = 1
rig.data.pose_position = 'POSE'
for t in rig.animation_data.nla_tracks:
    t.mute = True
action_name = os.environ.get('RUTA_STYLE_ACTION', 'Idle_Neutral_ProportionProposal')
action = bpy.data.actions[action_name]
rig.animation_data.action = action
rig.animation_data.action_slot = action.slots[0]
scene.frame_set(0)
assert before_actions == action_hash(), 'Appearance must not alter motion curves'
ground_root=rig.data.bones['Root'].head_local.copy()
ground_root.z=0
rig.matrix_world=Matrix.Translation(-ground_root)
bpy.context.view_layer.update()
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-native-style.blend'),compress=True)
views=[]
if os.environ.get('RUTA_STYLE_RENDER','1') == '1':
    for name,yaw in [('front',0),('three-quarter',math.pi/4),('e',math.pi/2)]:
        rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-ground_root)
        scene.frame_set(0)
        bpy.context.view_layer.update()
        q=world_to_camera_view(scene,scene.camera,rig.matrix_world@rig.pose.bones['Root'].head)
        views.append({'view':name,'yaw':yaw,'rootPx':[q.x*768,(1-q.y)*960]})
        scene.render.filepath = str(OUT/f'{name}-00.png')
        bpy.ops.render.render(write_still=True)
(OUT/'appearance.json').write_text(json.dumps({'status':'deterministic-native-appearance-study-not-approved','productionEnabled':False,'source':str(SOURCE),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'restMap':rest_map_path,'actionsHashBefore':before_actions,'actionsHashAfter':action_hash(),'headMode':head_mode,'headRestTiltDegrees':head_tilt_degrees,'rootTransform':'Rz(yaw)*T(-RootRestGround)','views':views,'newObjects':added,'changes':(['ready authored head geometry, UVs, normals and shaders preserved'] if head_mode=='source' else ['whole 3D head replacement and fixed rest-space UV face texture','Head-bound native copper wave meshes'])+['Chest-bound bow/buttons; one rounded Hips-bound bag with original single diagonal strap','rest-space cargo trouser tailoring and sleeve material assignment','native boot mesh welded/bisected/capped to ankle height, with bound cuffs and laces'],'limitations':['An appearance study, not final painted art','Proportions must come from independently reviewed whole-rig shape branch','Camera/origins and actual game walking are not yet accepted','No imagegen per-frame repaint, image warp or per-frame scale used']},indent=2)+'\n')
