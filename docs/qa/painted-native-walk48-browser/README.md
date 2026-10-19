# Independent painted-native Walk48 review — baseline b06b455

**Mechanical/browser delivery works; painted motion acceptance FAIL: a visible pop at39→40 remains. Do not inherit the preceding native render PASS.** New independent worktree/branch fromb06b455; no source art, runtime, packing algorithm or generation changed. Built-in generation/provenance belongs to root. NPC independently checks identity; this report addresses complete poses, registration/layout and actual loop presentation.

## Actual input and browser proof

Raw1295×1215 RGBA SHA7ce011d665feedb9a22015f59a501c0bcc14e73c83fde0969234e1a18fa20ffb is immutable. Independently verified padded atlas preserves every original RGBA byte; only transparent right/bottom padding is added. Native matched atlas equals supplied48-pose source sheet exactly. Fixed grid is origin0,30, pitch162×200,8×6; no per-frame alignment/scale/warp. The one diagnostic scale1.163156302/translation29.602459,53.313741 is a whole-asset comparison, **not a physically certified foot/root anchor**.

Actual Chromium desktop1280×800 and landscape844×390 runs at `http://localhost:5322/full48/review.html`:0 page errors/request failures/HTTP failures; all48 painted and all48 native source rectangles observed through real canvas drawImage calls. Each canvas has exactly one destination rectangle, so the player is not secretly correcting per-frame drift. Shared40/24s clock,28.8phases/s; pause stable; actual keyboard slider input reaches recorded phases including39/40/47/0; resume and live47→0 observed. CSS canvas aspect matches.8 within browser subpixel rounding. First incomplete harness attempt used an excessively strict1e−6 ratio tolerance (332.796875/416); corrected to1e−4, no CSS/model change. Original failed log is retained.

Baselinea983198 displayed reference as an img at full52vh, making it disproportionately larger than native/painted body. Author fixed comparator-only UI in1a16d10 (root88d4411) using a fixed reference canvas. Repeated both viewports against frozen revised page; `reference-canvas-repeat/` has separate HTML/manifest hashes, actual screenshots/video and instrumented draws. Painted/native source pixels, grid/scale/clock remain unchanged. These two UI states are not conflated.

## Visual observations and concrete failure

Viewed the full48 proper-alpha sheet,12 enlarged sampled poses, actual paused browser39/40/47/0, and decoded actual canvas-loop sequences. Style is closer to accepted Ruta: youthful shorter limbs, cream blouse/olive vest/red scarf, brown cargo/boots, long copper waves and one hip satchel. No obvious detached limb or duplicated bag in this E sequence. Face/head is repainted into a more true-profile view than the native rear-three-quarter guide; this is a real view/projection difference, so identical projected3D geometry is not asserted.

At39→40 the painted drawing jumps upward while native phase changes smoothly. Under the unchanged fixed canvas transform, robust crown moves raw y17→9 (8px; about12desktop CSS pixels). Body/boots also change position and stance appearance. `actual-browser-39-40-47-0.jpg` shows unchanged-size crops of actual revised-page screenshots. Full originals remain. This is not fixed by merely supplying48 images or by using a smoother player clock.47→0 is much closer in crown position(y9→10), so blindly moving the whole last row+8 would introduce a new closure jump.

The actual48 paintings are whole, distinct gait drawings, with visible extension/recovery/arm-swing intervals. This is not a claim that imagegen retained exact bone positions or timing of every anatomical event. Last-row leg spacing may also advance the apparent stance relative to native; semantic source-marker work is being performed separately, not inferred conclusively from silhouette alone.

## Shared-row gutter hypothesis — evidence before any fix

Raw aggregate crown/bottom bounds by row:40…207,243…410,443…611,642…816,846…1022,1039…1204. Last blank vertical gap is17px versus previous30–36px: compressed final-row layout is plausible. But a blank gutter alone cannot prove eight whole poses have one rigid coordinate shift.

Half-cycle pairs16↔40 through23↔47 compare similar source gait stages: painted crown differences−4…−5px versus native−1…−3px; painted lowest-sole/bbox differences−6…−9px versus native0…+2px, and painted total silhouette heights shrink1…4px. These are explicitly shape proxies: opposite-foot depth/occlusion, hair silhouette, stance and changed view can affect them. `row-hypothesis.json` and labelled raw-coordinate paired images preserve the evidence. It does **not** establish a valid uniform rigid row correction and does not justify per-frame fitting. Root/NPC semantic bow/chest and clasp/hip analysis is separate. No layout correction was applied by this reviewer.

## Real media and limits

Untouched actual browser screenshots and silent WebMs retained for both UI states/viewports. `actual-canvas-pair-60fps.webm` is an actual canvas captureStream(60) request with painted/native canvases copied uniformly2× over beige and diagnostic phase headers; no per-frame position correction. Actual codec/cadence is in `canvas-media.json` (VFR, requested60 is not guaranteed constant60). Decoded transition strips were viewed; sampled video labels can skip individual source phases, so exact paused39/40 and47/0 screenshots plus instrumented calls provide frame-specific evidence. rAF-minus-first-copy only approximates video origin.

Visual tools expose decoded still sequences, not a subjective human realtime video session. I inspected real loop-frame sequences and actual complete source poses, but do not assert final smoothness/no-slip by video file existence. This is a standalone in-place art/pose review, not game, route travel, physical phone, other directions, transitions or final artistic acceptance. Current painted motion needs correction; future redraw/row-decoding changes require a separate review and fresh hashes.
