"""Two actual camera variants x six native headings; real Walk and neutral Idle."""
from pathlib import Path
import bpy,json,math,hashlib,os
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-six-v1';OUT.mkdir(exist_ok=True);SOURCE=ROOT/'art/ready-character-adapted-v1/ruta-stock-adapted.blend'
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];cal=json.loads((ROOT/'art/ready-character-walk-v1/heading-contract.json').read_text());rig.rotation_mode='XYZ'
for track in rig.animation_data.nla_tracks:track.mute=True
meshes=[o for o in scene.objects if o.type=='MESH' and o.parent==rig]
root_rest_ground=rig.data.bones['Root'].head_local.copy();root_rest_ground.z=0
def place_heading(yaw):
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root_rest_ground)
 bpy.context.view_layer.update()
 root_world=rig.matrix_world@rig.data.bones['Root'].head_local
 assert root_world.xy.length<1e-7,tuple(root_world)
 return list(root_world)
def actionhash(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()
actions={'walk':('Walk',40),'idle':('Idle_Neutral',50)};hashes={k:actionhash(bpy.data.actions[n])for k,(n,end)in actions.items()};projected=world_to_camera_view(scene,scene.camera,Vector((0,0,0)));anchor=[projected.x*512,(1-projected.y)*640]
reference=json.loads((OUT/'static-origin-checks.json').read_text())['bodyReference']
report={'bodyReference':reference,'nativeHeightPx':reference['nativeHeightPx'],'status':'source-six-view-export-not-approved-Ruta-or-game-installation','productionEnabled':False,'source':str(SOURCE.relative_to(ROOT)),'sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'frameSize':[512,640],'footAnchor':anchor,'cameraElevationRadians':math.asin(.65),'orthographicScaleMeters':2.1,'orthographicWidthMeters':1.680000016,'nativeHorizontalPixelsPerMeter':304.76190185546875,'groundScale':.65,'originNormalization':{'nativeRootRestGround':list(root_rest_ground),'worldTransform':'Rz(yaw) @ Translation(-RootRestGround)','rootGroundWorld':[0,0,0],'perFrameCropOrShift':False},'actionHashes':hashes,'actions':{k:{'sourceAction':n,'sourceRange':[0,end],'frameCount':24,'cycleDurationMs':end/24*1000}for k,(n,end)in actions.items()},'cameraVariants':{},'headingReference':'../ready-character-walk-v1/heading-contract.json','limitations':['stock likeness unapproved','no root/runtime changes','Idle_Neutral selected as ready relaxed source Idle; original Idle also preserved in native source','no generated/retargeted poses','contact residual measurements in original motion-checks remain applicable']}
variant_filter=os.environ.get('READY_SIX_VARIANT');suffix='.'+variant_filter if variant_filter else '';suffix+=('.static' if os.environ.get('READY_SIX_STATIC')=='1' else '')
for variant,spec in cal['variants'].items():
 if variant_filter and variant!=variant_filter:continue
 report['cameraVariants'][variant]={'camera':spec['camera'],'scenes':spec['scenes'],'directions':{}}
 for direction,heading in spec['directions'].items():
  root_world=place_heading(heading['stockForwardMinusYBlenderYawRadians']);clips={}
  for clip,(action_name,end)in actions.items():
   action=bpy.data.actions[action_name];rig.animation_data.action=action;rig.animation_data.action_slot=action.slots[0];folder=OUT/'renders'/variant/direction/clip;folder.mkdir(parents=True,exist_ok=True);rows=[]
   for i in ([0] if os.environ.get('READY_SIX_STATIC')=='1' else range(24)):
    frame=end*i/24;scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();path=folder/f'{i:02}.png'
    rows.append({'index':i,'sourceFrame':frame,'file':str(path.relative_to(OUT))})
    if not path.exists() or os.environ.get('READY_SIX_FORCE')=='1':
     scene.render.filepath=str(path);bpy.ops.render.render(write_still=True)
   clips[clip]={'loop':True,'sourceAction':action_name,'sourceRange':[0,end],'cycleDurationMs':end/24*1000,'frames':rows}
   print('READY_SIX_PROGRESS',variant,direction,clip,str(len(rows))+'/24',flush=True)
  report['cameraVariants'][variant]['directions'][direction]={**heading,'normalizedRootGroundWorld':root_world,'clips':clips}
  (OUT/('source-contract'+suffix+'.checkpoint.json')).write_text(json.dumps(report,indent=2)+'\n')
  assert all(hashes[k]==actionhash(bpy.data.actions[n])for k,(n,e)in actions.items())
(OUT/('source-contract'+suffix+'.json')).write_text(json.dumps(report,indent=2)+'\n');print('READY_SIX_COMPLETE',len(report['cameraVariants'])*6*2*24,'whole source frames',flush=True)
