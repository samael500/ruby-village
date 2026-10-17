# Issue 61 — invalid placement remains editable

Core commit: `f7aac88`. Branch: `fix/61-invalid-preview`, based on integration `09bd466`.

An intentional invalid drop now keeps the selected piece, rotation and red field preview. The player can rotate and re-grab this preview, then confirm a valid destination. An explicit Cancel or Undo of the pending preview preserves an already confirmed piece. System pointer cancellation restores the gesture snapshot. Confirmed layout serialization accepts only `validPlacement`; an invalid preview never becomes saved layout.

The previous `finishDrag` always restored the pre-drag anchor/rotation after an invalid release, and field pointerdown could grab only a confirmed piece. The fix separates provisional release state from validated confirmation and allows grabbing the provisional footprint.

## Verification

- 78 automated state/game tests passed, including four new tests for retained invalid rotation, immutable confirmed placement, bridge validation and system cancellation/outside release.
- TypeScript `--noEmit` and Vite production build passed.
- `scripts/placement61-browser.py` exercises the actual production build with native Chromium mouse input and CDP native touch input, both drag and select modes, compound pieces and bridges. Saved-session fixtures open reproducible levels; all placement interactions and assertions use the live UI and persisted confirmed layout.
- Browser screenshots show red invalid and subsequent valid confirmed states. The mouse video records the passing sequence; the touch video deliberately preserves the fast-tap missing-click diagnostic. Videos record actual browser input, without an audio track. Browser emulation is not a physical phone test.
- Independent integration QA was performed by a separate agent; its evidence belongs to the coordinator's integration report, rather than being duplicated as this branch's result.

Reproduce: build and run Vite preview on `http://127.0.0.1:5188/ruby-village/`, then `/tmp/ruby-rc-tools/bin/python scripts/placement61-browser.py` (Playwright and Chromium required). The script derives fixture layout version from the branch, rather than assuming the later art migration version.

During harness development, an initial wrong fixture layout version opened the wrong level. A later wait for changed icon geometry timed out on a rotationally symmetric bridge. These were harness mistakes; the final script uses the correct branch version,80ms native tap duration and120ms gaps. Its fast run can reproduce the missing-click case and writes the failure trace before raising. The 500ms run passed all eight main cases and both lifecycle cases (`browser-checks-500ms.json`). A second native-CDP touch run uses 80ms press duration and 120ms gaps; all four main touch cases passed, with complete pointerdown/up/click timestamps and preview before/after in `*-rotation-events.json`. Every five-click compound rotation produced five preview changes. A repeated fast native-CDP run reproduced the discrepancy with a complete trace: five right-button pointerdown/up pairs (about92ms press), but only four native click events. The first tap after the drag did not receive click; every delivered click changed preview geometry. See `failure-rotation-events.json`, `failure-touch.png` and `touch-fast-missing-click.webm`. This is not five delivered clicks producing four rotations. The Chromium click-suppression cause remains unproven; no runtime timing workaround was added. A fast-tap lifecycle Cancel assertion failed once on this older branch; this branch does not claim that particular fast lifecycle sequence passed. Independent QA on current integration reports PASS; no runtime workaround or timing restriction was added.

No remote push, merge or publication was performed. Ownership of `src/main.ts` was returned to the coordinator after the core commit; this evidence commit does not change runtime code.
