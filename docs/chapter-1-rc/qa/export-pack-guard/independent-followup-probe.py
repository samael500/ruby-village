"""Actual Blender fixture regression; author input read-only, mutated copies only /tmp.
No rendered frames. Run Blender --background --disable-autoexec --python THIS.
"""
import bpy,json,hashlib,runpy,sys,tempfile,traceback,time
from pathlib import Path
ROOT=Path('/tmp/ruby-export-pack-qa');O=Path(__file__).resolve().parent;EXPORT=O/'exporter-followup-probe.py';SOURCE=ROOT/'art/ruta-ellie-head-v1/color-handoff/ruta-b-ellie-blue-copper-temporary.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();before=sha(SOURCE);tmp=Path(tempfile.mkdtemp(prefix='ruta-ready-visibility-'));rows=[]
def body():return bpy.data.objects['Adventurer_Body']
def target():
 o=bpy.data.objects.new('QA hidden dependency',None);bpy.context.scene.collection.objects.link(o);o.hide_viewport=True;return o
def collection_monitor(obj,eye=False):
 c=bpy.data.collections.new('QA disabled collection');bpy.context.scene.collection.children.link(c)
 for old in list(obj.users_collection):old.objects.unlink(obj)
 c.objects.link(obj);bpy.context.view_layer.update()
 if eye:bpy.context.view_layer.layer_collection.children[c.name].hide_viewport=True
 else:c.hide_viewport=True
def constraint_case():
 rig=bpy.data.objects['CharacterArmature'];c=rig.pose.bones['Root'].constraints.new('COPY_LOCATION');c.target=target()
def driver_case():
 obj=body();obj['QA']=0.;d=obj.driver_add('["QA"]').driver;v=d.variables.new();v.name='hidden';v.type='SINGLE_PROP';v.targets[0].id=target();v.targets[0].data_path='location.x';d.expression='0*hidden'
def subdiv_case():
 mod=body().modifiers.new('QA differing subdivision','SUBSURF');mod.levels=1;mod.render_levels=2
def instance_case():
 o=bpy.data.objects.new('QA unsupported collection instance',None);bpy.context.scene.collection.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=bpy.data.collections.new('QA instance payload')
cases=[('baseline',lambda:None,True),('object_eye_supported',lambda:body().hide_set(True),True),('object_monitor',lambda:setattr(body(),'hide_viewport',True),False),('collection_monitor',lambda:collection_monitor(body()),False),('collection_eye_explicitly_unsupported',lambda:collection_monitor(body(),True),False),('modifier_viewport_only_off',lambda:setattr(body().modifiers[0],'show_viewport',False),False),('modifier_render_only_off',lambda:setattr(body().modifiers[0],'show_render',False),False),('dependency_rig_monitor',lambda:setattr(bpy.data.objects['CharacterArmature'],'hide_viewport',True),False),('dependency_rig_collection_monitor',lambda:collection_monitor(bpy.data.objects['CharacterArmature']),False),('pose_bone_constraint_hidden_target',constraint_case,False),('driver_hidden_target',driver_case,False),('subdivision_levels_mismatch',subdiv_case,False),('scene_simplify_unsupported',lambda:setattr(bpy.context.scene.render,'use_simplify',True),False),('unsupported_geometry_nodes',lambda:body().modifiers.new('QA nodes','NODES'),False),('unsupported_collection_instance',instance_case,False)]
cases += [('UNSUPPORTED_VERTS_REJECT',lambda:setattr(body(),'instance_type','VERTS'),False),('UNSUPPORTED_FACES_REJECT',lambda:setattr(body(),'instance_type','FACES'),False)]
baseline=None
for name,mutate,expected in cases:
 bpy.ops.wm.open_mainfile(filepath=str(SOURCE));mutate();fixture=tmp/(name+'.blend');bpy.ops.wm.save_as_mainfile(filepath=str(fixture));dest=tmp/name;start=time.perf_counter();error=None;result=None
 sys.argv=[str(EXPORT),'--','--source',str(fixture),'--out',str(dest),'--frame-count','1','--contract-only']
 try:runpy.run_path(str(EXPORT),run_name='__main__');result=json.loads((dest/'dry-run-contract.json').read_text())
 except Exception as e:error=type(e).__name__+': '+str(e)
 success=result is not None;row={'case':name,'expectedPass':expected,'actualPass':success,'error':error,'seconds':time.perf_counter()-start,'fixtureSha256':sha(fixture),'renderedFrames':result['renderedFrameCount']if result else 0};assert success==expected,(name,row)
 if result:
  if name=='object_eye_supported':
   row['loadedObjectEyeHidden']=body().hide_get();assert row['loadedObjectEyeHidden']
  d=result['cameraVariants']['base']['directions']['e'];values={'height':d['nativeHeightPx'],'bounds':d['restGeometryBoundsWorld'],'frameBounds':d['clips']['walk']['frames'][0]['projectedUsedGeometryBoundsPx']}
  if baseline is None:baseline=values
  else:assert values==baseline;row['exactEyeVsBaselineGeometryAndHeight']=True
 rows.append(row);print('VISIBILITY_PROBE',json.dumps(row),flush=True)
# Cross-mode stale source guards must reject BEFORE source open/evaluation or frame writes.
for current,other in [('dry-run-contract.json','source-contract.json'),('source-contract.json','dry-run-contract.json')]:
 dest=tmp/('stale-'+current);dest.mkdir();(dest/other).write_text(json.dumps({'sourceSha256':'different-hash'}));sys.argv=[str(EXPORT),'--','--source',str(SOURCE),'--out',str(dest),'--frame-count','1']+(['--contract-only']if current.startswith('dry')else[])
 try:runpy.run_path(str(EXPORT),run_name='__main__');raise AssertionError('stale cross-mode output accepted')
 except RuntimeError as e:
  assert 'another source hash' in str(e);assert not(dest/current).exists()and not(dest/'renders').exists();rows.append({'case':'stale-opposite-mode-'+current,'actualPass':False,'expectedPass':False,'error':str(e),'noReportOrRenderWritten':True})
assert before==sha(SOURCE)
(O/'results-followup.json').write_text(json.dumps({'status':'ACTUAL-BLENDER-FAIL-CLOSED-REGRESSIONS-NOT-RENDER-OR-ART-ACCEPTANCE','sourceSha256':before,'sourceUnchanged':True,'exporterSha256':sha(EXPORT),'fixtureDirectoryLocalOnly':str(tmp),'fixturesAreTemporaryCopiesOnly':True,'caseCount':len(rows),'rows':rows},indent=2)+'\n')
