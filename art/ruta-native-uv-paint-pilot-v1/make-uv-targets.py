"""Derivative UV authoring only. Weld STAGING copies to unwrap; original topology/weights unchanged."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math,gzip,numpy as np
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');assert hashlib.sha256(P.read_bytes()).hexdigest()=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sc=bpy.context.scene

def invariants():
 out={}
 for o in sc.objects:
  if o.type=='MESH':
   p=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',p);out[o.name]=hashlib.sha256(p.tobytes()+repr([list(f.vertices)for f in o.data.polygons]).encode()+repr([[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]).encode()).hexdigest()
 return out
def dump_faces(name,payload):
 with gzip.open(O/(name+'.json.gz'),'wt')as f:json.dump(payload,f,separators=(',',':'))
before=invariants();paint=[o for o in sc.objects if o.type=='MESH'and not o.hide_render and not o.name.startswith('Ellie ready ')];temps=[];records=[];print('PREPARE',len(paint),flush=True)
for original in paint:
 tmp=bpy.data.objects.new('UVSTAGE '+original.name,original.data.copy());sc.collection.objects.link(tmp);bm=bmesh.new();bm.from_mesh(tmp.data);layer=bm.faces.layers.int.new('SourceFaceIndex');
 for i,f in enumerate(bm.faces):f[layer]=i
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.to_mesh(tmp.data);bm.free();uv=tmp.data.uv_layers.new(name='RutaPaint');tmp.data.uv_layers.active=uv;temps.append((original,tmp));records.append({'object':original.name,'sourceVertices':len(original.data.vertices),'stagingWeldedVertices':len(tmp.data.vertices),'sourceFaces':len(original.data.polygons),'stagingFaces':len(tmp.data.polygons)})
bpy.ops.object.select_all(action='DESELECT')
for a,b in temps:b.select_set(True)
bpy.context.view_layer.objects.active=temps[0][1];bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.015,area_weight=.2,correct_aspect=True,scale_to_bounds=True);bpy.ops.object.mode_set(mode='OBJECT');print('SMART_UV_DONE',flush=True)
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
  points=sourceFaces.get(f.index)
  if not points:missing+=1;continue
  for j in f.loop_indices:
   key=tuple(round(float(x),5)for x in original.data.vertices[original.data.loops[j].vertex_index].co);assert key in points,(original.name,f.index,key);uv.data[j].uv=points[key]
  name=original.data.materials[f.material_index].name if len(original.data.materials)>f.material_index and original.data.materials[f.material_index]else'';faces.append({'object':original.name,'material':name,'color':color(name),'uv':[list(uv.data[j].uv)for j in f.loop_indices]})
 records[next(i for i,x in enumerate(records)if x['object']==original.name)]['unmappedDegenerateFaces']=missing;original.data.uv_layers.active=uv;uv.active_render=True
 bpy.data.objects.remove(tmp,do_unlink=True)
assert invariants()==before,'original mesh topology/positions/weights changed';dump_faces('body-uv-faces',{'status':'technical-flatmaterialpainttarget-not-painted-art','uvLayer':'RutaPaint','faces':faces,'records':records})
# Native ready head and original6lock charts are valid, preserve their native UV exactly.
for label,names in [('head',['Ellie ready head']),('hair',['Ellie ready Loose cap']+['Ellie ready Layered wave '+str(i)for i in range(1,7)])]:
 fs=[]
 for name in names:
  o=bpy.data.objects[name];uv=o.data.uv_layers['UVMap']
  for f in o.data.polygons:fs.append({'object':name,'uv':[list(uv.data[j].uv)for j in f.loop_indices],'color':(200,133,97)if label=='head'else(167,83,32)})
 dump_faces(label+'-uv-faces',{'status':'existingnativeUVpaintguide-no-UVchanges','uvLayer':'UVMap','faces':fs})
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-native-uv-derivative.blend'),compress=True);(O/'uv-derivative-contract.json').write_text(json.dumps({'sourceSha256':'bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706','beforeGeometryWeightsHashes':before,'afterGeometryWeightsHashes':invariants(),'geometryWeightsExact':True,'newUVLayer':'RutaPaint','stagingMethod':'temporaryweldedcopies1e-7->SmartUV66deg->transfer originalface+cornerco; stagingremoved; original topology/positions/weights intact','objects':records,'nativeHeadHairUVPreserved':True,'paintApplied':False},indent=2)+'\n');print('UV_DERIVATIVE_READY',flush=True)
