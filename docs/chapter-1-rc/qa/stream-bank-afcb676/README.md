# Independent adaptive streambank review — #45 / #46 / #62

Review candidate `afcb676` (adaptive source `8914141`, common resource installation `3922fd7`; coordinator integration equivalents `6408e67` / `7299e89`). Reviewed the real isolated art-pilot build on port5306; served JS/CSS hashes recorded in `served-build.json`. Own branch/worktree, evidence-only changes; source authors did not perform this review.

**Scoped PASS: P1 cut-bank correction, logical alignment and retained pointer interaction.** This does not accept the plain bridge artwork, production activation, all eight scenes or the complete chapter.

## Actual visual observations

Viewed desktop1280×720 and emulated landscape-phone844×390 clean game scenes and exact logical-water overlays, plus the native close-up around cells5,3/5,4. Compared the prior `14b1f6f` defect area. The cut grass/stone rims previously following exposed hex edges are removed: the new channel has continuous earth/pebble margins at both bends. Boundary additions read as low ground treatment; no newly obstructing large rocks or bushes were seen. The native crop `native-bank-5-3-5-4.png` and current actual-game frames preserve this evidence.

Middle section of the installed three-hex bridge crosses visible water; both ends are on dry ground and join the confirmed paving. No visible hanging endpoint, bank foreground crossing the deck or opening between approach and deck was seen at these viewports. The bridge remains visually plain compared with the painted environment: **art enhancement is pending and is not approved by this bank review**.

Technical water tint and ≈ glyphs are genuinely absent in the runtime. `water-hit.py` independently checks their real DOM/computed styles, uses no presentation CSS, and saves untouched screenshots. The main review's optional clean-view CSS is now redundant; minor desktop screenshot differences are caused by live squirrel animation, not water suppression.

## Independent geometry and dry-shore measurements

- Full logical mask SHA-256 `1c37082ce71f5f99864c39abcbbb297866a6bbebfe339d42252301199534c857` unchanged from `14b1f6f`. Accepted geometry SHA-256 `34777b2c46a70ee5f966b9b2f369353956d59620af53e759eb0210b5016f58f1`.
- All seven actual visible-water body cell-centres255; bridge middle6,1=255, dry endpoints5,1 and7,1=0.
- Independently reconstructed free interiors from actual convex polygons: zero nonzero visible-water alpha beyond1px raster boundary tolerance. No water expansion onto playable ground.
- Independently reconstructed18px Euclidean free-polygon cores: **zero RGB changes** relative to canonical dry source.
- Dry boundary RGB edits1819 pixels; independent maximum distance to an exposed logical-water edge7.083117px, below allowed12px. Cyan-color diagnostic finds zero changed boundary pixels matching the stated blue/green heuristic. Color checks supplement visual inspection; they do not define terrain.
- This candidate intentionally permits boundary dry-ground changes. It is **not** described as old whole-free RGB-identical.

## Actual input, save and completion

Two independent runs use normal mouse and native CDP touch events respectively. Each places the full accepted solution through the tray/buttons/actual cells, then reselects the full three-cell instance, rotates pending preview, attempts an invalid move, cancels, moves, undoes, returns, undoes, reloads, checks the route and completes the actual normal-motion walk/dialog/result. Thirteen road/owner/clip states per run assert exact confirmed-cell union and unchanged confirmed save during invalid preview. No puzzle layout was injected. Pilot entry seeds only earlier level progress, as recorded by the separate review build.

`water-hit.py` additionally taps **all seven invisible-fill water cells in both input modes** with a land composite selected:14 real pointer interactions each produce invalid preview with byte-identical save. Every water hit polygon retains pointer-events:all despite opacity0. Water rules and hit targets remain intact. Source diff since `14b1f6f` changes water rendering only, not levels/engine/save rules.

Both runs finish without page errors or HTTP errors. Result image shows the actual restored stream, player road and resident. These are emulated browser phone checks, **not a physical phone or family test**.

## Media and limits

`mouse1280-actual-input-audio.mp4` and `touch844-actual-input-audio.mp4` contain actual uninterrupted browser input/walk/result video and that page's captured WebAudio. Named silent WebM and original audio WebM remain. Mux uses a declared estimated creation/navigation/MediaRecorder offset (0.1375s mouse,0.1513s touch), not hardware calibrated; no claim of human AV-sync or complete sound acceptance. Earlier user-approved hiss correction is not re-certified by merely capturing audio here.

Own scripts and machine results: `review.py`, `report.json`, `water-hit.py/json`, `independent-mask.py/json`. Real frames include clean, exact overlay, invalid preview, result, untouched water presentation, native bends and bridge approaches. No production gate changes, main merge or publication. Wide/native visual assessment here is confined to these game viewports, not a replacement for all-scene RC acceptance.
