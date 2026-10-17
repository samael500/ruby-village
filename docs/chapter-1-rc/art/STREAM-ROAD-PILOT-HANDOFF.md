# Stream / charoite pilot — isolated game review pending

Resources only; no runtime, common manifest, activation, merge or deploy changes.

## Review inputs

- `art/road-v1/charoite-repeat-2x2.webp`: repaired repeat, dense angular purple material. Original generation remains preserved; its first repeat was rejected because the center seams cut stones. `public/assets/road-v1/charoite.webp` is the repaired 1024px lossless derivative. Source/prompt and deterministic composition are in `repair-source-v2.json` and `encode.py`. Independent seam/art/game review remains pending.
- `art/chapter-1-v9/layers/water/stream-pilot/native-background.png`: baked native pilot, 1672×941.
- `geometry-overlay.png`, `entry-review.png`, `exit-review.png`, `bridge-review.png`: exact registration and enlarged shoreline review inputs; no bridge artwork is baked into this source.
- `wide-registered.png`: 3272×1200, original native rectangle `[800,129,1672,941]`. Flowing stream reaches both outer edges. Generated v1 was rejected for recomposing/enlarging the core. V2 receives one uniform source affine registration, an exact native board restore and a 48px decorative edge join. The entire 77-cell interior remains pixel-identical to the native pilot.
- `manifest.json` beside the pilot describes delivery files. `background.webp` already includes water; do not stack `logical-water.png` over it. `dry-background.webp` plus that overlay is the alternative separate-layer presentation.

## Reproduction and checks

Run `python3 art/road-v1/encode.py` and `python3 scripts/art-v9-stream-pilot.py`.

The rebuilt stream report is `layers/water/stream-pilot/checks.json`, distinct from the stale earlier `layers/water/checks.json`. It verifies the accepted 77-cell board and seven actual water cells; opaque water leak into full free-cell interiors is 0px (1px raster boundary tolerance); every dry free-cell interior has 0 changed RGB pixels; bridge center/end alpha is 255/0/0; rejected old bend is 0 and accepted new bend is 255. Logical masks have no erosion. Bank art feathers inward along sides only; first/last cells stay open at the complete board perimeter. Decorative continuation is clipped outside the complete board union, not outside just free cells.

Four built-in imagegen edits are retained with exact prompts and source paths: charoite central-cross repair, water-side bank strip, wide outpaint v1/v2 (v1 rejected). No external stock or runtime generation. The road edit restores original outer pixels before inverse offset. No mirrored stones, baked route, camera or CSS offset was introduced.

These raster checks do not certify natural banks, invisible wide joins, tiling appearance, bridge grounding or actual gameplay. Coordinator must review the installed earth→charoite→bank→bridge→bank fragment and real desktop/touch inputs, move/rotate/return/undo/save/reload before activation. Physical phone remains NOT RUN. Mill is not changed by this pilot.
