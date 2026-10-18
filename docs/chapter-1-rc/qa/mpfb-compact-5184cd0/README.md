# Independent compact camera proof review — #36 / PR71

Reviewed author commit `5184cd0` in an isolated worktree, no source or runtime edits. Verdict: **GO for the next technical full-cycle export in both camera groups**. This is not appearance approval, runtime integration approval, or chapter acceptance.

## Checks performed

- Opened the actual saved `mpfb-start-stop-technical.blend` in Blender 4.5.3, restored its named walk action bundle, and independently evaluated all 24 camera/pose combinations. Source SHA-256 was unchanged before/after.
- Native root translation from actual frame 1 to 25: `(0, -0.5687545537948608, 0)` metres. Reprojected through each actual camera; maximum heading discrepancy `3.15745e-7` radians. Recorded anchor/stride/source-sole readback errors were zero at saved precision. All camera matrices were proper rotations (determinant +1), ortho scale exactly 1.70 metres.
- Root anchor spread across all 24 views/poses: `0.000224841` native pixels. This supports a single anchor and constant scale, without per-direction silhouette normalization.
- All 24 distinct actual RGBA frames are 384×384 and contain the entire body/bag with transparent margins. Alpha heights range 244–271 pixels: perspective-dependent silhouette/foot spread is real; it is not evidence of changing model scale. At the current 136/251 conversion those silhouettes occupy approximately 132.2–146.8 scene pixels. Retain fixed physical calibration rather than independently forcing every silhouette to 136 pixels.
- E/W renders are not mirrored pixel derivatives. Visual inspection of the complete contact sheet confirms different front/back and side views, preserved asymmetric satchel/carrying hand, attached limbs and coherent whole-body pose in both sampled phases. No visible cuts or detached limbs were seen at this scope.
- Independently re-rendered base/SW/frame13 from the saved source. RGBA pixels are **identical** to the submitted PNG (all-channel RMS difference 0). Viewed the resulting full-resolution image as well as the 24-image sheet.

## Limits and next gates

Only phase 0 and 0.5 were rendered for each direction. These two poses cannot establish a continuous walking loop, clean swing/contact throughout a cycle, smooth turns, or multiangle start/stop. The earlier transition review remains separate; this report does not repeat its entire collision/stance audit.

The visible generic brown-haired technical figure remains **rejected appearance**, with rough clothing and no claim of resemblance to the approved painted Ruta. Changes to head, hair, wardrobe or silhouette require checking containment/calibration again. Any changed foot/limb geometry or skin weights require motion/contact rechecks.

Next export may proceed technically: full genuine frames at both calibrations, fixed ortho/ground anchor, source action/root metadata, no asymmetrical mirroring. Before game activation require complete loops/turns, start/stop variants, physical stride-to-runtime adapter, actual short/long/bridge routes and dialogue arrival. Arbitrary route residual handling remains unimplemented and blocks production integration. No game, phone, audio or family acceptance is claimed here.

## Evidence / reproducibility

- `independent-readback.json`: own 24-view Blender measurements.
- `independent-png-check.json`: own dimensions, hashes, containment, mirror checks.
- `independent-base-sw-13.png`: actual independent Blender render.
- `independent-blender-check.py`, `independent-png-check.py`, `blender.log`: exact review scripts/output (paths explicitly target this isolated worktree; adjust root to rerun elsewhere).
- Author source sheet: `art/characters-mpfb-v1/motion/sixview-proof/actual-two-calibration-proof-strip.jpg`.

No main merge, publication, shared asset mutation or other session process changes.
