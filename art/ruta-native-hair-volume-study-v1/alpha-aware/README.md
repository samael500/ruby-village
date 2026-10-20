# One alpha-derived closed-volume candidate — art/temporal gate OPEN

Frozen original combined actor b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7. This follows the rejected raw-quad union; no opaque rectangles are painted in place of native alpha. No source file/body/head/rig/action/camera edits.

## Reproducible native construction

`build.py`: sample ORIGINAL immutable daisyhair1.png bilinear alpha>.5 on native curved3D triangles. Large UV spans get initial subdivision; threshold-crossing triangles recursively subdivide toward2UVpixels/3worldmm, maxdepth6, then linearly intersect threshold edges in3D. This is approximate contour reconstruction, not exact every-pixel isocontour. Weld1µm, inward4mm Solidify,3mm Voxel union. No smoothing or decimation. ParentHead rigid weight1. Original Daisy is hidden only in the derivative; its geometry/material/UV/weights remain untouched. New geometry527846vertices/527874faces, boundary0/nonmanifold0. All527874polygons smooth-shaded explicitly via remesh option.

85closed components: main527094vertices and84tiny fragments retained, not silently deleted. Actual saved EWalk0 projections of every tiny component are in fragment-projections.json; largest projected dimension1.654pixels. Such fragments can still matter temporally; static smallness is not permission to ignore them.

`bake-render.py`: closest ORIGINAL native3Dtriangle→barycentric originalUV, explicit NativeSourceUV samples unchanged fixed painted DaisyRGB. Separate SmartProject VolumeBakeUV, one2048² native CyclesEMIT bake, then matte Diffuse with that single fixed baked image. NOT per-frame retouching/AI. Original14packedimages are exact; only one bake added. UV nearest-source transfer may choose adjacent overlapping cards; image/surface fidelity is not numerically certified. New fixed RGB bake SHA and vertex-source distances recorded in bake-contract.json.

Heavy reproducible geometry/baked blends+intermediate arrays are in ignored cache/ (not committed29MB failure assets). Output bake and three actual PNGs are committed. Run Blender4.5.3 `--background --threads 2 --disable-autoexec --python-exit-code 1 --python build.py`, then bake-render.py; measure.py/fragments.py/cold-check.py and compare.py provide evidence. Full bake+three still stage observed73.04seconds here; not universal performance.

## Geometry and actual silhouette limits

Native maxZ1.626555→volume1.626397, no added height. Deterministic20k volume-vertex distance to alpha-clipped surface: median1.753mm/p95 4.129mm/p99 4.517mm/max19.007mm. This one-sided distance includes inward walls/joins and does NOT equal outward silhouette inflation, but also does NOT justify a4mm all-surface fidelity claim. Source-triangle all-vertex transfer max28.398mm likewise flags correspondence ambiguity; no exact-Hausdorff/visible-envelope guarantee.

Actual fixed-camera alpha128 masks: E bbox[142,127,374,531] unchanged; front[143,112,357,540]→[142,112,357,540] (1pixel left); matching−π4 threequarter[128,110,357,544] unchanged. New opaque pixels outside old masks E174/front27/3q221, removed87/136/113. These include internal holes/occlusion, not solely exterior boundary. Red/cyan overlays in comparison JPGs show actual locations. No independent CSS/camera/registration shifts.

## Actual visual status

Three genuine Eevee128AA512×640 stills: EWalk0, frontIdle0, matching rootbaseline−π4 threequarterIdle0. Long waves are retained and the thin alpha-card surfaces are replaced by opaque closed volumes. This removes the literal alpha-card backface/cutout mechanism, but folded broad strips/crown contour and strong painted RGB streaks remain visible. Face stays obscured in E. Front is readable; this is not acceptance of likeness, natural hair flow or final colour. Static stills cannot certify reduced temporal shimmer. No48 test/render or runtime installation has been done.

Cold-open confirms ALL original mesh coordinates/topology/UV/weights/material slots exact,50actions exact, camera exact,14original packedimages byte-exact. New hair only is added plus original hair render visibility changed. Source input hash remains pinned. This is one candidate for root art review, not final replacement hair or a synthetic PASS.
