"""Read-only native rig projection for repaint guide registration. Run with Blender."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];SOURCE=ROOT/'art/ready-character-adapted-v1/ruta-stock-adapted.blend';OUT=ROOT/'art/painted-ruta-guides-v1'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature']
for t in rig.animation_data.nla_tracks:t.mute=True
p=rig.data.bones['Root'].head_local.copy();p.z=0
rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-p)
a=bpy.data.actions['Walk'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
def project(w):
 q=world_to_camera_view(scene,scene.camera,w);return [q.x*256,(1-q.y)*320]
def marker(w,origin):
 d=project(w);return {'worldMeters':list(w),'deliveryLocalPx':d,'keyGuideLocalPx':[x*1.5 for x in d],'keyGuideSheetPx':[d[j]*1.5+origin[j] for j in range(2)]}
rows=[]
for slot,i in enumerate(range(0,24,3)):
 f=40*i/24;scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();origin=[slot%4*384,slot//4*480]
 bones={name:marker(rig.matrix_world@rig.pose.bones[bone].head,origin)for name,bone in {'root':'Root','kneeLeft':'LowerLeg.L','kneeRight':'LowerLeg.R','ankleLeft':'Foot.L','ankleRight':'Foot.R'}.items()}
 bounds={};dg=bpy.context.evaluated_depsgraph_get()
 for label,names in {'head':['Adventurer_Head'],'headIncludingHair':['Adventurer_Head','Ruta CC0 ginger waves']}.items():
  pts=[]
  for name in names:
   ob=bpy.data.objects[name].evaluated_get(dg);mesh=ob.to_mesh();pts.extend(project(ob.matrix_world@v.co)for v in mesh.vertices);ob.to_mesh_clear()
  b=[min(v[0]for v in pts),min(v[1]for v in pts),max(v[0]for v in pts),max(v[1]for v in pts)]
  bounds[label]={'meshNames':names,'deliveryLocalXYXY':b,'keyGuideLocalXYXY':[v*1.5 for v in b],'keyGuideSheetXYXY':[v*1.5+origin[j%2]for j,v in enumerate(b)]}
 rows.append({'walkFrameIndex':i,'sourceFrame':f,'keyCellOrigin':origin,'markers':bones,'projectedHeadBounds':bounds})
report={'source':str(SOURCE.relative_to(ROOT)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'action':'Walk','heading':'base E','yawRadians':math.pi/2,'originNormalization':'Rz(yaw) @ Translation(-RootRestGround)','rootRestGround':list(p),'coordinates':'pixel x right / y down, continuous coordinates, no raster rounding','jointDefinition':'pose bone head: LowerLeg knee; Foot ankle; Root root. Left/right are anatomical.','headBoundsDefinition':'axis aligned projected evaluated mesh vertices, includes hidden geometry; not alpha bounds','frames':rows}
(OUT/'pose-markers-e8.json').write_text(json.dumps(report,indent=2)+'\n');print('POSE_MARKERS_OK',len(rows))
