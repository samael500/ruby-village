"""Optional derivative ONLY selected56 sole weights; frozen source never saved. Measure old Walk48 impact."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec((O/'check.py').read_text().split('joins=[]')[0])
sourceFeet=feet.data;baseline=[];detailNames=['Ankle boot lace L','Ankle boot lace R','Cream sock cuff L','Cream sock cuff R'];details=[]
def meshPoints(ob):
 ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();p=np.array([list(ev.matrix_world@v.co)for v in m.vertices]);ev.to_mesh_clear();return p
for j in range(48):
 evaluate('Walk_ProportionProposal',40/24*j/48);baseline.append(meshPoints(feet));details.append({n:meshPoints(bpy.data.objects[n])for n in detailNames})
originalWeights={str(vertexId):{feet.vertex_groups[g.group].name:g.weight for g in feet.data.vertices[vertexId].groups}for vertexId in ids};feet.data=feet.data.copy();feet.data.name='Adventurer_Feet_contactSoleOnly_VARIANT'
for side in ['L','R']:
 vertexIds=meta['regions'][side]['sole']
 for group in feet.vertex_groups:
  if group.name!='Foot.'+side:group.remove(vertexIds)
 feet.vertex_groups['Foot.'+side].add(vertexIds,1.,'REPLACE')
variant=[];detailDelta=0.
for j in range(48):
 evaluate('Walk_ProportionProposal',40/24*j/48);variant.append(meshPoints(feet))
 for n in detailNames:detailDelta=max(detailDelta,float(abs(meshPoints(bpy.data.objects[n])-details[j][n]).max()))
delta=np.array(variant)-np.array(baseline);unchanged=[i for i in range(len(feet.data.vertices))if i not in ids];metrics={'originalWalk48MaximumSolePointDisplacementM':float(np.linalg.norm(delta[:,ids],axis=2).max()),'originalWalk48RmsSolePointDisplacementM':float(np.sqrt(np.mean(delta[:,ids]**2))),'upperBootUnselectedVertexMaxAbsDeltaM':float(abs(delta[:,unchanged]).max()),'lacesSockCuffMaxAbsDeltaM':detailDelta,'changedSoleVertexCount':len(ids),'totalFootVertices':len(feet.data.vertices),'perFootOriginalWalk48MaximumSolePointDisplacementM':{s:float(np.linalg.norm(delta[:,meta['regions'][s]['sole']],axis=2).max())for s in ['L','R']}}
contact={}
for clip,c in contract['clips'].items():
 positions=[]
 for j in range(161):
  t=c['durationSeconds']*j/160;points,_,_=evaluate(c['action'],t,rootAt(c,t));positions.append(points)
 positions=np.array(positions);support='R'if clip=='start'else'L';end=80 if clip=='start'else 160;selected=positions[:end+1,sides[support]];span=np.ptp(selected,axis=0);contact[clip]={'supportSide':support,'supportIntervalSeconds':[0,c['durationSeconds']*end/160],'maximumSupportSoleAxisSpanM':span.max(axis=0).tolist(),'maximumSupportSoleEuclideanSpanBoundM':float(np.linalg.norm(span,axis=1).max()),'allFeetMinimumSoleZM':float(positions[:,:,2].min()),'maximumDepthBelowInferredFloorM':max(0,-.001194837037473917-float(positions[:,:,2].min()))};np.savez_compressed(O/(clip+'-sole-Foot1-variant.npz'),positions=positions,times=np.linspace(0,c['durationSeconds'],161),vertex_ids=np.array(ids))
bpy.data.libraries.write(str(O/'sole-weight-variant.blend'),{feet.data},fake_user=True,compress=True)
report={'status':'SOLE-WEIGHT-DERIVATIVE-STUDY-NOT-ACCEPTED-WALK-EQUIVALENCE','originalFrozenSourceUnchanged':True,'newWeights':'selected56actualsolevertices→correspondingFoot.side1; allother280footverticesunchanged','originalWeights':originalWeights,'groupIndexNames':[g.name for g in feet.vertex_groups],'geometryUVTopologyMaterialRestUnchanged':True,'sourceActionsRigRestUnchanged':True,'metrics':metrics,'transitionContact':contact,'sourceWalkVisualGeometryChanged':metrics['originalWalk48MaximumSolePointDisplacementM']>0,'limitations':['Intentional skin-weight delta affects old Walk visible sole; cannot claim original Walk deformation exact','No change to laces/upperboot but weight boundary needs actual render review','No physical no-slip guarantee; source floor and material-point subset inferred']};(O/'sole-weight-variant-contract.json').write_text(json.dumps(report,indent=2));print(json.dumps({'metrics':metrics,'contact':contact},indent=2),flush=True)
