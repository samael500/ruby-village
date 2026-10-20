# Painted motion v2 integration contract

This branch supplies a complete six-view candidate; `productionEnabled` stays false until visual acceptance. It does not edit `src/main.ts` or `src/character-animation.ts`. Original failed phase-generation sheets and the first cutout pilot remain traceable. `rejected-v2-unnormalized` preserves the later source-scale and knee-edge regression.

## Assets and camera

Load `assets/characters-walk-v1/animated-v2/manifest.json`. Pick `cameraVariants[sceneCameraVariant[sceneId]].directions`, never assume every scene uses gate projection. `base` covers gate/garden/stream/mill/forest; `calibrated-1` covers well/bakery/post (camera angle 0.04494904935533156). Both contain e/se/sw/w/nw/ne, drawn individually from the six-view source, with no mirroring. Exact `screenAngleRadians`, `sourceYawRadians` and `projectedStridePixels` are per view. Stride is specified at display height 136; scale proportionally for another display height.

Each frame has file, sourceRect, frameSize, footAnchor, durationMs and optional semantic `contact: left|right`. Atlas cells share one crop, uniform delivery scale and native anchor; never realign by each frame's visible bounds. Keep `targetDisplayHeightPx / nativeHeightPx` as the rendering scale. All original source PNGs and packed Blender data are retained.

## Physical time and route

One walk cycle is 800ms and .72 world units. Advance the route using actual projected stride, not a fixed whole-route duration. Start lasts 400ms and covers .18 world units with t² acceleration; stop lasts 400ms and covers .18 with 2t−t² deceleration. Start ends at L contact; stop-L/stop-R start at their corresponding planted source foot and end neutral. Queue an arbitrary stop until the next real contact. The isolated `PaintedMotionClock` implements these semantics and preserves one walk phase across direction changes.

Idle is a 3200ms loop, with subtle source-rig breathing/arm motion. Pause/hidden/portrait must freeze both route and animation and discard the first stale resume delta. Reduced motion settles once without extra contacts. Emit foot audio only from returned semantic contacts, using the actual scene surface. A different direction selects that view's frame at the same phase. Six directional drawings give discrete view changes; no crossfade/double silhouettes are presented as authored intermediate turn drawings.

The preview uses the real CharacterPlayer/CharacterRoute classes on a labelled motion bench, not production puzzle footage. Coordinator commit 5f39df1 fixes the final route-completion floating-point epsilon; the preview does not add a final movement tick.

## Reproduction and verification

Run Blender 4.5.3 with two threads on `art/blender/characters/ruta-motion-prototype.blend`, using `scripts/character-paint-export-v2.py -- --samples 16`; then run package-v2.py, audit-v2.py and contact-v2.py with Python3/Pillow. `--render-directions` and `--render-states` allow deterministic partial rerenders while retaining the full source contract. Run playback tests with Node 24 `--experimental-strip-types --test scripts/character-paint-playback.test.ts`. Serve Vite and run `character-paint-browser.py` through the installed Playwright Python environment.

Technical assertions cover evaluated planted-foot drift for walk/start/stop, actual scene projection, all source alpha canvases, contact-aligned stopping, frame-rate independence, pause and reduced motion. Browser evidence covers all directions and one route completion, real pause/select/reduced input, a calibrated post camera and portrait viewport blocking. These are desktop Chromium checks. Physical phone, iOS and family test remain not run; artistic acceptance remains Maksim's review.
