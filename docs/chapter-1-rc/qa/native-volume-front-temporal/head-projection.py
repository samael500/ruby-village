"""No render: ONE reference iris-color-ray/Head-local anchor, then actual full Head transforms."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;R=Path('/tmp/ruby-combined-loop/art/ruta-native-volume-front-proof-v1');c=json.loads((R/'source-contract.json').read_text());assert c['renderedFrameCount']==48;P=Path(json.loads((R/'scaffold-contract.json').read_text())['sourceCacheAbsolute']);assert hashlib.sha256(P.read_bytes()).hexdigest()==c['sourceSha256'];bpy.ops.wm.open_mainfile(filepath=str(P));sc=bpy.context.scene;cam=c['cameraVariants']['front-proof']['fixedRenderCamera'];sc.camera.matrix_world=Matrix(cam['matrixWorld']);sc.camera.data.ortho_scale=cam['orthoScale'];sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100;rig=bpy.data.objects['CharacterArmature'];rig.matrix_world=Matrix.Translation(Vector((0,.050602056086063385,0)));rig.animation_data.action=bpy.data.actions['Walk_ProportionProposal'];rig.animation_data.action_slot=rig.animation_data.action.slots[0];sc.frame_set(0);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ref=json.loads((O/'iris-all48.json').read_text())['frames'][0]['twoLargestSortedX'];head=rig.matrix_world@rig.pose.bones['Head'].matrix;eyes=[bpy.data.objects[n]for n in ['Ellie ready eye.L','Ellie ready eye.R']];anchors=[]
for r in ref:
 x,y=r['centerXY'];local=Vector((((x+.5)/512-.5)*cam['orthoScale']*512/640,(.5-(y+.5)/640)*cam['orthoScale'],0));origin=sc.camera.matrix_world@local;direction=sc.camera.matrix_world.to_3x3()@Vector((0,0,-1));hits=[]
 for eye in eyes:
  tree=BVHTree.FromObject(eye,dg);inv=eye.matrix_world.inverted();hit,n,idx,d=tree.ray_cast(inv@origin,(inv.to_3x3()@direction).normalized())
  if hit is not None:
   world=eye.matrix_world@hit;hits.append(((world-origin).length,eye.name,world))
 assert hits,'Reference visible iris ray did not intersect an actual eye object';_,name,world=min(hits,key=lambda x:x[0]);anchors.append({'referenceCVCenterXY':[x,y],'eyeObject':name,'worldReference':list(world),'HeadLocalReference':list(head.inverted()@world)})
attach=[]
for eye in eyes:
 groups={}
 for v in eye.data.vertices:
  for g in v.groups:groups.setdefault(eye.vertex_groups[g.group].name,set()).add(round(g.weight,7))
 attach.append({'object':eye.name,'parentType':eye.parent_type,'parentBone':eye.parent_bone,'modifiers':[m.type for m in eye.modifiers],'vertexGroupWeights':{k:sorted(v)for k,v in groups.items()}})
rows=[]
for i in range(48):
 frame=40*i/48;sc.frame_set(int(frame),subframe=frame%1);bpy.context.view_layer.update();M=rig.matrix_world@rig.pose.bones['Head'].matrix;v=world_to_camera_view(sc,sc.camera,rig.matrix_world@rig.pose.bones['Head'].head);points=[]
 for a in anchors:
  pt=M@Vector(a['HeadLocalReference']);p=world_to_camera_view(sc,sc.camera,pt);points.append([p.x*512-.5,(1-p.y)*640-.5])
 rows.append({'phase':i,'HeadBoneHeadPixelXY':[v.x*512,(1-v.y)*640],'fixedReferenceHeadAttachedEyeRaysPixelXY':points})
(O/'head-projection.json').write_text(json.dumps({'sourceSHA256':c['sourceSha256'],'definition':'Two CV phase0 visible-blue-region centroid rays intersect actual evaluated eye geometry, converted ONCE to Head-local points; all48project via full actual Head transform incl rotation. Not anatomical cornea/iris center, no per-frame fit. Raster centers use +.5 then subtract.5.','anchors':anchors,'eyeAttachment':attach,'frames':rows,'limits':'If eye-relative-Head deformation/gaze occurs, residual includes genuine geometry. Blue-region centroid can change with shading/occlusion/AA; threshold stability not exact joint stability.'},indent=2)+'\n')
