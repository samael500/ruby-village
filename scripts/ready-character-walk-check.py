"""Inspect real source skin/action invariants and in-place gait contacts."""
from pathlib import Path
import bpy,json,hashlib,statistics,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/ready-character-walk-v1'
def action_hash(a):
 return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()
def invariants():
 rig=bpy.data.objects['CharacterArmature'];meshes=[o for o in bpy.data.objects if o.type=='MESH' and o.parent==rig]
 return {'boneRestSha256':hashlib.sha256(repr([(b.name,tuple(b.head_local),tuple(b.tail_local))for b in rig.data.bones]).encode()).hexdigest(),'walkActionSha256':action_hash(bpy.data.actions['Walk']),'meshes':{o.name:{'vertices':len(o.data.vertices),'geometryWeightsSha256':hashlib.sha256(repr([(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices]).encode()).hexdigest()}for o in meshes}}
bpy.ops.wm.open_mainfile(filepath=str(OUT/'source/adventurer-imported.blend'));baseline=invariants()
bpy.ops.wm.open_mainfile(filepath=str(OUT/'adventurer-walk-pilot.blend'));current=invariants();assert baseline==current
rig=bpy.data.objects['CharacterArmature'];feet=bpy.data.objects['Adventurer_Feet'];contract=json.loads((OUT/'contract.json').read_text());sideids={}
for side in ['L','R']:
 sideids[side]=[v.index for v in feet.data.vertices if sum(g.weight for g in v.groups if feet.vertex_groups[g.group].name.endswith('.'+side))>.5]
rows=[]
for i in range(25):
 frame=40*i/24;bpy.context.scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();ev=feet.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();p=[ev.matrix_world@v.co for v in me.vertices];ev.to_mesh_clear()
 row={'index':i,'sourceFrame':frame,'seconds':frame/24,'root':list(rig.matrix_world@rig.pose.bones['Root'].head),'feet':{}}
 for side in ['L','R']:
  fp=[p[j]for j in sideids[side]];floor=min(v.z for v in fp);low=[v for v in fp if v.z<floor+.015];center=sum(low,Vector())/len(low)
  row['feet'][side]={'soleMinimumZ':floor,'soleLowCentroid':list(center),'ankle':list(rig.matrix_world@rig.pose.bones['Foot.'+side].head)}
 rows.append(row)
floor=min(r['feet'][s]['soleMinimumZ']for r in rows for s in ['L','R']);threshold=floor+.025;velocities=[];perfoot={}
for side in ['L','R']:
 for row in rows:row['feet'][side]['contact']=row['feet'][side]['soleMinimumZ']<=threshold
 vv=[]
 for a,b in zip(rows,rows[1:]):
  if a['feet'][side]['contact'] and b['feet'][side]['contact']:
   speed=-(b['feet'][side]['ankle'][0]-a['feet'][side]['ankle'][0])/(b['seconds']-a['seconds']);vv.append(speed);velocities.append(speed)
 perfoot[side]={'contactSamples':[r['index']for r in rows[:-1]if r['feet'][side]['contact']],'soleZRange':[min(r['feet'][side]['soleMinimumZ']for r in rows),max(r['feet'][side]['soleMinimumZ']for r in rows)],'contactBackwardAnkleSpeedsMetersPerSecond':vv}
median=statistics.median(velocities);residual=[v-median for v in velocities];roottravel=max((Vector(r['root'])-Vector(rows[0]['root'])).length for r in rows)
report={'status':'measured-source-evidence-not-art-or-no-slide-approval','nativeGeometryWeightsBonesAndWalkUnchanged':baseline==current,'invariants':current,'cycleSeconds':40/24,'inPlaceRootTravelMeters':roottravel,'globalSoleFloorMeters':floor,'contactToleranceMeters':.025,'contactRule':'sole minimum <= global source sole floor +25mm; diagnostic, not IK contact labels','perFoot':perfoot,'suggestedTravelSpeedMetersPerSecond':median,'suggestedStrideMetersPerCycle':median*40/24,'stanceSpeedResidualRangeMetersPerSecond':[min(residual),max(residual)],'stanceSpeedResidualRmsMetersPerSecond':math.sqrt(statistics.mean(v*v for v in residual)),'interpretation':'In-place source requires matching runtime root travel. Median backward ankle speed during inferred contact estimates travel; nonzero residual means source stance still slides/rolls under constant travel. Do not infer no-slide from endpoint equality. No runtime integration tested.','samples':rows}
(OUT/'motion-checks.json').write_text(json.dumps(report,indent=2)+'\n');contract['motionContract']={k:report[k]for k in ['cycleSeconds','inPlaceRootTravelMeters','suggestedTravelSpeedMetersPerSecond','suggestedStrideMetersPerCycle','stanceSpeedResidualRmsMetersPerSecond']};(OUT/'contract.json').write_text(json.dumps(contract,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['invariants','samples','perFoot']}))
