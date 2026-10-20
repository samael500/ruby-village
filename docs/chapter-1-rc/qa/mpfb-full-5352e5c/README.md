# Independent full technical walk export review — #36 / PR71

Author checkpoint `5352e5c`, independently reviewed in isolated `qa/36-full-cycle` worktree. **PASS for this technical 288-frame walking export and its fixed-scale/root-motion inputs. GO to reuse the measured source/action pipeline for the corrected appearance and further transition/turn work. Not approved for production activation or final character art.**

## Actual checks

Opened the immutable packed Blender source and independently evaluated all288 exported combinations (24 real walking poses ×6directions ×2accepted camera calibrations). Restored the actual named action bundle. Actual source world sole markers, root positions, projected anchors and stride vectors match receipts at saved precision: readback errors0; maximum projected heading error `3.98457e-7` radians. All camera transforms have determinant+1, ortho1.70m. Root anchor spread across288 views/poses `.000266736` pixels. Source hash remains unchanged.

Independently re-rendered base/NW/frame7 from saved Blender: submitted and independent RGBA pixels match exactly, RMS0. All288 submitted PNG hashes agree with their receipts, all288 are distinct and entirely contained in384×384 frames. Threshold16 alpha has one four-connected component of at least4pixels in every frame: no detached raster limb pieces detected. Viewed all12 independently assembled contact sheets containing every frame, plus full-resolution re-render. Legs bend and pass through distinct support/swing poses as whole connected 3D anatomy; no sliced or stretching single-image joints were observed. Carrying hand and asymmetric satchel remain consistent. Clothing and generic appearance remain rejected separately.

Actual raster heights vary241–271 pixels with pose/view; physical scale remains fixed. Do not normalize each sprite to its alpha height. Across all12 views, frame24→1 raster differences are below that view's largest ordinary interior step, consistent with no exceptional loop pop; this image metric alone is not motion acceptance.

Independently evaluated25 source frames including the loop endpoint at render-level boot subdivision. Sole stance-world drift maximum `.020248mm`; minimum actual boot Z `+.344815mm`. Root-relative frame1→25 sole error `1.50322e-7m`. Actual walking root advance remains approximately `.568754554m` per720ms. These are measured skin/contact results, not just desired IK target coordinates.

Ran an independent Chromium playback page preloading the actual288PNG, playing all12 views on one30ms/720ms clock for more than8cycles, followed by six held comparison frames. RAF trace includes every phase0–23, no page errors. Saved real browser video `actual-browser-twelve-loop.webm`, six actual page screenshots, trace, and the exact HTML/script. This is actual resource playback, **not a route in the game**. Visual review used complete phase contact sheets and held playback frames; no unsupported human real-time video-watch claim.

## Runtime/adapter boundaries and blockers

`adapter-input-contract.json` is honest metadata: production disabled, fixed native root applied once, genuine measured action/root samples, exact full-cycle scale, transition raster export explicitly false. It does not implement arbitrary route fitting. The quarter-stride goal-cell endpoint idea remains unimplemented/unvalidated; do not report it as accepted. Native start/stop actions have separate earlier scoped review but these288PNG contain walk only. Turns are explicitly not authored; six walking orientations are not turn transitions.

Before production integration: approved painted Ruta likeness on the actual MPFB model; renewed height/containment/foot/clothing checks for changed geometry/weights; new source-hash resource namespace; genuine transition and turn frames; route adapter with exact-once root, short/long path/bridge stopping and dialogue-facing checks. No source replacement may silently reuse the generic doll's raster cache. No gameplay, phone hardware, complete chapter, audio or family acceptance is claimed.

## Own evidence

- `independent-blender.py`, `independent-readback.json`, `blender.log`:288 actual saved-source/camera readbacks plus independent render.
- `independent-contact.py`, `native25-contact.json`, `contact-summary.json`: actual source sole stance/seam and render-level boot measurements.
- `png-check.py/json`: every PNG hash, bounds/component results and adjacent/seam raster metrics.
- Twelve `*-all24.jpg` sheets, `independent-base-nw-07.png`.
- `playback.html`, `browser-playback.py/json`, actual WebM and six frame screenshots.

No author source/runtime edits, main merge, publication or shared processes changed. Temporary own server5298 stopped after review.
