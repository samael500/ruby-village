# Painted head-registration diagnostic: independent browser review

Scope: author bb845ed / root 34f8384, frozen HTML and manifest hashes in report.json. Actual Chromium desktop 1280×800, baseline/clasp/head each played 4.2 seconds, followed by paused screenshots of 7/8, 15/16, 23/24, 31/32, 37/38, 39/40 and 47/0. Silent actual browser recording is linked by report.json. Page errors: none. This scoped comparison does not repeat the earlier landscape/control audit.

Recommendation: head registration is a useful improvement over baseline and clasp; retain 48 phases / 28.8 fps as the next candidate. This is **not motion acceptance**. Maksim accepted the painted appearance but explicitly rejected clasp-trial trembling/jerking. That feedback is not superseded by numerical registration results.

Viewed actual browser screenshots and decoded actual recording sequence (video-sequence.jpg). Baseline 39→40 has the dominant upward jump. Clasp reduces it but introduces residual head movement; head registration substantially reduces the conspicuous displacement at 39→40 and stabilizes 31→32. The head candidate still changes hair/fringe/face contours and the body/limb silhouette across poses. Whole-frame translation cannot repair these internal differences. Inspect 47→0 as a closure pair too; absence of the original large jump is not proof of a seamless painted face or physical foot contact. No cumulative drift claim is made: a periodic translation table can still contain undesirable cyclic wander.

Head and clasp use the same immutable painted pixels and fixed scale. Their translations are diagnostic image registration, not certified physical Root anchors. Native phase/heading and drawn anatomy are not asserted identical. Eye annotation statistics from the author are supporting evidence only, with substantial annotation uncertainty; they are not our perceptual acceptance criterion.

## Cadence study

Frozen root ff5ee32 / author 0072c88 study was independently opened at the root-served URL. Actual head-mode 48/24/16 playback, 4.2 seconds each, is recorded under cadence-study/. Same cycle duration, source frames and registration; fewer unique poses only. Decoded sequences show larger held-pose steps at lower rates. Retain 48 rather than presenting a menu to the user: reducing frequency does not address internal face/hair changes. The capture script and results retain actual state and recording provenance. Its HTML hash is a serialized DOM hash, not a source-file hash.

Viewing limitation: the reviewer inspected actual browser stills and decoded recording sequences, not a real-time human display playback. Browser video is sampled/encoded and cannot establish native 28.8-fps perceptual acceptance. The live page remains the reference for user judgement. CSS subpixel interpolation/double scaling may contribute to shimmer, but this audit does not identify it as the cause. No game, physical-phone, no-slip or final art acceptance.
