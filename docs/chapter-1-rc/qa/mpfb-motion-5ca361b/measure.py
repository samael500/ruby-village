"""Independent fresh Blender reopen; evaluated mesh and subframe samples only."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;source=ROOT/'art/characters-mpfb-v1/motion/pilot/mpfb-walk-technical.blend';bpy.ops.wm.open_mainfile(filepath=str(source));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');shoe=bpy.data.objects['Ruta.shoes01'];scene=bpy.context.scene
# Derive bottom, forefoot and heel source indices independently by bounding-box fractions.
indices={}
for side,sign in [('L',1),('R',-1)]:
 verts=[v for v in shoe.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in verts);bottom=[v for v in verts if v.co.z<=z+.004];lo=min(v.co.y for v in bottom);hi=max(v.co.y for v in bottom)
 indices[side]={'all':[v.index for v in bottom],'toe':[v.index for v in bottom if v.co.y<=lo+.20*(hi-lo)],'heel':[v.index for v in bottom if v.co.y>=hi-.20*(hi-lo)]}
subd=[m for m in shoe.modifiers if m.type=='SUBSURF'];subdivisionLevels=[{'viewport':m.levels,'render':m.render_levels}for m in subd]
for m in subd:m.levels=m.render_levels
records=[];integerMatrices=[];fullMinimum=[];upperBody={}
for step in range(97):
 frame=1+step/4;scene.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps)
 for name in ['head','neck01','spine03']:
  if name in er.pose.bones:
   mat=er.pose.bones['root'].matrix.inverted()@er.pose.bones[name].matrix;upperBody.setdefault(name,[]).append([x for row in mat for x in row])
 # Actual render-resolution evaluated boots, including subdivision, for floor test.
 es=shoe.evaluated_get(deps);fullMinimum.append(min((es.matrix_world@v.co).z for v in es.data.vertices))
 for m in subd:m.show_viewport=False
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();es=shoe.evaluated_get(deps)
 feet={}
 for side in ['L','R']:
  p=((frame-1)/24+(0 if side=='L' else .5))%1;pts={kind:[es.matrix_world@es.data.vertices[i].co for i in ids] for kind,ids in indices[side].items()};centers={k:list(sum(ps,Vector())/len(ps)) for k,ps in pts.items()};hip=er.matrix_world@er.pose.bones['upperleg01.'+side].head;knee=er.matrix_world@er.pose.bones['lowerleg01.'+side].head;ankle=er.matrix_world@er.pose.bones['foot.'+side].head
  feet[side]={'phase':p,'supportCycle':math.floor((frame-1)/24+(0 if side=='L' else .5)),'centers':centers,'minBottomZ':min(v.z for v in pts['all']),'bottomZSpan':max(v.z for v in pts['all'])-min(v.z for v in pts['all']),'kneeDegrees':math.degrees((knee-hip).angle(ankle-knee)),'elbowFlexDegrees':math.degrees((er.pose.bones['lowerarm01.'+side].head-er.pose.bones['upperarm01.'+side].head).angle(er.pose.bones['lowerarm02.'+side].tail-er.pose.bones['lowerarm01.'+side].head)),'wristRigLocal':list(er.pose.bones['lowerarm02.'+side].tail),'upperArmEuler':list(er.pose.bones['upperarm01.'+side].rotation_euler)}
 for m in subd:m.show_viewport=True
 if step%4==0:integerMatrices.append([v for bone in er.pose.bones for row in bone.matrix for v in row])
 records.append({'frame':frame,'fullSubdivisionMinZ':fullMinimum[-1],'rootWorld':list(rig.matrix_world.translation),'pelvisWorld':list(er.matrix_world@er.pose.bones['root'].head),'feet':feet})
summary={}
for side in ['L','R']:
 flat=[r['feet'][side] for r in records if .125<=r['feet'][side]['phase']<=.45];push=[r['feet'][side] for r in records if .49<=r['feet'][side]['phase']<=.59];swing=[r['feet'][side] for r in records if .65<=r['feet'][side]['phase']<=.95]
 def extent(rows,part):return max((Vector(a['centers'][part])-Vector(b['centers'][part])).length for a in rows for b in rows)
 summary[side]={'flatStanceToeDriftM':extent(flat,'toe'),'flatStanceHeelDriftM':extent(flat,'heel'),'pushOffToeDriftM':max(extent([r for r in push if r['supportCycle']==k],'toe') for k in set(r['supportCycle'] for r in push)),'kneeFlexRangeDegrees':[min(r['feet'][side]['kneeDegrees']for r in records),max(r['feet'][side]['kneeDegrees']for r in records)],'swingMinimumSoleZ':min(r['minBottomZ']for r in swing),'swingMaximumSoleZ':max(r['minBottomZ']for r in swing),'wristRigRelativeRangeM':max((Vector(a['feet'][side]['wristRigLocal'])-Vector(b['feet'][side]['wristRigLocal'])).length for a in records for b in records),'elbowFlexRangeDegrees':[min(r['feet'][side]['elbowFlexDegrees']for r in records),max(r['feet'][side]['elbowFlexDegrees']for r in records)],'upperArmXRangeRadians':max(r['feet'][side]['upperArmEuler'][0]for r in records)-min(r['feet'][side]['upperArmEuler'][0]for r in records)}
mesh=[]
for o in [o for o in bpy.data.objects if o.type=='MESH']:
 snapshots=[]
 for frame in [1,7,13]:
  scene.frame_set(frame);bpy.context.view_layer.update();eo=o.evaluated_get(bpy.context.evaluated_depsgraph_get());inverse=rig.matrix_world.inverted();snapshots.append([inverse@(eo.matrix_world@v.co) for v in eo.data.vertices])
 if len({len(v) for v in snapshots})!=1:continue
 delta=[(a-b).length for a,b in zip(snapshots[0],snapshots[1])];mesh.append({'name':o.name,'evaluatedVertexCount':len(delta),'armatureModifiers':sum(m.type=='ARMATURE'for m in o.modifiers),'vertexGroups':[g.name for g in o.vertex_groups],'changedRigRelativeVertexCount':sum(d>1e-5 for d in delta),'maxRigRelativeDeltaM':max(delta)})
rootDelta=Vector(records[-1]['rootWorld'])-Vector(records[0]['rootWorld']);seam=max(abs(a-b) for a,b in zip(integerMatrices[0],integerMatrices[-1]));hashes={hashlib.sha256(json.dumps(v).encode()).hexdigest() for v in integerMatrices[:24]}
result={'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'blender':bpy.app.version_string,'freshReopen':True,'rigBones':len(rig.data.bones),'sourceBodyVertices':len(bpy.data.objects['Ruta.MPFB.Body'].data.vertices),'subframeSamples':len(records),'physicalCycleRootTranslationM':list(rootDelta),'physicalStrideM':rootDelta.length,'rootRelativePoseEndpointMaxMatrixDelta':seam,'uniqueIntegerPoses':len(hashes),'fullSubdivisionShoeMinWorldZ':min(fullMinimum),'sourceSubdivisionLevels':subdivisionLevels,'floorProbeUsesRenderSubdivisionLevel':True,'summary':summary,'upperBodyVsPelvisMatrixRange':{name:max(abs(a-b)for row in values for a,b in zip(row,values[0]))for name,values in upperBody.items()},'pelvisZRangeM':[min(r['pelvisWorld'][2]for r in records),max(r['pelvisWorld'][2]for r in records)],'meshDeformations':mesh,'records':records,'markerDefinition':indices}
(OUT/'fresh-blender-measure.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['records','meshDeformations','markerDefinition']},indent=2))
