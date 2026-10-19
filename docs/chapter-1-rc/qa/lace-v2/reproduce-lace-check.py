"""Check whole 3D lace attachment throughout the source gait, and render one regression phase."""
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--render',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);source=Path(a.source).resolve();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);sha=hashlib.sha256(source.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;r=bpy.data.objects['CharacterArmature'];r.data.pose_position='POSE';action=bpy.data.actions['Walk_ProportionProposal'];r.animation_data.action=action;r.animation_data.action_slot=action.slots[0]
for t in r.animation_data.nla_tracks:t.mute=True
r.matrix_world=Matrix.Identity(4)
boots=bpy.data.objects['Adventurer_Feet'];laces=[bpy.data.objects['Ankle boot lace '+side]for side in ['L','R']]
def used_world(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles();vs=[ev.matrix_world@v.co for v in m.vertices];tri=[tuple(t.vertices)for t in m.loop_triangles];ev.to_mesh_clear();return vs,tri
rows=[]
for i in range(48):
 frame=40*i/48;s.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();vs,tri=used_world(boots);tree=BVHTree.FromPolygons(vs,tri,all_triangles=True)
 for lace in laces:
  coords,_=used_world(lace);distances=[tree.find_nearest(v)[3]for v in coords];rows.append({'phase':i,'sourceFrame':frame,'object':lace.name,'vertices':len(coords),'maxDistanceMeters':max(distances),'meanDistanceMeters':sum(distances)/len(distances)})
maximum=max(row['maxDistanceMeters']for row in rows);threshold=.006
report={'source':str(source),'sourceSha256':sha,'phases':48,'metric':'nearest evaluated boot triangle distance for every evaluated lace vertex throughout Walk; does not prove absence of all costume intersections','thresholdMeters':threshold,'thresholdReason':'6 mm maximum is under 1.4 native projected Z pixels; lace rest surface offset is 1.5 mm','maxDistanceMeters':maximum,'attachmentPass':maximum<threshold,'rows':rows,'physicalPhone':'NOT RUN'}
(out/'lace-attachment.json').write_text(json.dumps(report,indent=2)+'\n');print('LACE_DISTANCE',maximum,'PASS',report['attachmentPass'],flush=True)
if a.render:
 cal=json.loads((Path(__file__).resolve().parents[1]/'art/ready-character-walk-v1/heading-contract.json').read_text())['variants']['base'];rest=r.data.bones['Root'].head_local.copy();rest.z=0;r.matrix_world=Matrix.Rotation(cal['directions']['e']['stockForwardMinusYBlenderYawRadians'],4,'Z')@Matrix.Translation(-rest);g=cal['camera']['groundScale'];center=Vector((0,0,.85));cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=2.1;cam.location=center+Vector((0,-8,8*g/math.sqrt(1-g*g)));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();s.render.resolution_x=512;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.film_transparent=True;s.frame_set(3,subframe=1/3);s.render.filepath=str(out/'e-phase04.png');bpy.ops.render.render(write_still=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
if not report['attachmentPass']:raise RuntimeError('Lace separates from evaluated boot surface')
