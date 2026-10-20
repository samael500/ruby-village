from pathlib import Path
import bpy,json,hashlib,numpy as np
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=sha(P);assert h=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sc=bpy.context.scene;rows=[]
selected=['Adventurer_Body','Adventurer_Feet','Ruta stock long trousers','ONE diagonal satchel strap','Ellie ready head','Ellie ready Loose cap','Ellie ready Layered wave 1','Satchel rounded body','Satchel rounded flap']
for o in sc.objects:
 if o.type!='MESH'or o.hide_render:continue
 uv=[]
 for layer in o.data.uv_layers:
  coords=np.empty(len(layer.data)*2,dtype=np.float32);layer.data.foreach_get('uv',coords);coords=coords.reshape((-1,2));areas=[];hashes=[]
  for poly in o.data.polygons:
   ps=coords[list(poly.loop_indices)];area=abs(sum(float(ps[i,0]*ps[(i+1)%len(ps),1]-ps[(i+1)%len(ps),0]*ps[i,1])for i in range(len(ps))))*.5;areas.append(area);hashes.append(tuple(sorted(tuple(np.round(v,6))for v in ps)))
  uv.append({'name':layer.name,'rangeMin':coords.min(axis=0).tolist(),'rangeMax':coords.max(axis=0).tolist(),'uniqueRoundedUVCount':len(set(tuple(v)for v in np.round(coords,6))),'faceUVAreaSum':sum(areas),'zeroAreaFaces':sum(x<1e-12 for x in areas),'faceCount':len(areas),'exactDuplicateUVPolygonCount':len(hashes)-len(set(hashes)),'limitation':'summedarea/duplicates diagnose palette/overlap risk, not complete geometric-overlap proof'})
 coords=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',coords);rows.append({'object':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'positionsSha256':hashlib.sha256(coords.tobytes()).hexdigest(),'materialSlots':[m.name if m else None for m in o.data.materials],'uvLayers':uv})
materials=[]
for m in {m for o in sc.objects if o.type=='MESH'and not o.hide_render for m in o.data.materials if m}:
 if not m.use_nodes:continue
 materials.append({'name':m.name,'nodes':[{'name':n.name,'type':n.type,'group':n.node_tree.name if n.type=='GROUP'else None,'image':n.image.name if n.type=='TEX_IMAGE'and n.image else None}for n in m.node_tree.nodes],'links':[{'from':l.from_node.name+'.'+l.from_socket.name,'to':l.to_node.name+'.'+l.to_socket.name}for l in m.node_tree.links]})
(O/'packed-images').mkdir(exist_ok=True);images=[]
for im in bpy.data.images:
 if not im.packed_file:continue
 data=bytes(im.packed_file.data);suffix='.png'if data.startswith(b'\x89PNG')else'.jpg'if data.startswith(b'\xff\xd8')else'.bin';name=''.join(c if c.isalnum()or c in'.-_'else'_'for c in im.name);path=O/'packed-images'/(name+suffix);path.write_bytes(data);images.append({'image':im.name,'size':list(im.size),'sourceFilepath':im.filepath,'file':str(path.relative_to(O)),'sha256':sha(path),'exactPackedBytes':True})
report={'status':'READONLY-UV-MATERIAL-GEOMETRY-CONSTRAINTS-NO-PAINT-APPLIED','source':str(P),'sha256Before':h,'sha256After':sha(P),'visibleMeshes':rows,'materials':materials,'packedImages':images,'sourceSaved':False};assert report['sha256After']==h;(O/'constraints.json').write_text(json.dumps(report,indent=2)+'\n');print('CONSTRAINTS',len(rows),[(x['image'],x['size'])for x in images],flush=True)
