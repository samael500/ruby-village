from pathlib import Path
import bpy,json,gzip,math,hashlib
O=Path(__file__).resolve().parent;V=O/'v4-padded-accessories';V.mkdir(exist_ok=True);P=O/'v3-padded-trousers/ruta-padded-trousers-pilot.blend';bpy.ops.wm.open_mainfile(filepath=str(P));names=['Adventurer_Feet','ONE diagonal satchel strap','ONE rounded right hip satchel','Single rounded satchel flap'];source=O.parent/'ruta-native-uv-paint-pilot-v1/ruta-native-painted-hair-pilot.blend'
# Original uniform native materials for tiny charts and cloth pockets.
plainNames=['Brown_02','Brown2','Adapted warm brown leather','Ruta satchel warm leather','Cargo pocket cloth L','Cargo pocket cloth R']
with bpy.data.libraries.load(str(source),link=False)as(src,dst):dst.materials=[n for n in plainNames if n not in bpy.data.materials]
for name in ['Cargo side pocket L','Cargo side pocket R']:
 ob=bpy.data.objects[name];mat=bpy.data.materials['Cargo pocket cloth '+name[-1]]
 for slot in ob.material_slots:slot.material=mat
charts=[];records=[]
for name in names:
 ob=bpy.data.objects[name];me=ob.data;old=me.uv_layers['RutaPaint'];new=me.uv_layers.new(name='RutaPaintPaddedAccessories');par=list(range(len(me.polygons)));owners={}
 def find(i):
  while par[i]!=i:par[i]=par[par[i]];i=par[i]
  return i
 for f in me.polygons:
  for j in f.loop_indices:
   key=(f.material_index,)+tuple(round(float(x),6)for x in old.data[j].uv)
   if key in owners:par[find(f.index)]=find(owners[key])
   else:owners[key]=f.index
 groups={}
 for f in me.polygons:groups.setdefault(find(f.index),[]).append(f)
 selected=[];tiny=[]
 for fs in groups.values():
  oldname=me.materials[fs[0].material_index].name;plainname=oldname.removeprefix('Ruta painted garment ');plain=bpy.data.materials[plainname];me.materials.append(plain);pi=len(me.materials)-1
  for f in fs:f.material_index=pi
  if len(fs)>=12 and min(max(float(old.data[j].uv[k])for f in fs for j in f.loop_indices)-min(float(old.data[j].uv[k])for f in fs for j in f.loop_indices)for k in[0,1])>.002:
   ps=[tuple(old.data[j].uv)for f in fs for j in f.loop_indices];mn=[min(p[k]for p in ps)for k in[0,1]];mx=[max(p[k]for p in ps)for k in[0,1]];charts.append({'object':name,'faces':[f.index for f in fs],'sourceMaterial':plainname,'bounds':[mn,mx]});selected+= [f.index for f in fs]
  else:tiny+=[f.index for f in fs]
 records.append({'object':name,'selectedFaces':selected,'tinyOriginalMaterialFaces':tiny,'newUV':new.name})
count=len(charts)
def pack(scale):
 shelves=[];placements={}
 for index in sorted(range(count),key=lambda i:charts[i]['bounds'][1][1]-charts[i]['bounds'][0][1],reverse=True):
  mn,mx=charts[index]['bounds'];w=(mx[0]-mn[0])*scale+80;h=(mx[1]-mn[1])*scale+80
  if w>1984 or h>1984:return None
  shelf=next((r for r in shelves if r['height']>=h and r['x']+w<=2016),None)
  if shelf is None:
   y=32+sum(r['height']for r in shelves)
   if y+h>2016:return None
   shelf={'x':32,'y':y,'height':h};shelves.append(shelf)
  placements[index]=(shelf['x']+w/2,shelf['y']+h/2);shelf['x']+=w
 return placements
lo=0.;hi=10000.
for _ in range(40):
 mid=(lo+hi)/2
 if pack(mid):lo=mid
 else:hi=mid
scale=lo*.98;placements=pack(scale);faces=[]
for n,c in enumerate(charts):
 ob=bpy.data.objects[c['object']];me=ob.data;old=me.uv_layers['RutaPaint'];new=me.uv_layers['RutaPaintPaddedAccessories'];mn,mx=c['bounds'];center=[(mn[k]+mx[k])/2 for k in[0,1]];cx,cy=placements[n];placeholder=bpy.data.materials[c['sourceMaterial']].copy();placeholder.name='Ruta v4 padded accessory '+str(n);me.materials.append(placeholder);mi=len(me.materials)-1
 for index in c['faces']:
  f=me.polygons[index];f.material_index=mi
  for j in f.loop_indices:
   u,v=old.data[j].uv;new.data[j].uv=((cx+(u-center[0])*scale)/2047,1-(cy-(v-center[1])*scale)/2047)
  faces.append({'object':ob.name,'sourceFaceIndex':index,'chartIndex':n,'material':c['sourceMaterial'],'uv':[list(new.data[j].uv)for j in f.loop_indices]})
 c['chartIndex']=n;c['placeholderMaterial']=placeholder.name;c['actualBoundsPx']=[[cx-(mx[0]-mn[0])*scale/2,cy-(mx[1]-mn[1])*scale/2],[cx+(mx[0]-mn[0])*scale/2,cy+(mx[1]-mn[1])*scale/2]]
with gzip.open(V/'actual-UV-faces.json.gz','wt')as z:json.dump({'uvLayer':'RutaPaintPaddedAccessories','faces':faces},z)
(V/'padding-contract.json').write_text(json.dumps({'sourceSHA256':hashlib.sha256(P.read_bytes()).hexdigest(),'newUVLayer':'RutaPaintPaddedAccessories','paintBleedPixels':16,'constantUVScale':scale,'chartCount':count,'charts':charts,'objects':records,'clothPockets':'restored original uniform Cargo pocket cloth L/R, excluded from leather atlas','pantsV3Unchanged':True},indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(V/'ruta-accessories-newUV-source.blend'),compress=True);print('V4_ACCESSORIES_READY',count,flush=True)
