from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(O/'ruta-garment-uv-derivative.blend'))
print('LOADED',flush=True)
# Keep original palette-coordinate binding for all unpainted materials. RutaPaint remains stored but inactive.
for ob in bpy.data.objects:
 if ob.type=='MESH' and 'RutaPaint' in ob.data.uv_layers:
  original=next((u for u in ob.data.uv_layers if u.name!='RutaPaint'),None)
  if original:ob.data.uv_layers.active=original;original.active_render=True

sc=bpy.context.scene;rig=next(o for o in sc.objects if o.type=='ARMATURE' and 'Root' in o.data.bones)
def actions():
 return {a.name:hashlib.sha256(str([(fc.data_path,fc.array_index,[(tuple(k.co),k.interpolation)for k in fc.keyframe_points])for fc in a.fcurves]).encode()).hexdigest()for a in bpy.data.actions}
before=actions()

valid=json.load(open(O/'selected-texture-validation.json'));assert valid['oliveLikeInteriorFraction']==0
palette=json.load(open(O/'rejected-mixed-v1/palette-validation.json'))['perMaterial']
selected=[]
for row in palette:
 name=row['material']
 if row['erodedInteriorTexels']<1000 or name=='Ruta warm loose cargo cloth' or name=='Gold':continue
 expected='cream'if name=='Ruta cream shirt'else'olive'if name=='Ruta olive sleeveless vest'else'brown'
 ok=(row['creamLikeInteriorFraction']>.95)if expected=='cream'else(row['oliveLikeInteriorFraction']>.99)if expected=='olive'else(row['creamLikeInteriorFraction']<.01 and row['oliveLikeInteriorFraction']<.01 and row['backgroundLikeInteriorFraction']<.01)
 assert ok,(name,row)
 selected.append(name)
images={}
for key,path in [('mixed',O/'rejected-mixed-v1/painted-garment-uv-v1.png'),('trousers',O/'trousers-only/generated-v1/painted-trousers-uv-v1.png')]:
 images[key]=bpy.data.images.load(str(path));images[key].pack()
changed=[];materials={};kept=[]
for ob in sc.objects:
 if ob.type!='MESH' or 'RutaPaint'not in ob.data.uv_layers or ob.name.startswith('Ellie ready '):continue
 for slot in ob.material_slots:
  if not slot.material:continue
  old=slot.material;name=old.name
  if name not in selected and name!='Ruta warm loose cargo cloth':continue
  if ob.name.startswith('Ankle boot lace')or ob.name.startswith('Cream sock cuff'):kept.append(ob.name);continue
  key='trousers'if name=='Ruta warm loose cargo cloth'else'mixed'
  if name not in materials:
   mat=old.copy();mat.name='Ruta painted garment '+name;nt=mat.node_tree;nt.nodes.clear();output=nt.nodes.new('ShaderNodeOutputMaterial');diff=nt.nodes.new('ShaderNodeBsdfDiffuse');diff.inputs['Roughness'].default_value=.8;tex=nt.nodes.new('ShaderNodeTexImage');tex.image=images[key];uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map='RutaPaint';nt.links.new(uv.outputs['UV'],tex.inputs['Vector']);nt.links.new(tex.outputs['Color'],diff.inputs['Color']);nt.links.new(diff.outputs['BSDF'],output.inputs['Surface']);materials[name]=mat
  slot.material=materials[name];changed.append({'object':ob.name,'originalMaterial':name,'texture':key,'UVMap':'RutaPaint'})
(O/'partial-reuse-contract.json').write_text(json.dumps({'wholeMixedAtlasRejected':True,'trousersNeverUseMixed':True,'mixedReuseSelectedGroupsOnly':selected,'unchangedTinyLacesSocks':kept,'brassBowPreservedOriginal':True,'skinHeadHairPreservedOriginal':True,'bindings':changed},indent=2))
for a in bpy.data.actions:a.use_fake_user=True
contract=json.load(open(O.parent/'ruta-native-layered-walk48-v2/source-contract.json'));cam=contract['cameraVariants']['base']['fixedRenderCamera'];print('CAMERA',cam,flush=True)
sc.camera.matrix_world=Matrix(cam['matrixWorld']);sc.camera.data.type='ORTHO';sc.camera.data.ortho_scale=2.1
sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=32
rest=Vector(contract['rootRestGroundNative']);out=O/'renders';out.mkdir(exist_ok=True)
rows=[]
for name,phase,yaw,action in [('e-00',0,math.pi/2,'Walk_ProportionProposal'),('e-30',30,math.pi/2,'Walk_ProportionProposal'),('e-40',40,math.pi/2,'Walk_ProportionProposal'),('front-neutral',0,0,'Idle_Neutral_ProportionProposal'),('threequarter-neutral',0,math.pi/4,'Idle_Neutral_ProportionProposal')]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-rest);rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(phase*40/48),subframe=(phase*40/48)%1);bpy.context.view_layer.update();sc.render.filepath=str(out/(name+'.png'));print('RENDER',name,flush=True);bpy.ops.render.render(write_still=True);rows.append({'file':name+'.png','phase':phase,'yaw':yaw,'action':action})
assert before==actions();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-painted-garment-pilot.blend'))
(O/'pilot-contract.json').write_text(json.dumps({'status':'bounded-material-study-not-accepted-Ruta','changedMaterialsOnly':changed,'imageSHA256':valid['textureSHA256'],'actionHashesUnchanged':before,'renders':rows,'limitations':['Native profile/back-threequarter silhouette differs from accepted painted profile; UV cannot repair geometry','Original skin retained: generated skin edit failed moderation and was not retried','Hair UV edge coverage approximate; no UV warp or image cleanup']},indent=2));print('PILOT_DONE',flush=True)
