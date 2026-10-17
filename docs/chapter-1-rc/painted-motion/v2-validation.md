# Actual verification — painted motion v2

- Blender 4.5.3, two render threads, 16 samples: 708 actual RGBA PNGs; six distinct painted views for each of two real scene cameras.
- Source audit: all 12 views pass planted ankle cancellation for walk, accelerating start and decelerating stop; maximum drift <.01 source pixel (reported values in v2-technical-audit.json), actual camera angles/stride match scene-v8, sixteen distinct walk frames per view.
- Node 24: 63 tests pass (repository tests plus six playback tests); TypeScript noEmit and Vite production build pass.
- Actual Chromium/Playwright: full six-direction route, 26 semantic contacts, exact completion once without endpoint hack; real replay/pause/resume/select/reduced controls; calibrated post camera; portrait viewport freezes actor. See v2-browser-audit.json and v2-full-route.webm.
- Atlas delivery: 9339468 bytes compressed; 47775744 bytes decoded per active six-direction camera group. The review lazy-loads one group. Packed Blender source is approximately 1.9MiB with all 42 textures packed.

All sixteen phases and transition samples are supplied as contact sheets. Rounded source knee/shin caps remove the pointed cutout contour, and common body registration removes height jumps between views. Six views remain discrete turns with a continuous step phase, rather than continuous painted rotation. The isolated route video is silent; integrated footsteps/audio and arbitrary actual puzzle paths/bridges require coordinator integration and independent #37 verification. The preview path is explicitly a motion bench, not gameplay completion evidence.

A background-tab visibility listener is installed. Headless Chromium did not hide background tabs, so that real lifecycle case is not claimed tested; large-delta unit coverage and actual pause/portrait checks pass. Family test, physical phone and iOS remain not run. Artistic acceptance remains pending Maksim’s review; productionEnabled is false.
