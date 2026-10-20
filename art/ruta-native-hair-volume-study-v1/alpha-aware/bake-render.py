from pathlib import Path
import bpy,numpy as np,json,time,math,hashlib
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
O=Path(__file__).resolve().parent;C=O/'cache';bpy.ops.wm.open_mainfile(filepath=str(C/'alpha-volume-geometry.blend'));sc=bpy.context.scene;obj=bpy.data.objects['Daisy alpha-aware volume candidate'];rig=bpy.data.objects['CharacterArmature'];saved=rig.matrix_world.copy();rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();data=np.load(C/'source-correspondence.npz');tri=data['triangles'];uv=data['uv'];points=[Vector(x)for x in tri.reshape(-1,3)];bvh=BVHTree.FromPolygons(points,[(3*i,3*i+1,3*i+2)for i in range(len(tri))],all_triangles=True);coords=np.array([list(v.co)for v in obj.data.vertices]);outuv=[];dist=[];start=time.monotonic()
for p in coords:
 hit,normal,index,d=bvh.find_nearest(Vector(p));t=tri[index];v0=t[1]-t[0];v1=t[2]-t[0];v2=np.array(hit)-t[0];d00=v0@v0;d01=v0@v1;d11=v1@v1;den=d00*d11-d01*d01
 if abs(den)<1e-20:w=np.array([1,0,0])
 else:
  b=(d11*(v2@v0)-d01*(v2@v1))/den;c=(d00*(v2@v1)-d01*(v2@v0))/den;w=np.array([1-b-c,b,c])
 outuv.append(w@uv[index]);dist.append(d)
layer=obj.data.uv_layers.new(name='NativeSourceUV')
for l in obj.data.loops:layer.data[l.index].uv=outuv[l.vertex_index]
# Separate target UV; source sampling remains explicit NativeSourceUV.
layer2=obj.data.uv_layers.new(name='VolumeBakeUV');obj.data.uv_layers.active=layer2;layer2.active_render=True
for o in bpy.context.selected_objects:o.select_set(False)
obj.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=.003);bpy.ops.object.mode_set(mode='OBJECT');print('UV_READY',time.monotonic()-start,flush=True)
mat=bpy.data.materials.new('Alpha volume fixed native RGB bake');mat.use_nodes=True;t=mat.node_tree;t.nodes.clear();sourceuv=t.nodes.new('ShaderNodeUVMap');sourceuv.uv_map='NativeSourceUV';tex=t.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images['painted-daisy-rgb-v1.png'];emit=t.nodes.new('ShaderNodeEmission');out=t.nodes.new('ShaderNodeOutputMaterial');t.links.new(sourceuv.outputs['UV'],tex.inputs['Vector']);t.links.new(tex.outputs['Color'],emit.inputs['Color']);t.links.new(emit.outputs[0],out.inputs['Surface']);target=bpy.data.images.new('Fixed native 3D volume RGB bake',width=2048,height=2048,alpha=False);node=t.nodes.new('ShaderNodeTexImage');node.image=target;node.select=True;t.nodes.active=node;obj.data.materials.clear();obj.data.materials.append(mat);sc.render.engine='CYCLES';sc.cycles.samples=1;sc.render.bake.margin=8;bpy.ops.object.bake(type='EMIT');target.filepath_raw=str(O/'fixed-native-rgb-bake.png');target.file_format='PNG';target.save();target.pack();print('BAKE_READY',flush=True)
# Final hair uses bakedRGB and matte native Diffuse, no alpha cards.
t.links.remove(out.inputs['Surface'].links[0]);diff=t.nodes.new('ShaderNodeBsdfDiffuse');diff.inputs['Roughness'].default_value=.8;uvnode=t.nodes.new('ShaderNodeUVMap');uvnode.uv_map='VolumeBakeUV';t.links.new(uvnode.outputs[0],node.inputs['Vector']);t.links.new(node.outputs['Color'],diff.inputs['Color']);t.links.new(diff.outputs[0],out.inputs['Surface']);sc.render.engine='BLENDER_EEVEE_NEXT';rig.data.pose_position='POSE';rig.matrix_world=saved;sc.frame_set(0);bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(C/'alpha-volume-baked.blend'),compress=True);rest=Vector((0,-.050602056086063385,0))
for view,yaw,action in [('e',math.pi/2,'Walk_ProportionProposal'),('front',0,'Idle_Neutral_ProportionProposal'),('threequarter',-math.pi/4,'Idle_Neutral_ProportionProposal')]:
 rig.animation_data.action=bpy.data.actions[action];rig.animation_data.action_slot=rig.animation_data.action.slots[0];rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-rest);sc.frame_set(0);bpy.context.view_layer.update();sc.render.filepath=str(O/(view+'.png'));bpy.ops.render.render(write_still=True)
r={'closestSourceTransfer':'nearest original native3Dtriangle→barycentric originalUV; explicit sourceUV→fixed paintedRGB; one native CyclesEMIT bake to newVolumeBakeUV2048²','vertexSourceDistanceMeters':{'min':min(dist),'median':float(np.median(dist)),'p95':float(np.percentile(dist,95)),'max':max(dist)},'bakeSHA256':hashlib.sha256((O/'fixed-native-rgb-bake.png').read_bytes()).hexdigest(),'noPerFrameBakes':True,'sourceImageUnmodified':True,'seconds':time.monotonic()-start};(O/'bake-contract.json').write_text(json.dumps(r,indent=2)+'\n')
