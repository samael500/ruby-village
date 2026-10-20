# Independent runtime audit extension, #37

Tested QA merge `4ebab5c4412160ff0dc90ddbbb5f2542d642e74d` (includes integration audio race fix `b6cf21d`). Own rebuilt static production at5183. **Runtime checks below pass; final art/character acceptance remains blocked.**

-74/74 unit tests, TypeScript and production build pass.
- Native touch placement now independently PASS: selected tray piece, six rotations returning to original orientation, vertical lift50px followed by diagonal drop to valid anchor. Prior straight diagonal crossed native horizontal pan threshold and generated pointercancel; this was a harness correction, no game code changed. Measured cell40×30px; lift42px. Cancellation preserves layout; portrait/landscape roundtrip no page errors. See `../touch/report.json` and original screenshots.
- Native horizontal tray swipe at740×360 moved scrollLeft0→79px. Last item `gate-7` selected by actual touch, `aria-pressed=true`; `tray-pan.json` and `last-tray-piece.jpg`.
- Keyboard focus plus Enter on tray, rotation, field cell and placement PASS. This checks keyboard actionability, not a complete accessibility audit or every focus trap.
- Restart cancellation preserves placed tile; confirmed restart clears board and survives reload.
- OS reduced-motion preference: full real-input gate solution reaches post-journey dialog in129ms; replay78ms. Both show one completion, disable check while completed, retain restored gate on map. No duplicate completion observed in this scenario.
- Reset cancellation retains unlocked progress; confirmed chapter reset locks garden again and persisted completed array is empty.
- Complete-profile fixture: old invitation opens and closes, ending returns to eight-node map; chapter2 is not fabricated.
- Future layout version999 and invalid saved placement fixtures retain gate completion and garden availability. This checks observable recovery, not every malformed input permutation.
- Six-frame prologue back/skip exercised before these checks; independently validated text changes backward.
- No page errors in the extended runtime scenario.

`report.json` contains per-check results and durations. Scripts `independent-runtime-extra.py`, `independent-touch.py`, `independent-tray-pan.py` reproduce real inputs; only explicit save-fixture cases inject stored profiles. Baseline independent full eight-level run is documented in `../REPORT.md`.

## Genuine background-tab limitation

`independent-background.py` opened another actual target and brought it to foreground. Headless Chromium kept the game document `visible` / `hidden=false` throughout. No document.hidden override or synthetic visibility event was used. Therefore **background audio lifecycle remains NOT RUN**, rather than claiming a successful real background test. `background.json` preserves observations.

## Remaining gates

Final matching scene/data integration, NPC/poses/walking, updated final8 audiovisual walkthrough, artwork inspection, full audio/mix listening, physical phone/Safari and family comprehension remain pending. These runtime passes do not complete #37 or replace Maksim's review. Focused module audio checks from the earlier report are supplemented by the74-test suite, including the new asynchronous music pause regression; no new full mixed video was recorded in this extension.
