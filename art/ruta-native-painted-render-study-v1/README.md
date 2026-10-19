# Deterministic native painted-render study

Candidate fallback, **not accepted painted style or runtime art**. Frozen original read-only source SHA bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706. Same whole meshes, rest rig, skin weights, Walk timing/curves and approved costume source; no new face/hair geometry or per-frame image generation. Actual exporter base E camera512×640, fixed origin/scale.

The bounded change is shader/compositor only: preserve native Ellie face/eyes/hair UV/alpha shaders, retain existing warm toon body colours/shading, add very subtle pigment noise from a persistent rest-coordinate POINT attribute and warm facing-edge ink. Blender compositor adds one native pixel of warm silhouette contour. No Python pixel painting or image fitting. The rest attribute is the only mesh-data addition; base positions/polygons/weights, all rest bones and all actions are exactly hash-equal before/after.

render-study.py saves the native source/manifest before rendering only E phases0/30/40. The goal is stable actual3D motion with a more drawn surface. Matching the accepted generated illustration is an open artistic question; preserving the existing native silhouette/face may limit it. No full48 export, no gameplay/no-slip acceptance.

Blender Studio Ellie CC BY4.0 and inherited Quaternius/Cortu rights/provenance remain in the repository source handoffs. Material/compositor adaptation is recorded in manifest.json. Source packed textures and native shader protections are retained.
