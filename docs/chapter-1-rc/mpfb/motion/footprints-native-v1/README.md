# Actual evaluated boot footprints — native planning input

#36 / PR71. `art/characters-mpfb-v1/motion/footprints-native-v1/manifest.json` indexes335 actual render-level boot measurements over11 states: idle7, startL/R13each, walk25 (24raster poses plus terminal join), stopL/R13each, settle7, compact left/right60 pivots41each and left/right12081each. All use native30ms raster cadence, including measured poses that have **not** been rastered. This is physical source input, not a claim of335 new images or game route clearance.

Each foot has its own counterclockwise convex hull of every actual evaluated weighted boot vertex projected to XY. Source SUBSURF is evaluated at render level; side membership uses native L/R skin weights>.5 and requires nonempty regions. Every selected vertex is checked inside its resulting hull. Full boot, including the swinging/upper boot, is conservative; it does not fill the gap between left and right feet. WorldZ ranges are geometric height, not force/ground-contact simulation.

Root translation/orientation are separate at each timestamp. Two explicitly named equivalent hull coordinate forms are supplied:

- `fullBootXYHullRootRelativeNativeMeters`: actual worldXY minus rig-origin translation; **clip native yaw retained**. Apply only external placement heading before adding the physical root curve once.
- `fullBootXYHullActorOrientationRemovedMeters`: actual vertex minus rig origin, then inverse rig quaternion. Physical meters retained; apply complete external+clip orientation once, then physical root trajectory once.

Do not apply clip yaw twice, retime root alone, scale stride/hulls to fit roads or slide endpoints. Native forward is−Y; native XY→base-grid XY uses`[[0,-1],[-1,0]]`, a coordinate-basis change rather than image/model mirroring. Screen projection/camera calibration is separate. Current generic calibration is a reference only; final appearance needs renewed physical/body-height calibration.

The source/shoe receipt records complete source SHA, raw boot topology+skin-weight SHA, selected/evaluated vertex counts and render subdivision. **Generic hulls do not certify styled shoes.** Source geometry/weights/rig/source changes require fresh export and clearance checks; boot polygons cannot silently come from generic cached PNGs.

Reproduce with Blender4.5.3, isolated `/tmp/ruby-mpfb-motion-config`,`--threads 2 --python-exit-code 1 --python scripts/mpfb-motion-footprints.py`. This writes only its motion namespace, never source blends. Optional`RUBY_MPFB_FOOTPRINT_INCLUDE_NATIVE_KEYS=1` adds authored subframe keys; default30ms hulls are **not** a continuous swept-envelope certificate. The root planner owns confirmed-hex union containment, interpolation/swept checks, actual goal-hex endpoint safety and legal route coverage without puzzle/road/solver changes.

For final styled sources use`RUBY_MPFB_FOOTPRINT_SOURCE_SET=/absolute/source-set.json` and a fresh`RUBY_MPFB_FOOTPRINT_OUTPUT_NAMESPACE` inside motion. Source-set is a JSON array: each entry supplies`state`, `source`(absolute or repository relative), `actions`(object-name→action-name), `frames`, `durationMs`; optional`rigObject`, `bootObject`, `rasterScope`. Custom registry does not depend on generic source files. `RUBY_MPFB_BOOT_OBJECT` changes the default shoe name. Native scene units must already be meters and the actor root must remain upright with yaw-only proper placement; body lean belongs to native bones. No raster rendering, per-frame fitting or source saving occurs.

Example registry entry shape (replace source and real saved action names):

```json
{"state":"walk","source":"path/to/styled.blend","actions":{"Rig":"Actual saved native action"},"frames":[1,2,3],"durationMs":720,"rigObject":"Rig","bootObject":"Styled boots"}
```

The new generic signed/composed pivot source checkpoint is b5dc4f2. Original left60, straight and transition sources are unchanged. Appearance remains rejected, no runtime activation or one-hex/full body-bag clearance is claimed. Hull artifact size is about9.16MB; source-only metadata, zero new raster cost.
