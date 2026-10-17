# MPFB native IK — technical motion study, rejected appearance

Issue #36, isolated branch `art/36-mpfb-motion`, source checkpoint `25690fa`. This uses the genuine packed `appearance-v1` MPFB body, clothing and weighted standard rig. The generic face, hair, wardrobe and satchel are **not accepted Ruta art**. No runtime or approved appearance source is edited. This motion/action is intended to be reusable after separate likeness work; it is not user approval or production readiness.

The [official getting-started guide](https://static.makehumancommunity.org/mpfb/docs/getting_started.html) was read, including rig → clothes → helpers ordering. Existing source already has rigged clothes. MPFB2.0.18's local `LegHelpers.get_instance(...).apply_ik` builds native `LOWERUPPER` leg helpers; this study uses the complete four-segment native chain, knee pole control and no stretching. The separate upper-leg IK constraint is muted to avoid two competing solvers. The actual skinned 19158-vertex MPFB body, clothing and boots deform in 3D; no image cutouts or source-PNG deformation.

`art/characters-mpfb-v1/motion/pilot/` contains packed source, actual whole-frame Cycles renders, loop and diagnostic front/three-quarter strip. 24 genuinely different poses cover720ms; frame25 is the repeated action endpoint with one stride of continuous world translation. Rate100/3fps, sample spacing30ms. Root translation stays linear while pelvis is lower in double support and rises in midstance (32mm peak to peak), with1.49° yaw and14cm track width; the stance ankle remains in world coordinates, heel and toe rotate about distinct pivots, swing clearance45mm, reciprocal arms. Soles are weighted to their foot bones with a40mm blend to the original shin weights; accessories gain torso/root skin rather than remaining motionless armature-object children.

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
/tmp/blender-4.5.3-linux-x64/blender -b --threads 2 --python scripts/mpfb-motion-contact-render.py
python3 scripts/mpfb-motion-review.py
```

Set `RUBY_MPFB_RENDER=0` for source/measurement only. No install or vendor modification. Blender4.5.3LTS, CPU2threads, Cycles8samples and denoising,384px square. Existing licenses and source-asset provenance remain under `art/characters-mpfb-v1/licenses/`, `source-assets/`, inventory and MPFB README: native mesh/rig/assets CC0, MPFB source GPL3. No new third-party assets.

## Actual defects found, corrected and retained

The initial measured stance was offset too far behind the pelvis; the solver missed by up to69mm. Real side render and measurements are retained in `motion/rejects/initial-backreach*`. Corrected strike position is.30stride ahead of the cycle root. Independent fresh-process checking also caught newly created helper bones using quaternion rotation mode while Euler channels were being keyed. Explicit XYZ setup now makes the saved/reopened action match authored heel/toe poses. This is why generator target reports alone are insufficient.

`independent-contact-check.json` is from a separate Blender process opening the saved file. It measures actual armature-evaluated source shoe sole vertices in world coordinates, temporarily disabling subdivision solely to retain source vertex indices. The flat-stance sample window is phase.10–.46; knee angle uses actual hip/knee/ankle bones. Current measured flat-sole drift is about.020mm, knee flex15.75–52.89°, minimum sole height+.400mm on both sides. Measured toe-marker drift during phase.48–.60push-off is1.20mm, rather than the much smaller flat-stance value. These establish solver/skin contact accuracy only, not naturalness, final clothes quality or visual acceptance. Heel/toe roll and overall cadence still require visual review; no six-direction or start/stop pass is claimed yet.

Front-view inspection also identified the original27.8cm-wide MPFB rest stance as too wide for a calm child walk. Actual rejected strip is retained as `motion/rejects/wide-original-rest-track.jpg`. IK stance is narrowed to14cm, without remodeling anatomy. Independent evaluation establishes24 unique poses and endpoint root-relative bone matrices closing within3.1e−7.

The6 `fixed-world/` renders and `actual-fixed-world-strip.jpg` use an unchanged camera and10cm world checker plane. The root genuinely advances in world space while planted shoe vertices stay on that surface. These are rendered geometry, not image offsets. Fresh-process deformation check measures7840changed body vertices,8426shirt/trouser vertices,1722shoe vertices and3106evaluated waistcoat vertices between frames1and7. Exact displacement counts and distances are retained in the independent report.
