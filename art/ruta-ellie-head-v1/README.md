# Ellie ready-head source pilot (#36)

Stage1 source checkpoint: native original downloaded and inspected before binding. Original21.85MB Blend has all11textures packed; separate1659vertex head, real eye/brow/lash/teeth/tongue/hair meshes and full facial rig. Original embedded scripts were not auto-executed. Existing native modifiers evaluated at original neutral frame1; native render subdivision clamped1..2. Extracted12parts217971vertices with existing UV/materials. No new face primitives, drawn facial decal, raster manipulation or body/Walk change.

See ATTRIBUTION.md and source/provenance.json for CC BY4.0, primary URL and hashes. source/object-inspection.json records original object/material/modifier inventory; extraction.json records each selected object and derived geometry hash. ellie-native-head-parts.blend is a static native evaluated source library in original Ellie world coordinates. Full original is retained unchanged for facial rig/expressions and reproduction.

Head binding and neutral pilot remain pending corrected B source action inventory from root. Previous B saved source may have purged its unused Walk retarget action; do not claim that action is present without reopening corrected source. No runtime/main/common files, root-owned body/style source or shared tools touched. No push.

Reproduce extraction: Blender4.5.3 --disable-autoexec -b -t2 --python scripts/ruta-ellie-head.py. Extracted short dark hair is a source quality reference, not accepted Ruta hair. Static geometry freeze preserves complete 3D facial form but not standalone facial animation; original complete rig stays in source original.
