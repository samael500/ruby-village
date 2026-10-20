# Native first-step/stop pair — isolated technical prototype

Real new whole3D source actions `RutaContact_FirstStepL_PROTOTYPE`(400ms) and `RutaContact_StopL_PROTOTYPE`(420.495ms), in contact-actions.blend. Original frozen bae05a2f… file/Walk/Idle/rest/proportions unchanged. SourceIdle0 is delivered STATIC with zero endpoint tangents; original breathing action retained. Start joins outgoing Walk5 derivative; Stop joins incoming Walk5 derivative (source has a one-sided velocity kink there). All4poses match <.7µm; baked Bezier source tangents give numerical endpoint head-velocity differences≤4.37mm/s, angular≤.010rad/s. See numeric-check.json; finite checks are not continuous analytic/no-slip proof.

Rootbone remains0. External XYZ path is cubicHermite in build-contract.json/rootHermite; consume once. Start takes a genuine65mm lifted left first step while right initially supports, then joins Walk5. Stop settles the other foot and ends at Idle0. IK adjusts existing upper/lower leg poses, no rest-length changes; no unreachable targets, lowerlegtail errors≤3.2µm. Original curve hashes retained and asserted. New action-only source can be imported onto the pinned rig.

## Intentional sole-weight VARIANT, not original Walk deformation equivalence

Original-weight start has actual sole drift despite held Foot: vertex279 is50.111%Foot.R/49.889%LowerLeg.R. Exact LBS reconstruction error≤29.8nanometres proves the lowerleg contribution dominates ~10mm drift; all16Footworld entries checked. No PNG/Root pivot correction.

Separate sole-weight-variant.blend/contract changes ONLY56selected actual sole vertices to corresponding Foot.side1. Other280footvertices, upperboot, laces and cuffs unchanged. OriginalWalk48 max sole displacement4.484mm both sides, RMSXYZ.597mm; upperboot/lace/cuff max0. This is explicitly a DERIVATIVE with changed weights, original source untouched. Variant Start right-support fullsole span .0392mm; Stop left-support span1.086mm, no depth below the inferred floor in dense161-point checks. No friction/physical support/no-slip certification; weight boundary/sole appearance require independent visual review.

## Frozen80-frame actual proof

review.html / proof-manifest.json: staticIdle4 +Start12 +Walk48 +Stop12 +staticIdle4, exact per-frame timestamps. Walk retains1666.667ms and phase offset5, modulo40; finishes before5, then Stop at5. Six initial wrap samples were explicitly rerendered; initial-render-wrap-rejected.log retained as debugging provenance, not selected source. All80 source action/timestamp pose hashes replay-verified;48Walk hashes unique.256×320technical PNGs with fixed semantic Root camera/viewport, no per-frame fit/resize/warp. Original frozen body appearance is technical, not current accepted artwork or final sprites.

Two viewer modes consume d ONCE: fixedRoot scrolls ground/camera reference; route mode moves the whole native frame with ground fixed. No Roottranslation in source action or PNG. Replay explicitly resets the route after finalIdle, not a seamless closed-world walking cycle. HTML exposes reviewReady, reviewState, reviewPause(), reviewSeek(index), reviewSetMode('fixed'|'route'); selectors #stage/#play/#seek/#mode. Parent owns integration; no runtime changes.

Build/check/render/verify scripts included. Independent review pending; no game/art/transition-final/no-slip acceptance. Source/no-source-cache changes outside this directory. No heavy source model copy saved; new source files are action-only and sole-weight mesh library.
