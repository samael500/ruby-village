from pathlib import Path
import bpy,numpy as np,json,math,hashlib
from mathutils import Matrix,Vector
O=Path(__file__).resolve().parent;S=Path('/home/mskorokhod/life/ruby-village-36-ruta-render-style/art/ruta-native-painted-combined-v1/ruta-native-painted-combined.blend');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(S)=='b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7';bpy.ops.wm.open_mainfile(filepath=str(S));sc=bpy.context.scene;rig=bpy.data.objects['CharacterArmature'];saved=rig.matrix_world.copy();rig.matrix_world=Matrix.Identity(4);rig.data.pose_position='REST';bpy.context.view_layer.update();hair=bpy.data.objects['Ellie ready Daisy CC-BY hair'];original=np.array([list(hair.matrix_world@v.co)for v in hair.data.vertices]);cx,cy,cz=-.0095,.033,1.47;rx,ry,rz=.224,.180,.151
# Continuous capped crown, flow undulation vanishes at pole and rim; part notch fixed in rest3D.
verts=[];faces=[];N=96;M=32
for j in range(M+1):
 theta=(math.pi/2)*j/M
 for i in range(N):
  phi=2*math.pi*i/N;flow=.0038*math.sin(7*phi+theta*1.7)*math.sin(theta)**2*math.cos(theta);part=-.003*math.exp(-(math.sin(phi-.48)/.12)**2)*math.sin(theta)*math.cos(theta);verts.append((cx+(rx+flow)*math.sin(theta)*math.cos(phi),cy+(ry+flow)*math.sin(theta)*math.sin(phi),cz+rz*math.cos(theta)+part))
for j in range(M):
 for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
faces.append(tuple(reversed([M*N+i for i in range(N)])));mesh=bpy.data.meshes.new('Continuous crown organic rest topology');mesh.from_pydata(verts,[],faces);mesh.update();cap=bpy.data.objects.new('Ruta continuous crown proposal',mesh);sc.collection.objects.link(cap)
for p in mesh.polygons:p.use_smooth=True
mat=bpy.data.materials.new('Crown matte copper native diagnostic');mat.use_nodes=True;t=mat.node_tree;t.nodes.clear();d=t.nodes.new('ShaderNodeBsdfDiffuse');d.inputs['Color'].default_value=(.32,.095,.035,1);d.inputs['Roughness'].default_value=.8;out=t.nodes.new('ShaderNodeOutputMaterial');t.links.new(d.outputs[0],out.inputs['Surface']);mesh.materials.append(mat);group=cap.vertex_groups.new(name='Head');group.add(list(range(len(verts))),1,'REPLACE');cap.parent=rig;mod=cap.modifiers.new('Native Head attachment','ARMATURE');mod.object=rig
# Tuck upper card roots below the continuous crown; unchanged lower waves.
q=original.copy()
for i,p in enumerate(original):
 r2=((p[0]-cx)/rx)**2+((p[1]-cy)/ry)**2
 if p[2]>1.50 and r2<.98:
  top=cz+rz*math.sqrt(1-r2)-.006;w=min(1,max(0,(p[2]-1.50)/.045));w=w*w*(3-2*w);q[i,2]=p[2]+w*(min(p[2],top)-p[2])
inv=hair.matrix_world.inverted()
for v,p in zip(hair.data.vertices,q):v.co=inv@Vector(p)
hair.data.update();assert np.array_equal(q[original[:,2]<=1.50],original[original[:,2]<=1.50]);rig.data.pose_position='POSE';rig.matrix_world=saved;sc.frame_set(0);bpy.context.view_layer.update();output=O/'ruta-continuous-crown.blend';bpy.ops.wm.save_as_mainfile(filepath=str(output),compress=True);r={'sourceSha256':sha(S),'outputSha256':sha(output),'newCrownVertices':len(verts),'newCrownFaces':len(faces),'crownBounds':[np.min(verts,axis=0).tolist(),np.max(verts,axis=0).tolist()],'originalHairBounds':[original.min(0).tolist(),original.max(0).tolist()],'modifiedHairBounds':[q.min(0).tolist(),q.max(0).tolist()],'hairChangedVertexCount':int(np.any(q!=original,axis=1).sum()),'maxHairDisplacementMeters':float(np.linalg.norm(q-original,axis=1).max()),'protectedLowerWaveZ1p50VertexCount':int((original[:,2]<=1.50).sum()),'protectedLowerDelta':0,'headBodyCameraActionsUnchanged':True,'diagnosticOnlyNotFinalPaintedHair':True};rest=Vector((0,-.050602056086063385,0))
for view,yaw,action in [('e',math.pi/2,'Walk_ProportionProposal'),('front',0,'Idle_Neutral_ProportionProposal'),('threequarter',math.pi/4,'Idle_Neutral_ProportionProposal')]:
 rig.animation_data.action=bpy.data.actions[action];rig.animation_data.action_slot=rig.animation_data.action.slots[0];rig.matrix_world=Matrix.Rotation(yaw,4,'Z')@Matrix.Translation(-rest);sc.frame_set(0);bpy.context.view_layer.update();sc.render.filepath=str(O/(view+'.png'));bpy.ops.render.render(write_still=True)
assert sha(S)==r['sourceSha256'];(O/'contract.json').write_text(json.dumps(r,indent=2)+'\n')
