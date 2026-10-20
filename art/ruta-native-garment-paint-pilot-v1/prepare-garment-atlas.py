"""Derivative UV authoring only. Weld STAGING copies to unwrap; original topology/weights unchanged."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math,gzip,numpy as np
O=Path(__file__).resolve().parent;P=O.parent/'ruta-native-uv-paint-pilot-v1/ruta-native-painted-hair-pilot.blend';bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sc=bpy.context.scene

def invariants():
 out={}
 for o in sc.objects:
  if o.type=='MESH':
   p=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',p);out[o.name]=hashlib.sha256(p.tobytes()+repr([list(f.vertices)for f in o.data.polygons]).encode()+repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]).encode()).hexdigest()
 return out
def dump_faces(name,payload):
 with gzip.open(O/(name+'.json.gz'),'wt')as f:json.dump(payload,f,separators=(',',':'))
before=invariants();paint=[o for o in sc.objects if o.type=='MESH'and not o.hide_render and not o.name.startswith('Ellie ready ') and o.name!='Icosphere'];temps=[];records=[];print('PREPARE',len(paint),flush=True)
for original in paint:
 tmp=bpy.data.objects.new('UVSTAGE '+original.name,original.data.copy());sc.collection.objects.link(tmp);tmp.data.transform(original.matrix_world);bm=bmesh.new();bm.from_mesh(tmp.data);layer=bm.faces.layers.int.new('SourceFaceIndex');
 for i,f in enumerate(bm.faces):f[layer]=i
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if original.data.materials[f.material_index] and original.data.materials[f.material_index].name=='Skin'],context='FACES');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(tmp.data);bm.free();tmp.data.uv_layers.remove(tmp.data.uv_layers['RutaPaint'])if 'RutaPaint' in tmp.data.uv_layers else None;uv=tmp.data.uv_layers.new(name='RutaPaint');tmp.data.uv_layers.active=uv;temps.append((original,tmp));records.append({'object':original.name,'sourceVertices':len(original.data.vertices),'stagingWeldedVertices':len(tmp.data.vertices),'sourceFaces':len(original.data.polygons),'stagingFaces':len(tmp.data.polygons)})
bpy.ops.object.select_all(action='DESELECT')
for a,b in temps:b.select_set(True)
bpy.context.view_layer.objects.active=temps[0][1];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.015,area_weight=.2,correct_aspect=True,scale_to_bounds=True);bpy.ops.uv.average_islands_scale();bpy.ops.uv.pack_islands(rotate=True,scale=True,margin=.012);bpy.ops.object.mode_set(mode='OBJECT');print('SMART_UV_DONE',flush=True)
faces=[];colors={'skin':(225,161,116),'cream':(243,224,191),'white':(243,224,191),'olive':(94,111,54),'cargo':(127,80,46),'trouser':(127,80,46),'brass':(205,147,57),'gold':(205,147,57),'bow':(135,33,36),'burgundy':(135,33,36),'leather':(141,77,35),'brown':(141,77,35)}
def color(name):
 for k,v in colors.items():
  if k in name.lower():return v
 return(147,83,43)
for original,tmp in temps:
 uv=original.data.uv_layers.get('RutaPaint')or original.data.uv_layers.new(name='RutaPaint');sourceFaces={}
 for f in tmp.data.polygons:
  sourceIndex=tmp.data.attributes['SourceFaceIndex'].data[f.index].value;points={tuple(round(float(x),5)for x in tmp.data.vertices[tmp.data.loops[j].vertex_index].co):tuple(tmp.data.uv_layers['RutaPaint'].data[j].uv)for j in f.loop_indices};sourceFaces[sourceIndex]=points
 missing=0
 for f in original.data.polygons:
  if original.data.materials[f.material_index] and original.data.materials[f.material_index].name=='Skin':continue
  points=sourceFaces.get(f.index)
  if not points:missing+=1;continue
  for j in f.loop_indices:
   key=tuple(round(float(x),5)for x in (original.matrix_world@original.data.vertices[original.data.loops[j].vertex_index].co));nearest=key if key in points else min(points,key=lambda q:sum((a-b)**2 for a,b in zip(q,key)));assert sum((a-b)**2 for a,b in zip(nearest,key))<1e-8,(original.name,f.index,key);uv.data[j].uv=points[nearest]
  name=original.data.materials[f.material_index].name if len(original.data.materials)>f.material_index and original.data.materials[f.material_index]else'';faces.append({'object':original.name,'material':name,'color':color(name),'uv':[list(uv.data[j].uv)for j in f.loop_indices]})
 records[next(i for i,x in enumerate(records)if x['object']==original.name)]['unmappedDegenerateFaces']=missing;palette=next((u for u in original.data.uv_layers if u.name!='RutaPaint'),uv);original.data.uv_layers.active=palette;palette.active_render=True
 bpy.data.objects.remove(tmp,do_unlink=True)
assert invariants()==before,'original mesh topology/positions/weights changed';dump_faces('body-uv-faces',{'status':'technical-flatmaterialpainttarget-not-painted-art','uvLayer':'RutaPaint','faces':faces,'records':records})

bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-garment-uv-derivative.blend'),compress=True);(O/'mapping.json').write_text(json.dumps({'geometryWeightsExact':invariants()==before,'sourceSHA256':hashlib.sha256(P.read_bytes()).hexdigest(),'UVLayer':'RutaPaint','originalPaletteRenderUV':'UVMap','skinExcluded':True,'records':records},indent=2));print('GARMENT_UV_READY',flush=True)
