# Bounded cadence study

Sibling diagnostic page only; original head trial, pivots, artwork and native source remain frozen at `bb845ed`. No new atlas, image processing, interpolation, pose blending, arbitrary reordering or runtime change.

The absolute cycle remains40/24seconds. At clock phase k in0..47, stride d selects and holds source phase floor(k/d)*d for BOTH painted/native views, with that source phase's unchanged head pivot. Settings: d=1 gives48 unique source phases /28.8fps (default); d=2 gives24 unique phases /14.4fps; d=3 gives16 unique phases /9.6fps. Clock phase and actual held source phase are separately displayed and exposed through reviewState. Holds are not presented as48 unique newly generated poses.

This isolates temporal sampling/texture boil versus stepped cel cadence. A lower sampling frequency is not automatically smoother or an accepted fix. Actual A/B video and user perception must decide; root will recommend one version. Existing baseline/clasp/head modes remain available for internal diagnostics.

Author UI smoke selects end-of-cycle clock47 and confirms source47/46/45 at respective strides, unchanged40/24second duration and restoration to default48. This is controls evidence only, not video/perceptual acceptance or physical-phone verification.
