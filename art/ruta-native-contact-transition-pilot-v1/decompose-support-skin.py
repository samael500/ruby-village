from pathlib import Path
O=Path(__file__).resolve().parent
exec((O/'check.py').read_text().split('joins=[]')[0])
c=contract['clips']['start'];predicted=[];actual=[];contributions={};control=[];binds=[]
for j in range(81):
 time=j/80*.2;points,_,_=evaluate(c['action'],time,rootAt(c,time));actual.append(points);control.append([list(r)for r in rig.matrix_world@rig.pose.bones['Foot.R'].matrix]);frame=[]
 for vertexId in ids:
  vertex=feet.data.vertices[vertexId];bind=rig.matrix_world.inverted()@feet.matrix_world@vertex.co;binds.append(list(bind));result=Vector((0,0,0))
  for group in vertex.groups:
   name=feet.vertex_groups[group.group].name
   if name not in rig.pose.bones:continue
   pb=rig.pose.bones[name];part=(rig.matrix_world@pb.matrix@pb.bone.matrix_local.inverted()@bind)*group.weight;result+=part;contributions.setdefault((vertexId,name),[]).append(list(part))
  frame.append(list(result))
 predicted.append(frame)
a=np.array(actual);b=np.array(predicted);idsR=[ids[i]for i in sides['R']];rows=[]
for (vertexId,name),points in contributions.items():
 if vertexId in idsR:rows.append({'vertexId':vertexId,'bone':name,'weightedWorldContributionAxisSpanM':np.ptp(np.array(points),axis=0).tolist()})
report={'status':'LBS-SKIN-DECOMPOSITION-DIAGNOSTIC-NO-WEIGHT-EDIT','modifierPreserveVolume':[m.use_deform_preserve_volume for m in feet.modifiers if m.type=='ARMATURE'],'predictedVsActualMaximumAbsM':float(abs(a-b).max()),'FootRWorld16EntryMaximumSpan':float(np.ptp(np.array(control),axis=0).max()),'vertex279Contributions':[r for r in rows if r['vertexId']==279],'allRightSoleContributions':rows,'definition':'sum exact weighted (rigWorld*poseBone*restBone^-1*rigWorld^-1*meshWorld*restVertex), compared against evaluated actual mesh','weightsEdited':False};(O/'skin-contribution-check.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items()if k!='allRightSoleContributions'},indent=2))
