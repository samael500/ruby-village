import bpy,json
from pathlib import Path
P=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(P/'sources/victoria.blend'))
rows=[]
for o in bpy.data.objects:
 if o.type=='MESH' and ('hair' in o.name.lower() or 'bang' in o.name.lower()):
  edge={tuple(sorted(e.vertices)):0 for e in o.data.edges}
  for f in o.data.polygons:
   for e in f.edge_keys:edge[tuple(sorted(e))]+=1
  rows.append({'name':o.name,'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'dimensions':list(o.dimensions),'nonTwoFaceEdges':sum(v!=2 for v in edge.values()),'materials':[x.name for x in o.data.materials if x],'modifiers':[x.type for x in o.modifiers],'particles':len(o.particle_systems)})
(P/'mesh-inventory.json').write_text(json.dumps(rows,indent=2)); print(json.dumps(rows))
