# Painted Ruta from the native walk — art/animation pilot, not runtime assets

Maksim's latest direction: the native child-proportion 3D walk is a useful pose base; now make illustrated sprite frames resembling the approved Ruta. Native 3D technical acceptance is **not** inherited by this new repaint.

Created using the built-in `image_gen.imagegen` tool, transparent background requested. Exact prompts and ordered reference hashes are recorded in `generation-provenance.json`:

- `pose-source-12.png` → `painted-sheet-v1.png`: twelve evenly sampled native phases, illustrated style experiment. Prompt `prompt-v1.txt`.
- `full48/pose-source-48.png` → `full48/painted-sheet-v1.png`: all 48 consecutive native phases. Prompt `full48/prompt-v1.txt`. Ordered inputs: native pose sheet, approved `public/assets/characters-v1/ruta-idle-pilot.png`, and the twelve-pose beige style study.

All source poses originate from frozen native blend `bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706`. Source sheets are deterministic whole-canvas packing, not per-frame shape deformation. Raw generated outputs are copied unmodified from the tool cache and remain here; beige JPEGs are QA-only composites, not replacements for alpha PNGs.

The generator returned 1295×1215 for both sheets, rather than the requested 2048×1920; layout and actors changed scale. The painted result is not a pixel-locked render. Full48's measured shared extraction grid is 162×200, origin(0,30), eight columns/six rows, with one transparent right column and fifteen bottom rows added as atlas padding. No per-frame origin fitting, resizing or warping is authorized by this packing. Some raw background pixels have alpha1; no semantic pixel cleanup was performed.

Static independent review is in `docs/chapter-1-rc/qa/painted-native-style-v2/`. The drawings look closer to the approved young Ruta, but the visible heading shifts toward profile; exact native knee/sole positions, physical bag side, face identity from occluded views, registration stability and game integration are not proven by a sprite sheet. The full48 pilot must be viewed at the native cycle duration 40/24 seconds (28.8 phases/second); the twelve-pose experiment is not final smoothness.

Source reference credit remains: Quaternius CC0 body/gait; Ellie / Sprite Fright, Blender Studio / Blender Foundation CC BY4.0 native head/hair reference (full attribution in ../ruta-ellie-head-v1/ATTRIBUTION.md); approved Ruta identity/art from the repository. No source license is relabelled CC0 by this generated repaint.

Production/runtime activation: **NO**. Six walking headings/camera variants, native transitions and actual short/long/bridge game routes remain pending. Physical phone and family test NOT RUN.
