# Independent B1/B2 repeat — #35 / #48 / #62

Reviewed coordinator fixes `3675cb7` (Baker1360,405) and `7b0ba19` (shared dialogue camera) atop the earlier frozen four-scene audit. Local source head `bbc248a`; original private four-scene activation remains only in QA worktree. Evidence commit adds no runtime/production activation changes.

**B1 PASS. B2 still needs correction: Ruta is fixed, gate remains clipped.**

Four actual normal-motion mouse/native-CDP-touch runs: bakery/gate ×1280×720 and844×390. Actual placement, normal walk, all after-pages, replay/reload, prologue (gate), and own-scene results complete without page/HTTP errors. Forty actual state frames, twelve gate prologue frames and four actual silent browser videos retained. No solution/win injection or physical-phone claim.

## B1 — resolved in this scope

Baker feet are1360,405. Actual recorded Ruta sprite crop plus Baker alpha gives **zero any-alpha overlap in all six arrival pages and both result states** across the two viewports. Delivered conversation-left and actual optimized legacy-idle fallback both have0 full-nonzero-alpha overlap of accepted playable-ground/water polygons. Bakery dialogue actors remain fully above the panel; source map-matched building, replay/reload/results remain intact. Exact resource counts are two tested resource poses (one new facing and one fallback), not eight directions.

## B2 — remaining concrete defect

All actual Ruta arrival frame rectangles now fit above the dialogue. Background, residents and the main board's foreground share the same measured camera matrix; no independent actor/layer CSS shift is involved. No empty bands were seen in the actual captures.

However, the **open gate is still clipped by the SVG field/dialogue boundary** on both viewports:

| Viewport | Actual panel/field bottom | Actual open-gate alpha bottom | Clipped gate height |
| --- | ---: | ---: | ---: |
|844×390|252px|283.846907px|31.846907px|
|1280×720|552px|600.535830px|48.535830px|

This repeats on both after-pages, including the page stating the gate opens. Images: `gate/844/07-arrival.jpg`, `08-arrival.jpg`; desktop equivalents. The real alpha bounds of `gate-open.webp` are native `(1427,723,1453,876)`; transformed by the measured main foreground matrix, they exceed the available field. `camera-check.py/json` records the arithmetic. This uses the actual image alpha and screen matrices, not an estimated rectangle from a screenshot.

**Verified cause in `gameScene`:** `wide={...assets.wide.canvas,...assets.wide.originalRect}` overwrites actual wide3272×1200 dimensions with native-rectangle1672×941. `frameDialogueScene` therefore applies an incorrect minimum scale and vertical coverage clamp. For phone, the actual main matrix is scale.497607678 / screenY−152.057419; the incorrect941−129 extent prevents the needed upward framing despite the declared gate focus719…876. The same erroneous clamp affects desktop. The pure camera unit tests pass with correct wide inputs; the runtime constructs different inputs.

Do not move the accepted goal or shift the gate layer independently. Correct the dimensions passed to the shared camera, then repeat actual framing/coverage. This reviewer has not edited the fix.

## Validation/evidence limits

Clean independent Vite build passes; the two `dialogue-camera.test.ts` tests pass. These do not override the reproduced B2 visual defect. `served-build.json` binds bundle hashes. `geometry.py/json` retains accepted layout hash and resource-alpha/wide checks. `pairwise.py/json` binds B1 to real runtime sprites. Story grid/tray/ordinary field hiding and restored-road behaviour continue to pass.

Raw layout reports collected all document foreground matrices; later entries include hidden prologue and differently scaled result clones. Camera analysis explicitly uses the first/main `#board` foreground rather than misclassifying those separate SVGs as divergent game layers.

New MPFB art/motion, connected-road rollout, audio, complete chapter RC, family and physical phone remain outside this scoped repeat. No main merge/publication; original private activation must not enter production.
