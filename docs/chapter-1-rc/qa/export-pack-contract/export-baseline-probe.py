"""Whole-canvas ready-actor exporter. No model saves or per-frame image fitting.
Blender --background --threads 2 --disable-autoexec --python THIS -- --source FILE --contract-only
Default: base/e/walk, 24 phases. Larger scopes require --allow-batch explicitly.
"""
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector, Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path('/tmp/ruby-export-pack-qa')
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
def geometry():
 dg=bpy.context.evaluated_depsgraph_get();result={}
 for o in meshes:
  ev=o.evaluated_get(dg);me=ev.to_mesh();used=sorted({i for f in me.polygons for i in f.vertices});result[o.name]=[ev.matrix_world@me.vertices[i].co for i in used];ev.to_mesh_clear()
 return result
def bounds(vs):return {'min':[min(v[i]for v in vs)for i in range(3)],'max':[max(v[i]for v in vs)for i in range(3)]}
def screen(v):
 q=world_to_camera_view(sc,camera,v);return [q.x*512,(1-q.y)*640,q.z]
report={'status':'DRY-RUN-NO-RENDERS'if args.contract_only else 'WHOLE-SPRITE-SOURCE-CANDIDATE-NOT-ART-OR-GAME-ACCEPTANCE','productionEnabled':False,'source':str(source),'sourceSha256':source_hash,'exporterSha256':sha(Path(__file__)),'parameters':{'variants':variants,'directions':directions,'clips':clips,'frameCount':args.frame_count,'contractOnly':args.contract_only},'headingContract':str(calpath.relative_to(ROOT)),'headingContractSha256':sha(calpath),'frameSize':[512,640],'phaseCount':args.frame_count,'deliveryUniformScale':.5,'noPerFrameCropScaleOrTranslation':True,'rootRestGroundNative':list(rest),'actorTransform':'Rz(contractYaw) @ T(-RootRestGround)','cameraAngleAlreadyInHeadingYaw':True,'frameGeneration':'sourceFrame = endExclusive * phaseIndex /frameCount; endpoint checked separately, not duplicated','renderEngine':sc.render.engine,'renderVisibleMeshes':[o.name for o in meshes],'excludedMeshes':[o.name for o in sc.objects if o.type=='MESH'and o not in meshes],'geometryReference':'evaluated used mesh vertices in REST pose; render-visible collection filter, no bbox-bottom anchors','actionHashes':{k:actionhash(bpy.data.actions[actions[k][0]])for k in clips},'cameraVariants':{},'renderedFrameCount':0}
for variant in variants:
 spec=cal['variants'][variant];g=spec['camera']['groundScale'];assert 0<g<1
 center=Vector((0,0,.85));camera.location=center+Vector((0,-8,8*g/math.sqrt(1-g*g)));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();anchor=screen(Vector((0,0,0)))[:2];z0=screen(Vector((0,0,0)));z1=screen(Vector((0,0,1)));zppm=abs(z1[1]-z0[1]);c={'gameCamera':spec['camera'],'scenes':spec['scenes'],'fixedRenderCamera':{'matrixWorld':[list(r)for r in camera.matrix_world],'orthoScale':camdata.ortho_scale,'canvas':[512,640],'worldZPixelsPerMeter':zppm,'worldOriginAnchorPx':anchor},'directions':{}};report['cameraVariants'][variant]=c
 for direction in directions:
  heading=spec['directions'][direction];rig.matrix_world=Matrix.Rotation(heading['stockForwardMinusYBlenderYawRadians'],4,'Z')@Matrix.Translation(-rest);rig.data.pose_position='REST';bpy.context.view_layer.update();geo=geometry();flat=[v for vs in geo.values()for v in vs];rb=bounds(flat);height=rb['max'][2]-rb['min'][2];rig.data.pose_position='POSE';record={'heading':heading,'restGeometryBoundsWorld':rb,'visibleRestHeightMeters':height,'nativeHeightPx':height*zppm,'rootGroundReferenceWorld':list(rig.matrix_world@rest),'clips':{}};c['directions'][direction]=record
  for clip in clips:
   name,end=actions[clip];setaction(name,0);first=geometry();setaction(name,end);last=geometry();topology={k:len(v)for k,v in first.items()};assert topology=={k:len(v)for k,v in last.items()};seam=max((v-last[k][i]).length for k,vs in first.items()for i,v in enumerate(vs));rows=[]
   for i in range(args.frame_count):
    frame=end*i/args.frame_count;setaction(name,frame);geo=geometry();points=[screen(v)for vs in geo.values()for v in vs];projected={'min':[min(v[j]for v in points)for j in range(2)],'max':[max(v[j]for v in points)for j in range(2)]};file=Path('renders')/variant/direction/clip/f'{i:02}.png';row={'index':i,'sourceFrame':frame,'timeSeconds':frame/24,'file':file.as_posix(),'worldOriginAnchorPx':screen(Vector((0,0,0)))[:2],'poseRootPx':screen(rig.matrix_world@rig.pose.bones['Root'].head)[:2],'projectedUsedGeometryBoundsPx':projected,'geometryInsideCanvas':projected['min'][0]>0 and projected['min'][1]>0 and projected['max'][0]<512 and projected['max'][1]<640}
    if not args.contract_only:
     path=out/file;path.parent.mkdir(parents=True,exist_ok=True);sc.render.filepath=str(path);bpy.ops.render.render(write_still=True);row.update({'sha256':sha(path),'bytes':path.stat().st_size});report['renderedFrameCount']+=1
    rows.append(row)
   record['clips'][clip]={'sourceAction':name,'sourceRange':[0,end],'sourceFps':24,'durationSeconds':end/24,'loopEndpointMaxUsedVertexErrorMeters':seam,'frames':rows};print('READY_EXPORT',variant,direction,clip,'contract'if args.contract_only else 'rendered',flush=True)
   assert actionhash(bpy.data.actions[name])==report['actionHashes'][clip]
report['sourceSha256After']=sha(source);assert report['sourceSha256After']==source_hash;report['sourceUnchanged']=True;report['limitations']=['No art/style/wardrobe approval follows from geometry containment/seam.','No no-slip, turn/start/stop, gameplay or performance acceptance.','REST height uses visible accessories/hair too; independent body landmark height is a different metric.','Raster alpha containment is checked by packer only after actual render, not by dry-run.'];reportpath.write_text(json.dumps(report,indent=2)+'\n');print('READY_EXPORT_COMPLETE',str(reportpath),flush=True)
