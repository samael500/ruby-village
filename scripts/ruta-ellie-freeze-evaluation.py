"""Agree visible source viewport/render evaluation without changing rendered resolution."""
from pathlib import Path
import bpy,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'art/ruta-ellie-head-v1/layered-locks-pilot';f=P/'ruta-b-ellie-layered-locks.blend';bpy.ops.wm.open_mainfile(filepath=str(f),use_scripts=False);records=[]
for o in bpy.context.scene.objects:
 if o.hide_render:continue
 o.hide_viewport=False;o.hide_set(False)
 for m in o.modifiers:
  if m.type=='SUBSURF':m.levels=m.render_levels
  m.show_viewport=m.show_render
 records.append({'object':o.name,'hideRender':o.hide_render,'hideViewport':o.hide_viewport,'hideSet':o.hide_get(),'modifiers':[{'name':m.name,'type':m.type,'viewportEnabled':m.show_viewport,'renderEnabled':m.show_render,**({'viewportLevel':m.levels,'renderLevel':m.render_levels}if m.type=='SUBSURF'else{})}for m in o.modifiers]})
collections=[]
for c in bpy.data.collections:
 if not c.hide_render:c.hide_viewport=False
 collections.append({'collection':c.name,'hideRender':c.hide_render,'hideViewport':c.hide_viewport})
def layerfix(l):
 if not l.collection.hide_render:l.hide_viewport=False
 for c in l.children:layerfix(c)
for l in bpy.context.scene.view_layers:layerfix(l.layer_collection)
bpy.ops.wm.save_as_mainfile(filepath=str(f),compress=True);(P/'evaluation-contract.json').write_text(json.dumps({'status':'visible-source-evaluation-aligned-not-art-acceptance','renderGeometryUnchanged':True,'visibleObjects':records,'collections':collections},indent=2)+'\n');print('EVALUATION_FROZEN',flush=True)
