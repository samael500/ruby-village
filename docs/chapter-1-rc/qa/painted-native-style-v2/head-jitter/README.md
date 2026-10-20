# Head jitter: read-only semantic limits and visible-eye diagnostic

Appearance is already accepted; this investigation does not ask for a new identity/style decision. No image pixels, per-frame scale/warp, baseline or trial pivots are changed here. Native frozen input SHA remains bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706. Actual raw48 and semantic-pivot trial manifest hashes are pinned in eye-patch-diagnostic.json.

## Native reference delivered first

native-head-projections.json retains all48 actual posed Head bone **head and tail** endpoints in native world, FULL512×640 projected pixels and fixed packer-calibrated painted equivalents. Camera matrix/ortho viewport, E yaw and static Root normalization are the actual exporter contract. The native-head-probe.py never saves the source or renders. Bone endpoints are real Head-bound fixed references, **not the painted iris, crown or anatomy annotation**. Head orientation can change the apparent eye offset about that pivot. The native trajectory was handed directly to the packer before finishing this report, to preserve real native head bob rather than suppress all head movement.

## Visible eye evidence

All six enlarged raw ruler rows were visually inspected. The eye is tiny: a strict diagnostic chromatic-blue mask in a fixed semantic-eye ROI selects1–7pixels in46 phases,0 at27/28. The blue samples lie on the visible eye. At27/28 the eye remains visible but desaturated, so zero threshold samples are **not missing-eye/occlusion evidence**. No coordinates are fabricated for those phases.

The output is explicitly the centroid of a visible **blue colour patch**, not an exact anatomical iris/pupil centre or hand-placed joint. This distinction matters: changing colour/shading/occlusion can move this centroid without moving the eye geometry. Approximate per-axis annotation/selection uncertainty is1px, increased to1.5px for1–2selected pixels; unknown systematic correspondence bias remains. The mask is only diagnostic, never modifies RGBA and cannot certify subpixel tracking.

The side profile has no defensibly isolated nose tip at this resolution. No invented nose/jaw landmark is provided. Without two reliable well-separated face landmarks, this table cannot independently estimate a precise head scale/rotation or internal facial-distance variation. That is a measurement limit, not evidence that all internal distances are constant. Native projected bone head-to-tail length is provided separately as a source reference; it is not a painted face-size proxy.

## Adjacent residual after current clasp trial

Using the existing semantic-pivot trial’s exact translations/fixed scale, compare adjacent displayed blue-patch displacement to the actual native Head-pivot bob displacement. Units below are native comparison pixels (the half512×640 source plane), **not desktop screen pixels**. Constant placement bias cancels; head rotation, changing colour patch, redraw and physical-feature mismatch do not.

Largest adjacent residual norms are31→32:5.156px;47→0:5.055;15→16:4.542;38→39:4.453;10→11:3.825.39→40 is3.424 after the raw jump is mostly removed by clasp translation. For these pairs the blue-centroid annotation difference is approximately±2rawpx per axis (±2.5at39→40); multiply by the fixed1.163156 scale for comparison units. These are coarse diagnostic differences, not exact measured anatomical jitter or a standalone physical-error bound.

Important separation:39→40 clasp/bow diagnosis was consistent with whole upper-body translation. Remaining eye motion elsewhere and at the seam is not cancelled automatically by that conclusion. A body-clasp pivot does not force the Head-bound visible eye to follow the native head path. Conversely, noisy tiny-eye centroids cannot justify indiscriminately freezing the head or scaling the whole actor.

## Independent companion evidence and disposition

Packer’s separate head-template diagnostic reports upper/lower window disagreement (largest around28–31), a local head similarity preference around+7.8%scale/−3.875degrees at30 and independent torso-clasp disagreement. Those are its measurements, not newly reproduced anatomy measurements here. A local similarity success on hair does not establish whole-body scale change, and head-only tracking cannot authorize image warping.

This diagnostic provides the exact native Head trajectory and independent visible-eye evidence with uncertainty. It does **not** prove one rigid pivot fixes all remaining visual jitter, nor does it accept global per-frame scale/rotation, frozen head motion, physical foot anchors or no-slip. Appearance remains accepted. Root closed further manual-point expansion and chose a separate deterministic native painted-render fallback study; no endless landmark fitting or generative re-authoring is performed here.
