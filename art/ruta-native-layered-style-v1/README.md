# Historical native costume v1 — rejected detached boot laces

**Superseded by ../ruta-native-layered-style-v2. Actual v1 frames exposed detached lace loops; do not use this source as the final costume.**

Frozen source SHA256: `d33699efbf0a09dbedb3254c30ea645ee60ef2abd046ac73da21106cc659a3ae`.

This combines the independently audited B rest-proportion body and accepted source gait with Ellie authored face/blue iris/copper layered loose locks and the Ruta costume study. It is a new candidate addressing the rejected adult-looking painted pilot; resemblance and actual walking are **not yet accepted**. Static PNGs are native Blender renders, not game screenshots.

Reproduction:

```sh
RUTA_STYLE_INPUT="$PWD/art/ruta-ellie-head-v1/layered-locks-pilot/ruta-b-ellie-layered-locks.blend" RUTA_HEAD_MODE=source RUTA_STYLE_OUTPUT_DIR=art/ruta-native-layered-style-v1 /tmp/blender-4.5.3-linux-x64/blender --background --disable-autoexec --threads 2 --python-exit-code 1 --python scripts/ruta-native-style.py
```

Whole 3D rest modifications only. Head native materials/UV/normals preserved; one right-hip rounded satchel and one diagonal strap. Wrist/finger-weighted body faces retain the original skin material instead of receiving the cream sleeve override. Walk/Idle action hashes before/after are equal (appearance.json); the exporter must additionally cold-open and check the exact source.

Source gait/body: Quaternius CC0. Head/hair: Ellie, Sprite Fright — Blender Studio / Blender Foundation, CC BY 4.0; full credits and modifications in ../ruta-ellie-head-v1/ATTRIBUTION.md. No source license is relabelled.

Next gate: actual 48-frame E/Walk export and atlas pack, then independent browser loop/anchor/style review. Other directions, turns, short/long game routes, bridge and runtime integration remain pending. Physical phone NOT RUN.
