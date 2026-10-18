# Independent M3 correction review — MPFB5ca361b

**Verdict: GO for isolated start/stop and six-view technical prototypes from this cycle. M3's unmotivated held-forward hand is resolved by a coherent ONE-strap carry.** This is scoped engineering readiness, not production activation, final Ruta/appearance, a finished six-direction set or actual game-walk acceptance.

New own worktree `/tmp/ruby-qa-mpfb-5ca361b`, branch `qa/37-mpfb-motion-5ca361b`, immutable5ca361b (PR71). Repository instructions and current motion source/handoff read. Only this QA directory changed; body/head/source/runtime/vendor remain read only. Source exact commit/hash are in summary.json; before/after hash equality verified independently. Blender4.5.3LTS, CPU2threads, own `/tmp/ruby-mpfb-qa5ca-*` config/scripts/datafiles. No image generation, model alteration or source save. All following measures reopen the saved packed blend, not author target data.

## Actual visual review and naturalness decision

Actual side/front/three-quarter strips, fixed-world strip, all24 temporal poses, original GIF, seven browser loop cycles and the four real close grip renders were inspected. The right hand now has a visible purpose: closed fingers and thumb hold the existing diagonal strap at the upper chest. Its near-stationary elbow/wrist is appropriate to that support gesture rather than the previous open reaching hand. The left hand has a relaxed shape and visibly swings through the cycle. Torso counter-motion and a calmer head break up the previous rigid upper-body block. No obvious pose pop, hand/strap separation or unstable bag was apparent in the actual reviewed cycle.

This visual change, together with the independent geometry checks below, is sufficient to continue **technical** start/stop work and render/check six actual view prototypes. The next views and transitions still require their own review; copying this source does not make unreviewed exports accepted automatically. Appearance stays explicitly rejected generic source art.

The earlier slightly crouched/stepping impression **persists** in the unchanged lower-body motion. The fixed-world sequence still shows consistent support and swing clearance, without a visible collapse or sliding stance. This review does not claim that a hand gesture fixed the knees/pelvis, nor infer aesthetic naturalness solely from an angle range. The mild flexed impression remains a style/pose note to reassess on the accepted body/wardrobe and at game scale, rather than a newly observed blocking defect in this technical cycle. No clinical or universal gait-normality claim is made.

## Independent97-subframe contact and loop repeat

`measure.py` samples97 quarter frames1…25 from a fresh saved-file reopen. Stable source bottom4mm/forefoot20% shoe vertices measure actual skin contacts in world coordinates; floor tests explicitly use the actual shoe **render subdivision level1**, distinct from source viewportlevel0. Nothing is saved back.

- Flat stance phase0.125…0.45: toe/heel world drift ≈0.0182mm each side. Push-off phase0.49…0.59: toe drift≈0.669mm per support cycle. Different marker/window scope from author's broader report is explicit.
- Render-level1 boot minimum world Z +0.34468mm across97samples; no floor penetration in this sampled test. Mid-swing bottom clearance17.14…46.53mm in tested phase0.65…0.95.
- Physical root stride0.56875455m;24 distinct actual poses; frame1/25 root-relative bone matrix maximum difference5.782e−6. Loop endpoint closes within that precision; no assertion of analytic velocity continuity at every joint.
- Knee flex15.75…53.05°, pelvis32mm Z excursion, unchanged from prior technical cycle. Source body19158 vertices/167 rig bones. Clothing and accessories retain actual armature-evaluated deformation.
- Independent actual E alpha max251px at384px/ortho1.70m reproduces69.6101scene-pixel stride at136px height; recalibrate after accepted appearance/scale changes.

## Actual grip surfaces, nonempty masks and preserved bag

Own `grip.py` tests **actual evaluated skin triangles** against the actual ONE strap at all97 subframes. Body MASK is transiently disabled only for unambiguous source limb membership. Three independent weighted regions are nonempty with real faces:

| Region | Vertices | Polygons | Max strap triangle intersections | Skin-vertex→strap surface distance |
|---|---:|---:|---:|---:|
| Right palm |289|222|0|1.307–1.410mm|
| Right fingers |1265|1216|0|2.208–2.315mm|
| Right thumb |224|207|0|1.118–1.720mm|

Distances are sampled vertex-to-surface minima, with reverse strap-vertex→skin-surface results also retained in grip.json. They are not mislabeled exact global closest-triangle distances or force-based zero-gap contact. The small positive clearance plus actual closed grasp frames supports the visual carry pose; no visible floating hand is claimed from target positions alone. This is finite-sample geometry evidence, not a continuous-time cloth/contact simulation.

Bag, flap, buckle and strap raw mesh vertices/faces, object basis transforms, render visibility and non-armature geometry modifier signatures match the original appearance-v1 source. Exactly **one** actual strap mesh remains in the scene. The strap's skin weighting can intentionally follow chest/root; geometry, size and visibility are not faked by hiding/shrinking/replacing the bag. Source signatures and original comparison are recorded in grip.json.

Own `collision.py` additionally checks all97 subframes: body hand-only and forearm/hand sets on both sides, plus actual render-level1 shirt sleeves, against **bag+flap+buckle**. All six sets have real nonempty weighted vertices and polygons; every maximum is0. Body hand regions1569verts/1472faces each, body forearm/hand1932/1822 each, shirt sleeves2099/2026 and2259/2186. No empty shirt-hand mask is counted as a pass. This retains prior M2 correction; all-garment/body collision freedom is not claimed.

Independent actual torso/pelvis rotation excursion5.0419° total and world-head excursion0.34035° reproduce the intended counter-motion/stabilization. Left wrist fore/aft travel110.30mm; supporting right wrist0.4946mm. Actual elbow flex left9.8916…23.8802°, carrying right108.704…109.072°. Small right-arm travel is now motivated by holding a visible strap.

## Browser/render proof

46 distinct actual PNGs:24E poses, six front, six three-quarter, six fixed-world and four close grip views. **46renders do not mean46animation poses.** All hashes independently checked; source GIF24×30ms=720ms. Own browser plays original GIF plus exact source PNG sequence for seven cycles; logs observe all24indices and repeated boundary wraps. Temporal/seam sheets and silent browser video are retained. No interpolation, mirroring or synthesized pose. Six-frame diagnostic views are held120ms each; fixed-world replay resets for inspection and is not an infinite translated walk.

`actual-carry-E01-E13.jpg` and `actual-grip-close-reviewed.jpg` reproduce actual source renders only. These are technical artifacts and are not renamed final art. The visibly unfinished generic garment edges/face/hair remain in the rejected appearance scope; this verdict does not accept them.

## Limits and reproduction

No game renderer/controller integration, completed start/stop action, accepted six-direction exports, final anatomy/likeness, final game walking or RC certification. Physical phone/Safari/iOS/family NOT RUN. Proof video is silent; no audio claim. No main merge/deploy.

Reproduce fresh Blender `measure.py`, `collision.py`, `grip.py`, each `--threads 2` with isolated user config paths under/tmp. Serve checkout on5298 then run `browser-review.py` with `/tmp/ruby-rc-tools/bin/python`. Only QA outputs written. Approval here is to continue technical prototypes, not to activate them in production.
