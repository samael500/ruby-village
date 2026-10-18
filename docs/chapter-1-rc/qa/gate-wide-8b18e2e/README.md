# Independent B2 final repeat — #48 / #62

Reviewed fix `8b18e2e`, cherry-picked alone onto the frozen previous QA snapshot (local source `eb9a642`). **Scoped PASS: B2 gate/Ruta dialogue framing.** This resolves the clipping reproduced in `953b00f`; B1 bakery separation remains covered by that earlier report. No whole-chapter/production approval.

Two fresh actual normal-motion gate runs: mouse1280×720 and native CDP touch844×390. Actual puzzle placement, normal walk, both after-pages, intro/replay/reload, six prologue frames per viewport and results complete with zero page/HTTP errors. Retained18 actual state screenshots,12 prologue captures and two uninterrupted silent browser videos. No saved layout/win injection.

Own `visibility.py` decodes the real Ruta raster frame/idle alpha and actual open/closed-gate alpha, maps their bounds through measured runtime matrices and checks their **combined union** against the available board and dialogue top. All10 intro/replay/after-dialogue states pass; the smallest union margin to the tested viewport/panel boundary is20.519232px. This includes the intro Ruta and narrative-focus gate, not just Ruta's arrival position. Both after-pages now show the whole open gate leaf above the paper panel on desktop and landscape phone.

Main board background, resident-world and foreground matrices agree. Collection explicitly scopes to `#board`, excluding hidden prologue/result clones. The actual wide raster covers the complete main SVG in all18 captured states; no empty side/top/bottom bands were observed in the real frames. The original accepted ground geometry and logical goal are retained; only the shared fit/offset changes for conversation. Prologue and the own-scene result remain intact.

The corrected runtime preserves3272×1200 wide dimensions and passes original-rectangle offsets separately. No author runtime/source edits were made by this reviewer. Own Vite production build passes and served bundle hashes are recorded. Exact independent scripts/raw measurements: `review.py`, per-case reports, `visibility.py/json`, `served-build.json`.

Private four-scene activation remains confined to QA, is not included in this evidence commit, and must not enter production. Physical phone, family, audio, new MPFB appearance/motion, connected-road rollout and complete chapter acceptance remain outside scope. No main merge/publication.
