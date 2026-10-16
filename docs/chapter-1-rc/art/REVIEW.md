# #45 — courtyard pilot, awaiting Maksim's art review

Base: `add76709d66ab6a138014886642f045e658f53bf` (merged technical-layout PR #42). This branch changes no runtime, production assets, game data or UI.

## What to review

Compare `docs/ui-v7/references/00-gameplay-reference.png` with `art/chapter-1-v9/candidates/gate-v2-closed.png` and `gate-v3-base.png`. The recommended direction preserves the warm painted cottage, orange roof, flower-rich edges and calm playable lawn; the expanded accepted grid is wider than the original artistic reference. Review the whole image and the precise polygon overlays, not only object centers.

The v3 base is a genuine painted image, not a Blender render. It removes the front fence/gate for separate foreground compositing. Art acceptance is **pending**. No claim that all eight scenes are finished or that this art is active in the game.

## Contract

All layers use a 1672×941 canvas, origin (0,0), full-canvas crop, no independent resizing. The gate camera has radius 70, origin (140,290), angle 0 and groundScale 0.65. Start feet: (503.73066958946424,426.5); goal feet: (1352.435565298214,699.5). Camera is for ground anchors only; do not flatten character sprites. Shared transform must move art, anchors and logical polygons together.

The seven remaining exact handoff packages live under `art/chapter-1-v9/packages/<scene>`. Each has the unmodified exported geometry and SHA256, camera/start/goal, full free/blocker/water polygon masks and a layer contract. These packages are technical source material, **not final illustrations**. Do not manufacture seven copies of the unapproved pilot style.

`src/scene-v9.json` is a candidate manifest, not an active import. Integration #46 must activate approved art together with #44's matching data. Water/shore, bridges and mill wheel require separate assets and shared camera; no prebuilt bridge in a background.

## Provenance and rights

Existing v1/v2 candidates were recovered from the shared workspace. Their original generation prompts/tool records are unavailable; they remain explicitly unaccepted prior candidates. No external stock image was downloaded for this task. The style reference and geometry are existing repository material; no independent audit of their original license was performed here. v3 was produced with the built-in image_gen tool using the v2 candidate as edit target; complete current prompts and SHA256 hashes are recorded alongside the art. This is a provenance record, not a claim of exclusive copyright.

## Remaining blockers

- Maksim's artistic acceptance of one finished courtyard and the independent pilot Ruta.
- Exact gate/foreground alpha registration and movement verified in production by #46 after acceptance.
- Seven finished scene illustrations and all required moving layers after courtyard acceptance.
- Full desktop/phone gameplay evidence, production traversal and audio video belong to integration/QA; these art source checks do not replace them.

## Actual checks and known defects

- All eight packages are copied from the accepted engine exports, with full polygon masks and cryptographic source hashes; no geometry inferred from painted colors.
- `gate-v3-base.png` is 1672×941. RGBA extraction layers preserve a full-size transparent canvas. Browser-rendered reference comparison and geometry screenshots are under `art/chapter-1-v9/review/gate-v3-*.png`.
- The generated fixed-fence extraction changes small details around the left hinge and has colored fringe along some alpha edges. These are **known unfinished asset defects**, requiring cleanup/re-extraction before production, not a passed layering check.
- The closed composite is suitable for the artistic direction review. An animated open leaf, exact layer registration, walk-behind/depth and motion still need integration checks. No claim of successful gameplay QA is made.
- Reproduce geometry packages with `python3 scripts/art-v9-packages.py`; review SVG/hashes with `python3 scripts/art-v9-review.py`. Screenshots were captured in headless Chromium via Playwright, not from gameplay.

The independent gate-leaf extraction `gate-v3-gate-leaf.png` **failed positional fidelity** (enlarged/repositioned by the image tool) and is retained as a rejected candidate with its exact prompt/hash. Do not composite or animate this leaf. The review HTML deliberately uses the coherent closed foreground and the open aperture without pretending it is an approved opening animation.
