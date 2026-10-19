"""Single native rest-proportion proposal. Original actions preserved; no raster manipulation."""
from pathlib import Path
import bpy,json,math,hashlib,os,re
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ruta-native-proportions-v1';SOURCE=ROOT/'art/ready-character-adapted-v1/ruta-stock-adapted.blend'
BODY=float(os.environ.get('RUTA_BODY_SCALE','.70'));HEAD=float(os.environ.get('RUTA_HEAD_SCALE','1.60'));ARM=float(os.environ.get('RUTA_ARM_SCALE','.63'))
def digest(v):return hashlib.sha256(repr(v).encode()).hexdigest()
def curves(a):return [f for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]
def actionhash(a):return digest([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for f in curves(a)])
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.matrix_world=Matrix.Identity(4)
for t in rig.animation_data.nla_tracks:t.mute=True
rig.data.pose_position='REST';bpy.context.view_layer.update();meshobjects=[o for o in sc.objects if o.type=='MESH' and o.parent==rig];old={b.name:{'head':b.head_local.copy(),'tail':b.tail_local.copy(),'parent':b.parent.name if b.parent else None,'length':b.length}for b in rig.data.bones};sourcehashes={a.name:actionhash(a)for a in bpy.data.actions};weights_before=digest([(o.name,[[(g.group,g.weight)for g in v.groups]for v in o.data.vertices])for o in meshobjects]);counts={o.name:[len(o.data.vertices),len(o.data.polygons)]for o in meshobjects}
def scale(name):
 if name in ['Head','Neck']:return HEAD
 if name.startswith(('UpperArm.','LowerArm.')):return ARM
 if name.startswith('Wrist.'):return ARM*.95238095238
 if name.startswith(('Thumb','Index','Middle','Ring','Pinky')):return ARM*.873015873
 return BODY
new={}
for b in rig.data.bones:
 v=old[b.name];par=v['parent'];head=(new[par]['head']+(v['head']-old[par]['head'])*scale(par))if par else v['head']*BODY;new[b.name]={'head':head,'tail':head+(v['tail']-v['head'])*scale(b.name)}
def transform(p,name):return new[name]['head']+(p-old[name]['head'])*scale(name)
def usedbounds(objects):
 pts=[]
 for o in objects:
  used={i for f in o.data.polygons for i in f.vertices};pts.extend(o.data.vertices[i].co for i in used)
 return [[min(v[j]for v in pts),max(v[j]for v in pts)]for j in range(3)]
before={'body':usedbounds(meshobjects),'headMesh':usedbounds([bpy.data.objects['Adventurer_Head']]),'hair':usedbounds([bpy.data.objects['Ruta CC0 ginger waves']])}
# Same continuous weight-blended rest transform for every whole mesh, including garments/bag/hair.
for o in meshobjects:
 names={g.index:g.name for g in o.vertex_groups}
 for v in o.data.vertices:
  ws=[(names[g.group],g.weight)for g in v.groups if names[g.group]in old and g.weight>0];total=sum(w for n,w in ws);p=v.co.copy();v.co=sum((transform(p,n)*w for n,w in ws),Vector())/total if total else p*BODY
 # No welding, topology or skin weights changed.
 normals={}
 for poly in o.data.polygons:
  poly.use_smooth=True
 o.data.update()
 for poly in o.data.polygons:
  for vi in poly.vertices:
   key=tuple(round(c,6)for c in o.data.vertices[vi].co);normals[key]=normals.get(key,Vector())+poly.normal*poly.area
 o.data.normals_split_custom_set_from_vertices([normals.get(tuple(round(c,6)for c in v.co),Vector((0,0,1))).normalized()for v in o.data.vertices])
bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
for b in rig.data.edit_bones:b.head=new[b.name]['head'];b.tail=new[b.name]['tail']
bpy.ops.object.mode_set(mode='OBJECT');after={'body':usedbounds(meshobjects),'headMesh':usedbounds([bpy.data.objects['Adventurer_Head']]),'hair':usedbounds([bpy.data.objects['Ruta CC0 ginger waves']])}
retarget={}
for source_name in ['Walk','Idle_Neutral']:
 a=bpy.data.actions[source_name].copy();a.name=source_name+'_ProportionProposal';changed=[]
 for f in curves(a):
  match=re.match(r'pose.bones\["(.+)"\]\.location$',f.data_path)
  if not match:continue
  name=match.group(1);factor=scale(old[name]['parent'])if old[name]['parent'] else BODY
  for k in f.keyframe_points:k.co.y*=factor;k.handle_left.y*=factor;k.handle_right.y*=factor
  changed.append({'bone':name,'axis':f.array_index,'factor':factor})
 original=bpy.data.actions[source_name];assert [(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for f in curves(a)if'rotation'in f.data_path]==[(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for f in curves(original)if'rotation'in f.data_path]
 retarget[source_name]={'action':a.name,'hash':actionhash(a),'translationChannels':changed,'rotationCurvesExactlyPreserved':True,'keyframeTimesUnchanged':True}
assert all(actionhash(bpy.data.actions[name])==h for name,h in sourcehashes.items());assert weights_before==digest([(o.name,[[(g.group,g.weight)for g in v.groups]for v in o.data.vertices])for o in meshobjects]);assert counts=={o.name:[len(o.data.vertices),len(o.data.polygons)]for o in meshobjects}
rig.data.pose_position='POSE';a=bpy.data.actions[retarget['Walk']['action']];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0];sc.frame_set(0);p=rig.data.bones['Root'].head_local.copy();p.z=0;rig.matrix_world=Matrix.Translation(-p);bpy.context.view_layer.update()
# Lightweight warm native shading; root owns detailed material/accessory styling.
sc.render.engine='BLENDER_EEVEE_NEXT';sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.render.film_transparent=True
sc.view_settings.view_transform='Standard';sc.view_settings.look='Medium High Contrast'
for m in bpy.data.materials:
 if m.use_nodes:
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs:bs.inputs['Roughness'].default_value=.9
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'ruta-proportion-proposal.blend'))
contract={'status':'UNAPPROVED-native-rest-proportion-proposal-not-runtime','source':str(SOURCE.relative_to(ROOT)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'parameters':{'body':BODY,'headNeck':HEAD,'upperLowerArm':ARM,'wrist':ARM*.95238095238,'fingers':ARM*.873015873},'restTransform':'T_b(p)=newHead_b+s_b*(p-oldHead_b); newHead_b=newHead_parent+s_parent*(oldHead_b-oldHead_parent); rest vertices blended with unchanged normalized source weights','bones':{n:{'oldHead':list(v['head']),'oldTail':list(v['tail']),'newHead':list(new[n]['head']),'newTail':list(new[n]['tail']),'scale':scale(n),'parent':v['parent']}for n,v in old.items()},'restMeshBoundsBefore':before,'restMeshBoundsAfter':after,'originalActionsHashes':sourcehashes,'originalActionsUntouched':True,'retargetedActions':retarget,'weightsAndTopologyUnchanged':True,'bodyReference':'not frozen; root will calibrate after silhouette acceptance','limitations':['proposal proportions awaiting independent reference measurements','same source timing and rotation curves, changed translations/rest lengths mean changed motion metrics','no exact original-motion/no-slip claim','stock simple face, boot geometry, green shirt and single original satchel remain for separate root styling','no raster deformation or per-frame adjustments'],'views':[]}
(OUT/'rest-transform-contract.json').write_text(json.dumps(contract,indent=2)+'\n')
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-p);bpy.context.view_layer.update();q=world_to_camera_view(sc,sc.camera,rig.matrix_world@rig.pose.bones['Root'].head);sc.render.filepath=str(OUT/(name+'-walk00.png'));bpy.ops.render.render(write_still=True);contract['views'].append({'view':name,'frame':0,'yaw':yaw,'rootPx':[q.x*512,(1-q.y)*640]})
(OUT/'rest-transform-contract.json').write_text(json.dumps(contract,indent=2)+'\n');print('PROPORTION_PROPOSAL_TWO_VIEWS_READY',flush=True)
