# Exact whole-frame first-quarter packing / clarity comparison

Frozen review URL: http://127.0.0.1:5365/art/ruta-native-painted-production-v1/e-quarter0/packing/review.html . This is phases0..11 ONLY, never a full gait loop. Default paused; play uses28.8fps for12/28.8seconds then stops at11. Explicit user replay can restart the quarter. No automatic11→0 loop.

## One grid and immutable RGBA

The raw1295×1214 PNG is unchanged. Measured α>128 actor bounds show that330×400 at raw origin0,0 also clips third-row crowns (rawy797..799). The selected ONE shared source grid is origin(0,−11),pitch330×400,4×3. Pad the whole raw canvas TOP11 and RIGHT25 to1320×1225; no individual actor moves, resizes, alpha fitting or cleanup. Large components: exactly12 atα>16 and12 atα>128, minimum margins7px/8px. Tiny antialias fragments are separately enumerated; per-frame full α>16 pixel bounds/margins are also retained.

All originalRGBA pixels, including otherwise invisible noise, are byte-exact in the padded atlas at(0,11). Every saved330×400 cell decodes back to its exact atlas pixels; hashes are recorded. The bottom25atlas rows outside the three frame rows retain the remaining raw pixels unchanged (maxalpha1), rather than being removed. No red-speckle cleanup. Frame extraction uses only common grid rectangles, not per-actor cropping.

## Same apparent size, different source detail

Comparison uses the old accepted painted phase0 as one **static** calibration: match its α>128 silhouette height and top-centre with one global scale/translation. New sourceS=.5127893376456061, shared origin(31.47876740065729,61.04612777874709), identical for all12. Old uses its frozen head trial. This display-only calibration is explicit, not native Root/foot registration, a motion fix or individual height fitting. PNG assets stay original-size. A byte-copy old-reference-manifest.json pins old metadata; atlas provenance remains hashed.

Both panels use single-pass DPR-aware Canvas2D high smoothing and320×400 CSS, logical256×320. AtDPR2 backing640×800. On actual author DPR2phase0 screenshot the newer source has visibly cleaner ink edges, boot laces, hair/garment and bag details at the SAME apparent character height; the old source remains softer. This is a bounded image-quality observation, not a quantified temporal-stability pass. Large source pose/identity still needs independent review.

Author static observation of all12: consistent young Ruta look, copper waves/cream blouse/olive vest/bow, one visible rounded satchel/strap, sequential arm/knee progression. No obvious whole-character identity swap, missing hand or second bag. The generation references accepted painted poses rather than native bone geometry, so exact physical joint/sole identity is not certified. Face is partially side-occluded.

## Actual browser smoke

DPR1 and2, actual pause/scrub/replay controls: page starts paused0, both canvases have expected backing, phase0α128 rendered height agrees within2physicalpx, play reaches11 and stays11 after an extra600ms, keyboard Home returns to0 paused. No page errors. browser-smoke.json and actual screenshots retained. No source/runtime edits, no new imagegen, no full48 or no-slip claim.

Reproduce pack.py with Python/Pillow. Serve repository root on127.0.0.1:5365 and run browser-smoke.py with the existing Playwright environment. All writing stays in this packing/ directory; raw/refs/prompts/accepted gait and old assets remain read-only.
