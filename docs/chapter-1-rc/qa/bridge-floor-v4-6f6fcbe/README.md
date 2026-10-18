# Independent bridge floor-v4 game review — #45 / #46 / #62

Frozen pilot `6f6fcbe` / coordinator material `33d94ef`, actual port5308. Separate evidence-only worktree. **Scoped PASS: three-cell clipping, shared camera, water/shore registration, real input and current-material playback. Artistic acceptance remains pending.** This checks floor-v4, not the superseded floor-v3. No author runtime edits or production activation.

## Actual game / input

Two functional runs use mouse1280×720 and native CDP touch844×390, normal motion. Each has19 asserted states: accepted-solution placement via actual tray/rotate/cell/place controls; whole bridge selection;180° rotation and undo; moving the bridge from accepted water6,1 to legal water6,0 and undo; return and undo; whole land-composite selection/invalid preview/move/return/undo; real reload, byte-identical restored save, actual route walk/dialogue/result. No layout/win injection. Earlier completed progress is seeded only by the existing explicit stream review pilot. No page/HTTP errors.

The confirmed road union and exact land clip agree with real confirmed owners throughout. Invalid pending actions leave the confirmed layout/save unchanged. Whole-instance ownership stays three cells; move/rotation/return/undo restore the correct art and save without phantom paving or duplicate placement.

`review.py/report.json` and two actual silent WebMs cover reload. Clean/mask-overlay/invalid/moved/result frames are actual browser captures. The optional clean-view CSS only hides obsolete water fills/glyphs already absent in this pilot; logical overlay is diagnostic-only and does not change input.

## Independent exact geometry / camera / water

`geometry.py` makes ten further actual DOM readbacks across both input modes, solved/rotated/moved/undo states. Three bridge clip polygons equal the three actual owning-cell polygons to≤`.000038147px`. Independent accepted native polygons projected through the painted-world camera agree to≤`.000135497px` (browser SVG float precision; tolerance.001px). Bridge parent is the same ground plane as all puzzle cells. There is one native material registration before that shared projection, no separate CSS displacement.

Actual image URL is floor-v4 and served bitmap bytes match the source asset SHA recorded in `geometry.json`. Served JS/CSS hashes are retained. Visual review of clean desktop/landscape frames and close-up shows the current wooden three-hex deck connected to confirmed paving; water crosses beneath the middle and both ends remain on dry shores. No bank foreground was seen crossing the deck, nor visible detached approach ends at the accepted placement. This does not approve the optical/painted treatment of the distant coping for the user.

Full logical water mask remains SHA-256 `1c37082ce71f5f99864c39abcbbb297866a6bbebfe339d42252301199534c857`. Actual body centres all seven water cells255, bridge6,1middle255 and5,1/7,1ends0. Own polygon-derived free-interior water leakage0;18px free-core RGB changes0. Permitted dry shoreline boundary edits1819pixels, maximum depth7.083117px≤12. This is not the superseded whole-free RGB0 claim. Water/shore geometry is unchanged by the material update.

## Recommended current-material AV evidence

Use **`actual-av-no-navigation/mouse1280-actual-input-audio.mp4`** and **`actual-av-no-navigation/touch844-actual-input-audio.mp4`**. These are separate real uninterrupted-page runs with the same bridge/control operations, actual walk/result and that page's captured WebAudio. Reload is intentionally tested in the separate functional run. Original silent WebM and actual audio WebM remain beside each MP4.

An initial inherited harness incorrectly tried to mux audio across `q.reload()`: its in-page recorder/performance origin reset and only the second document's audio remained. That AV was rejected, wrong MP4/audio files removed, and diagnostic timing metadata retained in `rejects/`. Functional input/save observations remain valid. `review.py` now produces functional silent evidence only; `av-demo.py` provides uninterrupted AV.

The final MP4s decode H264/AAC with real nonzero audio. Observed first-running/recorder-start offsets are.670791s mouse /.389112s touch; video32.24s/audio30.683s and video25.64s/audio24.380s, with approximately.88s silent terminal video tail. `media-check.py`/`actual-av-no-navigation/media.json` retain hashes, clocks, durations and limits. This is browser-clock alignment, **not hardware synchronization or a human listening/AV-sync certification**. No fresh claim about hiss removal or final audio mix is inferred from file presence/RMS.

## Limits

Only stream is tested here, including a second legal stream bridge anchor; this is not a mill bridge result, complete chapter or final MPFB gait acceptance. Landscape phone is browser emulation, **physical phone/family not run**. New road/material artistic acceptance, other scenes, final character resources and whole-chapter RC remain separate. Pilot watermark says NOT RELEASE; global production gate remains closed. No main merge/publication or other session process changes.
