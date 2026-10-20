import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style');O=Path('/home/mskorokhod/life/ruby-village-36-painted-v2-review/docs/chapter-1-rc/qa/painted-native-style-v2');P=R/'art/ruta-native-layered-style-v2/ruta-native-style.blend';assert hashlib.sha256(P.read_bytes()).hexdigest()=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706';bpy.ops.wm.open_mainfile(filepath=str(P),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];a=bpy.data.actions['Walk_ProportionProposal'];rig.animation_data.action=a;rig.animation_data.action_slot=a.slots[0]
for t in rig.animation_data.nla_tracks:t.mute=True
rest=rig.data.bones['Root'].head_local.copy();rest.z=0;rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-rest);c=json.loads((R/'art/ruta-native-layered-walk48-v2/source-contract.json').read_text())['cameraVariants']['base']['fixedRenderCamera'];cam=bpy.data.objects.new('ReadOnlySemanticCamera',bpy.data.cameras.new('ReadOnlySemanticCamera'));sc.collection.objects.link(cam);cam.data.type='ORTHO';cam.data.ortho_scale=c['orthoScale'];cam.matrix_world=Matrix(c['matrixWorld']);sc.camera=cam;sc.render.resolution_x=512;sc.render.resolution_y=640;sc.render.resolution_percentage=100
rows=[]
for i in range(48):
 f=40*i/48;sc.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();features={}
 for name in ['Burgundy bow knot','Satchel warm brass clasp']:
  o=bpy.data.objects[name];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();used=sorted({j for p in me.polygons for j in p.vertices});p=sum((ev.matrix_world@me.vertices[j].co for j in used),Vector())/len(used);q=world_to_camera_view(sc,cam,p);xy=[q.x*512,(1-q.y)*640];features[name]={'nativeFullPx':xy,'paintedGlobalCalibrationPx':[(xy[0]/2-29.60245861921824)/1.1631563024644236,(xy[1]/2-53.313741280992616)/1.1631563024644236],'world':list(p),'usedVertexCount':len(used)};ev.to_mesh_clear()
 rows.append({'phase':i,'features':features})
(O/'full48-native-semantic-projections.json').write_text(json.dumps({'sourceSha256':hashlib.sha256(P.read_bytes()).hexdigest(),'definition':'centroid of all evaluated used mesh vertices of authored knot/clasp; not silhouette bbox or visible painted contour','camera':c,'globalCalibrationFromPacker':{'paintedToNativeHalfS':1.1631563024644236,'T':[29.60245861921824,53.313741280992616],'limitation':'global shape-proxy diagnostic not physical joint fit'},'rows':rows},indent=2)+'\n');print('PROJECTED',len(rows),flush=True)
