"""Measured render-level boot XY hulls; native meters, root travel/orientation separate.

No raster synthesis or runtime edits. Source-set JSON permits replacing styled
sources/object names without reusing generic shoe certificates.
"""
from pathlib import Path
import bpy,json,hashlib,math,os
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];MOTION=ROOT/'art/characters-mpfb-v1/motion';OUT=(MOTION/os.environ.get('RUBY_MPFB_FOOTPRINT_OUTPUT_NAMESPACE','footprints-native-v1')).resolve();assert OUT.is_relative_to(MOTION.resolve());OUT.mkdir(parents=True,exist_ok=True)
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def hull(points):
 points=sorted(set((float(p[0]),float(p[1])) for p in points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[];upper=[]
 for p in points:
  while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
  lower.append(p)
 for p in reversed(points):
  while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
  upper.append(p)
 result=lower[:-1]+upper[:-1];assert len(result)>=3;return result
def default_registry():
 registry=[]
 transition=MOTION/'transitions';meta=json.loads((transition/'manifest.json').read_text())
 for state in ['idle','start-L','start-R','stop-L','stop-R','settle']:
  clip=meta['clips'][state];registry.append({'state':state,'source':str(transition/'mpfb-start-stop-technical.blend'),'actions':clip['actionBundle'],'frames':[float(r['frame']) for r in clip['frames']],'durationMs':clip['durationMs'],'rasterScope':'Canonical native30ms action poses measured; standalone state raster not claimed.'})
 registry.append({'state':'walk','source':str(transition/'mpfb-start-stop-technical.blend'),'actions':meta['sourceActions'],'frames':list(range(1,26)),'durationMs':720,'rasterScope':'Frames1..24 correspond to existing actual walk rasters;25 is terminal join readback.'})
 for state,folder,filename in [('pivot-left60',MOTION/'pivot-study','mpfb-compact-pivot60-technical.blend')]+[(f'pivot-{v}',MOTION/'pivot-variants'/v,'mpfb-compact-pivot-technical.blend') for v in ['right60','left120','right120']]:
  m=json.loads((folder/'manifest.json').read_text());registry.append({'state':state,'source':str(folder/filename),'actions':m['turnActions'],'frames':list(range(1,round(m['durationMs']/30)+2)),'durationMs':m['durationMs'],'rasterScope':'All native30ms raster-cadence poses measured; only compact diagnostic subset has rendered PNGs.'})
 return registry
registry=json.loads(Path(os.environ['RUBY_MPFB_FOOTPRINT_SOURCE_SET']).read_text()) if os.environ.get('RUBY_MPFB_FOOTPRINT_SOURCE_SET') else default_registry()
source_receipts={};states={};current=None
for entry in registry:
 source=Path(entry['source']);source=source if source.is_absolute() else ROOT/source;sha=digest(source)
 if current!=str(source):bpy.ops.wm.open_mainfile(filepath=str(source));current=str(source)
 rig=bpy.data.objects[entry.get('rigObject','Ruta.MPFB.StandardRig')];shoe=bpy.data.objects[entry.get('bootObject',os.environ.get('RUBY_MPFB_BOOT_OBJECT','Ruta.shoes01'))];scene=bpy.context.scene;assert abs(scene.unit_settings.scale_length-1)<1e-9,'Normalize native scene units to meters before exporting this source'
 for name,action in entry['actions'].items():bpy.data.objects[name].animation_data.action=bpy.data.actions[action]
 for mod in shoe.modifiers:
  if mod.type=='SUBSURF':mod.levels=mod.render_levels
 frames=set(float(f) for f in entry['frames'])
 if os.environ.get('RUBY_MPFB_FOOTPRINT_INCLUDE_NATIVE_KEYS')=='1':frames|={float(k.co.x) for c in rig.animation_data.action.fcurves for k in c.keyframe_points if 1<=k.co.x<=1+entry['durationMs']/30}
 regions=None;records=[]
 for f in sorted(frames):
  scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();evaluated=shoe.evaluated_get(deps);er=rig.evaluated_get(deps);origin=er.matrix_world.translation;rotation=er.matrix_world.to_quaternion();inverse_rotation=rotation.inverted();assert abs((rotation@Vector((0,0,1))).z-1)<1e-6,'XY-only actor hull representation requires upright yaw-only root';assert er.matrix_world.to_3x3().determinant()>0,'Native source placement must be a proper transform';points=[evaluated.matrix_world@v.co for v in evaluated.data.vertices]
  if regions is None:
   regions={}
   for side in ['L','R']:
    groups={g.index for g in shoe.vertex_groups if g.name.endswith('.'+side)};indices=[v.index for v in evaluated.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5];assert len(indices)>3;regions[side]=indices
  rec={'frame':f,'timeMs':30*(f-1),'rootNativeTranslationMeters':list(origin),'rootNativeOrientationQuaternionWXYZ':list(rotation),'rootYawRadians':rig.rotation_euler.z,'feet':{}}
  for side,indices in regions.items():
   world=[points[i] for i in indices];relative=[p-origin for p in world];local=[inverse_rotation@p for p in relative];rh=hull(relative);lh=hull(local)
   # The hull is formed from actual vertices; verify it encloses every selected boot vertex.
   tolerance=1e-9
   for cloud,polygon in [(relative,rh),(local,lh)]:
    assert all((b[0]-a[0])*(p.y-a[1])-(b[1]-a[1])*(p.x-a[0])>=-tolerance for a,b in zip(polygon,polygon[1:]+polygon[:1]) for p in cloud)
   rec['feet'][side]={'evaluatedSelectedVertices':len(indices),'fullBootXYHullRootRelativeNativeMeters':rh,'fullBootXYHullActorOrientationRemovedMeters':lh,'actualWorldZRangeMeters':[min(p.z for p in world),max(p.z for p in world)],'actualRootRelativeXYBoundsMeters':[[min(p[i] for p in relative),max(p[i] for p in relative)] for i in range(2)]}
  records.append(rec)
 assert digest(source)==sha
 shoe_signature=hashlib.sha256(json.dumps({'vertices':[list(v.co) for v in shoe.data.vertices],'faces':[list(p.vertices) for p in shoe.data.polygons],'groups':[g.name for g in shoe.vertex_groups],'weights':[[(g.group,g.weight) for g in v.groups] for v in shoe.data.vertices]},sort_keys=True).encode()).hexdigest()
 source_receipts[sha]={'source':str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source),'sourceSha256':sha,'bootObject':shoe.name,'rawBootGeometryWeightSha256':shoe_signature,'rigObject':rig.name,'renderSubdivisionLevels':[m.render_levels for m in shoe.modifiers if m.type=='SUBSURF'],'evaluatedTopologyVertexCount':len(points),'appearanceValidity':'Only this exact source/shoe geometry and weights. New styled shoes/source require fresh export and independent clearance checks.'}
 result={'state':entry['state'],'sourceSha256':sha,'actionBundle':entry['actions'],'durationMs':entry['durationMs'],'rasterScope':entry.get('rasterScope','Custom source set; raster existence not asserted'),'sampling':'Native30ms raster cadence plus supplied frames; additional authored keys only when INCLUDE_NATIVE_KEYS=1. Not a continuous swept-volume certificate.','records':records};temporary=OUT/(entry['state']+'.tmp');temporary.write_text(json.dumps(result,indent=2)+'\n');temporary.replace(OUT/(entry['state']+'.json'));states[entry['state']]={'sourceSha256':sha,'recordCount':len(records),'file':entry['state']+'.json'};print('ACTUAL_BOOT_HULLS',entry['state'],len(records),flush=True)
contract={'schema':'mpfb-evaluated-boot-footprint/v1','status':'TECHNICAL GENERIC SOURCE INPUT; NOT FINAL APPEARANCE OR ROUTE CLEARANCE CERTIFICATE','units':'native physical meters','modelForward':[0,-1,0],'rootMotionSeparate':True,'referenceSceneCalibration':{'metersToScenePixels':136/(251/384*1.70),'nativeHeightReferencePixels':251,'displayHeightReferencePixels':136,'orthoMeters':1.70,'scope':'Current generic source only; new styled source requires renewed physical/body-height calibration.'},'hullCoordinates':{'fullBootXYHullRootRelativeNativeMeters':'Actual evaluated worldXY minus current rig-origin translation. Clip native yaw is retained. Apply only external actor placement heading, then add physical root trajectory once.','fullBootXYHullActorOrientationRemovedMeters':'Actual evaluated vertex minus rig origin, then inverse rig quaternion; physical meters retained, including source scale. Apply complete actor/clip orientation once and root trajectory once. Do not apply clip yaw to both representations.','winding':'Counterclockwise convex hull in native XY; full boot includes swing/upper boot and conservatively fills its own concavity. Separate L/R hulls, no combined convex gap fill.'},'nativeToBaseGridXY':[[0,-1],[-1,0]],'coverage':'Discrete evaluated boot XY projections only. No solver/road/path changes; no guarantee that interpolation/sweeps between timestamps or final styled shoes remain inside confirmed hex unions. Root planner must validate route and timing with these source-matched inputs.','samplingIncludesNativeKeys':os.environ.get('RUBY_MPFB_FOOTPRINT_INCLUDE_NATIVE_KEYS')=='1','sources':source_receipts,'states':states,'recordCount':sum(s['recordCount'] for s in states.values())};(OUT/'manifest.json').write_text(json.dumps(contract,indent=2)+'\n');print('FOOTPRINT_CONTRACT_COMPLETE',contract['recordCount'],flush=True)
