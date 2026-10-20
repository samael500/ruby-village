"""One fixed REST donor fit, ready solid Victoria hair. No new sculpt/strands or per-frame transforms."""
from pathlib import Path
import bpy,json,math,hashlib
import numpy as np
from mathutils import Matrix
R=Path(__file__).resolve().parents[1];H=R/'art/ruta-ellie-head-v1';O=H/'victoria-hair-pilot';S=O/'source/victoria-hair-only-raw-rest.blend';bpy.ops.wm.open_mainfile(filepath=str(H/'color-handoff/ruta-b-ellie-blue-copper-temporary.blend'),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];head=bpy.data.objects['Ellie ready head'];pts=np.empty(len(head.data.vertices)*3,dtype=np.float32);head.data.vertices.foreach_get('co',pts);pts=pts.reshape((-1,3));target_center=pts[:,:2].mean(axis=0);target_center=(pts[:,:2].min(axis=0)+pts[:,:2].max(axis=0))/2;target_radii=(pts[:,:2].max(axis=0)-pts[:,:2].min(axis=0))/2;target_skull=float(pts[:,2].max());target_root=rig.data.bones['Head'].head_local.z;contract=json.loads((H/'source/body-b-corrected-contract.json').read_text());target_crown=contract['restMeshBoundsAfter']['body'][2][1]
source_center=np.array([0.,(-.1528951228+.1076538637)/2]);source_radii=np.array([.1288955212,(.1076538637+.1528951228)/2]);knots=[1.0475807189941406,1.1515930891036987,1.4233322143554688,1.6544991731643677];values=[.86,target_root,target_skull,target_crown];sec=[(values[i+1]-values[i])/(knots[i+1]-knots[i])for i in range(3)];slopes=[sec[0],2*sec[0]*sec[1]/(sec[0]+sec[1]),2*sec[1]*sec[2]/(sec[1]+sec[2]),sec[-1]]
def zfit(z):
 if z<=knots[0]:return values[0]+(z-knots[0])*slopes[0]
 if z>=knots[-1]:return values[-1]+(z-knots[-1])*slopes[-1]
 i=next(i for i in range(3)if z<=knots[i+1]);h=knots[i+1]-knots[i];u=(z-knots[i])/h
 return (2*u**3-3*u**2+1)*values[i]+(u**3-2*u**2+u)*h*slopes[i]+(-2*u**3+3*u**2)*values[i+1]+(u**3-u**2)*h*slopes[i+1]
for n in ['Ellie ready hair_cut','Ellie ready CC0 Cortu waves']:bpy.data.objects[n].hide_render=True
with bpy.data.libraries.load(str(S),link=False)as(src,dst):dst.objects=[n for n in src.objects if n.startswith(('GEO-victoria_hair_main','GEO-victoria_hair_bangs'))]
assert len(dst.objects)==2,'exactly2nativehairpartsrequired'
assert sorted(len(o.data.vertices)for o in dst.objects)==[2110,2699]
records=[]
for o in dst.objects:
 sc.collection.objects.link(o);o.name='Ellie ready Victoria '+('main'if 'hair_main'in o.name else'bangs');p=np.empty(len(o.data.vertices)*3,dtype=np.float32);o.data.vertices.foreach_get('co',p);p=p.reshape((-1,3));oldp=p.copy();q=(p[:,:2]-source_center)/source_radii;r=np.linalg.norm(q,axis=1);u=np.maximum(r-1,0);newr=np.where(r<=1,r,1+.4*u+.6*(1-np.exp(-4*u))/4);ratio=np.ones_like(r);np.divide(newr,r,out=ratio,where=r>1e-8);p[:,:2]=target_center+q*ratio[:,None]*target_radii;p[:,2]=[zfit(float(z))for z in p[:,2]];o.data.vertices.foreach_set('co',p.ravel());o.data.update()
 for poly in o.data.polygons:poly.use_smooth=True
 o.parent=rig;o.matrix_parent_inverse=Matrix.Identity(4);o.matrix_basis=Matrix.Identity(4);o.vertex_groups.clear();g=o.vertex_groups.new(name='Head');g.add(list(range(len(o.data.vertices))),1.,'REPLACE');m=o.modifiers.new('Rigid native Head binding','ARMATURE');m.object=rig;sub=o.modifiers.new('Native donor surface subdivision','SUBSURF');sub.levels=1;sub.render_levels=1;o.hide_render=False
 materialnames=[]
 for mat in o.data.materials:
  if not mat or not mat.use_nodes:continue
  for n in mat.node_tree.nodes:
   if n.type=='BSDF_PRINCIPLED':
    sock=n.inputs['Base Color']
    for l in list(sock.links):mat.node_tree.links.remove(l)
    sock.default_value=(.27,.075,.018,1);n.inputs['Roughness'].default_value=.8
  materialnames.append(mat.name)
 records.append({'name':o.name,'baseVertices':len(o.data.vertices),'baseFaces':len(o.data.polygons),'sourceGeometrySha256':hashlib.sha256(oldp.tobytes()).hexdigest(),'fittedGeometrySha256':hashlib.sha256(p.tobytes()).hexdigest(),'fittedRestBBox':{'min':p.min(axis=0).tolist(),'max':p.max(axis=0).tolist()},'UVLayers':len(o.data.uv_layers),'materials':materialnames,'binding':'Head1 with native Armature; Subdivision1 smooth surface'})
print('VICTORIA_ONE_RESTFIT',records,flush=True);root=rig.data.bones['Root'].head_local.copy();root.z=0;whole=sc.camera;face=bpy.data.objects['Ellie native face proof camera'];views=[]
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root);bpy.context.view_layer.update()
 for kind,cam in [('whole',whole),('face',face)]:
  sc.camera=cam;sc.render.filepath=str(O/(name+'-'+kind+'.png'));print('VICTORIA_RENDER',name,kind,flush=True);bpy.ops.render.render(write_still=True);views.append(name+'-'+kind+'.png')
sc.camera=whole;rig.matrix_world=Matrix.Translation(-root);bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-b-ellie-victoria-hair-one-fit.blend'),compress=True)
def ah(a):return hashlib.sha256(repr([(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves]).encode()).hexdigest()
report={'status':'ONE-native-solid-donor-restfit-candidate-independent-art-review-pending-NOT-final-Ruta','sourceLibrary':str(S.relative_to(R)),'sourceSha256':hashlib.sha256(S.read_bytes()).hexdigest(),'sourceLicense':'Victoria/SpriteFright Blender Studio/Blender Foundation CC-BY4.0; extraction+restfit+recolor+subdivision modifications','restFit':{'definition':'single fixed global rest cage: matched inner head elliptical radii, softly compressed outer bouffant radial mass; monotone cubic height profile compresses crown and lengthens existing lower locks. No strand creation or per-frame change.','sourceHeadCenterXY':source_center.tolist(),'sourceHeadRadiiXY':source_radii.tolist(),'targetHeadCenterXY':target_center.tolist(),'targetHeadRadiiXY':target_radii.tolist(),'sourceHeadBoundsLimitation':'source raw skin points above authored Head-bone height, not exact scalp surface/opening measurements','radialFormula':'r<=1 ->r; r>1 ->1+.4u+.6*(1-exp(-4u))/4,u=r-1','zKnotsSource':knots,'zKnotsTarget':values,'zHermiteSlopes':slopes},'parts':records,'views':views,'actions':{n:ah(bpy.data.actions[n])for n in ['Walk_ProportionProposal','Idle_Neutral_ProportionProposal']},'materialProtection':'all visible head/hair ASCII prefix Ellie ready ; preserve shaders/normals/UV/alpha; honor hidden rejected donor objects','limitations':['1980s bouffant donor is not a ready Ruta hairstyle; shape must be judged from actual two views','rest lower locks are lengthened significantly; may read as broad lobes instead of natural waves','head/face/body/gait curves unchanged; no walking/contact/no-slip approval','donor originally has0UVlayers, not lost UV; materials/face assignments retained with native color changed']};(O/'manifest.json').write_text(json.dumps(report,indent=2)+'\n');print('VICTORIA_ONE_FIT_READY',flush=True)
