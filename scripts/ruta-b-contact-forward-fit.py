"""One periodic nonnegative translation contract from measured material sole vertices.
No bone edits, image transforms, camera fitting or ankle-as-contact substitution.
Run with numpy Python after Blender sampler. Units m, s.
"""
from pathlib import Path
import json, numpy as np, hashlib
R=Path(__file__).resolve().parents[1]; O=R/'art/ruta-b-contact-forward-v1'
m=json.loads((O/'sample-source.json').read_text()); a=np.load(O/'actual-sole-samples.npz');p=a['positions'];t=a['sample_times'];dt=t[1]-t[0];N=len(t)-1;T=t[-1];q=p[:-1];vel=(np.roll(q,-1,axis=0)-np.roll(q,1,axis=0))/(2*dt);u=vel[:,:,1];floor=float(p[:,:,2].min());side=np.array(m['columnSides']);region=np.array(m['columnRegions']);area=a['rest_area_weights'];tau=.025

def fit(h):
 w=area[None,:]*np.maximum(0,1-np.maximum(0,q[:,:,2]-floor)/h)**2; W=w.sum(axis=1);b=(w*u).sum(axis=1); wn=W/W.mean(); target=np.divide(b,W,out=np.zeros_like(W),where=W>0);lam=(tau/dt)**2
 A=np.diag(wn+2*lam)
 for i in range(N):A[i,(i+1)%N]-=lam;A[i,(i-1)%N]-=lam
 rhs=wn*target;v=np.linalg.solve(A,rhs)
 # Nonnegative constraint: projected gradient only if unconstrained solution is infeasible.
 iterations=0
 if v.min()<0:
  v=np.maximum(v,0);step=1/(wn.max()+4*lam)
  for iterations in range(100000):
   nv=np.maximum(0,v-step*(A@v-rhs))
   if np.max(abs(nv-v))<1e-12:v=nv;break
   v=nv
 grad=A@v-rhs;kkt=float(np.max(abs(np.where(v>1e-9,grad,np.minimum(grad,0)))))
 vc=np.r_[v,v[0]];s=np.r_[0,np.cumsum((vc[:-1]+vc[1:])*dt/2)]
 def metric(speed, mask=None):
  ww=w if mask is None else w*mask[None,:];r=vel.copy();r[:,:,1]-=np.asarray(speed).reshape(-1,1) if np.ndim(speed) else speed;den=ww.sum()
  return {'forwardRmsMps':float(np.sqrt((ww*r[:,:,1]**2).sum()/den)),'full3dRmsMps':float(np.sqrt((ww*(r*r).sum(axis=2)).sum()/den))}
 constant=float(b.sum()/W.sum());same=float(s[-1]/T);conf=np.array([w[:,side==x].sum(axis=1)for x in ['L','R']]).T;means=np.array([np.divide((w[:,side==x]*u[:,side==x]).sum(axis=1),conf[:,j],out=np.zeros(N),where=conf[:,j]>0)for j,x in enumerate(['L','R'])]).T;both=(conf>.01).all(axis=1);gap=means[:,0]-means[:,1];switch=np.where(np.any((conf>.01)!=np.roll(conf>.01,1,axis=0),axis=1))[0]
 stats={'heightBandM':h,'strideM':float(s[-1]),'speedMinMps':float(v.min()),'speedMaxMps':float(v.max()),'constantBestActualSoleMps':constant,'sameStrideConstantMps':same,'uniformBestActualSole':metric(constant),'uniformSameStride':metric(same),'previousAnkleDerivedUniform':metric(.707461237907431),'contactAware':metric(v),'unsmoothedPerPhaseLowerBound':metric(np.maximum(target,0)),'perFoot':{x:metric(v,side==x)for x in ['L','R']},'perRegion':{x:metric(v,region==x)for x in ['heel','toe','midsole']},'supportConfidenceThreshold':.01,'noFootAboveConfidenceFraction':float(np.mean((conf<=.01).all(axis=1))),'zeroTotalWeightFraction':float(np.mean(W==0)),'bothFootConfidenceFraction':float(both.mean()),'bothFootMeanDesiredSpeedGapRmsMps':float(np.sqrt(np.mean(gap[both]**2)))if both.any()else None,'bothFootMeanDesiredSpeedGapMaxMps':float(abs(gap[both]).max())if both.any()else None,'contactSwitchIndices':switch.tolist(),'maxAdjacentVelocityDeltaMps':float(abs(np.diff(vc)).max()),'maxAccelerationMps2':float(abs(np.diff(vc)/dt).max()),'switchAdjacentVelocityDeltaMaxMps':float(abs(v[switch]-v[(switch-1)%N]).max())if len(switch)else 0,'periodicVelocityJoinErrorMps':float(vc[-1]-vc[0]),'nonnegativeProgress':bool(np.all(np.diff(s)>=0)),'solverKktResidual':kkt,'projectedIterations':iterations}
 return stats,vc,s,conf
stats,v,s,conf=fit(.0175)
curve={'status':'AUTHORING-CANDIDATE-NOT-RUNTIME-NOT-NO-SLIP-NOT-ART-ACCEPTANCE','sourceCommit':'e6ab193','sourceSha256':m['sourceSha256Before'],'mesh':'Adventurer_Feet','sampleArchiveSha256':m['sampleArchiveSha256'],'durationSeconds':float(T),'strideMeters':float(s[-1]),'axes':{'forward':[0,-1,0],'up':[0,0,1],'headingAndCamera':'separate; rotate displacement once in future adapter'},'interpolation':'linear periodic velocity; integrate analytically within each interval for C1 distance; NOT linear distance interpolation','cycleRule':'distance(n*T+phase)=n*stride+distance(phase)','contactInference':{'floorM':floor,'floorDefinition':'minimum evaluated candidate sole z across cycle, NOT calibrated ground','heightBandM':.0175,'weight':'static rest surface area * max(0,1-max(0,z-floor)/heightBand)^2','contactConfidenceThreshold':.01,'uncertainty':'heuristic height band; compare +/-7mm, no measured physical contacts; above-plane vertices deliberately soft weighted'},'fit':{'objective':'sum normalizedTotalWeight*(v-weightedDesiredSpeed)^2 + lambda*sum cyclic adjacentVelocityDifference^2','desiredSpeed':'negative material vertex forward velocity, never changing contact centroid','smoothingSeconds':tau,'lambda':float((tau/dt)**2),'constraint':'v>=0','solverKktResidual':stats['solverKktResidual']},'samples':[{'timeSeconds':float(t[i]),'distanceMeters':float(s[i]),'velocityMps':float(v[i]),'leftConfidence':float(conf[i%N,0]),'rightConfidence':float(conf[i%N,1])}for i in range(N+1)]}
(O/'forward-distance-curve.json').write_text(json.dumps(curve,indent=2)+'\n')
diag={'main':stats,'heightBandSensitivity':[fit(h)[0]for h in [.0105,.0245]],'materialPointEndpointClosureMaxM':float(np.linalg.norm(p[-1]-p[0],axis=1).max()),'positionSourceUnchanged':m['sourceUnchanged'],'limitations':['Sampled finite differences at 480 intervals; not analytic continuous swept proof.','Nonzero lateral/vertical and within/between-foot velocities remain: one forward rigid translation cannot cancel this candidate set.','No source pose, shoe, scale, bone, runtime or camera modified. New shoe geometry/action invalidates these surface-derived metrics.','Soft contact candidates are not physical ground truth; lower bound is only for this explicitly weighted sampled set.']}
(O/'diagnostic.json').write_text(json.dumps(diag,indent=2)+'\n');print(json.dumps(diag,indent=2))
