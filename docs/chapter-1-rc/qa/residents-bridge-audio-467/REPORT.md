# Independent checkpoint: residents, bridge, audio and pruned export

2026-10-17. Baseline `467eab2`, local QA merge `c1e8318`. Their tracked trees are identical (`git diff 467eab2 c1e8318` empty). Reviewer did not author the runtime changes and made no application changes. Clean Vite production build, separate QA worktree and port 5297; root preview/dist untouched.

**Focused checks pass. This does not approve the final RC or the current rejected gait artwork.** Final map/architecture, water banks, wide backgrounds and replacement gait remain separate acceptance work.

## Runtime coverage

| Area | Independent result |
| --- | --- |
| Residents | 12 scene/viewport runs PASS: garden Rabbit, well Teacher, bakery Baker, stream Squirrel, mill Miller plus Squirrel, post Hedgehog. Present in dialog, puzzle, replay, reload and current-place result; no page errors. |
| Resident anchors/layers | Own audit of actual transformed SVG geometry PASS: all 14 actor instances across desktop/landscape have feet outside every playable ground polygon, live in the resident layer and inherit pointer-events:none. This tests feet, not a pixel-perfect alpha silhouette intersection. Full puzzles remain solvable through actual input. |
| Three-hex bridge | Both stream/mill, both viewports PASS: one painted deck, three transparent but interactive hit cells, correct restored result, hidden technical result layers. Overlay/art pairs captured. Art-only pictures temporarily hide water debug overlay and terrain symbols solely for inspection, as named; ordinary screenshots retain actual game layers. |
| Pruned production export | 16 actual full routes (8 × 2 viewports), 12 prologue frames and 2 maps PASS, zero HTTP errors, failed requests or JS errors. No injected progress/layout in this all-eight run. Reduced-motion enabled through settings for resource/state coverage, so this is not normal gait acceptance. |
| Tests/build | 98 tests PASS; TypeScript PASS; clean Vite production build PASS. |

Desktop is 1280×720; landscape is Chromium emulation at 844×390. Resident/bridge focused harnesses seed only prior progress to reach the scene; every puzzle placement is performed through tray, rotation, cell and Place controls. They then solve and win through real UI.

The harness repetition uses existing author scripts with only URL/output path redirected, orchestrated by `scripts/qa/independent-467-harnesses.py`. Independent reviewer separately inspected actual garden, mill and stream screenshots and performed its own anchors and native-audio audit. The legacy garden's table remains a pending artistic scale issue; presence of a Rabbit does not close every #62 garden concern.

## Native WebAudio and byte-preservation audit

`scripts/qa/independent-audio467.py` observes actual native AudioContext, AudioBufferSourceNode starts/stops and AudioParam ramps; it does not substitute a fake backend.

- Before first user gesture: 0 contexts.
- Playing: 1 running context, exactly 2 loops (12s mono ambience and 106.6666s stereo music).
- Pause: 0 active loops; resume: 2, with the same single context.
- Actual mute/unmute controls target master 0 / 0.7. Native keyboard adjusts music and SFX independently to 0 and restores defaults; no lowered master workaround.
- 42 files under delivered music, non-ambience SFX and music source assets hash-identical to the commit before the noise-only change. Includes all music masters/MIDI/soundfont and music manifest. Audio module itself is byte-identical, including master/default-bus gains.
- Five intentionally replaced ambience recordings differ. Each former original WAV is preserved byte-for-byte under `art/audio/sfx/noise-review-before/`.
- All 100 excluded export files still exist in source `public/` with the recorded sizes. Export keeps 64,806,028 bytes and omits 79,318,116 candidate/archive bytes; source repository is unchanged by pruning.

See `audio-and-source-audit.json` for exact SHA-256 values, native node snapshots and preserved source list. Network requests in this native-audio test returned no errors.

This verifies operation and preservation, **not subjective listening**. Perceived noise removal, music balance, click-free transitions and child comfort still require actual human listening; marked NOT RUN here.

## Evidence

- `residents/*-{dialog,puzzle,result}-*.jpg` and `residents/report.json`: six populated scenes, two viewports, replay/reload assertions.
- `anchor-audit.json`: independent native SVG foot/layer results.
- `bridges/*-{mask,art,result}-*.jpg` and `bridges/report.json`: both bridge contexts.
- `pruned-export/browser-report.json`, `export-assets.json`, `map-*.jpg`: actual full traversal and request coverage against pruned dist.
- `audio-and-source-audit.json`: real node lifecycle and content hashes.

These checks add no new claim of physical phone/Safari, family testing, human soundtrack listening or final gait/art acceptance. They do not authorize merge/publication. After final scene/layout/gait integration, repeat the affected checks and full independent acceptance.
