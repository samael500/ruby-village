# Separate semantic artist-pivot trial

This candidate changes whole-cel drawing translation metadata only. Baseline `full48/`, raw RGBA, source poses, common scale and cycle duration remain unchanged. It is not accepted artwork, physical Root recovery, contact certification or a runtime installation.

Open `review.html` through the parent packing directory HTTP server. Candidate, baseline and ghost overlay share the native 48-phase clock (40/24 seconds). Pause/seek, annotations and selected-frame metadata expose the correction. Mode changes preserve phase. Author controls smoke passed desktop and CDP touch landscape; physical phone NOT RUN. Independent browser animation review remains required.

## Explicit calibration

Use existing S=1.1631563024644236 and T=(29.60245861921824,53.313741280992616), mapping local painted pixels to native half-resolution comparison pixels. For the 43 visible manually annotated clasp centres, choose one coordinatewise median bias of baseline-painted minus actual native clasp: (-15.655435744238218,-10.020854561845198). This preserves robust baseline style placement; it does not alter the native trajectory.

For measured phase i, delta_i = nativeClasp_i/2 + bias - (S * paintedClasp_i + T). Draw the entire unchanged cel at T+delta_i with the SAME S. No measured pivot smoothing, scale changes, image deformation or bbox fitting occurs. The derived artist pivot is drawn-cel registration metadata, not an estimated bone joint.

Five occluded phases (14–17,32) use short-run linear interpolation of translation between measured neighbours. Their painted clasp positions remain null, their pivots are explicitly estimated, and total uncertainty is unknown. The native target path is unchanged; alignment of those hidden painted features cannot be verified. Visible annotation intervals (1.5 or 2.5 raw pixels per axis) are retained, but do not bound total systematic feature/style or global-bias uncertainty.

## Held-out check and limits

The bow knot is NEVER used to select scale, bias or pivots. Twelve sparse, partly obscured bow annotations carry ±3.5 raw-pixel per-axis annotation uncertainty plus unknown systematic feature mismatch. Descriptive mean-centred native-half-pixel RMS is 4.4135 baseline versus 3.0609 candidate. At 39→40 the held-out motion residual length is 11.8549 versus 1.3108; at 47→0 it is 1.5275 versus 1.3005. These observations support testing the translation hypothesis, not an acceptance threshold or proof of all-pose fidelity. Fitted clasp coincidence is algebraic, not independent validation.

The maximum adjacent correction is 11.931 native-half pixels. Actual loop review must check both seams and slow drift, not just this fitted landmark. The illustrated heading is closer to true profile than native rear three-quarter. Painted head, knees, soles and contact fidelity remain unverified; source pose/silhouette differences remain. No no-slip claim is made.

`manifest.json` records all 48 pivots/statuses, fixed calibration, source hashes, unchanged raw/frame verification, held-out statistics and provenance (semantic author 6720968). `inputs/` preserves the exact annotation and saved-native projection data. Generator verifies source/crop hashes and writes metadata only; no new raster frames are generated. Browser smoke screenshots show actual controls, not final animation approval.
