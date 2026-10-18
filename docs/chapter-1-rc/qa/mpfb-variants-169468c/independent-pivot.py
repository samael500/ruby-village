import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
R=Path('/tmp/ruby-qa-turn-variants');D=R/'art/characters-mpfb-v1/motion/pivot-study';O=R/'docs/chapter-1-rc/qa/mpfb-variants-169468c/pivot';m=json.loads((D/'manifest.json').read_text());src=D/'mpfb-compact-pivot60-technical.blend';before=hashlib.sha256(src.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;r=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];copy=shoe.copy();copy.data=shoe.data.copy();copy.hide_render=True;s.collection.objects.link(copy)
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
from mathutils.bvhtree import BVHTree
actions(m['turnActions']);rows=[];regions={}
for i in range(401):
 phase=i/400;frame(1+40*phase);rec=read();rec['phase']=phase;eo=shoe.evaluated_get(bpy.context.evaluated_depsgraph_get());verts=[eo.matrix_world@v.co for v in eo.data.vertices];trees={}
 for side in ['L','R']:
  if side not in regions:
   groups={g.index for g in shoe.vertex_groups if g.name.endswith('.'+side)};ids={v.index for v in eo.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5};polys=[list(p.vertices)for p in eo.data.polygons if all(v in ids for v in p.vertices)];assert ids and polys;regions[side]=polys
  trees[side]=BVHTree.FromPolygons(verts,regions[side])
 rec['bootTriangleIntersections']=len(trees['L'].overlap(trees['R']));rows.append(rec)
joins={}
for name,rec in [('entry',rows[0]),('exit',rows[-1])]:
 actions(m['idleActions']);frame(1);r.location=Vector(rec['root']);r.rotation_euler=(0,0,rec['yaw']);bpy.context.view_layer.update();idle=read();joins[name]=dict(soleMax=max(math.dist(rec['feet'][side]['sole'][kind],idle['feet'][side]['sole'][kind])for side in ['L','R']for kind in ['toe','heel']),bodyMatMax=max(abs(a-b)for n in rec['bones']for x,y in zip(rec['bones'][n],idle['bones'][n])for a,b in zip(x,y)))
flat={}
for side,windows in [('L',[(0,.12),(.5,1)]),('R',[(0,.62),(.96,1)])]:
 for i,(a,b)in enumerate(windows):
  sub=[rec for rec in rows if a+1e-8<=rec['phase']<=b-1e-8];flat[side+str(i)]={kind:max(math.dist(x['feet'][side]['sole'][kind],y['feet'][side]['sole'][kind])for x in sub for y in sub)for kind in ['toe','heel']}
summary=dict(samples=401,sourceSha256=before,flatDriftMeters=flat,joins=joins,maxAnkleError=max(rec['feet'][side]['ankleError']for rec in rows for side in ['L','R']),minBootZ=min(rec['minBootZ']for rec in rows),maximumBootTriangleIntersections=max(rec['bootTriangleIntersections']for rec in rows),regionPolygonCounts={side:len(ps)for side,ps in regions.items()},rootDelta=rows[-1]['root'],maxRootDistance=max(Vector(rec['root']).length for rec in rows),kneeFlexRange={side:[min(rec['feet'][side]['kneeFlex']for rec in rows),max(rec['feet'][side]['kneeFlex']for rec in rows)]for side in ['L','R']},maxAdjacentLegRotationDegrees={side:{kind:max(math.degrees(min((ang:=Quaternion(a['feet'][side][kind]).rotation_difference(Quaternion(b['feet'][side][kind])).angle),2*math.pi-ang))for a,b in zip(rows,rows[1:]))for kind in ['upperQuat','lowerQuat']}for side in ['L','R']})
assert summary['maximumBootTriangleIntersections']==0 and max(v for f in flat.values()for v in f.values())<.0001 and summary['maxAnkleError']<.0001 and summary['minBootZ']>0
assert max(j['soleMax']for j in joins.values())<.0001 and max(j['bodyMatMax']for j in joins.values())<.0001
assert hashlib.sha256(src.read_bytes()).hexdigest()==before
(O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(O/'actual401.json').write_text(json.dumps([{k:v for k,v in rec.items()if k!='bones'}for rec in rows],indent=2)+'\n');print(json.dumps(summary,indent=2))
