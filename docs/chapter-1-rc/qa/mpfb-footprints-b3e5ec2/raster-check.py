from pathlib import Path
import bpy,json,math,hashlib,os
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path('/tmp/ruby-qa-pivot-footprints');V=os.environ.get('RUBY_QA_VARIANT','pivot');D=R/'art/characters-mpfb-v1/motion'/('pivot-variants/'+V);O=R/'docs/chapter-1-rc/qa/mpfb-footprints-b3e5ec2'/V;m=json.loads((D/'manifest.json').read_text());meta=json.loads((D/'raster-path-metadata.json').read_text());src=D/'mpfb-compact-pivot-technical.blend';sha=hashlib.sha256(src.read_bytes()).hexdigest();assert sha==meta['sourceSha256Before'];bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;r=bpy.data.objects['Ruta.MPFB.StandardRig'];c=s.camera
for n,a in m['turnActions'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
for obj in s.objects:
 if obj.type=='MESH':
  for mod in obj.modifiers:
   if mod.type=='SUBSURF':mod.levels=mod.render_levels
s.render.resolution_x=s.render.resolution_y=384;s.render.resolution_percentage=100;s.cycles.samples=8;s.cycles.use_denoising=True;s.render.film_transparent=True;rows=[];chosen=21 if V=='right60'else 57
for rec in meta['renderedFrames']:
 f=rec['frame'];s.frame_set(f);bpy.context.view_layer.update();center=r.location+Vector((0,0,.68));el=math.asin(.65);c.data.type='ORTHO';c.data.ortho_scale=1.7;c.location=center+Vector((-4*math.cos(el),0,4*math.sin(el)));c.rotation_euler=(center-c.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();q=world_to_camera_view(s,c,r.matrix_world.translation);anchor=[384*q.x,384*(1-q.y)];err=math.dist(anchor,rec['rootGroundAnchorPixels']);assert err<.001;row=dict(frame=f,anchor=anchor,root=list(r.matrix_world.translation),anchorErrorPixels=err,cameraDeterminant=c.matrix_world.to_3x3().determinant())
 if V=='pivot':
  dg=bpy.context.evaluated_depsgraph_get();errs=[];bounds={}
  for name,expected in rec['actualRenderLevelGeometryXYBounds'].items():
   obj=bpy.data.objects[name];eo=obj.evaluated_get(dg);points=[eo.matrix_world@v.co for v in eo.data.vertices];box=[[min(v[i]for v in points),max(v[i]for v in points)]for i in range(2)];radius=max(math.hypot(v.x,v.y)for v in points);assert points and len(points)==expected['vertices'];errs.extend(abs(a-b)for xs,ys in zip(box,expected['worldXYBoundsMeters'])for a,b in zip(xs,ys));errs.append(abs(radius-expected['maxWorldXYRadiusFromPivotOriginMeters']));bounds[name]=dict(vertices=len(points),xy=box,radius=radius)
  row['sampledRenderGeometry']=bounds;row['maxAuthoredBoundsDifferenceMeters']=max(errs);assert max(errs)<1e-6
 rows.append(row)
 if f==chosen:s.render.filepath=str(O/'independent-render.png');bpy.ops.render.render(write_still=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
(O/'independent-raster-readback.json').write_text(json.dumps(dict(sourceSha256=sha,variant=V,independentRenderFrame=chosen,sampledFrames=rows,geometryScope='12 actual sampled poses only, not continuous swept footprint'),indent=2)+'\n');print('PASS_RASTER_READBACK',V,len(rows))
