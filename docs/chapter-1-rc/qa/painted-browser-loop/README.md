# Independent actual browser review — painted E pilot / #36

**BLOCKED for pilot loop quality: visible body dip at phase 17 → 18.** The page/controls work, but this is not a PASS for stable final animation. The coordinator is retaining this as a draft for art feedback, not replacing production.

Reviewed actual `http://localhost:5310/ruta-painted-ready-v1/review.html` after the author's presentation correction: canvas backing **360×360**, CSS **360×360**, drawing origin **(180,320)**, display at twice the intended game size. Earlier 600-backing presentation is not this evidence. Served page/proposal hashes match local source; before/after hashes bind all 24 painted frames, 24 native guide frames, page and origin proposal. None changed during capture. QA made no author-source, RGBA, rig, anchor, runtime or registration edits.

## Concrete blocker

See `actual-browser-body-dip-and-seam.png`, actual phase screenshots and videos. At 17 → 18 the painted alpha16 silhouette top moves **18 canvas/CSS pixels downward** while the native comparison moves **3 upward**. Painted silhouette extent height changes **287 → 274**, native **284 → 287**. The manually annotated visible satchel clasp, projected through the same draw formula, moves down approximately **15.67 canvas pixels** (manual contour-center uncertainty is separate). These image landmarks and the captured bodies show the dip; they are not measured bone/head-height changes or physical-anchor error. The 2× preview magnifies it; 18 preview pixels correspond to 9 intended game pixels.

Additional observation at 23 → 0: painted top moves up 11 canvas pixels, native down 1; painted silhouette extent grows 11 pixels, native shrinks 2. The main blocker remains 17 → 18. `analysis.json` preserves exact per-phase extents, proposed origins and optional visible clasp projections. The metrics diagnose the visible result; they do not establish whether the right repair is drawing pose, artist-origin metadata or both. Per-frame scaling/warping was not proposed or applied.

## Captured controls and containment

- Desktop 1280×800 and landscape browser phone emulation 844×390: **24 actual UI-selected phases each**, with viewport screenshots and actual painted/native canvas PNGs. All corresponding canvas pixels match across viewports. The files come from actual browser canvases after real range-control keyboard events; no frame images were substituted into the page.
- Real mouse/native CDP touch clicks pause/resume. Paused phase and painted canvas stayed unchanged over 300 ms. The range control traversed 0…23 using real Home/ArrowRight keyboard input, including in the touch context; a native finger swipe of the slider was not part of this scope.
- Real resumed playback runs approximately 8.7 seconds; both recordings observe all 24 phases and **six actual 23 → 0 transitions**. This is a count of wraps, not a claim of six whole cycles. The videos include paused frame controls and actual running playback; no synthetic seamless GIF was substituted.
- No alpha16 pixels touch the outer 2-pixel canvas border in any of the 96 painted/native captures. No page or HTTP errors. All actors are contained; containment does not establish body/feet stability or physical support.
- Landscape review uses vertical scrolling to inspect the painted canvas; the native comparison wraps to a later row. This is a review page, not a gameplay layout test. Physical phone **NOT RUN**.

`1280/` and `844/` contain the 24 phases, contact sheets, final-loop frame, raw reports and actual silent browser WebM recordings. `media.json` records hashes and stream metadata. There is no audio in this standalone review page/recording. A preliminary harness API-argument error occurred before phase capture and was corrected only in QA; its local aborted capture is excluded from the successful evidence.

**Not certified:** physical foot anchor, native contact/no-slip, unchanged physical body size, actual route displacement, turns, other five painted directions, game runtime integration, final artistic acceptance. Native physical-gait checks are separate earlier evidence. Here the origin is an **artist-origin proposal** derived from differently defined contour/vertex features, including interpolated phase 7; it is not a physical sole point. Body/feet loop quality remains blocked as stated above.
