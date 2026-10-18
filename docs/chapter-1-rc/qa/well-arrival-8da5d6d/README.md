# Independent well scene / Teacher arrival review — #35 / #45 / #46 / #62

Reviewed actual well pilot `8da5d6d` (coordinator fix `4929ac6`, art `daf567e`/`5144738`, source `6dbf644`). Own isolated worktree/build, browser server5298. **Scoped PASS: painted well/native-wide registration, teacher visibility and arrival separation.** This is not user artistic approval, all-scene production activation or chapter RC acceptance.

Initial review used the frozen author build while preparing the independent build. Own clean Vite production build then completed; JS/CSS bytes matched the frozen build exactly, hashes recorded in `served-build.json`. Own server was switched to the independently built directory. No common source/runtime changes or activation-gate bypasses were added by the reviewer; the existing explicit well-only review gate remains confined to this candidate. It seeds earlier progress only, never a solution.

## Actual game checks

Normal-motion actual UI solves at1280×720 desktop and844×390 emulated landscape phone, each covering two introduction pages, activity, two replay pages, persisted reload, three arrival dialogue pages and the result. Puzzle input and dialogue/settings actions use mouse or native CDP touch respectively; initial Continue uses Playwright's click. Recorded silent browser WebMs retain the real walk and arrival. No route/solution/state injection or reduced-motion shortcut.

Teacher stays visible at native feet1320,405 through those states. At arrival Ruta stops near accepted goal1231,456, looks toward the teacher, and the teacher's conversation-left view faces the encounter. Viewed desktop/phone first-arrival and result images: characters read separately, teacher is not hidden behind Ruta. All three after-pages and result use the same stable resident anchor; no page errors were raised. Replay/reload retain the actual teacher and scene. Result illustration shows this well/flowerbed, actual placed road and both characters, rather than a shared generic ending.

Independent reconstructed alpha comparison from actual recorded Ruta sprite crop and image matrices covers all8 arrival/result states. **Any-nonzero alpha overlap is0**, including dialogue view changes. Transparent image rectangles can overlap slightly; the report does not confuse those rectangles with visible occlusion. Viewport-pixel rounding and Lanczos resampling are declared in `pairwise-alpha.json`.

## Native art, field and wide checks

- Both2 delivered authored teacher views at1320,405: full nonzero alpha overlaps0 pixels of actual accepted playable-ground/water polygons. This is a full sprite audit, not a feet-only test.
- All14 flower-cell centres have actual flower alpha (165–251 in this source). No missing upper-row blockers. The natural lobed flowerbed is visible in real game frames.
- Flower edges have3 coarse raster-boundary free-mask intersections, consistent with the source's declared1px tolerance. There are **zero full-alpha intersections beyond that1px boundary tolerance**. This is not mislabeled as exact coarse-raster0.
- Native1672×941 pixels match wide3272×1200 crop `(800,129,1672,941)` exactly. Desktop and landscape-phone game/result frames show painted coverage without black/flat letterbox bands or abrupt visible native/wide seam.
- Accepted layout-adjustments, solution and well geometry files remain byte-identical to pre-anchor-fix `d831f52`, hashes in `clearance.json`. No rules, cells or saved placements were changed to fit art.

Source standalone `public/assets/chapter-1-garden-well/well-manifest.json` still contains the older proposed teacher1225,405 and pending-source wording; **actual installed common/runtime manifest is1320,405** and was verified in every recorded state. Coordinator was notified to reconcile final delivery metadata. Do not use the older proposal as an integration instruction.

## Evidence and limits

`review.py/report.json`: real input/state assertions and actual native sprite markup; `pairwise-alpha.py/json`: independently reconstructed character overlap; `clearance.py/json`: two complete delivered teacher-view alphas,14flower centres, exact wide registration and immutable geometry. Twenty actual state screenshots and two normal-motion silent WebMs; build log and served asset hashes.

Original user attachments were unavailable and are not claimed as inspected. This independently reproduces the described arrival/composition scenario. Emulated landscape phone is **not physical phone**; family test remains not run. Current painted-road union is isolated stream scope and is not claimed deployed here; well's old individual tile rendering is visible in these honest captures. MPFB replacement/turns, audio and all-eight complete chapter remain outside this report. No main merge/publication.

Count correction: the teacher facing manifest delivers exactly2 views (`conversation-left`, `conversation-front`). The8 arrival/result alpha checks count runtime states across two viewports, not8 different viewing angles. Legacy fallback/idle artwork was not separately audited by this facing-view script.
