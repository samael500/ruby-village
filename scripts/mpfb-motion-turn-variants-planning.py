"""Export exact evaluated source planning inputs independently of raster availability."""
from pathlib import Path
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'art/characters-mpfb-v1/motion/turn-variants-study'
for variant in ['right60','left120']:
 out=BASE/variant;meta=json.loads((out/'manifest.json').read_text());check=json.loads((out/'native-contact-join-check.json').read_text());assert check['summary']['nativeFeasibilityPass']
 source=out/('mpfb-native-right60-technical.blend' if variant=='right60' else 'mpfb-native-left120-technical.blend')
 assert hashlib.sha256(source.read_bytes()).hexdigest()==check['sourceSha256Before']==check['sourceSha256After']
 entry=meta.get('entrySourcePhase',0);samples=[]
 for record in check['records']:
  p=record['phase']+entry;feet={}
  for side,offset in [('L',0),('R',.5)]:
   f=(p+offset)%1;mode='heel-roll' if f<.1 else 'flat' if f<=.48 else 'toe-push' if f<.6 else 'swing'
   feet[side]={'semanticMode':mode,'actualAnkleWorldMeters':record['feet'][side]['ankleWorld'],'actualSoleWorldMeters':record['feet'][side]['sole']}
  samples.append({'timeMs':30*(record['frame']-1),'sourcePhase':p%1,'actualRootNativeMeters':record['rootWorld'],'actualYawRadians':record['heading'],'feet':feet})
 length=sum(math.dist(a['actualRootNativeMeters'],b['actualRootNativeMeters']) for a,b in zip(samples,samples[1:]))
 result={'status':'TECHNICAL SOURCE PLANNING INPUT; INDEPENDENT REVIEW PENDING; NOT RUNTIME ENABLED','variant':variant,'sourceSha256':check['sourceSha256Before'],'durationMs':meta['durationMs'],'entryStraightSourcePhase':entry,'exitStraightSourcePhase':entry,'angleRadiansActual':samples[-1]['actualYawRadians'],'rootDeltaMetersActual':samples[-1]['actualRootNativeMeters'],'actualDenseSamplePolylineLengthMeters':length,'distanceNote':'Actual evaluated 2.8125ms sample polyline, not exact analytic arc length; native stride remains .5687545573m per720ms. Saved LINEAR key chords are not exact C1.','calibration':{'orthoMeters':1.70,'nativeHeightPixels':251,'displayHeightPixels':136,'metersToScenePixels':136/(251/384*1.70),'groundScale':.65},'placement':'Root curve applied once. Rigidly rotate/translate complete native body, controls and root path together. No independent feet fitting, stride scaling, root retiming or vertex snapping.','routeCoverage':{'arbitraryLegalPathCertified':False,'constraint':'Moving-arc fillet tangent lengths can overlap at adjacent sharp corners on 1-hex-wide paths. This source does not certify containment.','fallbackCandidate':'Compact native in-place stepping turn with bounded root and support sole planted may be required; NOT AUTHORED or CERTIFIED here. Do not alter puzzle paths/goals to hide the gap.'},'samples':samples}
 heading=samples[-1]['actualYawRadians'];delta=samples[-1]['actualRootNativeMeters'];outgoing=delta[0]/math.sin(heading);incoming=-delta[1]-outgoing*math.cos(heading);scale=result['calibration']['metersToScenePixels']
 result['routeCoverage']['actualEntryExitRayIntersectionTangentSetbacks']={'incomingMeters':incoming,'outgoingMeters':outgoing,'incomingScenePixels':incoming*scale,'outgoingScenePixels':outgoing*scale,'method':'Solve actual saved endpoint displacement = incoming*(0,-1) + outgoing*(sin(yaw),-cos(yaw)). These are variable-curve endpoint tangent setbacks, NOT minimum-radius circular fillet estimates.','scope':'Root centerline only. Full body/bag/sole swept envelope and neighboring route clearance remain unvalidated.'}
 result['actualSampledRootXYBoundsMeters']=[[min(r['actualRootNativeMeters'][i] for r in samples),max(r['actualRootNativeMeters'][i] for r in samples)] for i in range(2)]
 raster=out/'raster-path-metadata.json'
 if raster.exists():
  data=json.loads(raster.read_text());assert data['sourceSha256Before']==result['sourceSha256']
  result['actualSavedKeyPolylineLengthMeters']=data['actualSavedKeyPolylineLengthMeters'];result['actualMinimumDiscreteCircumradiusMeters']=data['actualMinimumDiscreteCircumradiusMeters'];result['actualRootKeyCurveWithTangentAndProjection']=data['actualPath'];result['actualProjectedRootPathLengthScenePixels']=data.get('actualProjectedRootPathLengthScenePixels');result['coordinateContract']=data.get('coordinateContract')
 (out/'planning-input.json').write_text(json.dumps(result,indent=2)+'\n');print(variant,'PLANNING_EXPORT actual source samples',len(samples),'no runtime route coverage claim')
