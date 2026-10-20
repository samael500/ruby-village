# Fixed head-look diagnostic, not accepted art

One chosen −20° local-X REST head pitch, from frozen Daisy painted-RGB source `350c96cd…`. Actual internal −10° and −20° front stills are retained; final chosen self-contained model is `ruta-head-look-chosen.blend` (SHA256 `167d471c27f5e17b6267b141170de0987b0f6ea6421251b340f023b62112a1e9`). The two intermediate models remain local and reproducible with `prepare.py`; only the chosen model is delivered.

This is a common fixed 3D REST coordinate field for all visible Ellie head-attached meshes, not a camera offset or per-frame fit. Smooth weight zero below REST Z1.18, full rigid rotation above1.25; lower hanging hair is consequently partly protected. Body, bone rest rig, 50 actions, weights, topology, UV, ten packed images/materials and actual camera remain unchanged. Cold-open test gives zero evaluated displacement for 2946 protected neck vertices at Walk frames0/40. This is not a full-cycle intersection certificate.

`pitch-up20/front-diagnostic.png` and `chosen-threequarter-diagnostic.png` are actual Eevee128AA512×640 renders. Front/threequarter are explicit diagnostic actor yaws0/π4 and Idle0; final saved blend restores canonical E yawπ2/Walk0. Native forward-axis versus camera proxy changes36.59°→16.59°, not a measured physical iris gaze. Blue eyes read more clearly; worried brows and geometry/style differences remain. No likeness acceptance, runtime integration, heading-contract change or48-frame render.

## Black forehead line: material surface, not an alpha hole at tested pixels

`hairline-pixels.json` samples actual opaque pixels: (250,162)RGBA24,24,24,255, (240,159)18,18,19,255; skin below(250,174)255,198,163,255. `hairline-pixel-closeup.png` is a nearest-neighbour evidence enlargement only.

`hairline-cause.py` cold-opens the saved front model and raycasts the evaluated head object directly. This deliberately excludes old hidden rejected hair (scene-wide raycasts include hide_render objects and are unsuitable here). At all three dark samples the FIRST front-facing head surface is material `ellie.head_hair`; below, the first material is `ellie.head`. Polygon indices, normals and world positions are in `hairline-geometry-cause.json`. The dark band therefore exposes the native dark scalp material rather than passing through an empty skull at these rays. Shader-alpha-aware path tracing is not claimed. Head mesh has208 boundary edges,128 with both endpointsZ>1.35, so global watertightness is expressly NOT certified by this local result.

Do not add a scalp cap or paint the PNG to conceal this. Next minimal study, if approved, is material-only replacement of the existing dark scalp region, keeping actual geometry and original hair alpha; a genuine 3D underlay is only justified if a separate actual gap is demonstrated. No fix is included here.

Reproduce using Blender4.5.3 `--background --threads 2 --disable-autoexec --python-exit-code 1 --python <prepare.py|choose-and-render.py|cold-check.py|hairline-cause.py>`. Source models are read-only and retain their hashes.
