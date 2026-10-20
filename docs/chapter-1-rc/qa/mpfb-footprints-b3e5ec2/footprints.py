import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path('/tmp/ruby-qa-pivot-footprints');D=R/'art/characters-mpfb-v1/motion/footprints-native-v1';O=R/'docs/chapter-1-rc/qa/mpfb-footprints-b3e5ec2';m=json.loads((D/'manifest.json').read_text());rows=[];statecounts={};current=None;signatures={}
def hull(points):
 ps=sorted(set((p.x,p.y)for p in points))
 def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
 out=[]
 for seq in [ps,list(reversed(ps))]:
  chain=[]
  for p in seq:
   while len(chain)>1 and cross(chain[-2],chain[-1],p)<=0:chain.pop()
   chain.append(p)
  out+=chain[:-1]
 return out
for state,spec in m['states'].items():
 data=json.loads((D/spec['file']).read_text());receipt=m['sources'][spec['sourceSha256']];src=R/receipt['source'];sha=hashlib.sha256(src.read_bytes()).hexdigest();assert sha==spec['sourceSha256']==data['sourceSha256'];statecounts[state]=len(data['records'])
 if current!=sha:bpy.ops.wm.open_mainfile(filepath=str(src));current=sha
 rig=bpy.data.objects[receipt['rigObject']];shoe=bpy.data.objects[receipt['bootObject']];s=bpy.context.scene
 for n,a in data['actionBundle'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
 for mod in shoe.modifiers:
  if mod.type=='SUBSURF':mod.levels=mod.render_levels
 actualsig=hashlib.sha256(json.dumps({'vertices':[list(v.co)for v in shoe.data.vertices],'faces':[list(p.vertices)for p in shoe.data.polygons],'groups':[g.name for g in shoe.vertex_groups],'weights':[[(g.group,g.weight)for g in v.groups]for v in shoe.data.vertices]},sort_keys=True).encode()).hexdigest();assert actualsig==receipt['rawBootGeometryWeightSha256'];signatures[sha]=actualsig
 regions=None
 for rec in data['records']:
  f=rec['frame'];s.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(dg);eo=shoe.evaluated_get(dg);root=er.matrix_world.translation;rot=er.matrix_world.to_quaternion();inv=rot.inverted();points=[eo.matrix_world@v.co for v in eo.data.vertices]
  assert len(points)==receipt['evaluatedTopologyVertexCount'] and s.unit_settings.scale_length==1 and er.matrix_world.determinant()>0
  if regions is None:
   regions={}
   for side in ['L','R']:
    groups={g.index for g in shoe.vertex_groups if g.name.endswith('.'+side)};regions[side]=[v.index for v in eo.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5];assert regions[side]
  errors=[];roundtrip=[];wrongdouble=[]
  for side,ids in regions.items():
   actual=rec['feet'][side];assert len(ids)==actual['evaluatedSelectedVertices'];relative=[points[i]-root for i in ids];local=[inv@p for p in relative]
   for polygon,stored in [(hull(relative),actual['fullBootXYHullRootRelativeNativeMeters']),(hull(local),actual['fullBootXYHullActorOrientationRemovedMeters'])]:
    assert len(polygon)==len(stored);errors.extend(math.dist(a,b)for a,b in zip(polygon,stored));assert sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(stored,stored[1:]+stored[:1]))>0
   for i,p in zip(ids,local):roundtrip.append((rot@p+root-points[i]).length)
   for p in relative:wrongdouble.append((rot@p-p).length)
  row=dict(state=state,frame=f,sourceSha256=sha,rootError=(root-Vector(rec['rootNativeTranslationMeters'])).length,hullMaxReadbackError=max(errors),orientationRemovedWorldRoundtripMaxError=max(roundtrip),doubleYawWouldDisplaceMaxMeters=max(wrongdouble));assert max(errors)<1e-6 and row['rootError']<1e-6 and max(roundtrip)<1e-6;rows.append(row)
 assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
assert len(rows)==m['recordCount']==335 and len(statecounts)==11
out=dict(actualRecordCount=len(rows),stateCounts=statecounts,sourceShoeSignatures=signatures,maxHullReadbackError=max(r['hullMaxReadbackError']for r in rows),maxRootReadbackError=max(r['rootError']for r in rows),maxOrientationRemovedRoundtripError=max(r['orientationRemovedWorldRoundtripMaxError']for r in rows),maxWrongDoubleYawDisplacementMeters=max(r['doubleYawWouldDisplaceMaxMeters']for r in rows),scope='335 actual discrete records; not continuous swept volume; source/shoe hash invalidation required',records=rows);(O/'all335-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k!='records'},indent=2))
