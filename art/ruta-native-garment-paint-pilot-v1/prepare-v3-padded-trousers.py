from pathlib import Path
import bpy,json,hashlib,gzip
O=Path(__file__).resolve().parent;V=O/'v3-padded-trousers';V.mkdir(exist_ok=True);P=O/'ruta-painted-garment-pilot.blend';bpy.ops.wm.open_mainfile(filepath=str(P));ob=bpy.data.objects['Ruta stock long trousers'];me=ob.data;old=me.uv_layers['RutaPaint'];new=me.uv_layers.new(name='RutaPaintPaddedTrousers');parents=list(range(len(me.polygons)));owners={}
def find(i):
 while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
 return i
for f in me.polygons:
 for j in f.loop_indices:
  k=tuple(round(float(x),6)for x in old.data[j].uv)
  if k in owners:parents[find(f.index)]=find(owners[k])
  else:owners[k]=f.index
charts={}
for f in me.polygons:charts.setdefault(find(f.index),[]).append(f)
selected=[fs for fs in charts.values()if len(fs)>=20];excluded=[f.index for fs in charts.values()if len(fs)<20 for f in fs];assert len(selected)==11
# Preserve all old UV layers. Tiny charts keep original plain material; only explicit selected faces get new paint slot later.
with bpy.data.libraries.load(str(O.parent/'ruta-native-uv-paint-pilot-v1/ruta-native-painted-hair-pilot.blend'),link=False)as(src,dst):dst.materials=['Ruta warm loose cargo cloth']
plain=bpy.data.materials['Ruta warm loose cargo cloth'];me.materials.append(plain);plainIndex=len(me.materials)-1
for f in me.polygons:f.material_index=plainIndex
placeholder=plain.copy();placeholder.name='Ruta v3 padded trousers pending texture';me.materials.append(placeholder);paintIndex=len(me.materials)-1
scale=1450.;rows=[];faces=[]
for n,fs in enumerate(selected):
 ps=[tuple(old.data[j].uv)for f in fs for j in f.loop_indices];mn=[min(p[k]for p in ps)for k in[0,1]];mx=[max(p[k]for p in ps)for k in[0,1]];center=[(mn[k]+mx[k])/2 for k in[0,1]];cx=256+(n%4)*512;cy=341+(n//4)*682
 for f in fs:
  f.material_index=paintIndex
  for j in f.loop_indices:
   u,v=old.data[j].uv;x=cx+(u-center[0])*scale;y=cy-(v-center[1])*scale;new.data[j].uv=(x/2047,1-y/2047)
  faces.append({'sourceFaceIndex':f.index,'chartIndex':n,'uv':[list(new.data[j].uv)for j in f.loop_indices]})
 rows.append({'chartIndex':n,'faceCount':len(fs),'sourceFaceIndices':[f.index for f in fs],'actualBoundsPx':[[cx-(mx[0]-mn[0])*scale/2,cy-(mx[1]-mn[1])*scale/2],[cx+(mx[0]-mn[0])*scale/2,cy+(mx[1]-mn[1])*scale/2]]})
# Inactive palette binding stays native; later shader explicitly targets only new layer.
me.uv_layers.active=me.uv_layers['UVMap'];me.uv_layers['UVMap'].active_render=True
with gzip.open(V/'actual-UV-faces.json.gz','wt')as z:json.dump({'uvLayer':new.name,'faces':faces},z)
meta={'status':'technical-newUV-target-only','sourceSHA256':hashlib.sha256(P.read_bytes()).hexdigest(),'object':ob.name,'newUVLayer':new.name,'preservedUVLayers':[u.name for u in me.uv_layers if u.name!=new.name],'pixelSize':[2048,2048],'constantUVScalePxPerUVUnit':scale,'paintBleedPixels':16,'selectedCharts':rows,'selectedFaces':len(faces),'tinyUnpaintedFaces':excluded,'paintMaterialIndex':paintIndex,'plainMaterialIndex':plainIndex,'noRestGeometryRigWeightsActionsChanges':True}
(V/'padding-contract.json').write_text(json.dumps(meta,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(V/'ruta-trousers-newUV-source.blend'),compress=True);print('V3_UV_READY',flush=True)
