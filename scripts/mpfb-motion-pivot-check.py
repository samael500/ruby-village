"""Fresh actual turn soles/ankles/body joins against unchanged straight action."""
from pathlib import Path
import bpy,json,math,hashlib,os
from mathutils import Vector,Matrix,Quaternion
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-study';meta=json.loads((OUT/'manifest.json').read_text());SOURCE=OUT/'mpfb-compact-pivot60-technical.blend';before=hashlib.sha256(SOURCE.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(SOURCE));rig=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];measure=shoe.copy();measure.data=shoe.data.copy();measure.hide_render=True;bpy.context.scene.collection.objects.link(measure);scene=bpy.context.scene
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
for i in range(401):
 p=i/400;f=1+40*p;frame(f);r=read();r['phase']=p;r['frame']=f;r['timeMs']=p*meta['durationMs'];records.append(r)
joins={}
for name,observed in [('entry',records[0]),('exit',records[-1])]:
 activate(meta['idleActions']);frame(1);rig.location=Vector(observed['rootWorld']);rig.rotation_euler=(0,0,observed['heading']);bpy.context.view_layer.update();expected=read()
 joins[name]={'bodyWorldMatrixMaxElementError':max(abs(a-b) for n,rows in observed['bones'].items() for ra,rb in zip(rows,expected['bones'][n]) for a,b in zip(ra,rb)),'actualSoleWorldMaxErrorMeters':max((Vector(observed['feet'][s]['sole'][k])-Vector(expected['feet'][s]['sole'][k])).length for s in ['L','R'] for k in ['toe','heel'])}
flats={}
for side,windows in [('L',[(0,.12),(.50,1)]),('R',[(0,.62),(.96,1)])]:
 for index,(a,b) in enumerate(windows):
  window=[r for r in records if a+1e-8<=r['phase']<=b-1e-8]
  flats[f'{side}:{index}']={kind:max((Vector(x['feet'][side]['sole'][kind])-Vector(y['feet'][side]['sole'][kind])).length for x in window for y in window) for kind in ['toe','heel']}
summary={'samples':len(records),'sampleSpacingMs':3,'flatWorldSoleDriftMeters':flats,'maxActualAnkleTargetErrorMeters':max(r['feet'][s]['ankleTargetErrorMeters'] for r in records for s in ['L','R']),'minActualRenderLevelBootZ':min(r['minBootZ'] for r in records),'joinsToUnchangedFlatIdle':joins,'actualRootDeltaMeters':records[-1]['rootWorld'],'maxActualRootDistanceFromPivotOriginMeters':max(Vector(r['rootWorld']).length for r in records),'rootXYBoundsMeters':[[min(r['rootWorld'][i] for r in records),max(r['rootWorld'][i] for r in records)] for i in range(2)],'kneeFlexRangeDegrees':{s:[min(r['feet'][s]['kneeFlexDegrees'] for r in records),max(r['feet'][s]['kneeFlexDegrees'] for r in records)] for s in ['L','R']},'maxAdjacentLegRotationDegreesAt3ms':{s:{part:max(math.degrees(min((angle:=Quaternion(a['feet'][s][part]).rotation_difference(Quaternion(b['feet'][s][part])).angle),2*math.pi-angle)) for a,b in zip(records,records[1:])) for part in ['upperLegWorldQuaternion','lowerLegWorldQuaternion']} for s in ['L','R']}}
summary['nativeFeasibilityPass']=max(v for f in flats.values() for v in f.values())<.0001 and summary['maxActualAnkleTargetErrorMeters']<.0001 and summary['minActualRenderLevelBootZ']>0 and summary['maxActualRootDistanceFromPivotOriginMeters']<=.10 and max(j['actualSoleWorldMaxErrorMeters'] for j in joins.values())<.0001 and max(j['bodyWorldMatrixMaxElementError'] for j in joins.values())<.0001 and min(v[0] for v in summary['kneeFlexRangeDegrees'].values())>5 and max(v for row in summary['maxAdjacentLegRotationDegreesAt3ms'].values() for v in row.values())<5
result={'status':'ACTUAL SAVED NATIVE PIVOT CONTACT/JOIN CHECK; NO NATURALNESS OR ONE-HEX CLEARANCE CLAIM','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'summary':summary,'entryExitActualBodyWorldMatrices':{name:r['bones'] for name,r in [('entry',records[0]),('exit',records[-1])]},'records':[{k:v for k,v in r.items() if k!='bones'} for r in records]};assert result['sourceSha256Before']==result['sourceSha256After'];(OUT/'native-contact-join-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
