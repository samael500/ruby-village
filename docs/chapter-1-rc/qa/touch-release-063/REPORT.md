# Independent rapid-touch recheck #37 / #61

2026-10-17. Integration baseline `063bb19`, isolated worktree `ruby-village-37-runtime`, local merge `c9a6b2b` includes only prior QA additions. Clean production build served on the QA-only port 5297. Root source/worktree/dist were not edited.

**PASS: eight independent native-touch trials**, in addition to the author's full 10-case regression and 48-tap timing test, repeated independently.

## Independent new scenarios

`scripts/qa/independent-fast-touch.py` starts each trial with an empty browser profile and completes gate through actual UI, then enters garden. It does not inject either solved layout or saved progress. All touch drags/taps use Chromium CDP native input; mouse, Enter and Space use native Playwright input.

Six drag trials: real invalid drop → release → five successive rotation touch releases → alternating valid drop or cancel. Each rotation verifies the expected icon orientation 1,2,3,4,5, so missed/double activation cannot hide in a six-rotation cycle. Two additional select-mode trials verify rapid rotation followed by valid cell → Place or Cancel. Every trial then switches to another tile and verifies mouse click, Enter and Space after touch each activate normally.

There is **zero explicit hold/inter-tap sleep** in these scenarios, and no 500ms workaround. Native protocol calls and state assertions still take normal browser execution time; this is not a claim of physically simultaneous inputs. Each new tap obtains the current control bounds because the dock changes with selection/placement. Committed DOM is observed after rendering; an early test-harness assertion initially sampled the valid drop before its deferred render, and was corrected by capturing/observing the settled DOM rather than introducing a fixed input delay. The final run passes all eight trials.

- `independent/report.json`: all 8 cases, exact orientations, action, zero explicit delay, keyboard/mouse result, no page errors.
- `independent/rapid-drag-valid.mp4`, `rapid-drag-cancel.mp4`, `rapid-confirm-place.mp4`: real input recordings, no audio track.
- `independent/trial-*.jpg`: actual game states.

## Existing author scenarios repeated on this independent build

- `scripts/placement61-browser.py`: **10/10 PASS**: mouse/touch, drag/select, composite/bridge plus each device lifecycle. Includes capture release, undo/cancel/moved-piece restore, pointercancel, pause/reload, exact confirmed layout. This harness uses saved-state fixtures to enter a specific scene and setup lifecycle layouts; it is clearly distinct from the no-fixture independent scenarios above. `full-regression/browser-checks.json`.
- `scripts/qa/fast-touch-buttons.py`: **48 native touch taps PASS**, at 100/150/250/500ms gaps, then Enter, Space, mouse. Only URL and output path were redirected to QA build/evidence. `author-fast-recheck/report.json`.
- 98 tests PASS, TypeScript PASS, Vite production build PASS.

The first attempt to run the existing harness encountered a stopped QA HTTP server; it was restarted and the complete successful run produced the committed report. No application failure is inferred from that infrastructure attempt. The old-code failure rate was supplied by the author, not independently reproduced by this recheck.

## Limits

This is Chromium landscape touch emulation at 844×390, plus desktop mouse in the full regression. Physical phone/Safari, family playtest, human audio listening and final v9 art remain NOT RUN/not accepted. No final RC approval, merge or publication is implied. Original PNG/WebM captures remain locally preserved; curated JPEG/MP4 evidence is committed. No application code was modified by this reviewer.
