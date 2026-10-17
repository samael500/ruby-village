# Grounded arbitrary-path planner

`planGroundRoute(path, {directions, goalPolygon})` in `scripts/character-paint-route-planner.ts` accepts native scene points and the selected manifest camera variant. Pass the actual goal-ground polygon, not sprite bounds. A circular `goalRadius` is available when geometry really supplies a circular tolerance. `maxResidualPixels` may tighten the default bound.

The result is `ready` or explicit `requires-retarget`; no unsupported path silently slides. A ready plan keeps all intermediate path corners and stops at the nearest reachable physical contact endpoint inside the goal polygon. It may trim or extend only the final approach. The endpoint can differ from the target center by at most half of one authored half step: E/W 11.26 native pixels at display height 136, less for the diagonal views. It never changes source playback speed to conceal a distance mismatch. Exact center remains opt-in; a nonreachable center or narrow target returns a short-step retarget requirement.

A physical route has N half steps: start 400ms/.18 rig-world, N−1 walk half cycles at 400ms/.36 each, stop 400ms/.18. Total distance is N×.36 and duration (N+1)×400ms. Rig-world distance comes from each actual camera stride, not puzzle grid units. All supplied path segments must match a calibrated six-view direction. The returned points end at the planned grounded endpoint; do not feed the original center path back into a clamping route implementation.

`sampleGroundRoute(plan, elapsedMs)` returns position, continuous walk phase, direction, start/walk/stop/idle state, physical velocity and support-foot data. It uses one clock and exact authored curves; pause freezes elapsed time. Use existing semantic source contacts for audio, rather than creating a new timer. Source stop clip is selected from plan.stopFoot. Completion is at the grounded endpoint, with no final extra movement tick and no teleport to the center.

Six tests cover arbitrary lengths across all 12 camera views, polygon membership and residual bound, optional exact-center/narrow-target refusal, 30/60/144fps, continuous phase through corners and actual evaluated source-ankle stance in start/walk/stop (<.01 native px). At turns, the source changes between discrete painted views; these tests do not claim continuous painted turn anatomy. A full real puzzle route, especially over stream/mill bridges, still requires integration and independent #37 visual/input checks; the mathematical route test is not a substitute.

Actual browser evidence: `v2-ground-goal-route.webm` and gate/post screenshots show arbitrary-length routes with real pause/resume, changing direction without resetting phase, and a visible native ground polygon. The actor stops at the physical endpoint inside it, with no center correction.

- gate: native residual 0.745626px, grounded=True, duration 8000ms, 20 actual semantic source contacts, completion 1.
- post: native residual 7.197856px, grounded=True, duration 8000ms, 20 actual semantic source contacts, completion 1.

The fractional-tick source-contact regression is fixed by coordinator commit ed6f174 (local cherry-pick 7d32567). Final actual-source contact counts agree across 30/60/144fps and both browser routes. Total local suite: 71 passing tests, noEmit/build passing.
