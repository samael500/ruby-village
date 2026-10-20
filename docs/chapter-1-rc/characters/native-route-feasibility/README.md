# Native fixed Start/Stop vs actual game routes — not a drop-in controller

**The current native pair does not solve arbitrary game routes or exact goals.** This is read-only analysis of `/home/mskorokhod/life/ruby-village` at e32cad4. Actual root source files are byte-compared to `git show e32cad4:<file>`;17 SHA256 pins are in route-measurements.json. The analysis executes root `levels`, `winningPath`, `scenePoint`, `selectPaintedScene`, and `planGroundRoute` TS directly using installed Node24; no replacement BFS, source/runtime edits, asset installation or renders.

## Current code contract differs from the native prototype

Root `ruta-motion-view.ts` still loads characters-walk-v1/animated-v3/manifest.json: old stride.72, cycle800ms. Planner hardcodes HALF=.36, converts screen distance with projectedStride/.72, and uses quadratic.18 starts/stops over half a cycle. Playback also hardcodes.72/.18, starts Walk atphase0, and queues stops atphase0/.5. `RutaJourney` assumes one shared half-duration for start/stop and plans duration=(halfSteps+1)*halfDuration. Replacing only the images or cycle duration would not install the new motion contract.

Native prototype: Start.14m/400ms, Walk1.277750296m/1666.667ms with phaseoffset5/40=.125, Stop.140198487m/420.495ms plus native lateral−.021197921m and Z−.000273572m. Root travel is external metadata, source Rootbone and sprite registration stay fixed. Only the left-support pair exists. Old source sprites/start/stop clips must not be mixed into this native pair.

Main passes the actual projected goal hex polygon, **not exactCenter:true**. Current planner can shorten/extrapolate the route to an authored contact endpoint inside that polygon. For committed solutions its residual is.218–9.365scene pixels. All scenePoint start/goal centres exactly match scene metadata groundAnchors; no permission to move those anchors follows from the existing polygon tolerance. A new exact-goal requirement needs a different native trajectory/source contract.

## Scale: actual scene pixels vs explicit future-native assumption

The live renderer draws body height136×scene.fit. Camera.radius values are66,68.8333 or70; groundScale=.65, camera angle0 or.044949. Hex centres use `(sqrt(3)*radius*(q+r/2),1.5*radius*r)`, then camera rotation and Yforeshortening. Radius is not a metre value. Viewport fit scales body and road together.

For a future native comparison ONLY, use the prototype's fixed body-reference373.108721FULLnative pixels (186.554360after uniform.5 delivery), orthographic512×640/2.1, XY304.761905native px/m and body display136. This gives**111.087243scene ground px/native metre**. SourceZ/camera projection is already included in the measured body reference; do not unproject twice or divide by atlas frameheight. One hex edge then measures1.029059–1.091426native metres. This is not the old planner's units, not a final new-hair body-height calibration, and not physical no-slip truth. Recalibrate once if the final source reference changes; do not alter per-frame or per-direction scale to fit the road.

## Actual committed-solution routes

These are real `winningPath(level, level.solution)` results for the current accepted layouts, not exhaustive enumeration of all user placements. Paths can differ with legal layouts. Native lengths below use the declared future calibration; legacy world units are incompatible and retained separately in JSON.

| Scene | Edges / turns | Future native route length | Nearest fixed-L-pair forward residual (goal−pair) |
|---|---:|---:|---:|
| gate |9 /1|9.822838m|+.598388m|
| garden |11 /2|11.319652m|−.460300m|
| well |9 /1|9.659114m|+.434663m|
| bakery |9 /5|9.659114m|+.434663m|
| stream |8 /2|8.731412m|−.493039m|
| mill |9 /3|9.822838m|+.598388m|
| post |9 /5|9.659114m|+.434663m|
| forest |10 /6|10.290592m|−.211608m|

Ignoring turns/lateral motion, one fixed left pair reaches only `L(n)=.14+n*1.277750296+.140198487` for integer n≥0. None of these forward distances matches. Every pair also ends21.198mm sideways, so matching a scalar by accident would still not solve the2Dgoal. Negative residual means overshoot, not permission to extrapolate. The shortest real straight run is one forest/garden edge1.029059m: n0travels.280198m, n1travels1.557949m. Neither reaches it. The longest real run is garden6.174355m; arbitrary residuals remain after any number of whole cycles. Short routes cannot be handled by cutting off a moving pose or scaling its stride.

## Turns and bridges are separate constraints

All8committed paths turn1–6times. Current `setDirection` changes sprite direction at segment boundaries while preserving scalar phase. This does not establish native foot contact through a turn. With nonzero speed a60°corner changes velocity by magnitude v (120°gives sqrt(3)*v); rotating a support offset also moves its world point unless a contact-aware turn is authored. No instantaneous heading swap, phase reset or anchor translation solves that geometry.

Stream bridge crossing is segments4/5: ground(5,1)→water(6,1)→ground(7,1). Mill segments1/2: ground(1,3)→water(2,3)→ground(3,3). Each bank-centre to bank-centre span is2.182853m under the declared scale. Bridge validity uses3cells with water at its centre; `routeSurface` only labels the current cell wood/stone for surface feedback. There is no native bridge height/contact-collision solver in this route code. Reaching the bank/goal centre is not full-sole/body clearance acceptance. No braking/tail retarget should be hidden inside a bridge crossing without validating actual support and artwork footprint.

## ONE minimal next verification variant

**Standalone exact-goal test of the actual stream final E run**, from existing waypoint(4,1), pixel(685.596004,398.25), to unchanged level goal(9,1), pixel(1291.813787,398.25). This is a scoped subroute test, not replacing the chapter start anchor or claiming the full two-turn stream route solved.

Its5edges total5.457132315m. Preserve fixed Start.14 and four complete unchanged Walk cycles5.111001185m. A **new authored native Finish** must then advance.206131130m, end Root lateral0/Z0, and land at staticIdle0 with zero velocity. Current Stop is short65.932642mm and carries−21.198mm lateral/−.274mmZ; changing its duration does not change its baked displacement or resolve the contact constraints. One real contact-transfer/replant finish is required, not a speed multiplier, proportional foot slide, pixel warp or goal snap. The source Walk and its timing remain unchanged. This document creates no new finish action and does not assume its IK feasibility.

The bridge bank centres lie1.091426/3.274279m after this subroute's start. Finish begins at5.251001m, beyond the crossing, so the proposed tail test does not deliberately retarget stance on the bridge. Actual footprint/bridge support remains a separate visual/numeric gate.

Future test controller must consume native root metadata exactly once; sample steady Walk using `D(5/24+t)−D(5/24)` plus accumulated Start distance, add whole strides across modulo40, then switch to the new Finish at its measured incoming pose/velocity. PNG Root stays fixed. Native Finish may modify leg/foot poses/contacts while preserving rest mesh/rig, and must verify target-root endpoint and full sole trajectories. Existing sole-weight variant intentionally changes old Walk surface≤4.484mm and needs its own source binding/review; the original inferred contact curve is an engineering input, not a physical guarantee.

For later full chapter coverage, keep ONE conservative strategy: split routes into straight runs, finish at each real waypoint, perform an authored native in-place contact-aware turn, then Start the next run. This requires native short/length-conditioned Finish assets and turn actions plus controller refactor; none exist from this analysis. For any unrepresented residual/heading, return requires-native-retarget rather than synthesize a fake successful walk. No generic arbitrary-route readiness is claimed.

## Required future gates, not implementation

Strict immutable start/goal anchors and metre calibration; complete native sources for residual/turn; C0and one-sided velocity joins; source Root0 and continuous external XYZ without double shift; no Root endpoint lateral/Z displacement; all actual sole/skin and bridge clearance; actual route playback/pause/resume; independent review. Current image-quality gate is also unresolved. No runtime/source edits, new clips, renders, app publication or no-slip promise were made here.

Reproduce with installed Node24 `--experimental-strip-types analyze.mts`. It reads actual root TS and fails if any pinned runtime file differs. Numeric paths, angles, terrain transitions, old plan results, fixed-pair errors, selected next pilot and source SHA are in route-measurements.json.
