# Independent native MPFB start/stop review — 35cddba

**Verdict: GO for the next isolated twelve-camera/two-pose technical proof.** Actual E start/stop is coherent and fresh native-bundle checks pass for both leading legs. This is not accepted final Ruta/appearance, a rendered six-direction set, runtime activation or arbitrary-route stopping certification.

New immutable own checkout `/tmp/ruby-qa-mpfb-35cddba`, branch `qa/37-mpfb-transitions-35cddba`, source35cddba (PR71). Motion transition/API documentation and repository instructions read. Only this QA directory changed. Source model/head/body, existing pilot, runtime and vendor stay read only. Fresh Blender4.5.3LTS processes, CPU2threads, own `/tmp/ruby-mpfb-qa35-*` config. No source save, pose generation or runtime edits. Full source commit and before/after blend SHA256 match in summary.json.

## Actual temporal review

Original E GIF,55 source PNGs, author strip, independent near-join temporal sheet, first/last-step crops and five browser replay cycles were reviewed. The first lead foot lifts and completes its step before ordinary walking; stop allows the trailing swing to finish instead of freezing a mid-air foot. The actor then finishes heel roll and settles into a planted idle. Supported ONE-strap carry remains visually consistent; free arm motion fades rather than abruptly parking mid-swing. No blocking pose pop or stance slide was apparent in the actual E evidence.

The mildly flexed/crouched walking impression noted earlier remains a stylistic observation of the unchanged technical cycle. The transients do not add an obvious collapse or unnatural foot freeze. This is sufficient for further technical camera proof, not a final naturalness/likeness signoff on the rejected mannequin.

The demo is0…1620ms: start360ms, walk720ms, stop360ms, settle180ms. GIF55×30ms displays1650ms including the last frame's dwell; it deliberately replays/reset after the demonstration. That reset is **not** reported as a game teleport or claimed seamless spatial loop. The source walking cycle remains a separate cyclic action.

Only the left-lead E demo has actual renders. The right-lead bundles are natively authored and independently measured below, **not separately rendered** or cosmetically mirrored into proof.55 distinct PNG hashes are checked, but render-hash uniqueness alone is not treated as evidence that all action states or the right variant work.

## Fresh native contact, completion and floor measurements

Own `measure.py` activates every action bundle's **three** objects together: rig, native thumb target and thumb pole. It opens the saved transition blend and measures217 quarter-frame samples for each lead, rather than consuming author result assertions. Actual render-level1 full boots provide the floor test; independent bottom4mm/forefoot20% source-index skin markers provide world contact measurements. A transient non-rendering probe retains source indices; nothing is saved back.

Both native leads measure:

- Full render boot minimum Z +0.344874mm over217samples: no sampled floor penetration. Actual ankle/IK discrepancy maximum0.03197mm.
- Root monotonically advances0.85313183m (1.5physical strides) over the composed demonstration, with no backwards correction or double root motion.
- First lead heel advances≈0.283923m during start; last trailing heel advances≈0.283988m through the stopping step. Both are close to the planned half-stride, with actual heel-roll geometry explicitly measured. Actual heel lift peaks≈50.5/50.8mm, then reaches support; the swing is not stopped in place.
- Settle1440…1620ms has root drift0, actual sole marker drift below0.000315mm, and pelvis rise4.0001mm. Both feet remain planted while the body settles.
- Measured near-flat contact runs are derived from actual sole pitch/height, not declared planned targets. Walking stance drift≈0.0202mm. The initial support run's broad near-flat classification includes the first small toe-roll onset and therefore reaches≈0.1255mm heel motion; this is explicitly retained, not mislabeled the author's narrower flat-stance value. Later stop/settle support is below0.001mm.

These are finite sampled geometry tests, not continuous-time physics or a blanket all-collision proof.

## Bundle joins, all standalone states and API checks

At idle→start, start→source-walk, source-walk→stop, stop→settle and settle→idle, actual root-relative bone matrices differ by at most4.65e−6; thumb/pole local differences≤1.193e−7. Direct **actual world skin marker positions normalized only by rig root translation** join within6.40e−8m. No bounding-box or per-image anchor correction is used.

Own `clip-equivalence.py` additionally compares every saved standalone start/stop/settle quarter-frame to its native demo section, allowing only the required constant world root offset. It checks both variants: start49samples, stop49, settle25 each; standalone idle25samples remains steady. Root offset variation≤6.34e−8m, bone differences≤3.70e−6 and helper differences0. All original walking action bundles remain present. This covers the actual standalone clips beyond the55 E image hashes.

The isolated phase API is read as the contract, then independently tested: monotonic root and source phase modulo1, numeric derivative vs declared root speed, and1001 stop-request phases. Requests go to the **next** heel strike at0/.5 with≤360ms wait; an arbitrary active swing is not frozen. Analytic root speed joins0→0.7899369m/s→0 continuously. Saved actions are **linear30ms samples**, so their interval chord speeds are approximations: last-start interval0.779857 vs first-walk0.789937m/s; last-stop interval0.010079 vs settle0. These small discrete differences are recorded and not falsely claimed analytic C1 continuity in the saved curves. Actual E temporal review found no blocking join snap.

## Grip, bag and clothing across both complete demos

Own fresh `grip.py` and `collision.py`, run separately per lead, measure217 samples each. Palm289verts/222faces, fingers1265/1216, thumb224/207 are all genuinely nonempty weighted actual skin regions. All strap surface intersections are0. Skin-vertex→strap surface distances remain palm1.307…1.411mm, fingers2.208…2.315mm, thumb1.118…1.720mm. Reverse vertex/surface distances retained too; these are sampled clearances, not exact global closest-triangle or force contact assertions.

All six actual body hand/forearm and render-level1 shirt sleeve masks have nonempty vertices/polygons. Against retained bag+flap+buckle, all maxima0 for both native demos. Exactly one original strap remains; bag/strap raw mesh, basis transforms, render visibility and non-armature geometry modifier signatures match appearance-v1. Source geometry was not hidden, shrunk or replaced to clear a limb. This is the same actual carried accessory, not a floating or removed prop.

## Next proof gate and integration limits

The intended next review is **twelve camera configurations×two actual poses** (including both calibration groups), not completed production exports. No such proof was rendered here. The prepared `mpfb-motion-sixview-proof.py` currently opens the pilot-cycle blend and loops only six **base** cameras×two cycle poses (12renders). It does not implement twelve camera configurations or multi-angle transition renders. The owner must expand the helper to the intended camera scope before calling that coverage complete; this is a scope note, not a failure of the measured E action.

**Arbitrary player-route integration is NOT IMPLEMENTED or certified.** These actions have fixed source displacements, and correct root/phase joins do not prove exact-center stopping at every route length. A future actor stopping inside the actual goal-safe polygon with≤0.25stride along-tangent quantization is only a proposed design. It must preserve the logical goal/path, validate the real safe area and avoid source-image deformation; none of that route planner/controller behavior was tested or silently approved here. Heading is locked; turning transients are not authored or reviewed.

Rejected generic face/hair/wardrobe remain rejected. No actual game walk, final appearance, all-direction exports, physical phone/Safari/iOS/family or RC approval. Physical/family NOT RUN. Browser proof is silent. No main merge/deploy.

## Reproduce

Use own Blender config paths and `--threads 2`: `measure.py`, `clip-equivalence.py`, and `grip.py -- L/R`, `collision.py -- L/R` (after Blender's `--`). Serve this checkout at5298 and run browser-review.py with `/tmp/ruby-rc-tools/bin/python`. Scripts only write QA outputs. All reports, source hashes, actual crops and browser proof are here.
