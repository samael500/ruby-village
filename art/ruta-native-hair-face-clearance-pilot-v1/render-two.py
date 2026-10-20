from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;R=O.parents[1];r=json.load(open(O/'derivation.json'));check=json.load(open(O/'cold-check.json'));sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();sources=[('baseline',R/'art/ruta-native-hair-tone-pilot-v1/cache/ruta-hair-tone-trial.blend',r['sourceSha256']),('candidate',O/'cache/ruta-hair-face-clearance-trial.blend',r['outputSha256'])];rows=[]
for name,p,expected in sources:
 assert sha(p)==expected;bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.animation_data.action=bpy.data.actions['Walk_ProportionProposal'];rig.animation_data.action_slot=rig.animation_data.action.slots[0];rig.matrix_world=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(Vector((0,.050602056086063385,0)));sc.frame_set(0);bpy.context.view_layer.update();sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=32;eyeBounds=[];dg=bpy.context.evaluated_depsgraph_get()
 for n in ['Ellie ready eye.L','Ellie ready eye.R']:
  obj=bpy.data.objects[n];ev=obj.evaluated_get(dg);me=ev.to_mesh();pts=[world_to_camera_view(sc,sc.camera,ev.matrix_world@v.co)for v in me.vertices];eyeBounds.append({'name':n,'boundsPx':[[min(v.x for v in pts)*512,min((1-v.y)for v in pts)*640],[max(v.x for v in pts)*512,max((1-v.y)for v in pts)*640]]});ev.to_mesh_clear()
 sc.render.filepath=str(O/('e-'+name+'32.png'));bpy.ops.render.render(write_still=True);assert sha(p)==expected;rows.append({'state':name,'sourceSha256':expected,'renderSha256':sha(O/('e-'+name+'32.png')),'yaw':math.pi/2,'action':'Walk_ProportionProposal','sourceFrame':0,'AA':32,'cameraMatrix':[list(x)for x in sc.camera.matrix_world],'eyeGlobeProjectedBounds':eyeBounds})
assert rows[0]['cameraMatrix']==rows[1]['cameraMatrix'];(O/'render-proof.json').write_text(json.dumps({'status':'DIAGNOSTICONLY, earcontactriskOPEN','views':rows,'noFrontOrThreequarter':True},indent=2)+'\n')
