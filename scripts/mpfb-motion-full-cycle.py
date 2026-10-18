"""Resumable checkpoint A: 288 genuine technical walk poses, no transition rasters.

Source/action/metadata remain separate from raster caches so corrected appearance
can reuse authored motion after calibration/contact review, without old images.
"""
from pathlib import Path
import bpy,math,json,os,hashlib,shutil,time
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];motion_root=ROOT/'art/characters-mpfb-v1/motion';OUT=(motion_root/os.environ.get('RUBY_MPFB_OUTPUT_NAMESPACE','full-cycle-technical')).resolve();assert OUT.is_relative_to(motion_root.resolve());OUT.mkdir(parents=True,exist_ok=True)
SOURCE=Path(os.environ.get('RUBY_MPFB_SOURCE_BLEND',str(ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend'))).resolve();source_metadata=Path(os.environ.get('RUBY_MPFB_SOURCE_MANIFEST',str(SOURCE.parent/'manifest.json')));metadata=json.loads(source_metadata.read_text());native_height=metadata['nativeHeightReferencePx'];display_height=metadata['targetDisplayHeightReferencePx'];assert native_height>0 and display_height>0;source_hash=hashlib.sha256(SOURCE.read_bytes()).hexdigest();proofroot=ROOT/'art/characters-mpfb-v1/motion/sixview-proof';proof=json.loads((proofroot/'manifest.json').read_text());proofcheck=json.loads((proofroot/'render-check.json').read_text());proofhashes={r['path']:r['sha256']for r in proofcheck['records']}
# Replacing appearance must use a new export directory, never overwrite a reviewed cache.
if (OUT/'manifest.json').exists():assert json.loads((OUT/'manifest.json').read_text())['sourceSha256']==source_hash,'Changed source: choose a new reviewed export namespace before replacing technical artifacts'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
for name,action in metadata['sourceActions'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];camera=scene.camera;shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();measure.name='EXPORT measurement clone only';scene.collection.objects.link(measure);measure.hide_render=True
for m in measure.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels
markers={}
for side,sign in [('L',1),('R',-1)]:
 vertices=[v for v in measure.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vertices);sole=[v for v in vertices if v.co.z<z+.008];front=min(v.co.y for v in sole);back=max(v.co.y for v in sole);markers[side]={kind:[v.index for v in sole if(v.co.y<front+.025 if kind=='toe'else v.co.y>back-.025)]for kind in ['toe','heel']}
scene.frame_set(1);bpy.context.view_layer.update();root_start=rig.matrix_world.translation.copy();scene.frame_set(25);bpy.context.view_layer.update();root_delta=rig.matrix_world.translation-root_start
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=True;scene.render.resolution_x=384;scene.render.resolution_y=384;scene.render.resolution_percentage=100;scene.render.film_transparent=True;camera.data.type='ORTHO';camera.data.ortho_scale=1.70
legacy=json.loads((ROOT/'public/assets/characters-walk-v1/animated-v3/manifest.json').read_text());accepted=json.loads((ROOT/'src/scene-v8.json').read_text())
manifest={'schema':'mpfb-technical-walk-export/v1','status':'INCREMENTAL TECHNICAL CHECKPOINT A; APPEARANCE REJECTED; NOT GAME READY','independentCompactGo':'1d564c1','sourceBlend':str(SOURCE.relative_to(ROOT)),'sourceManifest':str(source_metadata.relative_to(ROOT)),'sourceSha256':source_hash,'sourceActionBundle':metadata['sourceActions'],'sourceCycleCommit':'5ca361b','sourcePackedCommit':'35cddba','blender':bpy.app.version_string,'mpfbVersion':'2.0.18','licenseAndProvenance':'Inherited motion/README and appearance source rights records; no new third-party assets','budget':{'totalWalkPng':288,'reusedIdenticalProofPng':24 if source_hash==proof['sourceSha256']else 0,'newRenderBudget':264 if source_hash==proof['sourceSha256']else 288,'transitionPng':0,'status':'Only checkpoint A authorized; no full transition raster batch'},'frameSize':[384,384],'frameMs':30,'cycleMs':720,'frameCountPerView':24,'actualNativeRootDeltaMeters':list(root_delta),'orthoScaleMeters':1.70,'nativeHeightReferencePixels':native_height,'displayHeightReferencePixels':display_height,'metersToScenePixels':display_height/(native_height/384*1.70),'rootPolicy':'Continuous native root applied once; PNG camera follows rig-object translation only; no per-frame anchor correction or direction fit','appearanceReplacement':'Reuse native action/phase contract, not old raster cache; changed source hash requires new namespace and renewed height/containment/contact review','transitionRasterStatus':'NOT EXPORTED; adapter metadata only; both start/stop variants remain in packed source','turnStatus':'NOT AUTHORED; six orientations of a walk are not turn transitions','cameraVariants':{}}
def atomic(path,payload):
 temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(payload,indent=2)+'\n');temp.replace(path)
def project(point):
 q=world_to_camera_view(scene,camera,point);return [384*q.x,384*(1-q.y)]
def measure_frame(frame):
 deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);es=measure.evaluated_get(deps);boot=shoe.evaluated_get(deps);root=rig.matrix_world.translation.copy();allmatrices=[list(value for row in b.matrix for value in row)for b in er.pose.bones];posehash=hashlib.sha256(json.dumps(allmatrices).encode()).hexdigest();forward=[b-a for a,b in zip(project(root),project(root+root_delta))];rec={'frame':frame,'timeMs':(frame-1)*30,'phase':(frame-1)/24,'rootNativeWorldMeters':list(root),'rootGroundAnchorPixels':project(root),'actualProjectedStridePixels':forward,'actualProjectedStrideScenePixels':[v*display_height/native_height for v in forward],'evaluatedNativeBoneMatrixHash':posehash,'pelvisWorldMeters':list(er.matrix_world@er.pose.bones['root'].head),'minFullRenderLevelBootZ':min((boot.matrix_world@v.co).z for v in boot.data.vertices),'feet':{}}
 for side,offset in [('L',0),('R',.5)]:
  phase=((frame-1)/24+offset)%1;f={'phase':phase,'semanticMode':'heel'if phase<.1 else'flat'if phase<=.48 else'toe'if phase<.6 else'swing','actualBoneWorldMeters':list(er.matrix_world@er.pose.bones['foot.'+side].head),'actualBoneProjectionPixels':project(er.matrix_world@er.pose.bones['foot.'+side].head),'sourceSole':{}}
  for kind,ids in markers[side].items():
   points=[es.matrix_world@es.data.vertices[i].co for i in ids];center=sum(points,Vector())/len(points);f['sourceSole'][kind]={'centerWorldMeters':list(center),'projectedPixels':project(center),'minZ':min(p.z for p in points),'sourceVertexIndices':ids}
  rec['feet'][side]=f
 return rec
for group,spec in legacy['cameraVariants'].items():
 ground=spec['camera']['groundScale'];elev=math.asin(ground);result={'camera':spec['camera'],'acceptedScenes':[n for n,s in accepted.items()if abs(s['camera']['angle']-spec['camera']['angle'])<1e-12 and abs(s['camera']['groundScale']-ground)<1e-12],'directions':{}};manifest['cameraVariants'][group]=result
 for direction,data in spec['directions'].items():
  directory=OUT/group/direction;directory.mkdir(parents=True,exist_ok=True);receipt_path=directory/'receipt.json';old=json.loads(receipt_path.read_text())if receipt_path.exists()else{};assert not old or old['sourceSha256']==source_hash;cache={r['frame']:r for r in old.get('frames',[])};orbit=math.atan2(math.sin(data['screenAngleRadians'])/ground,math.cos(data['screenAngleRadians']));azimuth=-math.pi+orbit;receipt={'sourceSha256':source_hash,'cameraVariant':group,'direction':direction,'screenAngleRadians':data['screenAngleRadians'],'nativeCameraAzimuthRadians':azimuth,'actorSceneHeadingRadians':orbit-spec['camera']['angle'],'orthoScaleMeters':1.70,'mirror':False,'frames':[],'complete':False}
  for frame in range(1,25):
   path=directory/f'{frame:02}.png';prior=cache.get(frame)
   if prior and path.exists()and hashlib.sha256(path.read_bytes()).hexdigest()==prior['sha256']:receipt['frames'].append(prior);continue
   scene.frame_set(frame);bpy.context.view_layer.update();center=rig.location+Vector((0,0,.68));camera.location=center+Vector((4*math.cos(elev)*math.cos(azimuth),4*math.cos(elev)*math.sin(azimuth),4*math.sin(elev)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();rec=measure_frame(frame);observed=math.atan2(rec['actualProjectedStridePixels'][1],rec['actualProjectedStridePixels'][0]);rec['projectedAngleErrorRadians']=math.atan2(math.sin(observed-data['screenAngleRadians']),math.cos(observed-data['screenAngleRadians']));assert abs(rec['projectedAngleErrorRadians'])<1e-5
   relative=f'{group}/{direction}/{frame:02}.png';candidate=proofroot/relative
   if source_hash==proof['sourceSha256']and relative in proofhashes and candidate.exists()and hashlib.sha256(candidate.read_bytes()).hexdigest()==proofhashes[relative]:shutil.copyfile(candidate,path);rec['rasterOrigin']='byte-identical independently reviewed compact proof'
   else:scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);rec['rasterOrigin']='actual Cycles8 source pose render'
   rec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();receipt['frames'].append(rec);atomic(receipt_path,receipt);print('MPFB_EXPORT_FRAME',group,direction,frame,rec['rasterOrigin'],flush=True)
  receipt['complete']=True;atomic(receipt_path,receipt);result['directions'][direction]={'receipt':str(receipt_path.relative_to(OUT)),'frames':24,'complete':True};atomic(OUT/'manifest.json',manifest);print('MPFB_EXPORT_VIEW_COMPLETE',group,direction,flush=True)
manifest['status']='TECHNICAL CHECKPOINT A RENDER COMPLETE; AUTHOR/INDEPENDENT FULL LOOP CHECK PENDING; APPEARANCE REJECTED';manifest['sourceSha256After']=hashlib.sha256(SOURCE.read_bytes()).hexdigest();assert manifest['sourceSha256After']==source_hash;atomic(OUT/'manifest.json',manifest);print('MPFB_EXPORT_CHECKPOINT_A_COMPLETE 288 actual PNG / no transition batch',flush=True)
