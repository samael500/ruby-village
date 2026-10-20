# Actual selected full-sole contact evidence — no transition clips

**Walk5/25 are defensible near-flat geometric join candidates for one future native transition probe; they are not certified planted/no-slip phases.** This strengthens the earlier heel-mean plan with every selected actual sole material vertex. No mesh, rig, source action, renderer, runtime or new clip changes; image-quality gate remains independent.

## What is measured and pinned

Read existing native transition inventory, final-sole sampling and PR71 notes first. Reuse481source samples/480intervals from the final boots archive, not old B's222split records. Final `Adventurer_Feet` has336vertices/610polygons; the sampler selected56actual used material vertices,28per foot, Foot.side weight≥.5 and restZ within8.4mm of that side's minimum. Heel/toe are the rear/front15% of rest-nativeY span. These are actual mesh points, not ankle markers, alpha bboxes or generated image landmarks. This selected lowest rest band is broader than a heel proxy, but it is NOT a continuous collision mesh of the whole shoe.

`verify-foot-pin.py` cold opens frozen bae05a2f… and the packed garment donor57d6668… read-only. Positions, polygon topology, skin weights/group names, Armature binding and Walk/Idle curves match exactly. Thus material/UV changes did not invalidate these geometry samples. `foot-source-pin.json` retains both input SHA values and actual foot/action fingerprints. The archive SHA638c78da… is verified against metadata. No duplicate sampling or re-fit was needed.

`analyze.py` uses the same experimental final forward curve (stride1.277750296m/1666.667ms), differentiates each material vertex before weighting, and computes fixed-point trajectories/velocities. It does not differentiate a changing contact centroid. `fullsole-phases.csv` contains960foot-phase rows: all-sole vertical envelope, heel/toe pitch, rest→pose rigid tilt and fitting residual, fullsole velocity residuals and soft confidence. All axes are nativeworldX/lateral,Y/backward,Z/up; heading/camera are separate.

## Geometric phase evidence

The inferred floor is−1.194837mm, the minimum sampled soleZ, not an authored collision plane. “All-sole low” below means **every selected point** is ≤the stated band above this floor. It does not mean every point touches the same plane.

| Actual envelope criterion | Left phase interval | Right phase interval |
|---|---|---|
| All heel points ≤10mm | .066667–.260417 | .566667–.747917 |
| All toe points ≤10mm | .075000–.225000 | .575000–.718750 |
| All28sole points ≤10mm | .075000–.225000 | .575000–.718750 |
| All28sole points ≤17.5mm | .066667–.329167 | .566667–.822917 |
| All28sole points ≤24.5mm | .058333–.377083 | .558333–.879167 |

The old minZ-confidence windows were wider (.045833–.3625 and.545833–.860417); some of those phases have a low subset but do not satisfy the stricter whole-selected-sole envelope. Height threshold crossings are descriptive heel/toe events, NOT proven heel-strike/toe-off or support ownership. Toe/heel shape and uncalibrated floor affect their order. Real contact events require authored constraint/collision evidence or a calibrated ground review.

| At selected join | Walk5 / L | Walk25 / R |
|---|---:|---:|
| Actual selected sole height range above inferred floor | .487–8.848mm | .513–8.836mm |
| Rest-area fraction ≤3mm |32.60%|32.60%|
| Rest-area fraction ≤8mm |92.82%|92.82%|
| Rest-area fraction ≤17.5mm |100%|100%|
| Rest→pose best rigid rotation tilt |.1399°|.1353°|
| Best rigid fit RMS |.2356mm|.2365mm|
| Geometric heel→toe mean pitch |1.7892°|1.7811°|

The1.78°heel/toe height angle includes rest sole shape; it is not1.78°of animated foot roll. Best-fit tilt relative to the actual fixed rest points is near0.14°. Fit residual is nonzero, and its cycle maximum reaches1.234mm: skinning is not exactly one rigid foot transform throughout the cycle. Do not flatten all selected points onto a plane to force a false contact assertion.

## Motion residuals and transition constraints

| Fullsole measure after experimental forward travel | Walk5 / L | Walk25 / R |
|---|---:|---:|
| Area-weighted3D velocity RMS |15.18mm/s|20.71mm/s|
| Forward velocity RMS |3.81mm/s|4.02mm/s|
| Fastest selected material point |18.80mm/s|24.08mm/s|
| Max point axis spans during ≤10mm envelope (X/Y/Z) |3.95/1.85/2.17mm|5.02/2.30/2.19mm|

Spans are over threshold-limited intervals of250.0ms(L)/239.6ms(R), not whole physical stance drift. A single rigid forward translation cannot cancel the residual lateral/vertical motion and foot rotation; preserving one heel mean does not lock every actual point. Even a best-fit6DOF foot pose leaves small native skinning deformation. Contact tolerances and which low points actually carry support remain unspecified.

Keep the earlier phase5/25 proposal, now justified by near-flat full selected geometry. A future bounded Start must still lift/reland a genuine lead foot: locking the same Idle heel directly to these source poses would require Root moving backward140/137mm. A Stop must preserve a calibrated contact patch/foot orientation and settle the other foot, not simply align heel means or source phase0. Existing endpoint root travel/lateral offsets remain constraints, not validated animation. Any native solver must preserve the source sole shape and demonstrate actual material-point residuals before claiming a foot lock. No new IK, transition actions, frames or runtime are produced here.

## Limits and next gate

Finite480interval measurements do not prove continuous swept contact or contact at interpolated extrema.17.5mmsoft-band labels and±7mm sensitivity are engineering assumptions, not physical measurements.10mmfull-envelope criterion is intentionally stricter than the earlier fuzzy confidence and still includes noncontact curved sole points. Rest-area weights include incident geometry and are not measured pressure. No simultaneous physical double support, friction, force or calibrated floor is inferred. Starts/stops may require different contact positions and velocity continuity checks across both native clips. Heading turns and terrain remain outside this evidence.

Reproduce data analysis with numpy Python: `python docs/chapter-1-rc/characters/native-fullsole-contact/analyze.py`; pin check with Blender4.5.3 `--disable-autoexec -b -t 2 --python-exit-code 1 --python .../verify-foot-pin.py`. Output is numeric evidence + future contract, not no-slip, artwork, game or transition acceptance.
