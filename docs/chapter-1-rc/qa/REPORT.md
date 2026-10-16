# Independent runtime audit, #37 — 2026-10-17

**Follow-up:** successful native touch drag/pan, keyboard, restart/replay/reset, reduced-motion completion and additional recovery checks are recorded in `runtime-extra/REPORT.md`; this earlier baseline remains preserved.

**Status: partial QA passed; chapter release acceptance BLOCKED.** Reviewer is independent of runtime, data, art and audio authors. This report does not complete #37.

## Builds and provenance

- Full actual-input playthrough and interaction suite: `cf3ce616ad470df08b884915f0875af3b5410e47`.
- Final focused audio/prologue smoke and rebuilt production bundle: `6301537ee497ee78fdc87d0435880fbaa87dfc4f`.
- Own worktree `ruby-village-37`, branch `qa/37-integration`, static Vite preview `http://127.0.0.1:5183/ruby-village/`. No dev HMR. Node v24.15.0. Chromium Playwright emulation, not a physical phone.
- Production intentionally uses layout 1 with matching legacy backgrounds. Accepted layout 2 is tested by the unit suite; it is not silently activated over incompatible old art.

## Results

| Check | Result | Evidence / limits |
| --- | --- | --- |
| Unit suite | PASS, 71/71 | `test-output.txt`; latest integrated commit |
| TypeScript and production Vite build | PASS | Both baseline and latest build; latest JS103.17kB / gzip31.60kB |
| New profile, six prologue frames, eight puzzles | PASS | `playthrough/browser-report.json`; mouse tray/rotate/cell/place/check, no injected layouts |
| Every before/after dialog and level completion | PASS | Same continuous run; all eight complete screenshots, final map reached |
| Actual audiovisual recording | PASS, baseline effects only | `playthrough/chapter-playthrough-with-audio.mp4`,93.134s, video+audio streams,7,562,042bytes. Predates integrated music/Ruta; not final mix evidence |
| Placement, partial-save reload, return and undo | PASS | `interactions/report.json`; real UI actions |
| Master mute/music/sfx preference persistence | PASS | Real settings controls, reload, persisted values inspected |
| Denied storage and corrupt storage | PASS | New profile still starts and tray remains usable, no page errors |
| v1 progress migration | PASS | Gate/garden/mill retained; well unlocked; bakery remains locked |
| Six landscape viewports plus portrait | PASS for gate visibility/overflow |1280×720,844×390,740×360,915×412,1024×768,1920×1080;390×844 portrait screenshot |
| Eight-scene visual matrix at six sizes | CAPTURED | `scenes/matrix-*.jpg`, unlocked fixture profile; not a second real-input playthrough. During matrix collection bundle rebuild crossed from baseline to latest, so do not attribute all48 images to latest commit |
| Touch rotation/cancel/orientation | PARTIAL | `touch/report.json`: cancellation preserves existing layout, orientation roundtrip no page error. Drag placement was false; harness lift offset42px assumption insufficient. This is NOT recorded as successful drag or a confirmed game defect |
| Latest music load and autoplay | PASS | `final-smoke/report.json`: no AudioContext before gesture, one afterward; music manifest/village/day/sfx return200 |
| Latest audio pause/resume/portrait | PASS | Native WebAudio observer:2active loops →0pause →2resume →0portrait; observer accounts for natural ended events |
| Latest six prologue frames and Ruta | CAPTURED | `final-smoke/prologue-*.jpg`, `gate-approved-ruta.jpg`; external artistic acceptance of appearance is not approval of walking |

## Findings and remaining acceptance work

- P3 stale HTML description said three puzzles. Reported to coordinator, fixed in `bfc2ea8`; latest build contains eight. No other confirmed runtime P1/P2 defect found in this limited audit.
- Latest prologue1280×720 visibly has plain dark green sidebars about134px each and flat SVG basket artwork. This remains unfinished #47/art acceptance; see `final-smoke/prologue-1.jpg`.
- Release blocker: matching final eight-scene art/data integration, full NPC portraits/poses and accepted directional walking remain incomplete. Legacy captures cannot approve the final artwork. Legacy stream image still visibly contains a small background flag; inspect replacement art against the explicit no-flags criterion.
- Re-run full actual-input eight-level walkthrough with final music, art, characters and animation after their atomic integration. Current continuous recording predates music; latest focused smoke proves music loading/lifecycle only.
- Still pending: successful real touch drag at native lift offset, tray swipe/last item, keyboard/focus, reduced-motion journey behavior, repeated/replayed completion/old letter/reset/restart, all save edge cases on accepted layout2, hidden/background tab lifecycle, all audio cues and footsteps sync, loop listening/clipping/mix review, load/size optimization.
- Physical phone/Safari, human listening and family comprehension test: **NOT RUN**. Browser emulation is not equivalent. Use `../release/HUMAN-ACCEPTANCE.md` for human checks.

## Reproduction

Use installed Node with `--experimental-strip-types --test tests/*.test.ts`, then run TypeScript `--noEmit` and Vite `build`. Serve the built `dist` at the documented base. Python environment `/tmp/ruby-rc-tools/bin/python` runs `scripts/qa/independent-{playthrough,interactions,touch,scenes,audio}.py`. The playthrough harness is adapted from the existing author harness; its result is independently executed and supplemented by separately designed behavioral and native WebAudio checks. No script result replaces visual/human acceptance.

Original PNG evidence is preserved. Automatic approval review rejected removal of originals following lossy JPEG conversion; no deletion or workaround was performed. Raw baseline WebM and captured audio are kept alongside the muxed MP4 for provenance.
