import bpy, math,json,hashlib
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parent;src=P/'sources/victoria.blend';before=hashlib.sha256(src.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(src));copies=[]
for name in ['GEO-victoria_hair_main','GEO-victoria_hair_bangs']:
 o=bpy.data.objects[name];n=bpy.data.objects.new(name+'_RAW_REST',o.data.copy());n.matrix_world=o.matrix_world.copy();copies.append(n)
bpy.data.libraries.write(str(P/'victoria-hair-only-raw-rest.blend'),set(copies))
sc=bpy.data.scenes.new('HairOnlyRawRest');bpy.context.window.scene=sc
for o in copies:sc.collection.objects.link(o);o.data.materials.clear()
sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='STUDIO';sc.display.shading.color_type='SINGLE';sc.display.shading.single_color=(.42,.25,.12);sc.display.shading.show_shadows=True;sc.display.shading.show_cavity=True;sc.world=bpy.data.worlds.new('Neutral');sc.render.resolution_x=600;sc.render.resolution_y=600;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
corners=[o.matrix_world@v.co for o in copies for v in o.data.vertices];lo=Vector(tuple(min(v[i]for v in corners)for i in range(3)));hi=Vector(tuple(max(v[i]for v in corners)for i in range(3)));center=(lo+hi)/2;camdata=bpy.data.cameras.new('InspectionCamera');cam=bpy.data.objects.new('InspectionCamera',camdata);sc.collection.objects.link(cam);sc.camera=cam;camdata.type='ORTHO';camdata.ortho_scale=max(hi-lo)*1.25
for label,direction in [('front',(0,-1,0)),('side',(1,0,0)),('back',(0,1,0)),('threequarter',(1,-1,.15))]:
 cam.location=center+Vector(direction).normalized()*3;cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(P/f'actual-hair-rest-{label}.png');bpy.ops.render.render(write_still=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()==before
(P/'source-hash.json').write_text(json.dumps({'officialBlendSha256':before,'sourceUnchanged':True,'views':'actual raw rest mesh main+bangs, original object matrices, no rig, modifiers/particles omitted, uniform camera, neutral clay; not final shaded hairstyle'},indent=2)+'\n')
