# Final boots vs reviewed B forward-distance curve

**Recommendation: retain the B curve as an explicitly experimental input, bound to this final-source compatibility report. Final-surface resampling was required and is now complete; no gait relearning is indicated. Not no-slip, physical-contact truth, art acceptance or runtime approval.**

Frozen final input: root style-v2 `ruta-native-style.blend`, SHA256 `bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706`. It is read-only, unchanged before/after sampling. Reference B is the independently reviewed frozen source and archive in `art/ruta-b-contact-forward-v1`; see `docs/chapter-1-rc/qa/contact-forward`. This worktree branches from e18d727. No source, action, camera, runtime or original curve is modified; no renders performed.

## Actual surface correspondence

Final Adventurer_Feet has336 base vertices/610polygons and only an Armature modifier, enabled identically in viewport/render. Using the same used-polygon, Foot.side weight>=.5 and rest-minZ+8.4mm selection gives56 actual material vertices,28/side. Every final point matches a group of original B points after undoing the authored foot-centered rest-X width1.3 transform. Original222 split material records occupy these56 coordinates. The JSON records all original IDs per final point; IDs themselves never define correspondence across welding. Scalp, lace/cuff and decorative geometry are not classified as contact soles.

Walk curve hashes are exactly equal; sampled Root and ankle paths have maximum difference0. After widening, actual sole trajectories are **not identical**: maximum absolute XYZ deltas12.509/2.889/.318mm; RMS7.535/.679/.069mm. Foot rotation carries rest-X changes into nativeY/Z. Incident rest polygon areas also differ (maximum normalized per-point weight delta.003917); upper cuff surgery may affect incident polygons. These facts rule out assuming contact equivalence from unchanged ankles alone.

## Same-method final resampling and fit

481timestamps/480intervals over1.666666667s; same minimum-z inferred ground,17.5mm soft contact band, per-foot rest-area weights,25ms regularized periodic common-forward fit. Each actual material-point velocity is differentiated before weighting.

| Quantity | B curve | Final same-method refit |
|---|---:|---:|
| Stride m |1.277957458|1.277750296|
| Final-surface forward RMS m/s |.012254577|.012279660|
| Final-surface full3D RMS m/s |.071798544|.071802829|

Maximum integrated distance difference is.300868mm; stride difference−.207162mm; maximum speed difference.001247886m/s. Same-old-stride uniform translation gives final-surface forward RMS.071433661m/s. The old curve’s slightly smaller unregularized residual does not disprove the refit: the solver also penalizes velocity roughness. This comparison supports practical compatibility, not exact geometric/source identity. The measured .301mm discrepancy is not a universal physical-slip tolerance.

`compatibility.json` is the main result, including full correspondence, objective and conclusion. `final-samples/` preserves actual material trajectories, rest coordinates, per-point areas and the **non-activated diagnostic refit**. Keep the existing B curve’s original provenance; attach this final hash/report when using its values. Do not relabel original B measurements as final-source measurements.

## Reproduce

Run Blender4.5.3 without autoexec on `scripts/ruta-final-sole-compatibility-probe.py`, then on `art/ruta-final-sole-compatibility-v1/reproduce-b-rest.py`. Run `reproduce-final-fit.py` and `compare.py` with numpy (Blender’s bundled python works). The final probe pins the external frozen SHA and fails on source substitution. The fit is the existing reviewed algorithm copied with output-path/sourceCommit redirection; no new model/learning method.

Contact is an inferred fuzzy surface band, not measured physical stance. Finite differences do not prove continuous swept contact. Nonzero lateral/vertical residual cannot be removed by one forward curve. Camera/heading, phase/stride mapping, actual visible contact, route endpoints and starts/stops/turns remain adapter-review work. No no-slip claim follows.
