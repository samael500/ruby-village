# Proposed PR #60 update (local review copy)

Title: `art(#36): six-view painted IK walking with source and browser evidence`

Refs #36, #62. Stack base PR #59 (`art/36-ruta-motion`), not main. No merge or game deployment.

Six individually painted cutout views now follow one IK action:16 phases/800ms, separate thighs/shins/boots, physical soft start/stop and stable identity. Root-up axis, knee/shin seams, cuff ownership, boot stretching and view-height registration are corrected. Satchel is not mirrored. Rejected phase generation and failed blink registration remain preserved as sources, never production faces.

Delivery:708 source RGBA frames, packed portable Blender file (~1.9MiB), source masks/provenance/reproducible scripts,12 lossless atlases (9,339,468 bytes), both actual scene-camera calibrations with measured stride/contact contracts. ProductionEnabled=false pending Maksim’s artistic review.

Ground planner handles arbitrary native paths by stopping at the nearest physical contact endpoint inside the actual goal polygon, without speed multiplier/teleport. Exact-center and unsupported narrow-target cases explicitly require retargeting. Native residual is bounded by half of one half step (E/W11.26px). All intermediate path corners remain.

Validation:71 tests, TypeScript noEmit and Vite build; actual evaluated source foot stance <.01nativepx in all12 views. Actual Chromium videos show all six directions, physical start/stop, pause/reduced/portrait controls, two calibrated arbitrary-length goal routes, exact semantic foot-contact counts and completion once. Evidence and JSON reports live in `docs/chapter-1-rc/painted-motion`, with exact API contracts in V2-INTEGRATION.md and GROUND-PLANNER.md.

Limits: these are silent, labelled motion benches on the approved courtyard, not production chapter or bridge gameplay. Six painted turn views are discrete with continuous step phase. Production route/bridge/audio verification and independent #37 remain integration work. Physical phone/iOS/family checks are not run. Headless tabs never became hidden, so real background-tab verification is not claimed.


Remote update authorized explicitly by Maksim on 2026-10-17: «Да, разрешаю push рабочих веток и обновление PR». This updates only the working branch and draft PR; main, merging and deployment remain excluded.
