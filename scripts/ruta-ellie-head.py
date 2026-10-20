"""Stage1: freeze complete native Ellie facial meshes, preserving evaluated native geometry/UV/materials."""
from pathlib import Path
import bpy,json,hashlib,os,re
R=Path(__file__).resolve().parents[1];O=R/'art/ruta-ellie-head-v1';S=O/'source/ellie-original.blend';bpy.ops.wm.open_mainfile(filepath=str(S),use_scripts=False);sc=bpy.context.scene;sc.frame_set(1)
EXPRESSION=os.environ.get('ELLIE_EXPRESSION','source-default');applied=[]
if EXPRESSION=='friendly':
 rig=bpy.data.objects['RIG-Ellie']
 for name in ['face_default','eyemask_content','mouth_smileclosed2']:
  a=bpy.data.actions[name]
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for f in bag.fcurves:
      value=f.evaluate(a.frame_range[0]);dest=rig.path_resolve(f.data_path)
      if hasattr(dest,'__setitem__'):dest[f.array_index]=value
      else:
       m=re.match(r'(.+)\["([^"]+)"\]$',f.data_path)
       if m:rig.path_resolve(m.group(1))[m.group(2)]=value
       else:
        owner,attr=f.data_path.rsplit('.',1);setattr(rig.path_resolve(owner),attr,value)
  applied.append({'nativePoseAsset':name,'sourceFrame':a.frame_range[0]})
 bpy.context.view_layer.update()
NAMES=['GEO-ellie_head','GEO-ellie_eye.L','GEO-ellie_eye.R','GEO-ellie_eye_highlights','GEO-ellie_eyebrows','GEO-ellie_eyelashes','GEO-ellie_face_line1','GEO-ellie_face_line2','GEO-ellie_teeth_top','GEO-ellie_teeth_btm','GEO-ellie_tongue','GEO-ellie_hair_cut'];parts=[];rows=[]
for name in NAMES:
 o=bpy.data.objects[name];originalmods=[{'name':m.name,'type':m.type,'viewportEnabled':m.show_viewport,'renderEnabled':m.show_render,'viewportLevels':m.levels if m.type=='SUBSURF'else None,'renderLevels':m.render_levels if m.type=='SUBSURF'else None}for m in o.modifiers]
 # Evaluate native render subdivision in dependency graph; no manual sculpt/shape substitute.
 if o.animation_data:
  for d in o.animation_data.drivers:
   if 'levels'in d.data_path:d.mute=True
 for m in o.modifiers:
  if m.type=='SUBSURF':m.show_viewport=True;m.levels=max(1,min(2,m.render_levels))
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dg);mesh=bpy.data.meshes.new_from_object(ev,preserve_all_data_layers=True,depsgraph=dg);mesh.transform(ev.matrix_world);part=bpy.data.objects.new('Ellie ready '+name.replace('GEO-ellie_',''),mesh);sc.collection.objects.link(part);part.hide_render=False;parts.append(part);rows.append({'sourceObject':name,'outputObject':part.name,'sourceVertices':len(o.data.vertices),'evaluatedVertices':len(mesh.vertices),'polygons':len(mesh.polygons),'originalModifiers':originalmods,'nativeSubdivEvaluation':'render levels, clamped1..2','sourceWasHiddenRender':o.hide_render,'meshSha256':hashlib.sha256(repr([tuple(v.co)for v in mesh.vertices]).encode()).hexdigest()})
# Freeze material driver values to current source values, avoiding a second character rig in derived static parts.
seen=set()
def freeze(tree):
 if not tree or tree.as_pointer()in seen:return
 seen.add(tree.as_pointer());tree.animation_data_clear()
 for n in tree.nodes:
  if n.type=='GROUP':freeze(n.node_tree)
for o in parts:
 for m in o.data.materials:
  if m:m.animation_data_clear();freeze(m.node_tree)
rig=bpy.data.objects['RIG-Ellie'];markers={n:list(rig.matrix_world@rig.pose.bones[n].head)for n in ['ORG-Head','ORG-Neck','DEF-Chin']}
for t in bpy.data.texts:
 if any(k in t.name.lower()for k in ['readme','license','credit']):(O/'source'/('upstream-'+t.name.replace('/','_')+'.txt')).write_text(t.as_string())
bpy.data.libraries.write(str(O/('ellie-native-head-parts'+('-friendly'if EXPRESSION=='friendly'else'')+'.blend')),set(parts),fake_user=True,compress=True)
report={'status':'native-Ellie-head-source-extraction-not-Ruta-acceptance','sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'sourceFrame':1,'expressionVariant':EXPRESSION,'appliedNativePoseAssets':applied,'autoExecScripts':False,'parts':rows,'sourceMarkersWorld':markers,'coordinateSystem':'native Ellie world meters, declared source expression at frame1 frozen','binding':'not yet bound; original complete rig/face actions preserved in source original','materials':'original native material graphs/textures/UV; driver values frozen only in derived static parts; no new face drawing or primitives','hair':'existing native haircut geometry, dark short hair not Ruta waves','limitations':['complete frozen neutral head has no independent facial animation in derivative; full upstream facial rig preserved in original blend','native existing modifier stack evaluated with subdivision render level clamped1..2','rig/script compatibility and source expression require visual review before acceptance']};(O/('extraction-friendly.json'if EXPRESSION=='friendly'else'extraction.json')).write_text(json.dumps(report,indent=2)+'\n');print('ELLIE_NATIVE_HEAD_EXTRACTED',len(parts),sum(len(o.data.vertices)for o in parts),flush=True)
