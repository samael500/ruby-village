# Corrected native costume pilot v2 — art/game acceptance pending

Frozen blend SHA256 `bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706`.

Same source proportions, gait, authored head, copper hair and costume as v1. Actual v1 frames exposed a wardrobe defect: cream boot laces detached below the lifted rear boot. Those rejected frames remain in ../ruta-native-layered-walk48-v1.

Root cause: the boot shaft blends LowerLeg and Foot weights, but added laces were rigidly bound to Foot. Fix: one REST-space ray projection onto the native front boot triangles, 1.5 mm outward offset and barycentrically inherited native skin weights. No pose keys, source gait, camera, frame origins or PNG transforms changed. The geometry test checks every lace vertex against evaluated boot triangles throughout 48 source phases. It measures attachment, not complete costume collision or art acceptance. A real rendered regression phase is included.

Reproduce model with scripts/ruta-native-style.py, same environment as v1 but RUTA_STYLE_OUTPUT_DIR=art/ruta-native-layered-style-v2 and RUTA_STYLE_RENDER=0. Reproduce check/render with scripts/ruta-native-lace-check.py -- --source art/ruta-native-layered-style-v2/ruta-native-style.blend --out art/ruta-native-layered-style-v2/lace-check --render.

Quaternius CC0 body/gait; Ellie Blender Studio / Blender Foundation CC BY4.0 head/hair, see ../ruta-ellie-head-v1/ATTRIBUTION.md. Actual 48-frame E/Walk export and exact lossless pack are now in ../ruta-native-layered-walk48-v2 (e70d049). Independent browser controls/anchor checks passed; visual closure and artistic review remain pending. Runtime unchanged; physical phone NOT RUN.
