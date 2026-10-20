import bpy,json,math
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parents[1];C=json.loads((R/'art/ruta-native-proportions-v1/rest-transform-contract.json').read_text());bpy.ops.wm.open_mainfile(filepath=str(R/'art/ready-character-adapted-v1/ruta-stock-adapted.blend'));rows=[]
for torso in [.70,.85,.90,.92]:
 bones={}
 for name,b in C['bones'].items():
  s=torso if name in ['Hips','Abdomen','Torso','Chest']else b['scale'];par=b['parent'];old=Vector(b['oldHead']);head=(Vector(bones[par]['newHead'])+(old-Vector(C['bones'][par]['oldHead']))*bones[par]['scale'])if par else old*.7;bones[name]={'scale':s,'newHead':list(head),'newTail':list(head+(Vector(b['oldTail'])-old)*s)}
 pts=[];hp=[]
 for ob in bpy.context.scene.objects:
  if ob.type!='MESH' or ob.parent!=bpy.data.objects['CharacterArmature']:continue
  names={g.index:g.name for g in ob.vertex_groups};used={i for p in ob.data.polygons for i in p.vertices}
  for i in used:
   v=ob.data.vertices[i];ws=[(names[g.group],g.weight)for g in v.groups if names[g.group]in bones and g.weight>0];total=sum(w for n,w in ws);q=sum(((Vector(bones[n]['newHead'])+(v.co-Vector(C['bones'][n]['oldHead']))*bones[n]['scale'])*w for n,w in ws),Vector())/total if total else v.co*.7;pts.append(q)
   if ob.name=='Adventurer_Head':hp.append(q)
 h=max(v.z for v in pts)-min(v.z for v in pts);row={'torsoScale':torso,'heightMeters':h,'headProxyFraction':(max(v.z for v in pts)-min(v.z for v in hp))/h,'shoulderAbsoluteZ':bones['UpperArm.L']['newHead'][2],'shoulderFraction':bones['UpperArm.L']['newHead'][2]/h,'hipFraction':bones['UpperLeg.L']['newHead'][2]/h}
 for name in ['UpperLeg.L','LowerLeg.L','UpperArm.L','LowerArm.L']:row[name+'LengthFraction']=math.dist(bones[name]['newHead'],bones[name]['newTail'])/h
 rows.append(row)
p=R/'art/ruta-native-proportions-study-v2';p.mkdir(exist_ok=True);(p/'torso-variant-numbers.json').write_text(json.dumps({'status':'numeric-study-not-approved','torsoBones':['Hips','Abdomen','Torso','Chest'],'bodyLegs':.70,'headNeck':1.60,'upperLowerArms':.63,'variants':rows},indent=2)+'\n');print(json.dumps(rows,indent=2))
