# Painted native-pose packing diagnostics

Primary current baseline is full48/review.html; see its README and audit for limits. This directory also preserves the earlier12selectedposes at7.2fps in review.html/manifest.json. Twelve poses are not full-density48motion. Both cases use one shared fixed grid per asset, whole native frames, unmodified raw RGBA and one constant diagnostic comparison calibration. Exact canonical reference is public/assets/characters-v1/ruta-idle-pilot.png; docs/prologue/ruta-approved.png was considered initially but is not the delivered reference.

New helper scripts/ruta-painted-native-pack.py supports `--case 48` / `--case 12`, default48. Source raw/prompt/provenance remain root-owned and unchanged. Native source/action tempo unchanged. No animation smoothness, physical anchor, art acceptance or game integration claim follows from mechanical packing.
