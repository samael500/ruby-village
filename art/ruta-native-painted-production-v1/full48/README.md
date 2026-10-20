# Frozen higher-detail48 clarity candidate

Review: http://127.0.0.1:5365/art/ruta-native-painted-production-v1/full48/review.html . Shared48clock,28.8fps,40/24seconds, unchanged accepted phase order. Compare old low-resolution accepted head trial with new exact-pixel high-detail source; selector changes NEW panel between baseline and separate head-translation trial. No runtime or imagegen.

## Exact pixels and one global scale

Each source quarter has ONE330×400 grid; measured raw origins Q0(0,−11),Q1(0,0),Q2(0,−20),Q3(0,+11). Each contains exactly12large components atalpha>16 and>128. Minimum margin across ALLalpha>16pixels per quarter is7/14/11/6px. RawRGBA remains unchanged in each quarter's padded atlas, including unused alpha1prefix/tail pixels. Q0partialpacking remains frozen; Q1–3 packing manifests retain exact source bounds/hashes.

Full48frames add the SAME13transparent rows above/below every330×400 cell, producing330×426; no frame-specific fit, shift, scale or warp in asset pixels. Every cell/frame/full-atlas pixel roundtrip is verified. The full2640×2556atlas stores8×6frames in source phase order0..47. Original extra sheet noise remains in quarter atlases rather than being cleaned.

GLOBAL new source-to-logical-display scale is .5127893376456061, unchanged from Q0static phase0 calibration. No per-quarter or per-frame scale normalization. Baseline origin only accounts for the common13top padding once. Q0's earlier page remains an explicit12phase forward-only partial study. Full48 can loop47→0.

## Separate metadata trial, not internal-shape repair

baseline-manifest.json is immutable packing/global display. manifest.json adds only whole-frame destination translations. Local parameterized copy reuses the frozen phase0 head-template+cyclic-neighbour least-squares algorithm and actual accepted native Head bone endpoint trajectory. Input code copies/hashes are under inputs/ (reference only, do not execute the old writer scripts). Translation gauge has median0 relative to new baseline. No native timing/path smoothing, head scaling, rotation or image warp.

Tracking uses a uniform half-size diagnostic array for speed, never resamples source/deliveryPNG. Source translation precision.0625px is numerical search spacing, not physical/anatomical accuracy. Upper patch is fitted; lower face held out. The same native Head bob is preserved by the trajectory formula; the patch is not a physical iris/Root point.

**Measured regression/limits:** held-out lower-vs-upper RMS3.098sourcepx, maximum norm7.914sourcepx at45 (4.058logicalpx). At11→12 held-out residual changes(−6.372,−6.610)sourcepx=(−3.267,−3.389)logicalpx after upper-head translation; a rigid whole-frame pivot cannot remove this disagreement. Other seam residual changes are23→24(−.822,−.381),35→36(−1.356,−.521),47→0(−1.713,−1.413)logicalpx. cross-quarter-diagnostics.json retains actual vectors, match scores, phases and native deltas. No hidden scale correction was applied; local face/shape/detail changes remain in the candidate. These are image-correspondence diagnostics, not exact anatomical growth measurements.

Author static review of all4sheets: young identity/outfit/one rounded bag remain recognizable; sequential knees/arms and clear boot/hair/fabric detail are present. No obvious duplicate bag, detached whole limb or identity replacement. Head fullness/face shape vary somewhat between quarters; source sharpness does not establish temporal image consistency. No new appearance approval requested; accepted movement is not changed to disguise image faults.

## Renderer/API / author smoke

Single-pass DPR-aware high smoothing, fixed logical256×320, desktop CSS320×400. Compact landscape uses the same aspect/display size for both panels and explicit DPR backing;844×390author smoke shows both full canvases/boot regions within viewport and no ResizeObserverfeedback. DesktopDPR1/2author controls exercise0,11/12,23/24,35/36,47; baseline/head switches retain phase and oneGLOBALscale; actual47→0playback observed. Screenshots and browser/compact-smoke.json retained. These checks certify UI/packing only, **not temporal clarity, no-slip or game acceptance**.

API: canvases#low/#high, button#play, range#frame0..47, select#mode head|baseline, window.reviewState{ready,playing,frame,nativePhaseIndex,frameCount,cycleSeconds,fps,mode,panels}. Each panel reports actualCSS/backing/sourceRect/scale/origin. Both panels share one clock; old retains accepted frozenheadmetadata. Native comparison coordinates are half512×640 source units, not raw high-res or CSSpixels. The new scale stays fixed under all mode/frame switches.

Reproduce scan-quarters.py,pack-full.py with Python/Pillow, then head-register.py with the existing numpy/Pillow environment. New generation source assets are read-only; only quarter1–3/packing and full48 are written. Original old source algorithms/raw/runtime are not edited. Independent actual motion/clarity review is required; no fallback work begins until its verdict.
