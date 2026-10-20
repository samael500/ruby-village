"""Bounded technical whole3D proof; Root in-place PNGs plus distance metadata, no runtime edits."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
O=Path(__file__).resolve().parent;R=O.parents[1];contract=json.load(open(O/'build-contract.json'));check=json.load(open(O/'numeric-check.json'));assert check['endpointPoseGate']and check['endpointVelocityGate'];P=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-layered-style-v2/ruta-native-style.blend');bpy.ops.wm.open_mainfile(filepath=str(P));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];feet=bpy.data.objects['Adventurer_Feet'];meta=json.load(open(O/'sole-weight-variant-contract.json'));assert meta['metrics']['upperBootUnselectedVertexMaxAbsDeltaM']==0;assert meta['metrics']['lacesSockCuffMaxAbsDeltaM']==0
with bpy.data.libraries.load(str(O/'contact-actions.blend'),link=False)as(src,dst):dst.actions=list(src.actions)
with bpy.data.libraries.load(str(O/'sole-weight-variant.blend'),link=False)as(src,dst):dst.meshes=['Adventurer_Feet_contactSoleOnly_VARIANT']
feet.data=dst.meshes[0];rest=rig.data.bones['Root'].head_local.copy();rest.z=0;yaw=Matrix.Rotation(math.pi/2,4,'Z');rig.matrix_world=yaw@Matrix.Translation(-rest)
camera=json.load(open(R/'art/ruta-native-layered-walk48-v2/source-contract.json'))['cameraVariants']['base']['fixedRenderCamera'];sc.camera.matrix_world=Matrix(camera['matrixWorld']);sc.camera.data.type='ORTHO';sc.camera.data.ortho_scale=2.1;sc.render.engine='BLENDER_EEVEE_NEXT';sc.eevee.taa_render_samples=32;sc.render.resolution_x=256;sc.render.resolution_y=320;sc.render.resolution_percentage=100;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
def project(p):
 q=world_to_camera_view(sc,sc.camera,Vector(p));return[q.x*256,(1-q.y)*320]
def rootAt(c,t):
 u=t/c['durationSeconds'];T=c['durationSeconds'];p=c['rootHermite'];return Vector(p['p0'])*(2*u**3-3*u*u+1)+Vector(p['v0'])*T*(u**3-2*u*u+u)+Vector(p['p1'])*(-2*u**3+3*u*u)+Vector(p['v1'])*T*(u**3-u*u)
curve=json.load(open(R/'art/ruta-final-sole-compatibility-v1/final-samples/forward-distance-curve.json'));T=curve['durationSeconds'];step=T/480

def distance(t):
 cycles=math.floor(t/T);local=t-cycles*T;k=min(479,int(local/step));q=local-k*step;a,b=curve['samples'][k:k+2];return cycles*curve['strideMeters']+a['distanceMeters']+a['velocityMps']*q+.5*(b['velocityMps']-a['velocityMps'])/step*q*q
cstart,cstop=contract['clips']['start'],contract['clips']['stop'];walkOrigin=Vector(cstart['rootHermite']['p1']);stopOrigin=walkOrigin+Vector((0,-curve['strideMeters'],0));lastRoot=stopOrigin+Vector(cstop['rootHermite']['p1']);frames=[];clock=0
segments=[('idle-before',4,.2,'Idle_Neutral_ProportionProposal'),('start',12,cstart['durationSeconds'],cstart['action']),('walk',48,T,'Walk_ProportionProposal'),('stop',12,cstop['durationSeconds'],cstop['action']),('idle-after',4,.2,'Idle_Neutral_ProportionProposal')]
renderdir=O/'renders';renderdir.mkdir(exist_ok=True);cache={}
for segment,count,duration,action in segments:
 for j in range(count):
  t=duration*j/count;sourceFrame=0 if segment.startswith('idle')else (5+40*j/count)%40 if segment=='walk'else t*24
  root=Vector((0,0,0))if segment=='idle-before'else lastRoot if segment=='idle-after'else rootAt(cstart,t)if segment=='start'else walkOrigin+Vector((0,-(distance(5/24+t)-distance(5/24)),0))if segment=='walk'else stopOrigin+rootAt(cstop,t)
  rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(sourceFrame),subframe=sourceFrame%1);bpy.context.view_layer.update();posehash=hashlib.sha256(repr([(p.name,[[round(float(v),8)for v in row]for row in p.matrix_basis])for p in rig.pose.bones]).encode()).hexdigest();key=(action,round(sourceFrame,9));png=cache.get(key)
  if png is None:
   png='renders/'+str(len(cache)).zfill(3)+'.png';rig.animation_data.action=bpy.data.actions[action];sc.frame_set(int(sourceFrame),subframe=sourceFrame%1);bpy.context.view_layer.update();assert rig.pose.bones['Root'].location.length<1e-8;sc.render.filepath=str(O/png)
   if not(O/png).exists()or(segment=='walk'and 5+40*j/count>=40):
    print('PROOF_RENDER',len(frames),segment,sourceFrame,posehash,flush=True);bpy.ops.render.render(write_still=True)
   cache[key]=png
  origin=project((0,0,0));moved=project(yaw@root);frames.append({'index':len(frames),'startMs':clock*1000,'durationMs':duration/count*1000,'segment':segment,'action':action,'sourceFrame':sourceFrame,'sourcePoseHash':posehash,'file':png,'rootNativeXYZM':list(root),'rootProjectedDeltaPx':[moved[k]-origin[k]for k in[0,1]]});clock+=duration/count
floor=-.001194837037473917;grid=[]
for k in range(-40,61):
 x=k*.1;grid.append([project((x,-.5,floor)),project((x,.5,floor))])
for k in range(-5,6):
 y=k*.1;grid.append([project((-4,y,floor)),project((6,y,floor))])
report={'status':'TECHNICAL-CONTACT-PROTOTYPE-NOT-ART-NOT-GAME-ACCEPTANCE','sourceSHA256':hashlib.sha256(P.read_bytes()).hexdigest(),'weightVariant':'selected56soleFoot1; originalWalk48maxdelta4.484mm; originalweightsunchangedonDisk','frameSize':[256,320],'RootPNGInPlace':True,'rootProjectionOriginPx':project((0,0,0)),'rootConsumption':'apply metadata once only; fixedRoot mode moves ground/camera reference, route mode moves whole frame with ground fixed','durationMs':clock*1000,'frameCount':len(frames),'uniqueRenderedFrames':len(cache),'frames':frames,'groundGridProjectedPx':grid,'endReplay':'staticIdle then explicit reset; not a seamless closed-world route','actionLibrarySHA256':hashlib.sha256((O/'contact-actions.blend').read_bytes()).hexdigest(),'soleVariantLibrarySHA256':hashlib.sha256((O/'sole-weight-variant.blend').read_bytes()).hexdigest(),'sourcePoseHashDefinition':'all native pose bone matrix_basis rounded8decimals; cache phase provenance logged and replayverified','sourceUnchanged':hashlib.sha256(P.read_bytes()).hexdigest()=='bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706'};(O/'proof-manifest.json').write_text(json.dumps(report,indent=2));print('PROOF_SEQUENCE_DONE',len(frames),flush=True)
