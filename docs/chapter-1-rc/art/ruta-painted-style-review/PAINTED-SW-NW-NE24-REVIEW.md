# Independent SW/NW/NE24 source review and E browser readback

Reviewed each6×4 complete sheet after proper RGBA-over-beige compositing and its corresponding native all12 guide. Each contains24 visibly whole pose drawings in the expected indexed layout. Low-alpha red fringe/scatter is not reported as a visible defect. Evidence includes six `*-composited.jpg` source/guide views and corrected `sw24-v2-composited.jpg`. No author art/runtime edits.

|Candidate|Static visual verdict|
|---|---|
|SWv1|Needs heading correction: face looks screen-right like SE instead of source SW's left/down heading. Torso reads nearly frontal. Legs do show recovery/passing changes; this is not24 frozen poses. Correct bag side cannot compensate for wrong head/view direction. Retain as reject.|
|NWv1|Promising rear-left view: all24 poses remain rear-facing toward the intended direction, with alternating boot extension/recovery and arm swing. Near-passing6–8/18–20 is distinct from split intervals. One satchel remains on screen-right anatomical-right hip, single back diagonal strap. Hair hides face as expected. No obvious limb tears or duplicate bag observed.|
|NEv1|Promising rear-right view: heading matches rear native guide, visible heel/sole/crossing changes across both halves; one screen-right anatomical-right hip satchel and one strap remain consistent. Back hair/vest/trousers/cuffs/boots match Ruta's accepted rear study. No midcycle body reversal or extra limbs observed.|
|SWv2|Heading corrected to left/down throughout; **bag/arm continuity now fails**. Phases0–5 largely hide a small bag at screen-right/lateral hip;6 onward a large bag appears at screen-left chest/underarm height, with a newly strap-gripping hand;12–15 retains that raised bag. Native guide retains the anatomical-right bag at screen-left HIP throughout. This changes position/side/height and arm action, not just natural occlusion. No convincing midloop torso reversal observed, but this bag migration blocks acceptance.|

NW/NE conclusions are still-image sequence scope, not proven exact bone coordinates or realtime temporal smoothness. Their guide silhouettes are naturally occluded near the travel axis; no absent half-cycle is inferred merely from overlapping legs. Uniform art/body size and world registration remain separate checks. SWv2 should be corrected with one stable anatomical-right hip bag/diagonal strap and native arm swing; do not mirror SE or make the arm hold the bag to conceal it.

## Actual E browser page

Used an independent Chromium visit to `http://localhost:5310/ruta-painted-ready-v1/review.html`. Page loaded with0 page errors, both painted/native canvases had nonzero alpha content, and live frame-number readbacks advanced2,4,6,8,10,12. `e-browser-actual.png` is an untouched real page screenshot and was inspected. `e-browser-check.py/json` records the method/results.

The current page explicitly uses per-frame **artist-origin proposal translations**, including an interpolated frame7 anchor; it is not the earlier unregistered loop. Its code does not warp sprite pixels, but registration proposals are not measured hidden joints. This browser check proves the animation actually runs and paints images; screenshots/readbacks do not certify subjective realtime gait smoothness or slip-free contact. No such pass is claimed. Final runtime movement, transitions, all-view consistency and artistic acceptance remain pending.
