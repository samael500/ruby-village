"""Verify retained straight actions, rig rest/constraints and shoe weights unchanged."""
from pathlib import Path
import os
import bpy,json,hashlib,re,os
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('RUBY_MPFB_PIVOT_VARIANT','right60');assert VARIANT in ['right60','left120','right120'];OUT=ROOT/'art/characters-mpfb-v1/motion/pivot-variants'/VARIANT;meta=json.loads((OUT/'manifest.json').read_text());source=OUT/'mpfb-compact-pivot-technical.blend';baseline=ROOT/'art/characters-mpfb-v1/motion/transitions/mpfb-start-stop-technical.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
def sha(data):return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
def action(a):return sha([{'path':c.data_path,'index':c.array_index,'extrapolation':c.extrapolation,'keys':[(list(k.co),list(k.handle_left),list(k.handle_right),k.interpolation)for k in c.keyframe_points]}for c in a.fcurves])
def rig(o):
 attrs=['type','subtarget','pole_subtarget','target_space','owner_space','influence','chain_count','pole_angle','use_stretch','use_x','use_y','use_z','invert_x','invert_y','invert_z','mix_mode','use_offset','head_tail','iterations']
 return sha({'bones':[(b.name,b.parent.name if b.parent else None,[list(row)for row in b.matrix_local])for b in o.data.bones],'constraints':{b.name:[{k:getattr(c,k)for k in attrs if hasattr(c,k)}for c in b.constraints]for b in o.pose.bones},'rotationModes':{b.name:b.rotation_mode for b in o.pose.bones}})
def shoe(o):return sha({'vertices':[list(v.co)for v in o.data.vertices],'faces':[list(p.vertices)for p in o.data.polygons],'groups':[g.name for g in o.vertex_groups],'weights':[[(g.group,g.weight)for g in v.groups]for v in o.data.vertices]})
action_names=list(meta['sourceActions'].values())+[name for clip in meta['transitionClips'].values() for name in clip['actionBundle'].values()];object_names=['Ruta.MPFB.StandardRig','Ruta.shoes01'];current_actions={n:action(bpy.data.actions[n])for n in action_names};current_objects={object_names[0]:rig(bpy.data.objects[object_names[0]]),object_names[1]:shoe(bpy.data.objects[object_names[1]])}
with bpy.data.libraries.load(str(baseline),link=False)as(a,b):b.actions=list(action_names);b.objects=list(object_names)
old_actions={n:action(a)for n,a in zip(action_names,b.actions)};old_objects={object_names[0]:rig(b.objects[0]),object_names[1]:shoe(b.objects[1])};result={'method':'Fresh turn source, import independent immutable straight source data; compare action keys/handles, rig rest and native constraint settings, raw sole geometry/weights','sourceOriginalSha256':hashlib.sha256(baseline.read_bytes()).hexdigest(),'sourceTurnSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'retainedActionsUnchanged':current_actions==old_actions,'rigRestConstraintsAndShoeWeightsUnchanged':current_objects==old_objects,'currentActionHashes':current_actions,'baselineActionHashes':old_actions,'currentObjectHashes':current_objects,'baselineObjectHashes':old_objects};assert result['retainedActionsUnchanged']and result['rigRestConstraintsAndShoeWeightsUnchanged'];(OUT/'idle-transition-source-preservation.json').write_text(json.dumps(result,indent=2)+'\n');print('STRAIGHT_PRESERVATION_PASS actual compared source actions/rest/constraints/shoe weights')

# Full asymmetric mesh data/weights retained; this independently rules out a mirrored bag/body asset.
mesh_names=[o.name for o in bpy.context.scene.objects if o.type=='MESH']
current_mesh={n:shoe(bpy.data.objects[n]) for n in mesh_names}
with bpy.data.libraries.load(str(baseline),link=False) as (a,b):b.objects=list(mesh_names)
baseline_mesh={n:shoe(o) for n,o in zip(mesh_names,b.objects)}
result['allAsymmetricMeshGeometryWeightsUnchanged']=current_mesh==baseline_mesh
assert result['allAsymmetricMeshGeometryWeightsUnchanged']
if 'retainedValidatedLeft60Actions' in meta:
 donor=ROOT/'art/characters-mpfb-v1/motion/turn-study/mpfb-native60-turn-technical.blend'
 wanted=list(meta['retainedValidatedLeft60Actions'].values());retained={n:action(bpy.data.actions[n]) for n in wanted}
 with bpy.data.libraries.load(str(donor),link=False) as (a,b):b.actions=list(wanted)
 original={n:action(o) for n,o in zip(wanted,b.actions)}
 result['retainedValidatedLeft60ActionsUnchanged']=retained==original
 result['validatedLeft60DonorSha256']=hashlib.sha256(donor.read_bytes()).hexdigest()
 assert result['retainedValidatedLeft60ActionsUnchanged']
(OUT/'idle-transition-source-preservation.json').write_text(json.dumps(result,indent=2)+'\n')
print('ALL_ASYMMETRIC_MESH_AND_RETAINED_ACTION_PRESERVATION_PASS')

if 'retained60Actions' in meta:
 donor=ROOT/meta['sourceRepositoryPath'];wanted=list(meta['retained60Actions'].values());current={n:action(bpy.data.actions[n]) for n in wanted}
 with bpy.data.libraries.load(str(donor),link=False) as(a,b):b.actions=list(wanted)
 result['retained60ActionsUnchanged']=current=={n:action(o) for n,o in zip(wanted,b.actions)};assert result['retained60ActionsUnchanged'];(OUT/'idle-transition-source-preservation.json').write_text(json.dumps(result,indent=2)+'\n')
