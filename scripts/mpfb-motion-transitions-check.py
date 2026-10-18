"""Fresh saved-file source measurements for isolated MPFB transient actions."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/characters-mpfb-v1/motion/transitions';path=OUT/'mpfb-start-stop-technical.blend';before=hashlib.sha256(path.read_bytes()).hexdigest();meta=json.loads((OUT/'manifest.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(path))
rig=bpy.data.objects['Ruta.MPFB.StandardRig'];shoe=bpy.data.objects['Ruta.shoes01'];thumb=bpy.data.objects['Motion ONE strap thumb pinch control'];pole=bpy.data.objects['Motion ONE strap anatomical thumb pole'];controls=[rig,thumb,pole]
for m in shoe.modifiers:
 if m.type=='SUBSURF':m.levels=m.render_levels;m.show_viewport=True
probe=shoe.copy();probe.name='MEASUREMENT ONLY stable-source-sole-index probe';bpy.context.collection.objects.link(probe);probe.hide_render=True
for m in probe.modifiers:
 if m.type=='SUBSURF':m.show_viewport=False
markers={}
for side,sign in [('L',1),('R',-1)]:
 vertices=[v for v in shoe.data.vertices if v.co.x*sign>0];z=min(v.co.z for v in vertices);sole=[v for v in vertices if v.co.z<z+.008];front=min(v.co.y for v in sole);back=max(v.co.y for v in sole);markers[side]={kind:[v.index for v in sole if (v.co.y<front+.025 if kind=='toe'else v.co.y>back-.025)]for kind in ['toe','heel']}
def activate(bundle):
 for o in controls:o.animation_data.action=bpy.data.actions[bundle[o.name]]
reports={}
for name,item in [(f'demo-{side}',d)for side,d in meta['demos'].items()]+list(meta['clips'].items()):
 activate(item['actionBundle']);records=[];groups={}
 for planned in item['frames']:
  frame=planned['frame'];bpy.context.scene.frame_set(frame);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();er=rig.evaluated_get(deps);es=shoe.evaluated_get(deps);ep=probe.evaluated_get(deps);r={'frame':frame,'state':planned['state'],'rootWorld':list(rig.matrix_world.translation),'minFullRenderBootZ':min((es.matrix_world@v.co).z for v in es.data.vertices),'feet':{}}
  for side,word in [('L','left'),('R','right')]:
   ankle=er.matrix_world@er.pose.bones['foot.'+side].head;target=er.matrix_world@er.pose.bones[word+'_foot_ik'].head;d={'contactMode':planned['feet'][side]['contactMode'],'ankleWorld':list(ankle),'targetWorld':list(target),'ankleTargetErrorMeters':(ankle-target).length,'sole':{}}
   for kind,ids in markers[side].items():
    points=[ep.matrix_world@ep.data.vertices[i].co for i in ids];center=sum(points,Vector())/len(points);d['sole'][kind]=list(center)
    if d['contactMode']=='flat':groups.setdefault((side,round(planned['feet'][side]['plannedBaseForwardMeters'],6),kind),[]).append(center)
   r['feet'][side]=d
  records.append(r)
 drift=max(((a-b).length for points in groups.values()for a in points for b in points),default=0);error=max(d['ankleTargetErrorMeters']for r in records for d in r['feet'].values());minimum=min(r['minFullRenderBootZ']for r in records);reports[name]={'summary':{'flatSoleMarkerDriftMeters':drift,'maxActualAnkleTargetErrorMeters':error,'minFullRenderLevelBootZ':minimum,'worstAnkleFrame':max(records,key=lambda r:max(f['ankleTargetErrorMeters']for f in r['feet'].values()))['frame']},'records':records}
summary={name:r['summary']for name,r in reports.items()};missing=[a for a in meta['sourceActions'].values()if a not in bpy.data.actions];result={'status':'MEASURED AUTHOR PROTOTYPE, NOT INDEPENDENT NATURALNESS REVIEW','method':'Fresh saved-file action-bundle playback; actual evaluated render-level full boots for floor; separate non-render measurement clone without subdivision for stable source sole indices; world skin marker drift grouped by flat stance/planned base identity, not target-only readback. No source save.','sourceSha256Before':before,'sourceSha256After':hashlib.sha256(path.read_bytes()).hexdigest(),'missingSourceWalkActions':missing,'summary':summary,'clips':reports};(OUT/'fresh-source-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'missingSourceWalkActions':missing,'summary':summary},indent=2))
