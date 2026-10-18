"""Isolated MPFB phase/root/contact prototype; no runtime integration.

All distances are model meters along forward (-Y). A caller places the actor root
once; rendered footAnchor is the projection of that root's ground point, not a
per-frame foot/bounding-box correction. Planned foot bases are not measured skin
contacts: independent Blender verification supplies the latter.
"""
import math,json
STRIDE=.5687545572916666
CYCLE_MS=720.
START_MS=STOP_MS=360.
SETTLE_MS=180.
IDLE_Z=-.002
STOP_END_Z=-.006
SPEED=STRIDE/(CYCLE_MS/1000)
def clamp(x):return max(0.,min(1.,x))
def smooth(x):x=clamp(x);return x*x*x*(10+x*(-15+6*x))
def cycle_z(p):return -.020-.016*math.cos(4*math.pi*p)
def foot(base,kind,pitch=0.,lift=0.,key=None):return {'plannedBaseForwardMeters':base,'contactMode':kind,'pitchRadians':pitch,'liftMeters':lift,'anchorId':key}
def cycle_foot(p,side,entry=0.):
 offset=0 if side=='L' else .5;u=p+offset;k=math.floor(u);f=u-k;a=(k-offset+.3-entry)*STRIDE
 if f<.6:
  pitch=-.12*(1-f/.1)if f<.1 else .26*(f-.48)/.12 if f>.48 else 0.
  return foot(a,'heel'if f<.1 else 'toe'if f>.48 else 'flat',pitch,key=f'{side}-cycle-{k}')
 s=(f-.6)/.4;return foot(a+STRIDE*s*s*(3-2*s),'swing',.26*(1-s)-.12*s,.045*math.sin(math.pi*s)**1.25)
def sample_clip(kind,time_ms,side='L'):
 if side not in ['L','R']:raise ValueError('side must be L or R')
 time_ms=max(0.,float(time_ms))
 entry=0. if side=='L' else .5
 if kind=='walk':
  seconds=max(0.,time_ms)/1000;p=entry+time_ms/CYCLE_MS
  return {'state':'walk','timeMs':time_ms,'cyclePhase':p%1,'sourcePhase':p%1,'poseAmplitude':1.,'rootDistanceMeters':seconds*SPEED,'rootVelocityMetersPerSecond':SPEED,'rootZ':cycle_z(p),'rootLateralExtraMeters':0.,'feet':{s:cycle_foot(p,s,entry)for s in ['L','R']}}
 duration={'start':START_MS,'stop':STOP_MS,'settle':SETTLE_MS,'idle':SETTLE_MS}[kind];time_ms=min(duration,time_ms);s=clamp(time_ms/duration);w=smooth(s)
 if kind=='start':
  p=entry-.5+.5*s;amp=w;distance=.2*STRIDE*(2.5*s**4-1.5*s**5);velocity=.2*STRIDE/(START_MS/1000)*(10*s**3-7.5*s**4);z=(1-w)*IDLE_Z+w*cycle_z(p);support='R'if side=='L'else'L'
  if time_ms<=96:lead=foot(0.,'toe',.26*smooth(time_ms/96),key=side+'-start-initial')
  else:
   u=clamp((time_ms-96)/(START_MS-96));lead=foot(.5*STRIDE*smooth(u),'swing'if u<1 else'heel',.26*(1-u)-.12*u,.045*max(0,math.sin(math.pi*u))**1.25,key=side+'-start-land'if u>=1 else None)
  trailing=foot(0.,'flat'if s<=.75 else'toe',(.26/6)*smooth((s-.75)/.25),key=support+'-start-support')
  feet={side:lead,support:trailing};lateral=(1 if support=='L'else-1)*.032*math.sin(math.pi*s)**2
 elif kind=='stop':
  p=entry+.5*s;amp=1-w;distance=STRIDE*(.5*s-.5*s**4+.3*s**5);velocity=STRIDE/(STOP_MS/1000)*(.5-2*s**3+1.5*s**4);z=amp*cycle_z(p)+(1-amp)*STOP_END_Z;trailing='R'if side=='L'else'L'
  support=foot(.3*STRIDE,'heel'if time_ms<72 else'flat',-.12*max(0,1-time_ms/72),key=side+'-stop-support')
  if time_ms<72:moving=foot(-.2*STRIDE,'toe',.26/6+(.26-.26/6)*time_ms/72,key=trailing+'-stop-old')
  elif time_ms<300:
   u=(time_ms-72)/228;moving=foot(-.2*STRIDE+.5*STRIDE*smooth(u),'swing',.26*(1-u)-.12*u,.045*math.sin(math.pi*u)**1.25)
  else:moving=foot(.3*STRIDE,'heel'if time_ms<360 else'flat',-.12*(1-smooth((time_ms-300)/60)),key=trailing+'-stop-land')
  feet={side:support,trailing:moving};lateral=(1 if side=='L'else-1)*.032*math.sin(math.pi*s)**2
 else:
  p=0.;amp=0.;distance=0.;velocity=0.;z=STOP_END_Z+(IDLE_Z-STOP_END_Z)*w if kind=='settle'else IDLE_Z;lateral=0.;feet={s:foot(0.,'flat',key=s+'-idle')for s in ['L','R']}
 return {'state':kind,'timeMs':min(duration,max(0,time_ms)),'cyclePhase':p%1,'sourcePhase':p%1,'poseAmplitude':amp,'rootDistanceMeters':distance,'rootVelocityMetersPerSecond':velocity,'rootZ':z,'rootLateralExtraMeters':lateral,'feet':feet}
def request_stop(phase):
 p=phase%1;boundary=math.ceil((p-1e-10)*2)/2;wait=(boundary-p)*CYCLE_MS
 return {'queueUntilHeelStrike':True,'waitMs':max(0.,wait),'entryPhase':boundary%1,'supportSide':'L'if round(boundary*2)%2==0 else'R','stopDurationMs':STOP_MS,'settleDurationMs':SETTLE_MS,'stopRootAdvanceMeters':.3*STRIDE,'headingLockedDuringStop':True}
def contract():
 result={'schema':'mpfb-isolated-motion-phase-api/v1','status':'TECHNICAL PROTOTYPE NOT FINAL ART','productionEnabled':False,'integration':'none; do not load from src/main','modelForward':[0,-1,0],'cycleMs':CYCLE_MS,'physicalStrideMeters':STRIDE,'walkSpeedMetersPerSecond':SPEED,'states':{'idle':{'rootVelocity':0,'feet':'both flat'},'start':{'durationMs':START_MS,'rootAdvanceMeters':.2*STRIDE,'firstLeadStepMeters':.5*STRIDE,'variants':['L','R'],'entry':'idle','exit':'walk at phase0(L) or.5(R)'},'walk':{'loopMs':CYCLE_MS,'rootAdvanceMeters':STRIDE,'heelStrikes':{'0':'L','.5':'R'}},'stop':{'durationMs':STOP_MS,'rootAdvanceMeters':.3*STRIDE,'variants':['L-support','R-support'],'entry':'request queued to next heel strike; never freeze an active swing','lastSwingLandsMs':300,'feet':'trailing foot completes a shortened step to support foot; support stays planted'},'settle':{'durationMs':SETTLE_MS,'rootAdvanceMeters':0,'body':'4mm gentle pelvis rise, both feet flat'}},'placement':{'rootMotionAppliedExactlyOnce':True,'footAnchor':'actual camera projection of rig object origin on Z0; same framing/scale across directions','contacts':'planned foot bases are not measured skin contact; verification records actual evaluated soles/bones','heading':'locked throughout start/stop; turns require separate planning/source, not authored here'},'stopRequestExamples':[{'phase':p,**request_stop(p)}for p in [0,.125,.4,.5,.75,.99]]}
 result['nativeRootDeltasMeters']={state:[0,-distance,0]for state,distance in [('idle',0),('start',.2*STRIDE),('walk',STRIDE),('stop',.3*STRIDE),('settle',0)]}
 result['phaseJoins']={'startExitByLead':{'L':0,'R':.5},'stopEntryBySupport':{'L':0,'R':.5},'stopExit':'both feet flat, zero gait amplitude; no active walk phase','supportSemantics':{'start':'opposite lead stays planted; lead lands at360ms','stop':'entry heel-strike foot stays planted; trailing foot lands at300ms and rolls flat by360ms','settle':'both feet planted'}}
 result['bodyHeightCalibration']={'nativeReferencePixels':251,'framePixels':384,'orthoMeters':1.70,'displayReferencePixels':136,'metersToScenePixels':136/(251/384*1.70),'policy':'one constant scale for all states and directions; no silhouette-height normalization'}
 result['arbitraryRouteAdapter']={'status':'PENDING','fixedClipsDoNotSolveArbitraryRouteLengths':True,'forbiddenShortcut':'no root retiming, stride scaling or endpoint sliding to fit residual path length','candidateOnly':'rendered actor endpoint adjustment inside fixed goal-cell safe area, along final tangent at most quarter stride; logical goal/path/solutions unchanged; not implemented or validated'}
 result['savedActionInterpolation']='LINEAR sampled at30ms; tiny chord-velocity jumps, no exact C1 continuity claim'
 return result
if __name__=='__main__':print(json.dumps(contract(),indent=2))
