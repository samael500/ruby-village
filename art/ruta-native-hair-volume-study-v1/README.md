# Native volumetric hair feasibility — conditional, no art candidate yet

Frozen original combined actor SHA b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7. No head/body/rig/action/camera/source edits. Only a private copied hair mesh is processed; reproducible technical blend under ignored cache/. No48 or new bitmap, no actual art renders, no runtime integration.

## Actual geometry probe

Daisy4940vertices/6639triangles,48connected surface components. Native4mm Solidify produces48closed components;3mm voxel union produces29closed components,577618vertices,0boundary/nonmanifold edges. Measured remesh3.30seconds here, not a performance promise. REST-world bounds grow at most approximately1.94mm at an axis side; exact bounds in geometry-probe.json. This is a topology feasibility result, not preservation of the opaque hair silhouette. It preserves separate wave sheets as thick volumes, not an automatically coherent authored hairstyle. It also destroys UV; old UV cannot silently be reused. No material/visual success is claimed.

**Important failure of the raw-card shortcut:** original cards contain meaningful transparent regions. Separate native-alpha study samples424896 equal-area-stratified points across all6639triangles: alpha>.5 area≈91.584%, transparent≈8.416%. Alpha sampling is approximate, not exact contour extraction. Unioning whole triangles fills that missing8.4%, including potentially decisive fringe/root gaps, so this raw-volume probe is NOT a faithful candidate and does NOT preserve the opaque envelope. It is not rendered or presented as good hair.

## What remains plausible and unproven

A proper next construction would tessellate native curved surfaces with sufficient UV sampling, clip ORIGINAL alpha>.5 isocontours in3D (not edit pixels), weld contour boundaries, thicken inward within the opaque envelope, then union overlapping volumes. Disconnected legitimate locks may remain; forcing a single component by large dilation risks merged/helmet hair. The present probe does not establish a valid thickness/voxel resolution for this alpha-aware case. Nor does a manifold union prove organic wave flow or fix E face occlusion.

Only after acceptable closed alpha-derived geometry should fixed paintedRGB transfer be attempted: closest original surface+nativeUV correspondence, with explicit handling of transparent/occluded cards, bake into new UV once in REST and preserve originalRGB image/source. Nearest-point transfers can choose the wrong overlapping sheet and need colour/seam checks. No bake is pretended to exist here. This is native3D authoring feasibility, not independent-frame retouching.

Verdict: **raw solidify/remesh FAILS the faithful-art contract**; native volumetric conversion remains technically plausible but requires the alpha-aware reconstruction and authored surface review above. It is not justified to spend three art stills on knowingly filled transparent quads. No claim that this quantified bounded probe proves all volumetric approaches impossible.

Run Blender4.5.3 `--background --threads 2 --disable-autoexec --python-exit-code 1 --python probe.py` and `alpha-area.py`. Parent hashes are asserted; only ignored derivative cache is saved. Renderer/camera/poses are not touched.
