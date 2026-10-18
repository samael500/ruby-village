"""Saved-file actual right hand/ONE strap grasp geometry and torso motion audit."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/pilot';bpy.ops.wm.open_mainfile(filepath=str(OUT/'mpfb-walk-technical.blend'))
body=bpy.data.objects['Ruta.MPFB.Body'];strap=bpy.data.objects['ONE diagonal satchel strap'];rig=bpy.data.objects['Ruta.MPFB.StandardRig']
for m in body.modifiers:
 if m.type=='MASK':m.show_viewport=False
# Verify the original bag/strap were not hidden, shrunk or replaced to fake clearance.
def shape_signature(o):
 payload={'vertices':[list(v.co)for v in o.data.vertices],'faces':[list(p.vertices)for p in o.data.polygons],'matrixBasis':[list(row)for row in o.matrix_basis],'hideRender':o.hide_render,'geometryModifiers':[(m.type,getattr(m,'width',None),getattr(m,'thickness',None),getattr(m,'segments',None))for m in o.modifiers if m.type!='ARMATURE']}
 return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
check_names=['Ruta ONE satchel','Satchel flap','Satchel buckle','ONE diagonal satchel strap'];current={name:shape_signature(bpy.data.objects[name])for name in check_names}
with bpy.data.libraries.load(str(ROOT/'art/characters-mpfb-v1/appearance-v1/ruta-appearance-v1.blend'),link=False)as(a,b):b.objects=list(check_names)
baseline={name:shape_signature(obj)for name,obj in zip(check_names,b.objects)}
preservation={'baselineAppearanceSource':'appearance-v1/ruta-appearance-v1.blend','originalMeshGeometryTransformsVisibilityUnchanged':current==baseline,'currentSignatures':current,'baselineSignatures':baseline,'actualStrapMeshCount':sum(o.type=='MESH'and o.name=='ONE diagonal satchel strap'for o in bpy.context.scene.objects)}
assert current==baseline,'Bag/strap source geometry or visibility changed'
regions={}
for name,keys in [('palm',['wrist','metacarpal']),('fingers',['finger2','finger3','finger4','finger5']),('thumb',['finger1'])]:
 groups={g.index for g in body.vertex_groups if g.name.endswith('.R')and any(k in g.name for k in keys)};regions[name]={v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5}
records=[]
for frame in range(1,26):
 bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();eb=body.evaluated_get(deps);es=strap.evaluated_get(deps);bv=[eb.matrix_world@v.co for v in eb.data.vertices];sv=[es.matrix_world@v.co for v in es.data.vertices];tree=BVHTree.FromPolygons(sv,[list(p.vertices)for p in es.data.polygons]);rec={'frame':frame,'grasp':{},'wristRigLocal':{s:list(rig.pose.bones['wrist.'+s].head)for s in ['L','R']},'wristWorld':{s:list(rig.matrix_world@rig.pose.bones['wrist.'+s].head)for s in ['L','R']}}
 for kind,ids in regions.items():
  closest=min(((tree.find_nearest(bv[i])[3],i,tree.find_nearest(bv[i])[0])for i in ids),key=lambda x:x[0]);faces=[list(p.vertices)for p in eb.data.polygons if all(i in ids for i in p.vertices)];skin=BVHTree.FromPolygons(bv,faces);rec['grasp'][kind]={'selectedVertices':len(ids),'nearestDistanceMeters':closest[0],'handVertex':closest[1],'handPointWorld':list(bv[closest[1]]),'strapPointWorld':list(closest[2]),'surfaceTriangleIntersections':len(tree.overlap(skin))}
 for name in ['root','spine01','spine02','neck01','head']:
  b=rig.pose.bones[name];rec[name]={'matrix':[list(row)for row in b.matrix],'rootRelativeMatrix':[list(row)for row in rig.pose.bones['root'].matrix.inverted()@b.matrix]}
 records.append(rec)
summary={'gripNearestDistanceRangeMeters':{kind:[min(r['grasp'][kind]['nearestDistanceMeters']for r in records),max(r['grasp'][kind]['nearestDistanceMeters']for r in records)]for kind in regions},'gripMaxTriangleIntersections':{kind:max(r['grasp'][kind]['surfaceTriangleIntersections']for r in records)for kind in regions}}
summary['actualWristForeAftTravelMeters']={side:max(r['wristRigLocal'][side][1]for r in records)-min(r['wristRigLocal'][side][1]for r in records)for side in ['L','R']}
summary['relativeTorsoRotationExcursionDegrees']=max(math.degrees(Matrix(a['spine01']['rootRelativeMatrix']).to_quaternion().rotation_difference(Matrix(b['spine01']['rootRelativeMatrix']).to_quaternion()).angle)for a in records for b in records)
summary['worldHeadRotationExcursionDegrees']=max(math.degrees(Matrix(a['head']['matrix']).to_quaternion().rotation_difference(Matrix(b['head']['matrix']).to_quaternion()).angle)for a in records for b in records)
(OUT/'grip-torso-check.json').write_text(json.dumps({'method':'Fresh saved-file actual evaluated body right palm/finger/thumb skin triangles and the unchanged ONE strap mesh. MASK disabled only in checker. Surface distances/intersections establish real geometry, not a target-only grip claim. Intentional contact is distinct from clean penetration-free grasp and must be visually reviewed.','bagStrapPreservation':preservation,'summary':summary,'records':records},indent=2)+'\n');print(json.dumps(summary,indent=2))
