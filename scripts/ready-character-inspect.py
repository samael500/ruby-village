import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];src=root/'art/ready-character-walk-v1/source/adventurer-original.gltf'
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(src))
report={'objects':[],'actions':[]}
for o in bpy.data.objects:
 row={'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'scale':list(o.scale)}
 if o.type=='ARMATURE':row.update(bones=[b.name for b in o.data.bones],tracks=[(t.name,[(s.name,s.action.name if s.action else None)for s in t.strips])for t in o.animation_data.nla_tracks])
 if o.type=='MESH':row.update(vertices=len(o.data.vertices),polygons=len(o.data.polygons),groups=len(o.vertex_groups),modifiers=[m.type for m in o.modifiers],materials=[m.name for m in o.data.materials])
 report['objects'].append(row)
for a in bpy.data.actions:report['actions'].append({'name':a.name,'range':list(a.frame_range),'slots':[(s.identifier,s.target_id_type)for s in a.slots]})
(root/'art/ready-character-walk-v1/source/inspection.json').write_text(json.dumps(report,indent=2)+'\n')
bpy.ops.wm.save_as_mainfile(filepath=str(root/'art/ready-character-walk-v1/source/adventurer-imported.blend'))
print(json.dumps(report))
