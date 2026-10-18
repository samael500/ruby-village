import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path('/tmp/ruby-qa-full-cycle');D=R/'art/characters-mpfb-v1/motion/full-cycle-technical';O=R/'docs/chapter-1-rc/qa/mpfb-full-5352e5c';m=json.loads((D/'manifest.json').read_text());src=(R/m['sourceBlend']).resolve();h=hashlib.sha256(src.read_bytes()).hexdigest();assert h==m['sourceSha256'];bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene
for n,a in m['sourceActionBundle'].items():bpy.data.objects[n].animation_data.action=bpy.data.actions[a]
r=bpy.data.objects['Ruta.MPFB.StandardRig'];c=s.camera;shoe=bpy.data.objects['Ruta.shoes01'];clone=shoe.copy();clone.data=shoe.data.copy();s.collection.objects.link(clone);clone.hide_render=True
for mod in shoe.modifiers:
 if mod.type=='SUBSURF':mod.levels=mod.render_levels
for mod in clone.modifiers:
 if mod.type=='SUBSURF':mod.show_viewport=False
s.frame_set(1);bpy.context.view_layer.update();p0=r.matrix_world.translation.copy();s.frame_set(25);bpy.context.view_layer.update();delta=r.matrix_world.translation-p0;rows=[]
def px(p):
 q=world_to_camera_view(s,c,p);return [q.x*384,(1-q.y)*384]
native=[]
receipt=json.loads((D/'base/e/receipt.json').read_text())
for frame in range(1,26):
 s.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();es=clone.evaluated_get(dg);boot=shoe.evaluated_get(dg);pose={}
 for side,foot in receipt['frames'][0]['feet'].items():
  pose[side]={}
  for kind,marker in foot['sourceSole'].items():
   pts=[es.matrix_world@es.data.vertices[i].co for i in marker['sourceVertexIndices']];pose[side][kind]=list(sum(pts,Vector())/len(pts))
 native.append(dict(frame=frame,feet=pose,root=list(r.matrix_world.translation),minBootZ=min((boot.matrix_world@v.co).z for v in boot.data.vertices)))
(O/'native25-contact.json').write_text(json.dumps(native,indent=2)+'\n');print('NATIVE25DONE')
