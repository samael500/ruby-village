# Independent exporter/packer code and dry-run audit — #36

Scope: baselineba9fb87 (root5dda786) plus separately reproduced NumPy follow-upe8e9ab7. Independent `review/36-export-pack` worktree; only QA documents/probes changed. **No actual render or actual atlas pack was performed or certified.** Future hair source is not the temporary actor audited here.

## Concrete finding requiring visibility policy

Baseline includes meshes by render collection paths/object.hide_render, independently of object eye (`hide_set`). Actual Blender probe on temporary Adventurer_Body verifies object-eye-hidden evaluated coordinates unchanged(max0). Good: toggling that eye does not move the computed reference.

However, object.hide_viewport=True with hide_render=False leaves the mesh included by the exporter filter while changing evaluated coordinates by up to.551649809m, because viewport dependency evaluation can skip deformation. This is a real **latent contract failure**, not an observed defect in the current temporary source. Current render-visible meshes have no viewport-disabled objects or modifier show_viewport/show_render divergence. Render/viewport subdivision-level differences, disabled dependency armatures/constraints and collection evaluation differences also need congruence or fail-closed handling. Sent author exact probe; author is implementing a separate conservative visibility/dependency guard, not reviewed in this baseline commit. Object eye support does not automatically establish collection-eye support.

Current reference filter correctly traverses parent collection exclusion/hide_render and unions objects reachable through allowed paths; hidden rejected source meshes stay out. Unexpected render-visible CURVE/CURVES/etc fail explicitly instead of silently omitting their height. Thus the forthcoming hair must be a supported mesh/evaluated dependency set or the exporter must refuse it. Collection instances, geometry nodes and render-only modifiers cannot be assumed covered by the ordinary scene-mesh enumeration; future source needs explicit support or rejection. Empty/no-polygon meshes should also be handled deliberately rather than crashing min/max.

## Static code/data conclusions

- Fixed orthographic2.1 camera targets worldZ.85 with elevation derived from groundScale; resolution512×640, pixel aspect1. Heading uses existing calibrated yaw once on the actor; game camera angle is metadata, not applied a second time to the render camera.
- Actor matrix is Rz(yaw)@T(−RootRestGround). Root rest XY is normalized, Z explicitly0. World-origin anchor is projected independently of silhouette. REST worldZ span of evaluated used render-visible mesh vertices times measured worldZ pixels/m defines nativeHeight; it includes hair/accessories and is neither canvas height nor anatomical body height.
- Walk24 samples end*i/24 for end40, duration40/24s; Idle end50 duration50/24s. Endpoint is checked separately, not duplicated. Arbitrary frame-count changes sampling density, not duration;48Idle remains50/24s. Multiple view/clip scopes need explicit allow-batch.
- Source file hash is captured before/after, selected action data checked, no source save occurs. Camera/settings/pose edits are memory-only. Existing output source-hash guard is per report mode; a future tightening should inspect both dry/actual report modes before mixed-mode output reuse. This is output provenance hardening, not evidence of source bytes being edited.
- Packer refuses zero rendered count; checks every declared PNG hash, full512×640RGBA size, nonempty full alpha and edge margins; checks endpoint geometry seam; applies uniform.5 to each whole canvas. Fixed6-column atlas uses paste without an alpha mask, preserving source RGBA. NativeHeight and anchor scale.5, frame rectangles256×320; clip duration/action/source provenance retained. WebP lossless exact roundtrip is checked against the actual constructed atlas. Those are sound code paths, **not executed delivery/alpha PASS here**. No dummy sprites substituted for actual export.

## Independently reproduced dry-runs of optimization

`comparison.json`, baseline/optimized reports and logs preserve actual local runs with unchanged temporary source hash. EWalk24 optimized7625 deterministic Blender-oracle points maxerror3.98976e−5px; calibratedNEIdle48 has14136 max4.59404e−5px. E24 geometric bounds versus baseline differ≤3.39848e−5px; REST nativeHeight difference0, anchor identical, containment flags identical. Both renderedFrameCount0. This confirms the claimed numerical optimization for these inputs, not every possible camera/modifier or raster output.

NumPy projection precomputes one ORTHO matrix per camera, uses foreach_get/used polygon-loop indices and bulk world transforms, while retaining independent world_to_camera_view checks at per-object quantiles/extrema plus camera frame boundaries. Source geometry data is float32, transformation/projection float64; small deviations from mathutils are expected and below1e−4px here. Mid-polygon/raster silhouette and future shader displacement remain outside dry-run proof.

## Offline cost observations

Baseline loops all vertices in Python and repeatedly calls world_to_camera_view, which repeatedly computes camera transforms/frame; this is the dominant unnecessary offline cost. NumPy follow-up directly addresses it without changing camera semantics. Own optimized E24 run4.05s, NEIdle48 run9.92s under concurrent load; these are **not controlled speed benchmarks** and do not independently establish author's42→3.1s ratio.

Remaining costs include repeated evaluated mesh acquisition/used-index extraction per REST/endpoint/phase and repeated validation screen calls; some may be cacheable only under a guaranteed static topology/dependency contract. Exporter always rerenders selected frames, with no hash-bound resume/cache, so restarting a long failed batch can repeat substantial rendering. Source engine/light/sample settings intentionally preserved; their render cost is not measured by a geometry dry-run. Packer method6 losslessWebP favours compression over encode speed; actual encode time/size and memory need measurement after real frames exist. None of this justifies reducing fidelity or changing output pixels without a separate contract.

## Remaining required evidence

Review future visibility/dependency guard and final hair input; then actual scoped export and pack, decode/alpha/hash/atlas validation, final nativeHeight/anchor, and actual browser review-player frame advancement/pause/slider/resume at desktop/landscape. Root's pending review HTML has not been run without an actual manifest. Runtime adapter, style acceptance, foot contact and gameplay remain untested. No common/runtime edits or production activation.
