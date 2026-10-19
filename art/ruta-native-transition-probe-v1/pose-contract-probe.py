from pathlib import Path
import bpy,json,hashlib,numpy as np
from mathutils import Matrix
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');h=hashlib.sha256(P.read_bytes()).hexdigest();assert h=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];feet=bpy.data.objects['Adventurer_Feet'];used={i for f in feet.data.polygons for i in f.vertices};regions={}
for s in ['L','R']:
 eligible=[v for v in feet.data.vertices if v.index in used and sum(g.weight for g in v.groups if feet.vertex_groups[g.group].name=='Foot.'+s)>=.5];z=min(v.co.z for v in eligible);ids=[v.index for v in eligible if v.co.z<=z+.0084];lo=min(feet.data.vertices[i].co.y for i in ids);hi=max(feet.data.vertices[i].co.y for i in ids);regions[s]={'sole':ids,'heel':[i for i in ids if feet.data.vertices[i].co.y>=hi-.15*(hi-lo)],'toe':[i for i in ids if feet.data.vertices[i].co.y<=lo+.15*(hi-lo)]}
p=rig.data.bones['Root'].head_local.copy();p.z=0;rig.matrix_world=Matrix.Translation(-p)
for t in rig.animation_data.nla_tracks:t.mute=True
rows=[];snapshot={}
for action,frames in [('Walk_ProportionProposal',[0,5,10,15,20,25,30,35,40]),('Idle_Neutral_ProportionProposal',[0,12.5,25,37.5,50])]:
 a=bpy.data.actions[action];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
 for frame in frames:
  sc.frame_set(int(frame),subframe=frame-int(frame));bpy.context.view_layer.update();ev=feet.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();sole={}
  for s,r in regions.items():
   sole[s]={}
   for label,ids in r.items():
    ps=np.array([list(ev.matrix_world@me.vertices[i].co)for i in ids]);sole[s][label]={'centroid':ps.mean(axis=0).tolist(),'minXYZ':ps.min(axis=0).tolist(),'maxXYZ':ps.max(axis=0).tolist()}
  ev.to_mesh_clear();bones={name:{'worldHead':list(rig.matrix_world@b.head),'worldTail':list(rig.matrix_world@b.tail)}for name,b in rig.pose.bones.items()};rows.append({'action':action,'sourceFrame':frame,'timeSeconds':frame/24,'sole':sole,'boneEndpoints':bones});snapshot[(action,frame)]=bones
idle=snapshot[('Idle_Neutral_ProportionProposal',0)];joins=[]
for action,frame in [('Walk_ProportionProposal',f)for f in[0,5,10,15,20,25,30,35,40]]:
 p=snapshot[(action,frame)];d={n:float(np.linalg.norm(np.array(p[n]['worldHead'])-idle[n]['worldHead']))for n in p};joins.append({'walkFrame':frame,'maximumBoneHeadDistanceToIdle0M':max(d.values()),'atBone':max(d,key=d.get),'footHeadDistancesToIdle0M':{s:d['Foot.'+s]for s in['L','R']},'RootHeadDistanceM':d['Root'],'HipsHeadDistanceM':d['Hips']})
report={'status':'READONLY-POSE-SURFACE-SAMPLES-NOT-PHYSICAL-SUPPORT-LABELS','sourceSha256':h,'regions':regions,'samples':rows,'walkToIdle0PoseDifferences':joins,'limitations':['minsoleheight is not physical stance/contact truth','no blending, IK, newactions or source saves','native axes forward0,-1,0; camera not used']};assert hashlib.sha256(P.read_bytes()).hexdigest()==h;(O/'pose-contract-samples.json').write_text(json.dumps(report,indent=2)+'\n');print('POSE_CONTRACT_SAMPLED',len(rows),flush=True)
