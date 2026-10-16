# #36 reproducible motion pilot — technical prototype

Base 1094c56 (pilot PR #54); branch art/36-ruta-motion. Maksim accepted the raster Ruta appearance through the coordinator; that acceptance is preserved and is not requested again. This deliverable is **not final painted motion** and does not replace the accepted raster in production.

## Source and export

- `scripts/character-rig.py` builds the editable armature, simple colored segmented model, materials, IK foot controls/poles and one shared 16-frame/800 ms cycle; `art/blender/characters/ruta-motion-prototype.blend` includes all geometry/materials/action, no external dependencies.
- Six directions are rendered from that one geometry/action. Camera is orthographic at [0,-8,4.8], looks at [0,0,1], scale2.65; frame256×256. Actual screen projection determines model yaw for e/se/sw/w/nw/ne. The asymmetric right-hip satchel is part of model geometry, never flipped.
- Fixed root-ground anchor [128,215.26] pixels across all96 frames. Original alpha is preserved. The anchor is the projected ground midpoint under the rig, not the transient lowest shoe pixel. Cycle stride .72 world units; planted control travels backward linearly, swing control rises .09 units. Vertical torso bob .012 units; head/arm motions are keyed in the same action.
- Loop includes matching source keys at1/17; exports1–16 at20fps. Contact markers at1/9. Frame/sourceRect/anchor/duration/direction/yaw/loop are in manifest. Export bounds inspected in contact sheet and six-directions.jpg.

Reproduce from repository root:

```
/tmp/blender-4.5.3-linux-x64/blender -b -t 2 --python scripts/character-rig.py
```

Blender4.5.3, Workbench256px,2threads. No other processes or other projects were modified. No generative independent animation frames were produced.

## Runtime and browser checks

`CharacterRoute` adds arc-length movement and one-time completion independent of sprites. Pause discards suspended time; reduced motion reaches the result without ongoing walking. Constructor copies/validates route input. Existing `CharacterPlayer` controls contacts and clip clocks. 57/57 tests pass (two additional tests compare30/144Hz completion and pause/reduced-motion); tsc and Vite build pass.

`preview.html` is an **isolated motion stand using the real TypeScript runtime**, over the repository's v8 courtyard background. It is not an actual production level and its illustrative hex route is not a puzzle solution. The phase clock scales by the projected stride per direction to match screen travel. It demonstrates all6 headings, a real pause button and reduced-motion input. Browser evidence: desktop1280×720, landscape844×390, silent six-directions-runtime.webm. `browser-checks.json`: pause preserves position, completion fires once, reduced motion completes, no page errors. Run with Vite port5186 and `python scripts/character-capture.py` in a Playwright environment. Video is silent intentionally: audio integration is owned by #50/#46, not a fake full-game mix.

## Remaining work / acceptance limits

- The model is deliberately simple technical geometry. Face/hair/clothes are not the accepted painted Ruta; **do not ship these renders as final art**. Final model detailing, coherent paint/stylization of all rendered directions and alpha-edge art review are still needed.
- IK stance contacts are a procedural first pass, not approved gait. Need perceptual check for foot slide, knee shapes, weight transfer and perspective against final production camera; idle breathing/blink, soft start/stop/turn blends are unfinished.
- Browser stop currently selects frame1; this is a technical transition, not an approved relaxed idle.
- No crouch/basket poses yet, no six villagers. No production prologue/gameplay integration or bridge/fence occlusion acceptance. These screenshots/video must not be presented as those checks.
- Actual phone, family test and final auditory/visual game QA remain not-run.
