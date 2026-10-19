import bpy,json
from pathlib import Path
R=Path('/tmp/ruby-export-pack-qa');O=R/'docs/chapter-1-rc/qa/export-pack-contract'
bpy.ops.wm.open_mainfile(filepath=str(R/'art/ruta-ellie-head-v1/color-handoff/ruta-b-ellie-blue-copper-temporary.blend'));rig=bpy.data.objects['CharacterArmature'];a=bpy.data.actions['Walk_ProportionProposal'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
for t in rig.animation_data.nla_tracks:t.mute=True
obj=bpy.data.objects['Adventurer_Body'];bpy.context.scene.frame_set(10)
def snapshot():
 bpy.context.view_layer.update();ev=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();v=[tuple(ev.matrix_world@p.co)for p in me.vertices];ev.to_mesh_clear();return v
base=snapshot();obj.hide_set(True);eye=snapshot();obj.hide_set(False);obj.hide_viewport=True;disabled=snapshot();obj.hide_viewport=False
report={'renderVisibleViewportDisabledObjects':[o.name for o in bpy.context.scene.objects if o.type=='MESH' and not o.hide_render and o.hide_viewport],'modifierVisibilityDivergence':[(o.name,m.name,m.type,m.show_viewport,m.show_render)for o in bpy.context.scene.objects if o.type=='MESH' and not o.hide_render for m in o.modifiers if m.show_viewport!=m.show_render],'object':obj.name,'vertexCount':len(base),'eyeHiddenMaxCoordinateChange':max(abs(x-y)for a,b in zip(base,eye)for x,y in zip(a,b)),'objectDisableViewportMaxCoordinateChange':max(abs(x-y)for a,b in zip(base,disabled)for x,y in zip(a,b))};(O/'visibility-probe.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
