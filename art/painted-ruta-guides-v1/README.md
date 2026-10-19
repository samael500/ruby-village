# Walk E repaint guides (#36)

Deterministic transparent technical guides, not finished painted sprites. No Idle, labels, grid, source rig modification or artistic raster generation.

- `walk-e24-guide.png`: 1536×1280 RGBA, row-major 6×4, cells256×320. Frame indices0–23, source Walk frames40*i/24; cycle1666.6667ms.
- `walk-e8-key-guide.png`: 1536×960 RGBA, row-major4×2, cells384×480, indices[0,3,6,9,12,15,18,21]. Each entire delivery cell uniformly enlarged1.5 with Lanczos.
- Root local pixel coordinates: E24[128,258.42965602874756], E8[192,387.64448404312134]. Global root equals local root plus cell origin. No per-frame centering, cropping, scale or translation.
- `guide-contract.json`: exact source hashes, cell map, output checks. E24 decoded pixels equal original final atlas Walk cells exactly.
- `pose-markers-e8.json`: continuous native evaluated skeletal joint projections and head/head+hair projected vertex bounds. Anatomical left/right, x right/y down. Knee=LowerLeg bone head, ankle=Foot bone head; bounds include hidden geometry and are not alpha bounds. All8Root projections match the fixed anchor exactly.

Reproduce from repository root:

```
python3 scripts/painted-ruta-guides.py
blender -b -t 2 --python scripts/painted-ruta-posemarkers.py
```

Native source/actions/weights and all runtime/common files remain unchanged. Underlying stock likeness is not approved Ruta; guides preserve accepted native gait for the separately owned artistic repaint. Later painted output must retain registration and be checked for full alpha containment and pose/contact consistency.
