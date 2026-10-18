# MPFB native IK — technical motion study, rejected appearance

Issue #36, isolated branch `art/36-mpfb-motion`, source checkpoint `25690fa`. This uses the genuine packed `appearance-v1` MPFB body, clothing and weighted standard rig. The generic face, hair, wardrobe and satchel are **not accepted Ruta art**. No runtime or approved appearance source is edited. This motion/action is intended to be reusable after separate likeness work; it is not user approval or production readiness.

The [official getting-started guide](https://static.makehumancommunity.org/mpfb/docs/getting_started.html) was read, including rig → clothes → helpers ordering. Existing source already has rigged clothes. MPFB2.0.18's local `LegHelpers.get_instance(...).apply_ik` builds native `LOWERUPPER` leg helpers; this study uses the complete four-segment native chain, knee pole control and no stretching. The separate upper-leg IK constraint is muted to avoid two competing solvers. The actual skinned 19158-vertex MPFB body, clothing and boots deform in 3D; no image cutouts or source-PNG deformation.

`art/characters-mpfb-v1/motion/pilot/` contains packed source, actual whole-frame Cycles renders, loop and diagnostic front/three-quarter strip. 24 genuinely different poses cover720ms; frame25 is the repeated action endpoint with one stride of continuous world translation. Rate100/3fps, sample spacing30ms. Root translation stays linear while pelvis is lower in double support and rises in midstance (32mm peak to peak), with1.49° yaw and14cm track width; the stance ankle remains in world coordinates, heel and toe rotate about distinct pivots, swing clearance45mm, a free left arm and intentional right-hand strap carry. Soles are weighted to their foot bones with a40mm blend to the original shin weights; accessories gain torso/root skin rather than remaining motionless armature-object children.

The E camera is actual3D side projection, model forward−Y mapped to scene+X. Production angle0, groundScale.65 gives camera elevation `asin(.65)`. No mirrored opposite-direction exports. Model→scene scale uses the measured real E frame cycle maximum alpha height251px at384px / ortho1.70m, mapped to136scene pixels; retained physical stride.568755m,69.61scene pixels at that calibrated height. The earlier study baseline67.46px was based on259px projected height; correcting actual final silhouette height changes scale by3.19%, with physical stride unchanged. This is a technical calibration, not an artistic approval. It must be recalibrated after accepted appearance and matching game scale.

## Reproduce

```sh
BLENDER_USER_CONFIG=/tmp/ruby-mpfb-motion-config/config \
BLENDER_USER_SCRIPTS=/tmp/ruby-mpfb-motion-config/scripts \
BLENDER_USER_DATAFILES=/tmp/ruby-mpfb-motion-config/data \
PYTHONDONTWRITEBYTECODE=1 \
/tmp/blender-4.5.3-linux-x64/blender -b --threads 2 --python scripts/mpfb-motion-pilot.py

# Fresh process: independently measured evaluated boot vertices, never target-only readback.
BLENDER_USER_CONFIG=/tmp/ruby-mpfb-motion-config/config \
BLENDER_USER_SCRIPTS=/tmp/ruby-mpfb-motion-config/scripts \
BLENDER_USER_DATAFILES=/tmp/ruby-mpfb-motion-config/data \
/tmp/blender-4.5.3-linux-x64/blender -b --threads 2 --python scripts/mpfb-motion-verify.py
BLENDER_USER_CONFIG=/tmp/ruby-mpfb-motion-config/config \
BLENDER_USER_SCRIPTS=/tmp/ruby-mpfb-motion-config/scripts \
BLENDER_USER_DATAFILES=/tmp/ruby-mpfb-motion-config/data \
/tmp/blender-4.5.3-linux-x64/blender -b --threads 2 --python scripts/mpfb-motion-contact-render.py

BLENDER_USER_CONFIG=/tmp/ruby-mpfb-motion-config/config \
BLENDER_USER_SCRIPTS=/tmp/ruby-mpfb-motion-config/scripts \
BLENDER_USER_DATAFILES=/tmp/ruby-mpfb-motion-config/data \
/tmp/blender-4.5.3-linux-x64/blender -b --threads 2 --python scripts/mpfb-motion-grip-render.py
python3 scripts/mpfb-motion-review.py
```

Set `RUBY_MPFB_RENDER=0` for source/measurement only. No install or vendor modification. Blender4.5.3LTS, CPU2threads, Cycles8samples and denoising,384px square. Existing licenses and source-asset provenance remain under `art/characters-mpfb-v1/licenses/`, `source-assets/`, inventory and MPFB README: native mesh/rig/assets CC0, MPFB source GPL3. No new third-party assets.

## Actual defects found, corrected and retained

The initial measured stance was offset too far behind the pelvis; the solver missed by up to69mm. Real side render and measurements are retained in `motion/rejects/initial-backreach*`. Corrected strike position is.30stride ahead of the cycle root. Independent fresh-process checking also caught newly created helper bones using quaternion rotation mode while Euler channels were being keyed. Explicit XYZ setup now makes the saved/reopened action match authored heel/toe poses. This is why generator target reports alone are insufficient.

`independent-contact-check.json` is from a separate Blender process opening the saved file. It measures actual armature-evaluated source shoe sole vertices in world coordinates, temporarily disabling subdivision solely to retain source vertex indices. The flat-stance sample window is phase.10–.46; knee angle uses actual hip/knee/ankle bones. Current measured flat-sole drift is about.020mm, knee flex15.75–52.89°, minimum sole height+.400mm on both sides. Measured toe-marker drift during phase.48–.60push-off is1.20mm, rather than the much smaller flat-stance value. These establish solver/skin contact accuracy only, not naturalness, final clothes quality or visual acceptance. Heel/toe roll and overall cadence still require visual review; no six-direction or start/stop pass is claimed yet.

Front-view inspection also identified the original27.8cm-wide MPFB rest stance as too wide for a calm child walk. Actual rejected strip is retained as `motion/rejects/wide-original-rest-track.jpg`. IK stance is narrowed to14cm, without remodeling anatomy. Independent evaluation establishes24 unique poses and endpoint root-relative bone matrices closing within5.8e−6.

The6 `fixed-world/` renders and `actual-fixed-world-strip.jpg` use an unchanged camera and10cm world checker plane. The root genuinely advances in world space while planted shoe vertices stay on that surface. These are rendered geometry, not image offsets. Fresh-process deformation check measures7840changed body vertices,8426shirt/trouser vertices,1722shoe vertices and3106evaluated waistcoat vertices between frames1and7. Exact displacement counts and distances are retained in the independent report.


## M1/M2 correction after independent review of24315ea — d7249c0 history

Independent review correctly rejected constant7.19776° elbows and right-hand/satchel intersections in21/24frames. The preserved24315ea source remains available in Git; its actual three-view sheet is retained under `motion/rejects/24315ea-rigid-elbow-hand-bag.jpg`. Contact accuracy did not imply natural arm motion.

The d7249c0 correction aimed both complete native upper-arm and forearm segments per phase, resetting base rotations each frame to avoid accumulated roll. At d7249c0, left elbow varied4.99–29.41°, bag-side right elbow13.95–25.68°. The M3 carry below supersedes this held-forward arm path. The bag-side upper arm swings in a smaller anterior arc, with a softly changing elbow bend and wrist aligned to the forearm through the native middle-finger base, so hand, forearm and sleeve pass in front of the actual satchel. Bag/strap geometry, foot contacts, physical stride and720ms duration are preserved. No bag removal, invisibility or speed reduction.

`scripts/mpfb-motion-arm-check.py` opens the saved source independently and intersects actual evaluated body hand/forearm and shirt sleeve triangles against satchel, flap and buckle. Body masks are disabled only in that measurement process; the shirt keeps its actual render subdivision and evaluated interpolated weights define limb membership. All24poses currently report0triangle intersections in those checked regions. This is a repeatable implementation check; external reviewer confirmation and visual naturalness review remain pending. It does not certify all clothing/body collisions or final game art.


## M3 correction — intentional carry of the existing ONE strap

Independent repeat b9573ae correctly rejected the unmotivated open reaching hand and rigid upper-body block at d7249c0. Its actual three-view image is retained under `motion/rejects/d7249c0-open-reaching-arm.jpg`; the immutable source remains in Git. This continuation chooses one concrete gesture: the right hand holds the existing diagonal strap near the upper chest, while the left arm swings freely opposite its leg. The strap remains one original mesh. There is no bag hiding, shrinking, removal, extra strap or gait-speed reduction.

Closed native fingers form the grasp. A native three-bone thumb IK/pole routes the thumb around the near strap edge; it is not pushed through the band. The hand targets the actual evaluated strap surface; FK arm lengths are solved analytically and the wrist follows the chest/strap orientation. The same original strap geometry gains chest-to-root skin weights so its upper end follows the torso and lower end follows the bag. `mpfb-motion-grip-check.py` compares the original bag, flap, buckle and strap raw mesh, object transforms, geometry modifiers and render visibility against appearance-v1: all signatures match, with exactly one actual strap mesh.

Fresh saved-file measurement reports0palm/finger/thumb surface intersections with the strap over25cycle samples, with nearest clearances palm1.31–1.41mm, fingers2.21–2.31mm and thumb1.12–1.72mm. These small mesh clearances describe a supported carry pose, not a force-based cloth/contact simulation or mathematically exact zero-gap contact. The original failed grasp looked plausible in a close render but had real surface penetration and a drifting reference; its image/check log are retained under `motion/rejects/m3-first-grip-*`. The final check uses actual evaluated skin triangles, not generator target coordinates.

Left wrist rig-local fore/aft travel is110.30mm; the intentionally supporting right wrist follows the strap (0.49mm fore/aft travel). Left elbow flex9.89–23.88°; the carrying right elbow stays108.70–109.07° because it supports the strap. Distributed torso counter-rotation spans5.04° relative to pelvis (±2.52°), while separate neck stabilization limits whole-head orientation excursion to0.340° total. This gives a living torso and calm head without adding nodding. Lower-body world contacts, physical stride0.568755m,720ms duration and gentle swing clearance are unchanged. The earlier slightly crouched impression is not claimed resolved by the arm gesture.

Actual exports now contain24Ecycle frames,12front/three-quarter diagnostics,6fixed-world diagnostics and4native close grip views:46distinct rendered PNGs, not46animation poses. `actual-grip-close-strip.jpg` shows real front/three-quarter frame1/13hand/strap geometry; `E-actual-cycle.gif` remains24frames×30ms. Reproduce the extra views with `scripts/mpfb-motion-grip-render.py` and run the saved-file grip audit with `scripts/mpfb-motion-grip-check.py`, both with the same isolated Blender environment and `--threads 2` above.

Author implementation checks currently pass foot/loop/unique-pose and checked bag/limb/sleeve/grip surface scopes. Independent97-subframe repeat and whole-character naturalness review of M3 remain pending. Appearance, face, hair and wardrobe remain explicitly rejected generic source art. No six-direction set, start/stop completion, runtime integration, final Ruta or game approval is claimed.
