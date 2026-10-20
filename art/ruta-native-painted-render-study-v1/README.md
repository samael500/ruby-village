# Deterministic native painted-render study

Candidate fallback, **not accepted painted style or runtime art**. Frozen original read-only source SHA bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706. Same whole meshes, rest rig, skin weights, Walk timing/curves and approved costume source; no new face/hair geometry or per-frame image generation. Actual exporter base E camera512×640, fixed origin/scale.

The bounded change is shader/compositor only: preserve native Ellie face/eyes/hair UV/alpha shaders, retain existing warm toon body colours/shading, add very subtle pigment noise from a persistent rest-coordinate POINT attribute and warm facing-edge ink. Blender compositor adds one native pixel of warm silhouette contour. No Python pixel painting or image fitting. The rest attribute is the only mesh-data addition; base positions/polygons/weights, all rest bones and all actions are exactly hash-equal before/after.

render-study.py saves the native source/manifest before rendering only E phases0/30/40. The goal is stable actual3D motion with a more drawn surface. Matching the accepted generated illustration is an open artistic question; preserving the existing native silhouette/face may limit it. No full48 export, no gameplay/no-slip acceptance.

Blender Studio Ellie CC BY4.0 and inherited Quaternius/Cortu rights/provenance remain in the repository source handoffs. Material/compositor adaptation is recorded in manifest.json. Source packed textures and native shader protections are retained.

Actual three-pose outcome: thin warm silhouette ink and subtle surface variation appear, but the native back-three-quarter face, smooth3D hair and sparse garment/bag detail remain visibly different from the accepted painted target. This study **does not match or replace the accepted artwork**; bounded fallback completed without a48batch. comparison-native-v-accepted.png uses one shared global scale/translation for the painted reference display, never individual fitting. Cold-open source-data checks are recorded separately.

Reproduce with Blender4.5.3 `--disable-autoexec --python-exit-code 1 -b -t 3 --python art/ruta-native-painted-render-study-v1/render-study.py`. Python exit exceptions must fail. This original run was explicitly checked by final log marker, three actual outputfiles and a separate cold-open probe, not exitcode alone.
