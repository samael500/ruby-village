# Internal ready-head costume combination — NOT approved Ruta

This proof combines the ready native friendly Ellie head with the corrected B body and root costume study. The original short dark haircut/brown eyes remain here; they do not meet Ruta identity. This is an internal intermediate, not an artistic acceptance request or final sprite.

Reproduction from committed inputs:

```
RUTA_STYLE_INPUT="$PWD/art/ruta-ellie-head-v1/friendly-pilot/ruta-b-ellie-head-pilot.blend" RUTA_HEAD_MODE=source RUTA_STYLE_OUTPUT_DIR=art/ruta-native-ready-style-v1 /tmp/blender-4.5.3-linux-x64/blender --background --disable-autoexec --threads 2 --python-exit-code 1 --python scripts/ruta-native-style.py
```

Native head materials and normals are preserved, particularly the transparent cornea and iris. Body styling alone changes vest/cream sleeves, bow/buttons, cargo tailoring, rounded single bag, ankle boot cut/cuffs/laces. Rest rig and motion curves remain unchanged. The model uses a single fixed Root normalization, unchanged map camera and fixed full canvas. No painted per-frame registration or raster warp is introduced.

The three PNGs are native static model renders, not game screenshots. The generated blend is a reproducible local cache; committed head source and body/source scripts preserve the required inputs. The next ready-head revision addresses blue eyes and copper long wave hair before loop/style review.

Head source: Ellie, Sprite Fright — Blender Studio / Blender Foundation, CC BY4.0. See ../ruta-ellie-head-v1/ATTRIBUTION.md for full credit and modifications. Stock body/gait is Quaternius CC0. Neither source license is relabelled.
