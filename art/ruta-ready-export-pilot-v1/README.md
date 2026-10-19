# Whole ready-sprite exporter — contract-only checkpoint

Ownership: only `scripts/ruta-ready-sprite-export.py`, `scripts/ruta-ready-sprite-pack.py` and this directory. Frozen source baseline9d8c3ac; no model, wardrobe, old exporter or runtime edits. Temporary blue/copper actor is not final art. This checkpoint contains **no rendered frames or atlas**.

## Defaults and explicit scope

```
blender --background --threads 2 --disable-autoexec --python scripts/ruta-ready-sprite-export.py -- --source art/ruta-ellie-head-v1/color-handoff/ruta-b-ellie-blue-copper-temporary.blend --contract-only
```

Default base/e/walk24, source Walk_ProportionProposal frames0..40 with endpoint excluded from24phases, actual duration40/24s. Idle_Neutral_ProportionProposal uses0..50 and duration50/24s. `--frame-count 48` renders48interpolated Blender poses of the SAME duration, not a changed gait or image interpolation. `--variants all --directions all --clips all --allow-batch` is available but **not run or authorized for rendering before art review**. A single clip/camera/heading remains default; explicit multiple selections require `--allow-batch`. Use a separate `--out` for a different source hash.

Without `--contract-only`, renders actual full512×640RGBA PNGs. Once source-contract.json and actual frames exist:

```
python scripts/ruta-ready-sprite-pack.py --contract art/ruta-ready-export-pilot-v1/source-contract.json
```

Packer refuses contract-only input. It verifies each actual source PNG hash/dimensions, alpha containment, endpoint geometry seam and applies **one .5 resize of every full canvas**. Atlas is6columns×ceil(N/6), losslessWebP with decoded-byte roundtrip check. Manifest retains source/algorithm/heading/action/file hashes, source ranges/durations, source frames, cameras and foot anchor. No global or per-frame crop, warp, position fit, direction resize or baked route. No atlas/frame files are claimed until rendered and packed.

## Coordinate and geometry contract

Yaw comes directly from existing heading-contract.json, including its camera angle correction once. Actor matrix is `Rz(yaw) @ T(-RootRestGround)`. Fixed ortho2.1m, fixed targetZ.85m,512×640, camera elevation from that variant's groundScale. Native RootGround is Root rest XY with Z explicitly0. Anchor is world_to_camera_view(world origin), not bbox-bottom. NLA muted, action bound to correct slot. Source render engine/materials/lights/world/color settings preserved, no source save.

REST reference is actual evaluated **used** vertices of all render-visible meshes, respecting object hide_render, collection hide_render and excluded view-layer collections. Hidden rejected CC0 hair is excluded both from reference and source render visibility. Unexpected visible non-mesh geometry fails closed instead of silently omitting its height. Height is measured worldZ span × measured worldZ projected pixels/m (projection of world(0,0,1) minus worldorigin), never canvas640. Accessories/hair participate; a body-only anatomical height is a different metric.

Dry-run actual temporary actor:19includedmeshes; excluded Adventurer_Head, RutaCC0gingerwaves, EllieCC0Cortuwaves and Icosphere. REST height1.613150998m, measuredZ231.599035px/m, nativeHeight373.604215px (delivery186.802107px). Worldorigin anchor(256,516.859312) stays fixed at24phases. Walk0/40 evaluated used-vertex seam0m. Projected geometry24/24within canvas. Source SHA unchanged. These are geometry/camera checks **not alpha/raster, art, contact/no-slip, runtime or gameplay acceptance**.

Only actual E24 render with the final supplied actor can exercise source shading, alpha containment, PNG delivery and atlas packing. The two new scripts pass Python syntax compilation; no dummy rendered frames were substituted to claim packer acceptance. No full576export run.

## Scoped exporter performance follow-up

`performance-check.json` records actual single-run local elapsed time: original ba9fb87 E/base/Walk24 dry-run **42.01s**, optimized **3.10s** (~13.55×). Blender4.5.3, threads2, separate sequential processes, same frozen .blend. Additional calibrated-1/NE/Idle48 dry-run **5.39s**. These are observations, not universal performance claims; zero frames were rendered.

Exporter only: evaluated mesh coordinates and used polygon-loop vertex indices now use NumPy foreach_get/bulk world transforms; camera inverse and orthographic view_frame are composed once per camera. Blender's original world_to_camera_view is retained for anchor/height measurement and as numerical oracle. Deterministic quantiles plus world-axis extrema of **every visible mesh** at REST, source endpoints and all requested phases, plus camera corners/center/one-pixel-outside frame boundaries: E24 **7625** sampled comparisons, maximum error **.00003990px**; calibratedNE/Idle48 **14136**, maximum **.00004594px**. Threshold .0001px is asserted. This is sampled equivalence, not bitwise identity of every vertex. Entire E24 geometry bounding extents versus original differ at most **.00003399px**; nativeHeight/restheight/camera/anchor unchanged, seam0. All checks bind the exporter/source hashes. `timing-baseline/` retains original numerical report/process log; main dry-run is optimized. Packer and source models/runtime unchanged.
