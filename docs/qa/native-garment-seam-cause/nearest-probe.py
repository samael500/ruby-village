exec(compile((__import__('pathlib').Path(__file__).parent/'albedo-probe.py').read_text().split("for mode in ['original-albedo'")[0],__file__,'exec'))
sc=setup(sources['original'])
for m in bpy.data.materials:
 if m.name.startswith('Ruta painted garment ')and'shirt'not in m.name and'vest'not in m.name:
  for n in m.node_tree.nodes:
   if n.type=='TEX_IMAGE':n.interpolation='Closest'
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_depth='8';sc.render.filepath=str(O/'nearest-texture-front.png');bpy.ops.render.render(write_still=True)
