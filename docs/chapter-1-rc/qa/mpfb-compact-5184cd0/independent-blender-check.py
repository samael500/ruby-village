import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path('/tmp/ruby-qa-compact-view');D=R/'art/characters-mpfb-v1/motion/sixview-proof';O=R/'docs/chapter-1-rc/qa/mpfb-compact-5184cd0';m=json.loads((D/'manifest.json').read_text());src=(D/m['source']).resolve();h=hashlib.sha256(src.read_bytes()).hexdigest();assert h==m['sourceSha256'];bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene
for n,a in m['actionBundle'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
r=bpy.data.objects['Ruta.MPFB.StandardRig'];c=s.camera;shoe=bpy.data.objects['Ruta.shoes01'];clone=shoe.copy();clone.data=shoe.data.copy();s.collection.objects.link(clone);clone.hide_render=True
for mod in clone.modifiers:
 if mod.type=='SUBSURF':mod.show_viewport=False
s.frame_set(1);bpy.context.view_layer.update();p0=r.matrix_world.translation.copy();s.frame_set(25);bpy.context.view_layer.update();delta=r.matrix_world.translation-p0;rows=[]
def px(p):
 q=world_to_camera_view(s,c,p);return [q.x*384,(1-q.y)*384]
for group,sp in m['cameraVariants'].items():
 for direction,v in sp['directions'].items():
  for rec in v['frames']:
   s.frame_set(rec['frame']);bpy.context.view_layer.update();center=r.location+Vector((0,0,.68));el=math.asin(sp['camera']['groundScale']);az=v['nativeCameraAzimuthRadians'];c.data.ortho_scale=1.7;c.location=center+Vector((4*math.cos(el)*math.cos(az),4*math.cos(el)*math.sin(az),4*math.sin(el)));c.rotation_euler=(center-c.location).to_track_quat('-Z','Y').to_euler();bpy.context.view_layer.update();root=r.matrix_world.translation;pp=px(root);dd=[b-a for a,b in zip(pp,px(root+delta))];es=clone.evaluated_get(bpy.context.evaluated_depsgraph_get());errs=[]
   for side,markers in rec['actualSourceSoleMarkers'].items():
    for kind,marker in markers.items():
     points=[es.matrix_world@es.data.vertices[i].co for i in marker['sourceVertexIndices']];centerfoot=sum(points,Vector())/len(points);errs.append((centerfoot-Vector(marker['centerWorld'])).length)
   err=math.atan2(math.sin(math.atan2(dd[1],dd[0])-v['screenAngleRadians']),math.cos(math.atan2(dd[1],dd[0])-v['screenAngleRadians']));rows.append(dict(group=group,direction=direction,frame=rec['frame'],anchor=pp,anchorError=math.dist(pp,rec['rootGroundAnchorPixels']),stride=dd,strideError=math.dist(dd,rec['actualProjectedStridePixels']),angleError=err,soleWorldError=max(errs),cameraDeterminant=c.matrix_world.to_3x3().determinant(),ortho=c.data.ortho_scale))
   if group=='base' and direction=='sw' and rec['frame']==13:
    s.render.resolution_x=384;s.render.resolution_y=384;s.render.resolution_percentage=100;s.cycles.samples=8;s.cycles.use_denoising=True;s.render.filepath=str(O/'independent-base-sw-13.png');bpy.ops.render.render(write_still=True)
assert len(rows)==24
assert max(x['anchorError'] for x in rows)<.001
assert max(x['soleWorldError'] for x in rows)<1e-6
assert max(abs(x['angleError'])for x in rows)<1e-5
assert all(abs(x['cameraDeterminant']-1)<1e-6 for x in rows)
assert hashlib.sha256(src.read_bytes()).hexdigest()==h
(O/'independent-readback.json').write_text(json.dumps(dict(sourceSha256=h,actualNativeDelta=list(delta),records=rows),indent=2)+'\n');print('INDEPENDENT PASS',len(rows))
