"""Authorized12 actual E-camera diagnostic poses after native contact/joins pass."""
from pathlib import Path
import os
import bpy,json,math,hashlib,os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('RUBY_MPFB_PIVOT_VARIANT','right60');assert VARIANT in ['right60','left120','right120'];OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-variants'/VARIANT;meta=json.loads((OUT/'manifest.json').read_text());check=json.loads((OUT/'native-contact-join-check.json').read_text());assert check['summary']['nativeFeasibilityPass'];carry=json.loads((OUT/'carry-check.json').read_text());assert carry['armBagAndGripPass'];surface=json.loads((OUT/'boot-surface-check.json').read_text());assert surface['maximumBootIntersectionPairs']==0;source=OUT/'mpfb-compact-pivot-technical.blend';before=hashlib.sha256(source.read_bytes()).hexdigest();assert before==check['sourceSha256Before']==surface['sourceSha256Before']==carry['sourceSha256Before'];bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera
for name,action in meta['turnActions'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
def set_frame(value):scene.frame_set(int(value),subframe=value-int(value));bpy.context.view_layer.update()
def project(point):
 q=world_to_camera_view(scene,camera,point);return [384*q.x,384*(1-q.y)]
# Actual saved action key positions/tangents, distinct from analytic generation plans.
keys=sorted({p.co.x for c in rig.animation_data.action.fcurves if c.data_path=='location'for p in c.keyframe_points});path=[]
for f in keys:set_frame(f);path.append({'frame':f,'timeMs':30*(f-1),'rootNativeMeters':list(rig.matrix_world.translation),'headingRadians':rig.rotation_euler.z})
length=0.;radii=[]
for i,p in enumerate(path):
 a=Vector(path[max(0,i-1)]['rootNativeMeters']);b=Vector(path[min(len(path)-1,i+1)]['rootNativeMeters']);d=b-a;p['sampledTangentNative']=list(d.normalized())
 if i:length+=(Vector(p['rootNativeMeters'])-Vector(path[i-1]['rootNativeMeters'])).length
 if 0<i<len(path)-1:
  b=Vector(p['rootNativeMeters']);c=Vector(path[i+1]['rootNativeMeters']);cross=(b-a).cross(c-a).length
  if cross>1e-10:radii.append((b-a).length*(c-b).length*(c-a).length/(2*cross))
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True;scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.render.film_transparent=True;camera.data.type='ORTHO';camera.data.ortho_scale=1.70;elev=math.asin(.65);records=[]
for obj in scene.objects:
 if obj.type=='MESH':
  for modifier in obj.modifiers:
   if modifier.type=='SUBSURF':modifier.levels=modifier.render_levels
cache={}
checkpoint_file=OUT/'raster-checkpoint.json'
if checkpoint_file.exists():
 checkpoint=json.loads(checkpoint_file.read_text())
 if checkpoint.get('sourceSha256')==before:
  cache={r['frame']:r for r in checkpoint.get('records',[]) if (OUT/'E'/f"{r['frame']:02}.png").exists() and hashlib.sha256((OUT/'E'/f"{r['frame']:02}.png").read_bytes()).hexdigest()==r['sha256']}
for f in ([1,5,9,13,17,21,25,29,33,35,39,41] if meta.get('segments',1)==1 else [1,9,17,25,33,41,49,57,65,69,77,81]):
 if f in cache:records.append(cache[f]);continue
 set_frame(f);center=rig.location+Vector((0,0,.68));camera.location=center+Vector((-4*math.cos(elev),0,4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);root=rig.matrix_world.translation;rec={'frame':f,'timeMs':30*(f-1),'headingRadians':rig.rotation_euler.z,'actualRootNativeMeters':list(root),'rootGroundAnchorPixels':project(root),'actualFootBoneWorld':{s:list(er.matrix_world@er.pose.bones['foot.'+s].head)for s in ['L','R']},'actualFootBoneProjectionPixels':{s:project(er.matrix_world@er.pose.bones['foot.'+s].head)for s in ['L','R']}};rec['actualRenderLevelGeometryXYBounds']={}
 for obj in scene.objects:
  if obj.type!='MESH' or obj.hide_render:continue
  evaluated=obj.evaluated_get(deps);points=[evaluated.matrix_world@v.co for v in evaluated.data.vertices]
  if not points:continue
  rec['actualRenderLevelGeometryXYBounds'][obj.name]={'vertices':len(points),'worldXYBoundsMeters':[[min(v[i] for v in points),max(v[i] for v in points)] for i in range(2)],'maxWorldXYRadiusFromPivotOriginMeters':max((v.x*v.x+v.y*v.y)**.5 for v in points)}
 scene.render.filepath=str(OUT/'E'/f'{f:02}.png');bpy.ops.render.render(write_still=True);rec['sha256']=hashlib.sha256((OUT/'E'/f'{f:02}.png').read_bytes()).hexdigest();records.append(rec);checkpoint={'status':'INCREMENTAL TECHNICAL RASTER CHECKPOINT','sourceSha256':before,'variant':VARIANT,'records':records};temporary=OUT/'raster-checkpoint.tmp';temporary.write_text(json.dumps(checkpoint,indent=2)+'\n');temporary.replace(OUT/'raster-checkpoint.json')
result={'status':'ACTUAL12POSE DIAGNOSTIC; AUTHOR/INDEPENDENT TURN NATURALNESS REVIEW PENDING','appearance':'rejected generic technical mannequin','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(source.read_bytes()).hexdigest(),'camera':{'view':'fixed-world E orientation, follows rig translation only','frameSize':[384,384],'orthoScaleMeters':1.70,'groundScale':.65,'nativeHeightReferencePx':251,'displayHeightReferencePx':136},'actualPath':path,'actualSavedKeyPolylineLengthMeters':length,'actualMinimumDiscreteCircumradiusMeters':min(radii) if radii else None,'pathNote':'Actual compact root balance curve, not a moving-arc fillet. No constant-radius or exact C1 saved-curve claim.','entryTangentNative':path[0]['sampledTangentNative'],'exitTangentNative':path[-1]['sampledTangentNative'],'renderedFrames':records,'variant':VARIANT,'durationMs':meta['durationMs'],'stepCount':2*meta.get('segments',1),'supportMetadata':'planning-input.json actual pivot support modes; no walk-phase contract','geometryBoundsScope':'Actual render-level evaluated geometry at12 diagnostic poses only, not a certified continuous body/bag sweep.','routeConstraints':'Native stopped flat-idle pivot candidate. Requires stop+settle before pivot and new start afterward. Root bound does not certify full body/bag one-hex clearance or arbitrary legal routes. No puzzle/solver changes, stride scaling, root retiming or endpoint sliding.'};assert result['sourceSha256Before']==result['sourceSha256After'];(OUT/'raster-path-metadata.json').write_text(json.dumps(result,indent=2)+'\n');print('TURN_ACTUAL12_COMPLETE source unchanged; no full batch')
