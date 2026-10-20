from pathlib import Path
import bpy,json,math,hashlib,gzip
from mathutils import Matrix,Vector
from mathutils.bvhtree import BVHTree
O=Path(__file__).resolve().parent;P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();assert sha(P)=='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';bpy.ops.wm.open_mainfile(filepath=str(P));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();hair=bpy.data.objects['Ellie ready Daisy CC-BY hair'];head=bpy.data.objects['Ellie ready head'];world=hair.matrix_world.copy();inv=world.inverted();bvh=BVHTree.FromPolygons([head.matrix_world@v.co for v in head.data.vertices],[tuple(f.vertices)for f in head.data.polygons],all_triangles=False)
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
field=[]
for v in hair.data.vertices:
 before=world@v.co;p=before.copy();crown=smooth(1.485,1.565,p.z)
 if crown:
  q,n,idx,d=bvh.find_nearest(p)
  if q is not None:p=p.lerp(q-n*.004,crown)
 # One fixed rest displacement moves side locks rearward, opening profile; no per-pose fit.
 face=smooth(.10,.22,abs(before.x))*(1-smooth(-.16,-.045,before.y))*(1-smooth(1.40,1.50,before.z));p.y+=.065*face
 v.co=inv@p
 if (p-before).length>1e-8:field.append({'vertexIndex':v.index,'beforeWorldRest':list(before),'afterWorldRest':list(p),'deltaWorldRest':list(p-before),'crownWeight':crown,'faceClearanceWeight':face})
with gzip.open(O/'vertex-field.json.gz','wt')as z:json.dump(field,z)
rig.data.pose_position='POSE';rest=Vector((0,-.050602056086063385,0));sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=128
for name,yaw,action in [('e-walk00',math.pi/2,'Walk_ProportionProposal'),('front-neutral',0,'Idle_Neutral_ProportionProposal'),('threequarter-neutral',math.pi/4,'Idle_Neutral_ProportionProposal')]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-rest);rig.animation_data.action=bpy.data.actions[action];sc.frame_set(0);bpy.context.view_layer.update();sc.render.filepath=str(O/(name+'.png'));print('RENDER',name,flush=True);bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-native-hair-restfit.blend'),compress=True);(O/'restfit-contract.json').write_text(json.dumps({'sourceSHA256':sha(P),'outputSHA256':sha(O/'ruta-native-hair-restfit.blend'),'hairObject':hair.name,'changedVertices':len(field),'totalVertices':len(hair.data.vertices),'maximumRestDisplacementM':max(Vector(f['deltaWorldRest']).length for f in field),'crown':'smoothstep z1.485→1.565 projects roots4mm below actual head nearest surface; source head untouched','face':'hair side absX .10→.22, frontY -.16→-.045 and belowZ1.40→1.50: fixed rearward65mm max','shaderChanged':False,'scope':'one geometry-only hair rest-fit pilot, not accepted likeness/loop','protectedHeadNeck':'all non-Daisy vertices immutable'},indent=2));print('RESTFIT_DONE',flush=True)
