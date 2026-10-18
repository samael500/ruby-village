"""Fresh actual turn soles/ankles/body joins against unchanged straight action."""
from pathlib import Path
import bpy,json,math,hashlib,os
from mathutils import Vector,Matrix,Quaternion
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('RUBY_MPFB_TURN_VARIANT','right60');assert VARIANT in ['right60','left120'];OUT=ROOT/'art/characters-mpfb-v1/motion/turn-variants-study'/VARIANT;meta=json.loads((OUT/'manifest.json').read_text());SOURCE=OUT/('mpfb-native-right60-technical.blend' if VARIANT=='right60' else 'mpfb-native-left120-technical.blend');before=hashlib.sha256(SOURCE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(SOURCE));rig=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();measure.hide_render=True;bpy.context.scene.collection.objects.link(measure);scene=bpy.context.scene
for m in measure.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels
markers={}
for side,sign in [('L',1),('R',-1)]:
 vs=[v for v in measure.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vs);sole=[v for v in vs if v.co.z<z+.008];front=min(v.co.y for v in sole);back=max(v.co.y for v in sole);markers[side]={k:[v.index for v in sole if(v.co.y<front+.025 if k=='toe'else v.co.y>back-.025)]for k in ['toe','heel']}
def activate(bundle):
 for name,action in bundle.items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
def frame(value):scene.frame_set(int(value),subframe=value-int(value));bpy.context.view_layer.update()
def read():
 deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);es=measure.evaluated_get(deps);boot=shoe.evaluated_get(deps);rec={'rootWorld':list(rig.matrix_world.translation),'heading':rig.rotation_euler.z,'bones':{b.name:[list(row)for row in er.matrix_world@b.matrix]for b in er.pose.bones},'feet':{},'minBootZ':min((boot.matrix_world@v.co).z for v in boot.data.vertices)}
 for side in ['L','R']:
  b=er.pose.bones['foot.'+side];helper=er.pose.bones[('left'if side=='L'else'right')+'_foot_ik'];hip=er.pose.bones['upperleg01.'+side].head;knee=er.pose.bones['lowerleg01.'+side].head;ankle=b.head
  rec['feet'][side]={'kneeFlexDegrees':180-math.degrees((hip-knee).angle(ankle-knee)),'upperLegWorldQuaternion':list((er.matrix_world@er.pose.bones['upperleg01.'+side].matrix).to_quaternion()),'lowerLegWorldQuaternion':list((er.matrix_world@er.pose.bones['lowerleg01.'+side].matrix).to_quaternion()),'ankleWorld':list(er.matrix_world@b.head),'helperWorld':list(er.matrix_world@helper.head),'ankleTargetErrorMeters':(b.head-helper.head).length,'sole':{}}
  for kind,ids in markers[side].items():
   points=[es.matrix_world@es.data.vertices[i].co for i in ids];rec['feet'][side]['sole'][kind]=list(sum(points,Vector())/len(points))
 return rec
activate(meta['turnActions']);records=[]
#257 non-key-aligned phases: avoids checking only the authored97 helper targets.
segments=meta.get('segments',1)
for i in range(256*segments+1):
 p=i/256;frame(1+24*p);rec=read();rec['phase']=p;rec['frame']=1+24*p;records.append(rec)
actual={name:records[i]for name,i in [('entry',0),('exit',-1)]};joins={}
for name,observed in actual.items():
 activate(meta['sourceActions']);frame(1+24*meta.get('entrySourcePhase',0));rig.location=Vector(observed['rootWorld']);rig.rotation_euler=(0,0,observed['heading']);bpy.context.view_layer.update();expected=read();joins[name]={'bodyWorldMatrixMaxElementError':max(abs(a-b)for n,rows in observed['bones'].items()for ra,rb in zip(rows,expected['bones'][n])for a,b in zip(ra,rb)),'actualSoleWorldMaxErrorMeters':max((Vector(observed['feet'][s]['sole'][k])-Vector(expected['feet'][s]['sole'][k])).length for s in ['L','R']for k in ['toe','heel']),'ankleWorldMaxErrorMeters':max((Vector(observed['feet'][s]['ankleWorld'])-Vector(expected['feet'][s]['ankleWorld'])).length for s in ['L','R'])}
flats={}
for segment in range(segments):
 for side,offset in [('L',0),('R',.5)]:
  window=[r for r in records if segment<=r['phase']<segment+1 and .1<=((r['phase']+offset+meta.get('entrySourcePhase',0))%1)<=.46]
  flats[f'{segment}:{side}']={k:max((Vector(a['feet'][side]['sole'][k])-Vector(b['feet'][side]['sole'][k])).length for a in window for b in window)for k in ['toe','heel']}
internal={}
if segments==2:
 observed=records[256]
 for label,bundle,f in [('previous60Exit',meta['retainedValidatedLeft60Actions'],25),('next60Entry',meta['retainedValidatedLeft60Actions'],1)]:
  activate(bundle);frame(f);rig.location=Vector(observed['rootWorld']);rig.rotation_euler=(0,0,observed['heading']);bpy.context.view_layer.update();expected=read()
  internal[label]={'bodyWorldMatrixMaxElementError':max(abs(a-b)for n,rows in observed['bones'].items()for ra,rb in zip(rows,expected['bones'][n])for a,b in zip(ra,rb)),'actualSoleWorldMaxErrorMeters':max((Vector(observed['feet'][s]['sole'][k])-Vector(expected['feet'][s]['sole'][k])).length for s in ['L','R']for k in ['toe','heel'])}
activate(meta['turnActions']);frame(1);loopstart=read();step=Vector(actual['exit']['rootWorld']);origin=Vector()
count=round(2*math.pi/abs(meta['angleRadians']))
for k in range(count):origin+=Matrix.Rotation(k*meta['angleRadians'],3,'Z')@step
frame(1+24*segments);rig.location=origin;rig.rotation_euler=(0,0,count*meta['angleRadians']);bpy.context.view_layer.update();loopend=read();loop={'rootClosureMeters':Vector(loopend['rootWorld']).length,'soleClosureMaxMeters':max((Vector(loopstart['feet'][s]['sole'][k])-Vector(loopend['feet'][s]['sole'][k])).length for s in ['L','R']for k in ['toe','heel']),'bodyWorldMatrixMaxElementError':max(abs(a-b)for n,rows in loopstart['bones'].items()for ra,rb in zip(rows,loopend['bones'][n])for a,b in zip(ra,rb)),'method':f'{count} rigidly composed actual saved{abs(round(math.degrees(meta["angleRadians"])))}deg clips; terminal native rig/skin closure only, no complete raster-loop claim'}
summary={'samples':len(records),'internalActual60Joins':internal,'flatWorldSoleDriftMeters':flats,'maxActualAnkleTargetErrorMeters':max(r['feet'][s]['ankleTargetErrorMeters']for r in records for s in ['L','R']),'minActualRenderLevelBootZ':min(r['minBootZ']for r in records),'joinsToUnchangedStraight':joins,'compositionTerminalClosure':loop,'actualRootDeltaMeters':actual['exit']['rootWorld']}
summary['kneeFlexRangeDegrees']={s:[min(r['feet'][s]['kneeFlexDegrees']for r in records),max(r['feet'][s]['kneeFlexDegrees']for r in records)]for s in ['L','R']}
summary['maxAdjacentLegRotationDegreesAt2_8125ms']={s:{part:max(math.degrees(min((angle:=Quaternion(a['feet'][s][part]).rotation_difference(Quaternion(b['feet'][s][part])).angle),2*math.pi-angle))for a,b in zip(records,records[1:]))for part in ['upperLegWorldQuaternion','lowerLegWorldQuaternion']}for s in ['L','R']}
summary['nativeFeasibilityPass']=min(v[0] for v in summary['kneeFlexRangeDegrees'].values())>5 and max(v for d in summary['maxAdjacentLegRotationDegreesAt2_8125ms'].values() for v in d.values())<5 and max(v for f in flats.values()for v in f.values())<.0001 and summary['maxActualAnkleTargetErrorMeters']<.0001 and summary['minActualRenderLevelBootZ']>0 and max(j['actualSoleWorldMaxErrorMeters']for j in joins.values())<.0001 and max(j['bodyWorldMatrixMaxElementError']for j in joins.values())<.0001 and loop['soleClosureMaxMeters']<.0001 and all(j['actualSoleWorldMaxErrorMeters']<.0001 and j['bodyWorldMatrixMaxElementError']<.0001 for j in internal.values())
result={'status':'FRESH ACTUAL NATIVE FEASIBILITY CHECK; NO NATURALNESS OR GAME CLAIM','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'summary':summary,'entryExitActualBodyWorldMatrices':{n:r['bones']for n,r in actual.items()},'records':[{k:v for k,v in r.items()if k!='bones'}for r in records]};assert result['sourceSha256Before']==result['sourceSha256After'];(OUT/'native-contact-join-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
