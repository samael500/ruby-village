# Calm whole-pose E pilot v5 — needs motion fixes

This replaces neither production assets nor the user-rejected cutout animation. Eight complete painted poses now form a720ms candidate loop. Hands are lowered/open, the passing boot stays near the ground, trouser anatomy is continuous, and the visible cargo-pocket leg alternates with the far plain leg. Artistic acceptance is pending. Only E is attempted; no mirrored satchel and no mass six-direction export.

Sources: art/characters-walk-v1/calm-east-v5. All builtin imagegen inputs, raw results and exact prompts are retained, including failed wide stance, wrong pocket ownership and placement retries. Four keys were edited individually, then four whole painted inbetweens added. Two nonfinal cut-and-translated boot placement guides were used as input for subsequent **whole-pose imagegen cleanup**; those rough guides are not final frames. No bone stretching or runtime cutout motion is used in this pilot.

Registration: all generated outputs1254×1254. One affine source scale.188 is used for every frame; no per-frame height normalization. Whole-frame translation aligns the manually inspected gold waist-buckle center, a visible root landmark. The original pixels/registration remain reproducible in character-paint-calm-package.py. Target packed canvas320×320, nativeHeight224, waist/root[160,149], footAnchor[160,256]. This registration alone does not certify footplant.

## Actual measurements and failure

See painted-soles-source-grid.jpg, annotated sole-landmark-*.jpg and painted-sole-audit.json. Manual visible forefoot-pad correspondences are measured from the actual painting, with±8source-pixel uncertainty; boot rotation/occlusion limits exact correspondence. Alpha-boundary Y is taken from the actual painted sole, not guide coordinates.

| Quantity | Value |
|---|---:|
| Measured source full stride |530px on1254px canvas |
| Shared raw→packed scale |.188 |
| Packed/native stride |99.64px |
| Native sprite height contract |224px |
| Scene actor height |136px |
| Resulting stride in native scene coordinates |60.4957px (=99.64×136/224) |
| Cycle |720ms,8×90ms |
| Near support horizontal spread |7.05packed px /4.2804scene px |
| Far support horizontal spread |18.33packed px /11.1289scene px |

**NOT-FOOTPLANT-PASS.** Even allowing manual uncertainty, constant-speed support landmarks drift beyond1scene pixel. In particular phase6/7 still advance the far support unevenly. The painting also changes sole shape/rotation and partly occludes the far boot. Do not label this complete walking or hide the error by a movement multiplier, independent character scaling or an unexplained root offset. The guide's originally estimated45scene-pixel stride is not the measured stride and is not used by the bench.

## Evidence

calm-east-v5-all8.jpg is the native packed contact sheet. calm-east-v5.html is the labelled browser bench. calm-east-v5-actual.webm is a real Chromium recording: large loop, candidate traversing the courtyard at the measured60.4957scene-pixel stride, and toggled actual sole markers. Browser JSON records no page errors and real pause stability. This is a silent resource animation bench, not puzzle gameplay or independent chapter QA. Phone/family/background-tab checks are not run.

## Next constrained work

Keep the successful coherent anatomy/relaxed hands/identity. Correct the far support placement in phases6/7 and the near quarter-step timing/placement, using whole-pose painting with explicitly pinned sole points. Re-measure heel/toe and support, inspect the actual moving loop, and only then proceed to other directions/start/stop/turn. If the image editor cannot retain physical stance at those anchors, a properly modeled appearance-matched continuous3D character is required; the existing capsule proof is not Ruta final art. No Kling upload or paid generation was performed.
