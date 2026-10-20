# Independent joined-road STREAM PILOT review — c64b249

**Status: functional checks PASS; artistic pilot needs further work. NOT FINISHED, NOT RC, NOT production activation.** No rollout to the other seven scenes is approved.

Separate checkout `/tmp/ruby-qa-stream-c64b249`, branch `qa/37-stream-road-c64b249`, created at immutable review commit `c64b249`. Repository AGENTS.md, coordination and road contract read. Real TypeScript/Vite production build passed (89.1MiB exports). Own server5298; root5306, integration5286 and user5180 untouched. QA changes only; integration layout1 gate remains outside this branch.

## Review gate and data provenance

This is an explicitly watermarked, non-release branch. `review-gate.patch` records the source patch: connected-road pilot flag true, layout version2 in this review only, activation audit restricted to accepted stream and the full-polygon **visual** audit blocker filtered out. Camera, endpoint, resident-anchor and wide metadata checks still run. This is deliberately weakened review gating, not evidence that the unfinished visual audit passed. Index supplies the four-prior-level progress fixture and a visible non-release watermark; next/result navigation controls are hidden. The harness adds no layout or progress fixture and never injects a rendered solution.

Solution comes from `art/chapter-1-v9/layers/water/stream-pilot/manifest.json`, skips null stream-b. Three placed pieces: stream-a at8,1/0; bridge at6,1/0; stream-v6-a at4,1/2. Actual solution cells, current owner attributes and clip polygons are retained in report.json.

## Findings requiring further art review

**P1 — artificial polygon-stepped river banks.** The actual clean scene follows sharp hexagonal boundary corners, especially below the bridge through6,2→5,3→5,4. Stones/grass decorate the bank, but the silhouette still reads as a hard geometric cutout rather than a natural integrated stream. This is visible on desktop and landscape; see `mouse1280-bank-road-crop.png`, both clean full frames and paired water overlays. Correct logical masking and zero interior leakage do not establish natural bank artwork. Root was notified; this is not called finished.

**P2 — ground-to-paving perimeter remains a clipped flat edge.** The merged stone material is continuous, but its outside perimeter is chiefly a thin uniform stroke against grass. At the bridge approach it lacks a visibly painted earth/paving transition or grounded bank landing treatment. Crops show the current appearance clearly; this is an artistic completion finding, not an extra-cell/input defect. No author asset or runtime fix was made by QA. Further grounded-edge/bank treatment and actual-game review are needed before accepting the earth→road→bank→bridge→bank pilot.

No abrupt material-tile border was apparent in the inspected road/bridge crops. The stone texture has its own natural small seams; no extra ownership-hex rim appears inside the merged installed surface. This is a local visual inspection, not a blanket source-texture approval.

## Functional and geometric evidence

`review.py` completes the accepted stream solution twice through actual UI: mouse1280×720 and native CDP touch844×390. It taps tray, rotate, board and Place, without forced click, renderer/layout injection or skipped route. Both normal-motion Check actions reach arrival/result without page or HTTP errors. Native browser touch is emulation; no physical-device claim.

At every captured stage road cell IDs equal confirmed **non-bridge** owners union fixed endpoints1,3 and9,1. Actual SVG clip polygon coordinates independently match the exact corresponding input polygons, not just the data labels. The solution has six land clip cells:1,3;2,3;3,2;4,1;8,1;9,1. Three bridge cells5,1;6,1;7,1 are excluded from the stone surface.

Whole placed three-cell composite selection adds the whole-instance outline. Pending rotation and invalid board destination preserve confirmed surface, outside edge and byte-identical localStorage. Cancel, combined valid move/rotation to0,3/0, undo, return-to-tray, undo and reload are exercised with both input types. Moving/returning changes confirmed clip/edge; undo/reload restores the exact solved road. Pending preview retains the confirmed instance outline; committing clears it. Input ownership stays whole-piece.

`edge-audit.py` derives actual polygon union edge multiplicities independently and compares actual road and bridge path segments at every stage with a bridge. Exact outside boundaries match; shared land/land, land/bridge and internal bridge-hex rims are absent. Returning the bridge-neighbor composite exposes the appropriate outside/cap edge, undo closes it again. These are actual DOM path checks, not only source assertions.

`water-audit.py` uses accepted geometry polygons and actual logical water mask. Bridge middle6,1 alpha255; dry ends5,1 and7,1 alpha0. Initial coarse raster intersection produced46 boundary candidates; analytical polygon distances show every candidate within0.552px of the free-cell boundary under integer and pixel-center conventions, **none beyond the documented1px tolerance**. Both raw result and analytical method are recorded, not rounded away into an unconditional zero-mask claim. No water-mask erosion or game geometry/camera edits were used. This does not pass P1/P2 artistic findings.

## Presentation evidence

Each input case has technical solved, clean solved and paired accepted-water-polygon overlay screenshots in the actual scene camera. Clean view hides **only** technical water-cell fills and ≈ glyph labels; all road/bridge/bank art and watermark remain. The overlay is a separate diagnostic SVG group, removed before interactions resume; it does not alter renderer/layout data. Enlarged crops derive from those real screenshots. Solved and result frames were visually inspected desktop/landscape.

## Actual input and audio capture

Both cases retain the raw silent input/walk WebM, actual browser Opus audio and muxed H264/AAC MP4. Capture hooks only AudioContext construction and the existing connection to its real destination, routing the same output to one MediaStreamDestination. Each run records exactly one AudioContext; no added soundtrack. Mean/max levels: desktop−39.0/−18.3dB, touch−39.1/−17.5dB. Human listening was NOT RUN.

Mux offsets are estimates from page-creation monotonic time, navigation performance.now and MediaRecorder construction: desktop~0.137s, touch~0.079s. They are **not hardware-synchronized** or verified by an audiovisual sync event. Browser recorder/suspended-context timing means audio and video durations differ; media.json reports exact stream starts/durations, and original streams remain available for re-alignment. No claim of sample-exact sync. Video retains its full tail rather than truncating evidence with `-shortest`.

Final art, complete chapter layout2 activation, MPFB/Ruta gait, other scenes, physical phone, Safari/iOS and family playtest remain pending. This scoped result authorizes no main merge/deploy or mass road activation.

Reproduce: build this review checkpoint and serve dist at5298, then run `review.py`, `edge-audit.py`, `water-audit.py` using `/tmp/ruby-rc-tools/bin/python` from repository root. QA scripts and evidence are contained here; the source review gate patch must not be cherry-picked into ordinary integration with this QA report.
