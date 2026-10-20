"""Independent actual skin/strap triangles, sampled surface gaps and source preservation."""
import bpy,json,sys,hashlib,math
from pathlib import Path
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;source=ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend';bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;rig=next(o for o in scene.objects if o.type=='ARMATURE');body=bpy.data.objects['Ruta.MPFB.Body'];strap=bpy.data.objects['ONE diagonal satchel strap']
for mod in body.modifiers:
 if mod.type=='MASK':mod.show_viewport=False
names=['Ruta ONE satchel','Satchel flap','Satchel buckle','ONE diagonal satchel strap']
def signature(obj):
 payload={'vertices':[list(v.co)for v in obj.data.vertices],'polygons':[list(p.vertices)for p in obj.data.polygons],'basis':[list(r)for r in obj.matrix_basis],'renderVisible':not obj.hide_render,'geometryModifiers':[(m.type,getattr(m,'width',None),getattr(m,'thickness',None),getattr(m,'segments',None))for m in obj.modifiers if m.type!='ARMATURE']};return hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
current={n:signature(bpy.data.objects[n])for n in names};oneStrapCount=sum(o.type=='MESH'and o.name=='ONE diagonal satchel strap'for o in scene.objects)
with bpy.data.libraries.load(str(ROOT/'art/characters-mpfb-v1/appearance-v1/ruta-appearance-v1.blend'),link=False)as(avail,loaded):loaded.objects=list(names)
baseline={n:signature(o)for n,o in zip(names,loaded.objects)};assert current==baseline and oneStrapCount==1
regions={}
for region,terms in {'palm':['wrist','metacarpal'],'fingers':['finger2','finger3','finger4','finger5'],'thumb':['finger1']}.items():
 groups={g.index for g in body.vertex_groups if g.name.endswith('.R')and any(t in g.name for t in terms)};ids={v.index for v in body.data.vertices if sum(g.weight for g in v.groups if g.group in groups)>.5};faces=[list(p.vertices)for p in body.data.polygons if all(i in ids for i in p.vertices)];assert groups and ids and faces;regions[region]={'ids':ids,'faces':faces}
records=[];torso=[];heads=[]

lead=sys.argv[-1];assert lead in ['L','R'];manifest=json.loads((ROOT/'art/characters-mpfb-v1/motion/transitions/manifest.json').read_text());bundle=manifest['demos'][lead]['actionBundle'];assert len(bundle)==3
for objectName,actionName in bundle.items():bpy.data.objects[objectName].animation_data.action=bpy.data.actions[actionName]
for step in range(217):
 f=1+step/4;scene.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();b=body.evaluated_get(deps);s=strap.evaluated_get(deps);vertices=[b.matrix_world@v.co for v in b.data.vertices];sv=[s.matrix_world@v.co for v in s.data.vertices];sf=[list(p.vertices)for p in s.data.polygons];assert sv and sf;surface=BVHTree.FromPolygons(sv,sf);record={'frame':f,'regions':{},'wrists':{side:list(rig.pose.bones['wrist.'+side].head)for side in ['L','R']}}
 for name,part in regions.items():
  skin=BVHTree.FromPolygons(vertices,part['faces']);forward=min(surface.find_nearest(vertices[i])[3]for i in part['ids']);reverse=min(skin.find_nearest(v)[3]for v in sv);record['regions'][name]={'vertices':len(part['ids']),'faces':len(part['faces']),'triangleIntersections':len(surface.overlap(skin)),'skinVertexToStrapSurfaceMinM':forward,'strapVertexToSkinSurfaceMinM':reverse}
 records.append(record);torso.append((rig.pose.bones['root'].matrix.inverted()@rig.pose.bones['spine01'].matrix).to_quaternion());heads.append((rig.matrix_world@rig.pose.bones['head'].matrix).to_quaternion())
summary={name:{'vertices':records[0]['regions'][name]['vertices'],'polygons':records[0]['regions'][name]['faces'],'maxTriangleIntersections':max(r['regions'][name]['triangleIntersections']for r in records),'skinVertexToStrapSurfaceRangeM':[min(r['regions'][name]['skinVertexToStrapSurfaceMinM']for r in records),max(r['regions'][name]['skinVertexToStrapSurfaceMinM']for r in records)],'strapVertexToSkinSurfaceRangeM':[min(r['regions'][name]['strapVertexToSkinSurfaceMinM']for r in records),max(r['regions'][name]['strapVertexToSkinSurfaceMinM']for r in records)]}for name in regions}
excursion=lambda values:max(math.degrees(a.rotation_difference(b).angle)for a in values for b in values)
result={'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'actualStrapMeshCount':oneStrapCount,'bagGeometryObjectTransformVisibilityModifierSignaturesUnchanged':current==baseline,'currentSignatures':current,'baselineSignatures':baseline,'samples':217,'grip':summary,'torsoVsPelvisRotationExcursionDegrees':excursion(torso),'worldHeadRotationExcursionDegrees':excursion(heads),'wristForeAftRangeM':{side:max(r['wrists'][side][1]for r in records)-min(r['wrists'][side][1]for r in records)for side in ['L','R']},'records':records,'method':'Own fresh-reopen BVH actual evaluated triangles and two-sided vertex-to-surface gap samples; actual nonempty weighted palm/fingers/thumb;217quarterframes. These sampled distances are not a proof of exact global minimum or force/contact simulation. Source not saved.'}
(OUT/(f'grip-{lead}.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='records'},indent=2))
