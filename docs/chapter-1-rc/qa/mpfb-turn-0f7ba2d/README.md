# Independent native60° turn feasibility — #36 / PR71

Author source `0f7ba2d`, reviewed in separate worktree `qa/36-native60-turn`. **GO for120° composition feasibility and adapter planning.** This is a native left60° turn feasibility checkpoint, not complete turns, approved appearance, a seamless raster loop or game acceptance.

## Actual independent measurements

Own `check.py` opens the packed source, activates actual saved turn actions, samples257 phases (2.8125ms spacing, including non-key times), evaluates skin soles and render-level boots, and compares real entry/exit poses against retained straight actions. No source writes.

- Maximum flat-stance sole-world drift `.028932mm`; actual ankle-to-IK error maximum `.029853mm`; minimum full-render boot height `+.339684mm`. No stance-foot sliding beyond the stated submillimetre numerical tolerance.
- Actual knee flex ranges: L17.738–53.420°, R9.318–49.050°. Largest adjacent leg quaternion change1.463° at2.8125ms sampling; no discontinuous knee flips found.
- Entry/exit against straight phase0: sole maximum error `.000257mm`, body world-matrix element error maximum `7.213e-6`. Straight-source actions/rest/constraints/shoe geometry and weights additionally verified by audited fresh-baseline import (`fresh-baseline-preservation.json`). That instrumentation is an explicitly reviewed re-run of the author's preservation check, separate from the reviewer's own257-phase sampler.
- Six actual clips rigidly composed by measured endpoint displacement/yaw: evaluated every entry and exit, not a reset GIF. Root closes to numerical precision, sole closure `1.589e-7m`; successive endpoints have continuous skin/body joins recorded in `summary.json`. The source's257-phase measurements are invariant under those rigid placements. This does not pretend all six clips were rendered or shown as a continuous360° animation.

Saved turn source SHA-256 `6023f79f2bda78731d59605c3ff9bbdb64bf48d9482b81948c9e691df846dc30` unchanged. The original straight source hash is `5b10e45b08695e51f1fed2e251e1981dfe3c405ae9ee63144fa0c43c3501ed8e`; retained actions are unchanged. Rejected early contact-event source remains archived and was not used as passing evidence.

## Root curve and coordinate sign

Actual saved endpoint native `(0.2675198317, -0.4633579850, 0)m`; yaw `+1.0471975803rad`. Independently recomputed saved-key polyline length `.5687520573m` and minimum discrete circumradius `.4499892670m`, matching metadata. These describe a variable-curvature sampled path, not a constant-radius circle or exact analytic C1 interpolation.

In base grid coordinates native+60° means grid−60° (E→NE), **not screen−60°**. With groundScale.65 the actual screen endpoint heading is about−.844522rad (−48.387°). Fixed-camera mapping is native `(x,y)`→screen `(-y,-.65x)`; this basis conversion is not an image mirror. Other camera calibrations and right turns still need actual projections. The nonzero root displacement/curve must be consumed once by a future adapter; snapping the sprite around a sharp path vertex would discard this proof.

## Raster / body review

Viewed all12 genuine diagnostic poses in the full author strip and the independent native frame13 render. Body, shoulders and bent legs rotate coherently, with a modest body lean and anticipatory head orientation; no sliced limb or obvious rubber twist was seen in these samples. The asymmetric bag/carrying hand stay consistent. Technical generic appearance/clothing remain rejected and are not implicitly accepted here.

All12RGBA384×384 images are entirely contained and match their declared hashes. Fixed E camera follows root translation only, ortho1.70m and groundScale.65. Audited render instrumentation was re-run for frame13; the independent image matches submitted RGBA exactly (all-channel RMS0), confirming the saved3D source reproduces the visible proof. Root/sole pixel metadata references the same source/camera; no per-frame scale normalization.

The GIF is a720ms one-way turn demonstration followed by a hold/reset. It is **not a seamless loop**, and no natural closed360° raster cycle is claimed. Twelve sampled poses do not establish every transition frame's visual quality or contact with new clothing/hair.

## Remaining gates

GO only to a measured120° composition study and planning the route adapter. Opposite-sign turns, other calibrations/headings, real complete turn rasters and start/stop transitions are not supplied by this checkpoint. Before integration require actual path containment around grid corners/bridges, correct root/timing/stance across turn joins, arbitrary route residual handling, approved appearance with renewed contacts/containment, and actual game routes/dialog arrivals. No real phone/family/complete chapter acceptance or publication.

Evidence: own `check.py`, `actual257.json`, `summary.json`; fresh baseline hashes; `raster-path-check.json`, fresh source path/render metadata, independent frame13 and audited re-run scripts/logs. No common runtime/source files changed.
