"""Compose TWO evaluated validated left60 clips; no gait/foot rescaling or mirrors."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/characters-mpfb-v1/motion/turn-variants-study/left120'
SOURCE=ROOT/'art/characters-mpfb-v1/motion/turn-study/mpfb-native60-turn-technical.blend'
meta=json.loads((SOURCE.parent/'manifest.json').read_text());before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene
rig=bpy.data.objects['Ruta.MPFB.StandardRig'];controls=[bpy.data.objects[n] for n in meta['turnActions']]
for obj in controls:obj.animation_data.action=bpy.data.actions[meta['turnActions'][obj.name]]
def frame(f):scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update()
keys=sorted({float(p.co.x) for c in rig.animation_data.action.fcurves if c.data_path=='location' for p in c.keyframe_points})
samples=[]
for f in keys:
 frame(f);samples.append({'frame':f,'root':rig.location.copy(),'rotation':rig.rotation_euler.copy(),'basis':{b.name:b.matrix_basis.copy() for b in rig.pose.bones},'controls':{o.name:o.location.copy() for o in controls if o!=rig}})
step=samples[-1]['root'].copy();angle=float(samples[-1]['rotation'].z);bundle={}
for obj in controls:
 action=bpy.data.actions.new('MPFB native120L two validated60 / '+obj.name);action.use_fake_user=True;obj.animation_data.action=action;bundle[obj.name]=action.name
plans=[]
for segment in range(2):
 origin=Vector() if segment==0 else step;rot=Matrix.Rotation(segment*angle,3,'Z')
 for index,s in enumerate(samples):
  if segment and index==0:continue
  f=s['frame']+24*segment;frame(f)
  for name,m in s['basis'].items():rig.pose.bones[name].matrix_basis=m
  rig.location=origin+rot@s['root'];rig.rotation_euler=s['rotation'];rig.rotation_euler.z+=segment*angle
  for obj in controls:
   if obj!=rig:obj.location=s['controls'][obj.name]
  bpy.context.view_layer.update();rig.keyframe_insert('location',frame=f);rig.keyframe_insert('rotation_euler',frame=f)
  for b in rig.pose.bones:b.keyframe_insert('location',frame=f);b.keyframe_insert('rotation_euler',frame=f)
  for obj in controls:
   if obj!=rig:obj.keyframe_insert('location',frame=f)
  p=(s['frame']-1)/24
  plans.append({'frame':f,'timeMs':30*(f-1),'segment':segment,'phase':p,'headingRadians':rig.rotation_euler.z,'rootNativeMeters':list(rig.location)})
for obj in controls:
 for c in obj.animation_data.action.fcurves:
  for k in c.keyframe_points:k.interpolation='LINEAR'
# New packed copy excludes unrelated transition/demo actions. Immutable donor keeps all originals.
keep=set(meta['sourceActions'].values())|set(meta['turnActions'].values())|set(bundle.values())
for action in list(bpy.data.actions):
 if action.name not in keep:bpy.data.actions.remove(action)
scene.frame_start=1;scene.frame_end=49;scene.frame_set(1);bpy.context.preferences.filepaths.save_version=0
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb-native-left120-technical.blend'))
result={'status':'UNREVIEWED ACTUAL TWO-CLIP COMPOSITION; CONTACT/JOIN CHECK REQUIRED','appearance':'rejected generic technical mannequin','source':'../../turn-study/mpfb-native60-turn-technical.blend','sourceSha256':before,'sourceActions':meta['sourceActions'],'retainedValidatedLeft60Actions':meta['turnActions'],'turnActions':bundle,'angleRadians':2*angle,'durationMs':1440,'segmentDurationMs':720,'segments':2,'stepCount':4,'composition':'Two evaluated saved validated60 clips, second rigidly rotated/translocated by actual first endpoint. All local native body/control poses retained. No mirror/foot offset/stride scale.','exactContactEventPhases':[.1,.48,.5,.6,.98],'maximumKeySpacingMs':7.5,'rootArcLengthPlannedMeters':2*.5687545572916666,'rootDisplacementPlannedMeters':list(step+Matrix.Rotation(angle,3,'Z')@step),'cameraProofBudget':12,'renderStatus':'NOT RENDERED','routeCoverage':'Moving arc does not certify arbitrary 1-hex-wide legal routes. Adjacent corner fillets can overlap; compact planted stepping pivot fallback is not authored or certified.','frames':plans}
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before
(OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('LEFT120_SOURCE_BUILT; validated donor unchanged')
