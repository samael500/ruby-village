import bpy,json,hashlib,math
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
R=Path('/tmp/ruby-ready-walk-qa');S=R/'art/ready-character-walk-v1';O=R/'docs/chapter-1-rc/qa/ready-walk-source'
def digest(v):return hashlib.sha256(repr(v).encode()).hexdigest()
def inspect(path):
 bpy.ops.wm.open_mainfile(filepath=str(path));rig=bpy.data.objects['CharacterArmature'];walk=bpy.data.actions['Walk'];keys=[(f.data_path,f.array_index,[(tuple(k.co),k.interpolation,tuple(k.handle_left),tuple(k.handle_right)) for k in f.keyframe_points]) for l in walk.layers for s in l.strips for b in s.channelbags for f in b.fcurves];return {'bones':len(rig.data.bones),'rest':digest([(b.name,tuple(v for row in b.matrix_local for v in row)) for b in rig.data.bones]),'action':digest(keys),'meshes':{o.name:digest([(tuple(v.co),[(g.group,g.weight) for g in v.groups]) for v in o.data.vertices]) for o in bpy.data.objects if o.type=='MESH' and o.parent==rig}}
a=inspect(S/'source/adventurer-imported.blend');b=inspect(S/'adventurer-walk-pilot.blend');scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];poses=[]
for f in [0,40]:
 scene.frame_set(f);bpy.context.view_layer.update();poses.append({p.name:list(v for row in p.matrix for v in row) for p in rig.pose.bones})
seam=max(abs(a-b) for name in poses[0] for a,b in zip(poses[0][name],poses[1][name]));camera=scene.camera;anchor=world_to_camera_view(scene,camera,Vector((0,0,0)));up=camera.rotation_euler.to_matrix()@Vector((0,1,0));report={'sourceAndPilotInvariantsEqual':a==b,'invariants':b,'all62BoneEndpointMatrixMaxError':seam,'action':rig.animation_data.action.name,'unmutedNlaTracks':[t.name for t in rig.animation_data.nla_tracks if not t.mute],'cameraType':camera.data.type,'cameraGroundForeshortening':math.sqrt(up.x**2+up.y**2),'projectedWorldOriginPx':[anchor.x*512,(1-anchor.y)*640],'resolution':[scene.render.resolution_x,scene.render.resolution_y],'fps':scene.render.fps,'orthographicScale':camera.data.ortho_scale};(O/'blender-report.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
