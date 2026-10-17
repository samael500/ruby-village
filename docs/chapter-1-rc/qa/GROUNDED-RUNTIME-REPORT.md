# Independent runtime review #37, #61, #62

Date: 2026-10-17. Reviewer: `qa_runtime`, independent of runtime/art authors.

This is a **runtime checkpoint, not final chapter/RC approval**. Production deliberately uses layout 1 with its matching legacy art. Accepted layout 2 and final v9 art were not activated or certified here. No merge, publication, remote push or PR creation was performed.

## Exact builds and method

- Main test baseline: `6637b8c` (`integrate/46-chapter-1` snapshot).
- Completion-background follow-up: root `5dc2036`, cherry-picked locally as `237162a`; tracked trees are identical (`git diff 5dc2036 237162a` empty).
- Separate worktree: `ruby-village-37-runtime`, branch `qa/37-grounded-runtime`.
- Clean production build served from its own `dist` at `http://127.0.0.1:5297/ruby-village/`. Root preview/dist remained untouched.
- Real Chromium mouse, native CDP touch drags, and locator touch taps. No solution/layout was injected into application state. Reference solution JSON only determined the real tray/rotate/cell/place actions.
- Desktop 1280×720. Landscape phone emulation 844×390. This is not a physical phone/Safari test.

An initial run accidentally targeted an already occupied port 5188. It was stopped; the exact-build run on 5297 replaced every curated full-run frame, report, audio and MP4. Only the report identifying 5297 is evidence below. Test-script development also caught incorrect test rotations; final compound/bridge reports are from the corrected real-input runs.

## Results

| Check | Result and evidence |
| --- | --- |
| Eight puzzles, normal motion, prologue | PASS: actual mouse input, six prologue frames, eight wins, no page errors. `grounded-runtime/browser-report.json` |
| Actual walking in the game | PASS on all eight canonical routes: `data-motion=walking`, start → walk → stop-L/R → idle; native route clocks monotone and finished. Durations 19.2–24s, rather than the former 3.5s glide. `grounded-observer/summary.json` |
| Directions covered by canonical solutions | e, se, ne, nw. **w and sw were not exercised on actual puzzle routes**; six-direction source/stand checks do not replace that missing coverage. |
| Pause/resume while walking | PASS on gate: route time stable over 800ms after pause modal settled, then route resumed and completed. No endless clock wait. Additional 5dc2036 landscape touch gate run: actual viewport rotation to portrait held clock stable 1500ms, landscape return advanced and finished. `grounded-walk-portrait/report.json` |
| Audio | Real browser master stream recorded and muxed with its real video. Foot-stone and foot-wood variants were requested during the all-eight walk. Captured MP4 has a non-silent audio track (mean −38.1dB, peak −15.0dB). This does not claim subjective listening/mix acceptance. |
| #61 mouse and touch invalid release | PASS: single stone, composite garden-a, bridge; invalid preview retained after release, three rotations retain it, capture released, move retained preview to a valid position/drop, reload keeps confirmed placement. `grounded-input`, `grounded-composite`, `grounded-bridge` report JSON |
| #61 confirm mode/cancel/persistence | PASS: invalid Place disabled, cancel new preview, cancel moved placed piece restores original without duplication; pause → portrait → landscape → reload serializes confirmed layout only. `grounded-cancel/report.json` |
| All-eight landscape touch scene pass | PASS: real touch taps, correct eight results, hidden narrative ground and controls, no page errors. Reduced-motion enabled explicitly for this separate scene pass; it does not establish phone walking quality. `grounded-phone-scenes/report.json` |
| Result background defect | Baseline 6637 showed technical grid/tray behind the result modal. Author's known fix 5dc2036 was independently retested on all eight landscape results: controls/grid display:none; current restored place remains in result. |
| Unit/type/build | 96 tests PASS; `tsc --noEmit` PASS; Vite production build PASS. |

## #62 acceptance status

| Item | Independent status |
| --- | --- |
| 1 Rabbit/table scale and duplication | NOT ACCEPTED: legacy garden still has the large background table; final art and resident placement pending. |
| 2 Story stone readability | Prologue recorded, but no final artistic acceptance or pixel-size threshold is claimed. |
| 3 Fully hidden technical field in story | PASS in actual narrative scenes at 844×390; ground/controls display:none, not reduced opacity. Victory dialogue intentionally retains the restored road and hides grid. |
| 4 Real walking and calm speed | Runtime checkpoint PASS on eight actual paths, four directions. Final art/turn quality and w/sw actual-path coverage remain open. |
| 5 Invalid release retained | PASS for exercised single/composite/bridge mouse and native-touch cases; system-level browser interruption and all possible edge/overlap orientations are not exhaustively covered. |
| 6 Bridge/stream visual alignment | Mechanics and walking pass on current legacy stream/mill. Final v9 water/bank/mask art remains outside this approval. |
| 7 Map trails | Actual completed map captured. Procedural irregular dirt/individual charoite paving and timber crossing are present. At 844px viewport paving reads as a thin purple trail; artistic acceptance and final map-to-level architecture comparison remain open. |
| 8 Eight current-place results | PASS: eight actual restored scenes and roads; baseline background grid/tray fixed and retested on 5dc2036. |
| 9 Residents in playable scenes | NOT ACCEPTED: portrait dialogue is present; full scene residents/anchors are still pending final-art integration. |

The additional map/level architectural consistency request is not fulfilled by the legacy-art checkpoint. User's original screenshot files were unavailable and were not claimed as viewed. All evidence here was captured independently from the game.

## Evidence

- `grounded-runtime/chapter-playthrough-with-audio.mp4`: 185.339s, actual gameplay and browser audio; no added soundtrack. Desktop, 6637 baseline.
- `grounded-runtime/walking-contact-sheet.jpg`: distinct sampled gait phases and turn from that actual video.
- `grounded-input/input-0.mp4`, `input-1.mp4`: single-stone desktop/touch release workflows, no audio track.
- `grounded-bridge/input-0.mp4`, `input-1.mp4`: real-input bridge workflows, no audio track. Reduced-motion enabled while reaching stream.
- `grounded-phone-scenes/*-story.jpg`, `*-solved.jpg`, `*-result.jpg`, `map-complete.jpg`: latest 5dc2036-equivalent landscape scenes.
- `grounded-observer/report.json`: raw sampled native marker state and native audio request URLs; `summary.json` is the concise aggregate.

PNG/raw WebM sources remain on disk in the separate worktree; curated JPEG/MP4 evidence is committed. No source captures were deleted.

## Remaining required acceptance

Final v9 scenes plus layout 2 must be integrated together, then all-eight input/walking/bridge/results/save migration reviewed again. Final scene residents and map/scene comparison need a final integrated pass. Portrait orientation during active walking passed on the current layout-1 gate; repeat after final integration. Physical phone, iOS/Safari, real background-tab suspension, human soundtrack listening, and family playtest are **NOT RUN**. This checkpoint does not replace release preparation #49.
