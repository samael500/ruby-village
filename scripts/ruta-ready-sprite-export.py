"""Whole-canvas ready-actor exporter. No model saves or per-frame image fitting.
Blender --background --threads 2 --disable-autoexec --python THIS -- --source FILE --contract-only
Default: base/e/walk, 24 phases. Larger scopes require --allow-batch explicitly.
"""
import argparse, hashlib, json, math, sys, time
import numpy as np
started=time.perf_counter();geometry_seconds=0.0;projection_seconds=0.0;validation=[]
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',default='art/ruta-ready-export-pilot-v1');p.add_argument('--variants',default='base');p.add_argument('--directions',default='e');p.add_argument('--clips',default='walk');p.add_argument('--frame-count',type=int,default=24);p.add_argument('--contract-only',action='store_true');p.add_argument('--allow-batch',action='store_true');args=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
source=Path(args.source).resolve();out=Path(args.out).resolve();out.mkdir(parents=True,exist_ok=True);sha=lambda x:hashlib.sha256(Path(x).read_bytes()).hexdigest();source_hash=sha(source);calpath=ROOT/'art/ready-character-walk-v1/heading-contract.json';cal=json.loads(calpath.read_text());actions={'walk':('Walk_ProportionProposal',40),'idle':('Idle_Neutral_ProportionProposal',50)}
variants=list(cal['variants'])if args.variants=='all'else args.variants.split(',');directions=['e','se','sw','w','nw','ne']if args.directions=='all'else args.directions.split(',');clips=list(actions)if args.clips=='all'else args.clips.split(',')
assert all(x in cal['variants']for x in variants)and all(x in actions for x in clips)
assert all(d in cal['variants'][v]['directions']for v in variants for d in directions)
assert 1<=args.frame_count<=240
count=len(variants)*len(directions)*len(clips)*args.frame_count
if len(variants)*len(directions)*len(clips)>1 and not args.allow_batch:p.error('Scope exceeds24; explicit --allow-batch required after art review')
reportpath=out/('dry-run-contract.json'if args.contract_only else 'source-contract.json')
if reportpath.exists():
 old=json.loads(reportpath.read_text())
 if old.get('sourceSha256')!=source_hash:raise RuntimeError('Output already belongs to another source hash: use a new --out')
bpy.ops.wm.open_mainfile(filepath=str(source));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];assert rig.type=='ARMATURE';rig.animation_data_create()
for track in rig.animation_data.nla_tracks:track.mute=True
sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;sc.render.pixel_aspect_x=1;sc.render.pixel_aspect_y=1;sc.render.fps=24;sc.render.fps_base=1;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.image_settings.color_depth='8';sc.render.use_file_extension=True
# Preserve source render engine, materials, lights, world and color management.
camdata=bpy.data.cameras.new('ReadyExportFixedCamera');camera=bpy.data.objects.new('ReadyExportFixedCamera',camdata);sc.collection.objects.link(camera);sc.camera=camera;camdata.type='ORTHO';camdata.ortho_scale=2.1;camdata.clip_start=.01;camdata.clip_end=100
rest=rig.data.bones['Root'].head_local.copy();rest.z=0
# Render collection visibility, including parent exclusion, independent of viewport eye icon.
allowed=set()
def collect(lc,parent=True):
 ok=parent and not lc.exclude and not lc.collection.hide_render
 if ok:allowed.update(o.name for o in lc.collection.objects)
 for child in lc.children:collect(child,ok)
collect(bpy.context.view_layer.layer_collection)
meshes=[o for o in sc.objects if o.type=='MESH'and not o.hide_render and o.name in allowed];assert meshes
unsupported=[o.name for o in sc.objects if o.type in ['CURVE','CURVES','SURFACE','META','FONT','VOLUME']and not o.hide_render and o.name in allowed]
if unsupported:raise RuntimeError('Visible non-mesh geometry needs explicit support/reference definition: '+repr(unsupported))
def actionhash(a):
 curves=[(f.data_path,f.array_index,[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]
 return hashlib.sha256(json.dumps(curves,separators=(',',':')).encode()).hexdigest()
def setaction(name,frame):
 a=bpy.data.actions[name];rig.animation_data.action=a
 if a.slots:rig.animation_data.action_slot=a.slots[0]
 sc.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update()
def make_projection():
 # Same ORTHO camera inverse/view_frame as world_to_camera_view, computed ONCE/camera.
 assert camera.data.type=='ORTHO'
 inverse=np.array(camera.matrix_world.normalized().inverted(),dtype=np.float64)
 frame=camera.data.view_frame(scene=sc);xmin,xmax=frame[2].x,frame[1].x;ymin,ymax=frame[1].y,frame[0].y
 projection=inverse.copy();projection[0]*=512/(xmax-xmin);projection[0,3]-=xmin*512/(xmax-xmin);projection[1]*=-640/(ymax-ymin);projection[1,3]+=640+ymin*640/(ymax-ymin);projection[2]*=-1
 return projection[:3]
def project_many(world):
 global projection_seconds
 start=time.perf_counter();result=world@projection[:,:3].T+projection[:,3];projection_seconds+=time.perf_counter()-start;return result
def validate_camera_boundaries():
 # Camera frame corners, center and one-pixel outside corners, in front of camera.
 frame=camera.data.view_frame(scene=sc);xmin,xmax=frame[2].x,frame[1].x;ymin,ymax=frame[1].y,frame[0].y
 refs=[]
 for u,v in [(0,0),(0,1),(1,0),(1,1),(.5,.5),(-1/512,-1/640),(1+1/512,1+1/640)]:
  refs.append(camera.matrix_world@Vector((xmin+u*(xmax-xmin),ymin+v*(ymax-ymin),-8)))
 actual=project_many(np.array(refs));expected=np.array([screen(v)for v in refs]);error=float(abs(actual[:,:2]-expected[:,:2]).max());assert error<1e-4,('camera boundary projection mismatch',error)
 validation.append({'mesh':'CAMERA_FRAME_BOUNDARY','sampleCount':len(refs),'maxErrorPx':error,'referencePixels':expected[:,:2].tolist(),'bulkPixels':actual[:,:2].tolist()})
def geometry():
 global geometry_seconds
 start=time.perf_counter();dg=bpy.context.evaluated_depsgraph_get();result={}
 for o in meshes:
  ev=o.evaluated_get(dg);me=ev.to_mesh()
  # Loops are exactly polygon-used vertex indices; loose vertices stay excluded.
  loop_indices=np.empty(len(me.loops),dtype=np.int32);me.loops.foreach_get('vertex_index',loop_indices);used=np.unique(loop_indices)
  coords=np.empty(len(me.vertices)*3,dtype=np.float32);me.vertices.foreach_get('co',coords);local=coords.reshape(-1,3)[used].astype(np.float64);matrix=np.array(ev.matrix_world,dtype=np.float64);world=local@matrix[:3,:3].T+matrix[:3,3];result[o.name]=world
  if len(used):
   # Fixed quantiles + each axis extrema: every object, every REST/phase/endpoint readback.
   checks=np.unique(np.r_[np.linspace(0,len(used)-1,min(9,len(used)),dtype=int),np.argmin(world,axis=0),np.argmax(world,axis=0)])
   actual=project_many(world[checks]);references=np.array([screen(ev.matrix_world@me.vertices[int(used[j])].co)for j in checks]);errors=np.max(abs(actual[:,:2]-references[:,:2]),axis=1);worst=int(np.argmax(errors));error=float(errors[worst]);assert error<1e-4,('bulk projection mismatch',o.name,error)
   validation.append({'mesh':o.name,'sourceFrame':float(sc.frame_current)+sc.frame_subframe,'restPose':rig.data.pose_position=='REST','sampleCount':len(checks),'maxErrorPx':error,'worstVertexIndex':int(used[checks[worst]]),'referencePx':references[worst,:2].tolist(),'bulkPx':actual[worst,:2].tolist()})
  ev.to_mesh_clear()
 geometry_seconds+=time.perf_counter()-start;return result
def bounds(vs):return {'min':np.min(vs,axis=0).tolist(),'max':np.max(vs,axis=0).tolist()}
def screen(v):
 q=world_to_camera_view(sc,camera,v);return [q.x*512,(1-q.y)*640,q.z]
report={'status':'DRY-RUN-NO-RENDERS'if args.contract_only else 'WHOLE-SPRITE-SOURCE-CANDIDATE-NOT-ART-OR-GAME-ACCEPTANCE','productionEnabled':False,'source':str(source),'sourceSha256':source_hash,'exporterSha256':sha(Path(__file__)),'parameters':{'variants':variants,'directions':directions,'clips':clips,'frameCount':args.frame_count,'contractOnly':args.contract_only},'headingContract':str(calpath.relative_to(ROOT)),'headingContractSha256':sha(calpath),'frameSize':[512,640],'phaseCount':args.frame_count,'deliveryUniformScale':.5,'noPerFrameCropScaleOrTranslation':True,'rootRestGroundNative':list(rest),'actorTransform':'Rz(contractYaw) @ T(-RootRestGround)','cameraAngleAlreadyInHeadingYaw':True,'frameGeneration':'sourceFrame = endExclusive * phaseIndex /frameCount; endpoint checked separately, not duplicated','renderEngine':sc.render.engine,'renderVisibleMeshes':[o.name for o in meshes],'excludedMeshes':[o.name for o in sc.objects if o.type=='MESH'and o not in meshes],'geometryReference':'evaluated used mesh vertices in REST pose; render-visible collection filter, no bbox-bottom anchors','actionHashes':{k:actionhash(bpy.data.actions[actions[k][0]])for k in clips},'cameraVariants':{},'renderedFrameCount':0}
for variant in variants:
 spec=cal['variants'][variant];g=spec['camera']['groundScale'];assert 0<g<1
 center=Vector((0,0,.85));camera.location=center+Vector((0,-8,8*g/math.sqrt(1-g*g)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();projection=make_projection();validate_camera_boundaries();anchor=screen(Vector((0,0,0)))[:2];z0=screen(Vector((0,0,0)));z1=screen(Vector((0,0,1)));zppm=abs(z1[1]-z0[1]);c={'gameCamera':spec['camera'],'scenes':spec['scenes'],'fixedRenderCamera':{'matrixWorld':[list(r)for r in camera.matrix_world],'orthoScale':camdata.ortho_scale,'canvas':[512,640],'worldZPixelsPerMeter':zppm,'worldOriginAnchorPx':anchor},'directions':{}};report['cameraVariants'][variant]=c
 for direction in directions:
  heading=spec['directions'][direction];rig.matrix_world=Matrix.Rotation(heading['stockForwardMinusYBlenderYawRadians'],4,'Z')@Matrix.Translation(-rest);rig.data.pose_position='REST';bpy.context.view_layer.update();geo=geometry();flat=np.concatenate(list(geo.values()),axis=0);rb=bounds(flat);height=rb['max'][2]-rb['min'][2];rig.data.pose_position='POSE';record={'heading':heading,'restGeometryBoundsWorld':rb,'visibleRestHeightMeters':height,'nativeHeightPx':height*zppm,'rootGroundReferenceWorld':list(rig.matrix_world@rest),'clips':{}};c['directions'][direction]=record
  for clip in clips:
   name,end=actions[clip];setaction(name,0);first=geometry();setaction(name,end);last=geometry();topology={k:len(v)for k,v in first.items()};assert topology=={k:len(v)for k,v in last.items()};seam=max(float(np.linalg.norm(vs-last[k],axis=1).max())for k,vs in first.items()if len(vs));rows=[]
   for i in range(args.frame_count):
    frame=end*i/args.frame_count;setaction(name,frame);geo=geometry();points=project_many(np.concatenate(list(geo.values()),axis=0));projected={'min':points[:,:2].min(axis=0).tolist(),'max':points[:,:2].max(axis=0).tolist()};file=Path('renders')/variant/direction/clip/f'{i:02}.png';row={'index':i,'sourceFrame':frame,'timeSeconds':frame/24,'file':file.as_posix(),'worldOriginAnchorPx':screen(Vector((0,0,0)))[:2],'poseRootPx':screen(rig.matrix_world@rig.pose.bones['Root'].head)[:2],'projectedUsedGeometryBoundsPx':projected,'geometryInsideCanvas':projected['min'][0]>0 and projected['min'][1]>0 and projected['max'][0]<512 and projected['max'][1]<640}
    if not args.contract_only:
     path=out/file;path.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(path);bpy.ops.render.render(write_still=True);row.update({'sha256':sha(path),'bytes':path.stat().st_size});report['renderedFrameCount']+=1
    rows.append(row)
   record['clips'][clip]={'sourceAction':name,'sourceRange':[0,end],'sourceFps':24,'durationSeconds':end/24,'loopEndpointMaxUsedVertexErrorMeters':seam,'frames':rows};print('READY_EXPORT',variant,direction,clip,'contract'if args.contract_only else 'rendered',flush=True)
   assert actionhash(bpy.data.actions[name])==report['actionHashes'][clip]
report['bulkProjectionValidation']={'reference':'world_to_camera_view on original mathutils matrix @ mesh vertex; quantile and axis-extrema deterministic samples of every object/evaluated phase','thresholdPx':1e-4,'sampleCount':sum(r['sampleCount']for r in validation),'maxErrorPx':max(r['maxErrorPx']for r in validation),'rows':validation};report['timingsSeconds']={'totalBeforeReportWrite':time.perf_counter()-started,'geometryIncludingReferenceValidation':geometry_seconds,'bulkProjection':projection_seconds};report['sourceSha256After']=sha(source);assert report['sourceSha256After']==source_hash;report['sourceUnchanged']=True;report['limitations']=['No art/style/wardrobe approval follows from geometry containment/seam.','No no-slip, turn/start/stop, gameplay or performance acceptance.','REST height uses visible accessories/hair too; independent body landmark height is a different metric.','Raster alpha containment is checked by packer only after actual render, not by dry-run.'];reportpath.write_text(json.dumps(report,indent=2)+'\n');print('READY_EXPORT_COMPLETE',str(reportpath),flush=True)
