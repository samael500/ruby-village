import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
import os
V=os.environ.get('RUBY_MPFB_TURN_VARIANT','right60');assert V in ['right60','left120'];R=Path('/tmp/ruby-qa-turn-variants');D=R/'art/characters-mpfb-v1/motion/turn-variants-study'/V;O=R/'docs/chapter-1-rc/qa/mpfb-variants-169468c'/V;m=json.loads((D/'manifest.json').read_text());src=D/('mpfb-native-right60-technical.blend'if V=='right60'else'mpfb-native-left120-technical.blend');before=hashlib.sha256(src.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(src));segments=m.get('segments',1);entry=m.get('entrySourcePhase',0);s=bpy.context.scene;r=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];copy=shoe.copy();copy.data=shoe.data.copy();copy.hide_render=True;s.collection.objects.link(copy)
for mod in copy.modifiers:
 if mod.type=='SUBSURF':mod.show_viewport=False
for mod in shoe.modifiers:
 if mod.type=='SUBSURF':mod.levels=mod.render_levels
markers={}
for side,sign in [('L',1),('R',-1)]:
 vs=[v for v in copy.data.vertices if v.co.x*sign>0];bottom=min(v.co.z for v in vs);sole=[v for v in vs if v.co.z<bottom+.008];front=min(v.co.y for v in sole);back=max(v.co.y for v in sole);markers[side]={kind:[v.index for v in sole if(v.co.y<front+.025 if kind=='toe'else v.co.y>back-.025)]for kind in ['toe','heel']}
def actions(bundle):
 for name,a in bundle.items():bpy.data.objects[name].animation_data.action=bpy.data.actions[a]
def frame(t):s.frame_set(int(t),subframe=t-int(t));bpy.context.view_layer.update()
def read():
 dg=bpy.context.evaluated_depsgraph_get();er=r.evaluated_get(dg);es=copy.evaluated_get(dg);boot=shoe.evaluated_get(dg);feet={}
 for side in ['L','R']:
  ankle=er.pose.bones['foot.'+side];ik=er.pose.bones[('left'if side=='L'else'right')+'_foot_ik'];upper=er.pose.bones['upperleg01.'+side];lower=er.pose.bones['lowerleg01.'+side];soles={}
  for kind,ids in markers[side].items():soles[kind]=list(sum((es.matrix_world@es.data.vertices[i].co for i in ids),Vector())/len(ids))
  feet[side]=dict(sole=soles,ankleError=(ankle.head-ik.head).length,upperQuat=list((er.matrix_world@upper.matrix).to_quaternion()),lowerQuat=list((er.matrix_world@lower.matrix).to_quaternion()),kneeFlex=180-math.degrees((upper.head-lower.head).angle(ankle.head-lower.head)))
 return dict(root=list(r.matrix_world.translation),yaw=r.rotation_euler.z,feet=feet,bones={b.name:[list(row)for row in er.matrix_world@b.matrix]for b in er.pose.bones},minBootZ=min((boot.matrix_world@v.co).z for v in boot.data.vertices))
actions(m['turnActions']);rows=[]
for i in range(256*segments+1):
 p=i/256;frame(1+24*p);rec=read();rec['phase']=p;rows.append(rec)
joins={}
for name,rec in [('entry',rows[0]),('exit',rows[-1])]:
 actions(m['sourceActions']);frame(1+24*entry);r.location=Vector(rec['root']);r.rotation_euler=(0,0,rec['yaw']);bpy.context.view_layer.update();straight=read();joins[name]=dict(soleMax=max(math.dist(rec['feet'][side]['sole'][kind],straight['feet'][side]['sole'][kind])for side in ['L','R']for kind in ['toe','heel']),bodyMatMax=max(abs(a-b)for n in rec['bones']for x,y in zip(rec['bones'][n],straight['bones'][n])for a,b in zip(x,y)))
internal={}
if segments==2:
 obs=rows[256]
 for label,f in [('previous60Exit',25),('next60Entry',1)]:
  actions(m['retainedValidatedLeft60Actions']);frame(f);r.location=Vector(obs['root']);r.rotation_euler=(0,0,obs['yaw']);bpy.context.view_layer.update();expected=read();internal[label]=dict(soleMax=max(math.dist(obs['feet'][side]['sole'][kind],expected['feet'][side]['sole'][kind])for side in ['L','R']for kind in ['toe','heel']),bodyMatMax=max(abs(a-b)for n in obs['bones']for x,y in zip(obs['bones'][n],expected['bones'][n])for a,b in zip(x,y)))
# Evaluate actual composed clip endpoints using the measured rigid placements.
step=Vector(rows[-1]['root']);origin=Vector();compositions=[];actions(m['turnActions']);previous=None
for k in range(round(2*math.pi/abs(m['angleRadians']))):
 rot=Matrix.Rotation(k*m['angleRadians'],3,'Z');pair=[]
 for f in [1,1+24*segments]:
  frame(f);local=r.location.copy();yaw=r.rotation_euler.z;r.location=origin+rot@local;r.rotation_euler=(0,0,k*m['angleRadians']+yaw);bpy.context.view_layer.update();pair.append(read())
 seam=0 if previous is None else max(math.dist(previous['feet'][side]['sole'][kind],pair[0]['feet'][side]['sole'][kind])for side in ['L','R']for kind in ['toe','heel']);bodyseam=0 if previous is None else max(abs(a-b)for n in previous['bones']for x,y in zip(previous['bones'][n],pair[0]['bones'][n])for a,b in zip(x,y));compositions.append(dict(clip=k,origin=list(origin),entryRoot=pair[0]['root'],exitRoot=pair[-1]['root'],previousSoleSeam=seam,previousBodyMatrixSeam=bodyseam));previous=pair[-1];origin+=rot@step
closure=max(math.dist(rows[0]['feet'][side]['sole'][kind],previous['feet'][side]['sole'][kind])for side in ['L','R']for kind in ['toe','heel'])
flat={};legRot={}
for side,off in [('L',0),('R',.5)]:
 subset=[a for a in rows if .1<=((a['phase']+off+entry)%1)<=.46 and a['phase']<1];flat[side]={kind:max(math.dist(a['feet'][side]['sole'][kind],b['feet'][side]['sole'][kind])for a in subset for b in subset)for kind in ['toe','heel']};legRot[side]={kind:max(math.degrees(min((ang:=Quaternion(a['feet'][side][kind]).rotation_difference(Quaternion(b['feet'][side][kind])).angle),2*math.pi-ang))for a,b in zip(rows,rows[1:]))for kind in ['upperQuat','lowerQuat']}
for seg in range(segments):
 for side,off in [('L',0),('R',.5)]:
  subset=[a for a in rows if seg<=a['phase']<seg+1 and .1<=((a['phase']+off+entry)%1)<=.46];flat[f'{seg}:{side}']={kind:max(math.dist(a['feet'][side]['sole'][kind],b['feet'][side]['sole'][kind])for a in subset for b in subset)for kind in ['toe','heel']}
summary=dict(internal60Joins=internal,samples=len(rows),sourceSha256=before,flatDriftMeters=flat,joins=joins,maxAnkleError=max(rec['feet'][side]['ankleError']for rec in rows for side in ['L','R']),minBootZ=min(rec['minBootZ']for rec in rows),maxAdjacentLegRotDegrees=legRot,kneeFlexRange={side:[min(rec['feet'][side]['kneeFlex']for rec in rows),max(rec['feet'][side]['kneeFlex']for rec in rows)]for side in ['L','R']},actualRootDelta=rows[-1]['root'],actualExitYaw=rows[-1]['yaw'],sixCompositions=compositions,sixRootClosure=origin.length,sixSoleClosure=closure)
assert max(v for f in flat.values()for v in f.values())<.0001 and summary['maxAnkleError']<.0001 and summary['minBootZ']>0
assert max(j['soleMax']for j in joins.values())<.0001 and max(j['bodyMatMax']for j in joins.values())<.0001 and closure<.0001
assert hashlib.sha256(src.read_bytes()).hexdigest()==before
(O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(O/'actual-samples.json').write_text(json.dumps([{k:v for k,v in rec.items()if k!='bones'}for rec in rows],indent=2)+'\n');print(json.dumps(summary,indent=2))
