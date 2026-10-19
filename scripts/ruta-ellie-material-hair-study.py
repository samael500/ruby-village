"""Read-only native hair island inventory and minimal native material adaptation on saved head pilot."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Matrix
R=Path(__file__).resolve().parents[1];H=R/'art/ruta-ellie-head-v1';O=H/'material-adaptation';O.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(H/'source/ellie-original.blend'),use_scripts=False);rows=[]
for name in ['GEO-ellie_hair','GEO-ellie_hair_cut','GEO-ellie_hair.groom_base']:
 o=bpy.data.objects[name];mesh=o.data;parent=list(range(len(mesh.vertices)))
 def find(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for e in mesh.edges:
  a,b=map(find,e.vertices)
  if a!=b:parent[b]=a
 groups={}
 for v in mesh.vertices:groups.setdefault(find(v.index),[]).append(v.index)
 parts=[]
 for ids in sorted(groups.values(),key=len,reverse=True):
  pts=[o.matrix_world@mesh.vertices[i].co for i in ids];parts.append({'vertices':len(ids),'vertexIndices':ids,'worldBBox':[[min(v[j]for v in pts),max(v[j]for v in pts)]for j in range(3)],'worldCentroid':[sum(v[j]for v in pts)/len(pts)for j in range(3)]})
 rows.append({'object':name,'sourceVertices':len(mesh.vertices),'sourcePolygons':len(mesh.polygons),'edgeConnectedIslandCount':len(parts),'parts':parts,'sourceModifiers':[m.type for m in o.modifiers]})
(O/'native-hair-components.json').write_text(json.dumps({'status':'native-source-inventory-no-new-hair-created','sourceSha256':hashlib.sha256((H/'source/ellie-original.blend').read_bytes()).hexdigest(),'componentDefinition':'topological edge connected original mesh islands; seam duplicates not welded; indices source base mesh','objects':rows},indent=2)+'\n')
print('HAIR_COMPONENTS',[(r['object'],r['edgeConnectedIslandCount'],[p['vertices']for p in r['parts'][:12]])for r in rows],flush=True)
bpy.ops.wm.open_mainfile(filepath=str(H/'friendly-pilot/ruta-b-ellie-head-pilot.blend'),use_scripts=False);sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature']
def geo():return hashlib.sha256(repr([(o.name,[(tuple(v.co),[(g.group,g.weight)for g in v.groups])for v in o.data.vertices])for o in sc.objects if o.type=='MESH']).encode()).hexdigest()
def ah():return hashlib.sha256(repr([(a.name,[(f.data_path,f.array_index,[(tuple(k.co),k.interpolation)for k in f.keyframe_points])for l in a.layers for s in l.strips for b in s.channelbags for f in b.fcurves])for a in bpy.data.actions]).encode()).hexdigest()
gh=geo();actionhash=ah();edits=[]
# Only colored native iris ramp stops change. Existing exact black stop and white-eye material stay intact.
m=bpy.data.materials['ellie.eyes_pupils'];ramp=m.node_tree.nodes['ColorRamp.004'].color_ramp;old=[(e.position,list(e.color))for e in ramp.elements];assert len(ramp.elements)==3 and max(ramp.elements[0].color[:3])==0
ramp.elements[1].color=(.005,.065,.22,1);ramp.elements[2].color=(.025,.32,.68,1);edits.append({'material':m.name,'node':'ColorRamp.004','before':old,'after':[(e.position,list(e.color))for e in ramp.elements],'mask':'native UV/depth-driven iris ramp, black pupil stop and all positions preserved; ellie.eyes white material unchanged'})
# Reuse native author palette outputs Earth/Orange through existing strand shader/color mix.
m=bpy.data.materials['ellie.hair_mesh'];nt=m.node_tree;palette=nt.nodes['Group.010'];target_socket=next(l.to_socket for l in nt.links if l.from_node==palette and l.from_socket.name=='Black' and l.to_node.name=='Mix.010');mix=nt.nodes.new('ShaderNodeMixRGB');mix.name='Ruta copper native palette';mix.blend_type='MIX';mix.inputs[0].default_value=.45;nt.links.new(palette.outputs['Earth'],mix.inputs[1]);nt.links.new(palette.outputs['Orange'],mix.inputs[2]);nt.links.new(mix.outputs[0],target_socket);edits.append({'material':m.name,'nativePalette':'45% Orange/55% Earth replaces Black input to original Mix.010; original strand masks/BSDF preserved'})
m=bpy.data.materials['ellie.eyebrows'];bs=m.node_tree.nodes['Principled BSDF'];before=list(bs.inputs['Base Color'].default_value);bs.inputs['Base Color'].default_value=(.12,.035,.009,1);edits.append({'material':m.name,'before':before,'after':list(bs.inputs['Base Color'].default_value),'field':'native unlinked Principled Base Color; lashes unchanged'})
assert gh==geo() and actionhash==ah();root=rig.data.bones['Root'].head_local.copy();root.z=0;wholecam=sc.camera;facecam=bpy.data.objects['Ellie native face proof camera'];views=[]
for name,yaw in [('front',0),('three-quarter',math.pi/4)]:
 rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-root);bpy.context.view_layer.update();sc.camera=facecam;sc.render.filepath=str(O/(name+'-face-color.png'));print('RENDER_COLOR',name,flush=True);bpy.ops.render.render(write_still=True);views.append(name+'-face-color.png')
sc.camera=wholecam;rig.matrix_world=Matrix.Translation(-root);bpy.ops.wm.save_as_mainfile(filepath=str(O/'ruta-b-ellie-native-color.blend'),compress=True);(O/'material-proposal.json').write_text(json.dumps({'status':'internal-color-study-not-approved-Ruta-hair','geometryWeightsAndActionsUnchanged':True,'geometryWeightsSha256':gh,'allActionCurvesSha256':actionhash,'edits':edits,'views':views,'limitations':['existing native short haircut remains short; no claimed waves','blue iris relies on original iris material mask, white and black stops not recolored','no new sculpt, face decals, primitive hair or imagegen','no gait/contact/no-slip claim']},indent=2)+'\n');print('NATIVE_COLOR_STUDY_READY',flush=True)
