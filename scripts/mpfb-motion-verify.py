"""Independent fresh-process evaluated mesh/contact evidence, no target readback shortcut."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pilot'
bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');shoe=bpy.data.objects['Ruta.shoes01']
# Disable only subdivision for persistent source-vertex indices in this verification process.
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
markers={}
for side,sign in [('L',1),('R',-1)]:
 vertices=[v for v in shoe.data.vertices if v.co.x*sign>0]
 z=min(v.co.z for v in vertices)
 sole=[v for v in vertices if v.co.z<z+.008]
 front=min(v.co.y for v in sole);back=max(v.co.y for v in sole)
 markers[side]={k:[v.index for v in sole if (v.co.y<front+.025 if k=='toe' else v.co.y>back-.025)]for k in ['toe','heel']}
records=[];pose_matrices=[];pose_hashes=[]
for frame in range(1,26):
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);es=shoe.evaluated_get(deps)
 matrices=[[list(row)for row in b.matrix]for b in er.pose.bones];pose_matrices.append(matrices);pose_hashes.append(hashlib.sha256(json.dumps(matrices).encode()).hexdigest())
 record={'frame':frame,'feet':{}}
 for side,offset in [('L',0),('R',.5)]:
  phase=((frame-1)/24+offset)%1
  d={'phase':phase,'markers':{}}
  for kind,ids in markers[side].items():
   points=[es.matrix_world@es.data.vertices[i].co for i in ids];center=sum(points,Vector())/len(points);d['markers'][kind]={'centerWorld':list(center),'minZ':min(p.z for p in points),'sourceVertexIndices':ids}
  thigh=er.pose.bones['upperleg01.'+side].head;knee=er.pose.bones['lowerleg01.'+side].head;ankle=er.pose.bones['foot.'+side].head
  d['kneeFlexDegrees']=180-math.degrees((thigh-knee).angle(ankle-knee));record['feet'][side]=d
 records.append(record)
summary={}
for side in ['L','R']:
 toe_roll=[r['feet'][side] for r in records[:24] if .48<r['feet'][side]['phase']<.60]
 samples=[r['feet'][side] for r in records[:24] if .10<=r['feet'][side]['phase']<=.46]
 summary[side]={'toePushOffMeasuredDriftMeters':max((Vector(a['markers']['toe']['centerWorld'])-Vector(b['markers']['toe']['centerWorld'])).length for a in toe_roll for b in toe_roll),'flatSoleMeasuredDriftMeters':{kind:max((Vector(a['markers'][kind]['centerWorld'])-Vector(b['markers'][kind]['centerWorld'])).length for a in samples for b in samples)for kind in ['heel','toe']},'kneeFlexRangeDegrees':[min(r['feet'][side]['kneeFlexDegrees']for r in records),max(r['feet'][side]['kneeFlexDegrees']for r in records)],'minSoleHeightMeters':min(r['feet'][side]['markers'][k]['minZ']for r in records for k in ['heel','toe'])}
garments={}
for name in ['Ruta.MPFB.Body','Ruta.male_casualsuit01','Ruta.shoes01','Ruta fitted olive waistcoat']:
 o=bpy.data.objects[name];samples=[]
 for frame in [1,7]:
  bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();eo=o.evaluated_get(bpy.context.evaluated_depsgraph_get());samples.append([v.co.copy()for v in eo.data.vertices])
 delta=[(a-b).length for a,b in zip(*samples)];garments[name]={'armatureModifiers':sum(m.type=='ARMATURE'for m in o.modifiers),'vertexGroups':len(o.vertex_groups),'changedEvaluatedVertices':sum(d>1e-5 for d in delta),'maxObjectSpaceDisplacementMeters':max(delta)}
(OUT/'independent-contact-check.json').write_text(json.dumps({'method':'Fresh .blend reopen; armature-evaluated source shoe sole vertices, subdivision disabled only for stable index correspondence; all contacts measured in world coordinates','summary':summary,'actualWeightedGarmentDeformation':garments,'uniqueEvaluatedPoseCount':len(set(pose_hashes[:24])),'rootRelativeLoopEndpointMaxMatrixError':max(abs(a-b)for ma,mb in zip(pose_matrices[0],pose_matrices[-1])for ra,rb in zip(ma,mb)for a,b in zip(ra,rb)),'records':records},indent=2)+'\n');print(json.dumps(summary,indent=2))
