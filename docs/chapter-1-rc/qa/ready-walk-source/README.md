# Independent ready-character stock walk pilot review — #36

**Recommendation: retain Walk as a usable stock motion foundation and proceed with character adaptation and the remaining five views (six total). Do not describe this as Ruta likeness accepted, runtime-ready or slip-free.** I did not author this model, motion or renderer; this QA worktree changes evidence only.

The24-position contact sheet and decoded largeMP4 samples show a coherent alternating gait: each knee bends during recovery, feet pass beneath the pelvis, the opposite leg extends toward the next step, arms counter-swing, and torso/backpack remain connected. I found no frozen-leg sequence, cutout deformation, impossible limb break or conspicuous endpoint pose discontinuity that warrants rejecting the source clip. The long-stride adult/adventurer appearance is a separate adaptation concern. The comparison is stock-source quality, not approval of the final child protagonist.

## Independently reproduced source and render checks

Opened both saved source and pilot in Blender4.5.3. Compared all62 rest-bone matrices, mesh coordinates/skin weights for all4 meshes, and Walk animation channel values/interpolation/handles: exact match. Selected action is Walk; all NLA tracks muted. All62 evaluated pose matrices at source0/40 match exactly. This proves endpoint pose continuity, not ground-contact quality or constant velocity.

Camera is orthographic,512×640, native world-origin anchor256,516.859312. Independently projected ground foreshortening0.649999976 agrees with.65. Fixed camera/rig yaw creates E; the source renderer samples24 full frames across0≤frame<40 at source24fps, giving1.666667s per cycle and14.4 rendered samples/sec. No per-frame camera, crop, translation, body scaling or raster warping is in the render script. Alpha bounds remain within the canvas for all24 unique frame files.

Independent atlas unpacking finds all24 alpha channels and every nonzero-alpha RGBA pixel exact against its original512×640 frame. Raw whole-buffer equality is false only because alpha-compositing discarded invisible RGB under zero-alpha pixels; that is explicitly recorded rather than called bit-exact whole-buffer packing. No visible sprite change results.

MP4 decodes cleanly at512×640,72 frames,14.4fps,5seconds: three source cycles. I inspected the24-frame contact sheet and extracted MP4 samples0,12,23,24,48 (`mp4-decoded-review.jpg`), including the23→0 boundary and repeated cycle starts. This is a decoded-sequence review, **not a claim of realtime playback with subjective timing evaluation**. PNG/contact-sheet observations and Blender pose checks are the primary independent visual/motion evidence.

## Foot contact limitation

The stock action is in place. Author mesh/ankle samples report estimated travel1.049523m/s and1.749206m per1.666667s cycle. The reported stance residualRMS0.192322m/s is approximately18.3% of that travel speed: substantial enough that constant-speed root translation may visibly skate at enlarged scale. Inferred stance is based on sole minimum within25mm of source floor, not authored IK/contact labels; foot rolling and changing low vertices affect that estimate. Neither a repeating endpoint nor grounded-looking still poses establishes slip-free motion.

This is a known integration task rather than evidence of a broken stock action: before runtime acceptance, preview translated motion over a marked floor at declared native scale and actual travel speed, inspect each stance and transition, and align speed/cadence or correct contact in the rig if needed. Keep one stable world foot anchor; do not stabilize sprites by per-frame raster shifts. The six camera directions should remain outputs of the same rig/action. Only E has actually been rendered and reviewed here.

## Provenance / scope

Quaternius' current [official Ultimate Modular Women pack page](https://quaternius.com/packs/ultimatemodularwomen.html) was independently opened during this review: it declares CC0 and animated modular characters, including glTF/Blend. Existing provenance explicitly records official Drive quota failure and a fixed GitHub mirror commit/download URL. Every saved provenance hash independently matches the file. Bundled License.txt incorrectly says'Males'; the mismatch is preserved and not silently rewritten. Author's Women-specific CC0 page supports this pack's licensing; this does not magically turn the mirror into an official author-hosted download.

Evidence: `blender-audit.py`, `blender-report.json`, `blender.log`, `pixel-report.json`, `mp4-decoded-review.jpg`. Reviewed source `art/ready-character-walk-v1`, contract/action/preview scripts. ProductionEnabled remains false; no source mesh, animation, art, common manifest or runtime changed. No actual-game walk, character likeness, five unrendered directions, audio, physical device or final production acceptance is claimed.
