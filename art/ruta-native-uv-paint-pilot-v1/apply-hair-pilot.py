from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O/'ruta-native-uv-derivative.blend'))
print('LOADED',flush=True)
sc=bpy.context.scene;rig=next(o for o in sc.objects if o.type=='ARMATURE' and 'Root' in o.data.bones)
def actions():
 return {a.name:hashlib.sha256(str([(fc.data_path,fc.array_index,[(tuple(k.co),k.interpolation)for k in fc.keyframe_points])for fc in a.fcurves]).encode()).hexdigest()for a in bpy.data.actions}
before=actions()
mat=bpy.data.materials['ellie.hair_mesh'].copy();mat.name='Ellie ready Stable painted copper UV pilot';nt=mat.node_tree
im=bpy.data.images.load(str(O/'inputs/painted-hair-uv-v1.png'));im.pack();tex=nt.nodes.new('ShaderNodeTexImage');tex.image=im;uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='UVMap';nt.links.new(uv.outputs['UV'],tex.inputs['Vector']);g=nt.nodes.get('Group.009');assert g and g.node_tree.name=='SH-Hair';nt.links.new(tex.outputs['Color'],g.inputs['Base Color'])
diff=nt.nodes.new('ShaderNodeBsdfDiffuse');diff.inputs['Roughness'].default_value=.8;nt.links.new(tex.outputs['Color'],diff.inputs['Color']);output=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');nt.links.new(diff.outputs['BSDF'],output.inputs['Surface'])
changed=[]
for o in sc.objects:
 if o.type=='MESH' and (o.name=='Ellie ready Loose cap' or o.name.startswith('Ellie ready Layered wave ')):
  for slot in o.material_slots:
   if slot.material and slot.material.name=='ellie.hair_mesh':slot.material=mat
  changed.append(o.name)
assert len(changed)==19,len(changed)
for a in bpy.data.actions:a.use_fake_user=True
contract=json.load(open(O.parent/'ruta-native-layered-walk48-v2/source-contract.json'));cam=contract['cameraVariants']['base']['fixedRenderCamera'];print('CAMERA',cam,flush=True)
sc.camera.matrix_world=Matrix(cam['matrixWorld']);sc.camera.data.type='ORTHO';sc.camera.data.ortho_scale=2.1
sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
sc.render.engine='CYCLES';sc.cycles.samples=24
rest=Vector(contract['rootRestGroundNative']);out=O/'renders';out.mkdir(exist_ok=True)
rows=[]
for name,phase,yaw,action in [('e-00',0,math.pi/2,'Walk_ProportionProposal'),('e-30',30,math.pi/2,'Walk_ProportionProposal'),('e-40',40,math.pi/2,'Walk_ProportionProposal'),('front-neutral',0,0,'Idle_Neutral_ProportionProposal'),('threequarter-neutral',0,math.pi/4,'Idle_Neutral_ProportionProposal')]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-rest);rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(phase*40/48),subframe=(phase*40/48)%1);bpy.context.view_layer.update();sc.render.filepath=str(out/(name+'.png'));print('RENDER',name,flush=True);bpy.ops.render.render(write_still=True);rows.append({'file':name+'.png','phase':phase,'yaw':yaw,'action':action})
assert before==actions();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-native-painted-hair-pilot.blend'))
(O/'pilot-contract.json').write_text(json.dumps({'status':'bounded-material-study-not-accepted-Ruta','changedMaterialsOnly':changed,'imageSHA256':hashlib.sha256((O/'inputs/painted-hair-uv-v1.png').read_bytes()).hexdigest(),'actionHashesUnchanged':before,'renders':rows,'limitations':['Native profile/back-threequarter silhouette differs from accepted painted profile; UV cannot repair geometry','Original skin retained: generated skin edit failed moderation and was not retried','Hair UV edge coverage approximate; no UV warp or image cleanup']},indent=2));print('PILOT_DONE',flush=True)
