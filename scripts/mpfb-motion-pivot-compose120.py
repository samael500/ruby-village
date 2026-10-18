"""Two actual saved60 compact pivots; retain all local native body/carry poses."""
from pathlib import Path
import bpy,json,math,hashlib,os
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('RUBY_MPFB_PIVOT_VARIANT','left120');assert VARIANT in ['left120','right120'];OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-variants'/VARIANT
SOURCE=(ROOT/'art/characters-mpfb-v1/motion/pivot-study/mpfb-compact-pivot60-technical.blend') if VARIANT=='left120' else (OUT.parent/'right60/mpfb-compact-pivot-technical.blend')
meta=json.loads((SOURCE.parent/'manifest.json').read_text());native=json.loads((SOURCE.parent/'native-contact-join-check.json').read_text());assert native['summary']['nativeFeasibilityPass'];assert json.loads((SOURCE.parent/'boot-surface-check.json').read_text())['maximumBootIntersectionPairs']==0;assert json.loads((SOURCE.parent/'carry-check.json').read_text())['armBagAndGripPass'];before=hashlib.sha256(SOURCE.read_bytes()).hexdigest();assert native['sourceSha256Before']==before
bpy.ops.wm.open_mainfile(filepath=str(SOURCE));scene=bpy.context.scene;rig=bpy.data.objects['Ruta.MPFB.StandardRig'];controls=[bpy.data.objects[n] for n in meta['turnActions']]
for obj in controls:obj.animation_data.action=bpy.data.actions[meta['turnActions'][obj.name]]
def frame(f):scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update()
keys=sorted({float(p.co.x) for c in rig.animation_data.action.fcurves if c.data_path=='location' for p in c.keyframe_points});samples=[]
for f in keys:
 frame(f);samples.append({'frame':f,'root':rig.location.copy(),'rotation':rig.rotation_euler.copy(),'basis':{b.name:b.matrix_basis.copy() for b in rig.pose.bones},'controls':{o.name:o.location.copy() for o in controls if o!=rig}})
step=samples[-1]['root'].copy();angle=float(samples[-1]['rotation'].z);bundle={}
for obj in controls:
 action=bpy.data.actions.new('MPFB compact '+VARIANT+' two actual60 / '+obj.name);action.use_fake_user=True;obj.animation_data.action=action;bundle[obj.name]=action.name
plans=[]
for segment in range(2):
 origin=Vector() if segment==0 else step;rot=Matrix.Rotation(segment*angle,3,'Z')
 for index,s in enumerate(samples):
  if segment and index==0:continue
  f=s['frame']+40*segment;frame(f)
  for name,m in s['basis'].items():rig.pose.bones[name].matrix_basis=m
  rig.location=origin+rot@s['root'];rig.rotation_euler=s['rotation'];rig.rotation_euler.z+=segment*angle
  for obj in controls:
   if obj!=rig:obj.location=s['controls'][obj.name]
  bpy.context.view_layer.update();rig.keyframe_insert('location',frame=f);rig.keyframe_insert('rotation_euler',frame=f)
  for b in rig.pose.bones:b.keyframe_insert('location',frame=f);b.keyframe_insert('rotation_euler',frame=f)
  for obj in controls:
   if obj!=rig:obj.keyframe_insert('location',frame=f)
  plans.append({'frame':f,'timeMs':30*(f-1),'segment':segment,'phase':(s['frame']-1)/40,'rootNativeMeters':list(rig.location),'yawRadians':rig.rotation_euler.z})
for obj in controls:
 for c in obj.animation_data.action.fcurves:
  for k in c.keyframe_points:k.interpolation='LINEAR'
scene.frame_start=1;scene.frame_end=81;scene.frame_set(1);bpy.context.preferences.filepaths.save_version=0;bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'mpfb-compact-pivot-technical.blend'),compress=True)
result={'status':'UNREVIEWED TWO ACTUAL60 PIVOT COMPOSITION; MEASURED JOINS/CONTACTS REQUIRED','variant':VARIANT,'appearance':'rejected generic technical mannequin','sourceRepositoryPath':str(SOURCE.relative_to(ROOT)),'sourceSha256':before,'retained60Actions':meta['turnActions'],'sourceActions':meta['sourceActions'],'idleActions':meta['idleActions'],'transitionClips':meta['transitionClips'],'turnActions':bundle,'angleRadians':2*angle,'durationMs':2400,'segments':2,'segmentDurationMs':1200,'frames':plans,'rootBalancePlannedMaximumMeters':.03,'worldRootBoundTargetMeters':.10,'entryExit':'Unchanged flat idle at yaw0/+or-120,root0; internal actual60 idle-to-idle join at1200ms. Requires stop+settle before and native start afterward, not continuous walking.','composition':'Second complete native clip rigidly rotated by actual first endpoint yaw; no mirror, independent foot offsets, stride scale or root distance fit.','renderStatus':'NOT RENDERED','proofBudget':12,'routeCoverage':'Not certified full body/bag/boot swept clearance or arbitrary legal route coverage.'};assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before;(OUT/'manifest.json').write_text(json.dumps(result,indent=2)+'\n');print('COMPACT120_SOURCE',VARIANT,'unreviewed; donor unchanged')
