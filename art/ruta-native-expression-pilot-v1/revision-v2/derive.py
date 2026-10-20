from pathlib import Path
import bpy,numpy as np,json,re,hashlib
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;R=O.parents[2];C=O/'cache';C.mkdir(exist_ok=True);SOURCE=R/'art/ruta-ellie-head-v1/source/ellie-original.blend';TARGET=R/'art/ruta-native-hair-volume-study-v1/alpha-aware/cache/alpha-volume-baked.blend';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(TARGET)=='09acadc1f01d1abb940723c80b8fdbd357553aa9cf8be09f7e7d225ea4b1715d';assert sha(SOURCE)=='3dd235218725a9e68890073bbeacb4820f9b34db65d44f80c31bb88696a3c54c';bpy.ops.wm.open_mainfile(filepath=str(SOURCE),use_scripts=False);sc=bpy.context.scene;sc.frame_set(1);rig=bpy.data.objects['RIG-Ellie'];names=['head','eye.L','eye.R','eye_highlights','eyebrows','eyelashes','face_line1','face_line2','teeth_top','teeth_btm','tongue']
allowedChannels=[]
def setpose(name,weight=1,brow_only=False):
 a=bpy.data.actions[name]
 for l in a.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for f in bag.fcurves:
     if brow_only and not re.match(r'pose\.bones\["[^"]*Eyebrow[^"]*"\]\.(location|rotation_euler|scale)$',f.data_path):continue
     if brow_only:allowedChannels.append({'path':f.data_path,'index':f.array_index,'weight':weight,'asset':name})
     value=f.evaluate(a.frame_range[0]);dest=rig.path_resolve(f.data_path)
     if hasattr(dest,'__setitem__'):dest[f.array_index]=dest[f.array_index]*(1-weight)+weight*value
     else:
      m=re.match(r'(.+)\["([^"]+)"\]$',f.data_path)
      if m:owner=rig.path_resolve(m.group(1));owner[m.group(2)]=owner[m.group(2)]*(1-weight)+weight*value
      else:owner,attr=f.data_path.rsplit('.',1);obj=rig.path_resolve(owner);setattr(obj,attr,getattr(obj,attr)*(1-weight)+weight*value)
 bpy.context.view_layer.update()
for n in names:
 o=bpy.data.objects['GEO-ellie_'+n]
 if o.animation_data:
  for d in o.animation_data.drivers:
   if 'levels'in d.data_path:d.mute=True
 for m in o.modifiers:
  if m.type=='SUBSURF':m.show_viewport=True;m.levels=max(1,min(2,m.render_levels))
def snapshot():
 bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();out={}
 for n in names:
  o=bpy.data.objects['GEO-ellie_'+n];ev=o.evaluated_get(dg);me=ev.to_mesh();out[n]=np.array([list(ev.matrix_world@v.co)for v in me.vertices]);ev.to_mesh_clear()
 return out
for pose in ['face_default','eyemask_content','mouth_smileclosed2']:setpose(pose)
baseline=snapshot();setpose('eyemask_relaxed',.65,brow_only=True);setpose('mouth_smileopen',.35);candidate=snapshot();np.savez(C/'native-expression-delta.npz',**{n:candidate[n]-baseline[n]for n in names});np.savez(C/'native-baseline.npz',**baseline)
# Match explicit historical fixed head-fit and current fixed pitch, not new bbox-fitting.
fit=json.load(open(R/'art/ruta-ellie-head-v1/friendly-pilot/pilot-manifest.json'))['uniformHeadFit'];scale=fit['scale'];offset=np.array(fit['offset']);rot=np.array(Matrix.Rotation(np.deg2rad(-20),3,'X'));pivot=np.array([-.0002406428,-.0249527972,1.256375432])
def transform(p):
 p=p*scale+offset;t=np.clip((p[:,2]-1.18)/.07,0,1);w=t*t*(3-2*t);return p+w[:,None]*((p-pivot)@rot.T+pivot-p)
bpy.ops.wm.open_mainfile(filepath=str(TARGET),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];rows=[];deltas={}
for n in names:
 o=bpy.data.objects['Ellie ready '+n];current=np.array([list(v.co)for v in o.data.vertices]);expected=transform(baseline[n]);assert current.shape==expected.shape;res=np.linalg.norm(current-expected,axis=1);delta=transform(candidate[n])-expected;delta[current[:,2]<=1.18]=0;rows.append({'part':n,'vertices':len(current),'explicitBaselineMappingMaxErrorMeters':float(res.max()),'expressionChangedVertices':int((np.linalg.norm(delta,axis=1)>1e-8).sum()),'expressionDeltaMaxMeters':float(np.linalg.norm(delta,axis=1).max())});deltas[n]=delta
# Fail closed before applying if baseline mapping is not validated.
(O/'derivation.json').write_text(json.dumps({'sourceOriginalSha256':sha(SOURCE),'parentSha256':sha(TARGET),'nativePoseRecipe':['face_default','eyemask_content','mouth_smileclosed2','blend65%eyemask_relaxed ONLY Eyebrow bonechannels','blend35%mouth_smileopen'],'parts':rows,'nativeBrowChannelAllowlist':allowedChannels,'mapping':'historicaluniformHeadFit thenexistingup20RESTneckfield; no newheadscalefit'},indent=2)+'\n');assert max(r['explicitBaselineMappingMaxErrorMeters']for r in rows)<2e-5,'Baseline mapping mismatch; no target edits applied'
assert max(float(np.linalg.norm(deltas[n],axis=1).max())for n in ['eye.L','eye.R','eye_highlights','eyelashes'])<1e-7,'Brow controls indirectly moved lash/eye geometry; do not render'
for n,delta in deltas.items():
 o=bpy.data.objects['Ellie ready '+n]
 for v,d in zip(o.data.vertices,delta):v.co+=Vector(d)
 o.data.update()
bpy.ops.wm.save_as_mainfile(filepath=str(C/'ruta-expression-trial.blend'),compress=True);assert sha(TARGET)=='09acadc1f01d1abb940723c80b8fdbd357553aa9cf8be09f7e7d225ea4b1715d';print('DERIVATIVE_SAVED_NO_RENDER',flush=True)
