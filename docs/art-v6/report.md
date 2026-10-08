# Art v6 integration

## Contract clarification

Maksim explicitly approved redesigning the layouts under the new backgrounds, with verified solutions. The original HANDOFF constraint preserving exact coordinates/sets is superseded by that answer. Stable level IDs, original dialogue text, controls and progress identity remain.

All eight levels now use a regular 11×7 logical grid displayed with yScale=.65. Sandbox retains 7×5, 9×6, 11×7. Board radius70 and origin140,330 are calibrated in source1672×941 pixels; the background and ground translation use the same uniform contain scale. Rotation60 is logical, pointer hits use inverse projection. No raster was regenerated or distorted.

`src/art-geometry.ts` defines conservative manually traced foreground exclusions and explicit water-cell rows; no color segmentation. Apple canopy/trunk and flowerbed are blocked and not duplicated. Forest has no river in the new background, so its bridge is replaced with stone pieces. Each level has a separately validated reference; gate uses all seven singles, later levels allow one spare. Sets changed where longer routes required it. A reproducible small DFS is in `scripts/solve-art-v6.ts`; solutions are `src/art-solutions.json`. Uniqueness is not claimed.

## Screens and persistence

Live DOM main menu, light wood tray, paper dialogue/results and pause menu follow the UI references; the UI PNGs are references only, not clickable backgrounds. Start/continue, choose level, settings, next level and map use actual state. Restart requires confirmation and preserves chapter completion. After forest the completed chapter is shown, without playable chapter two.

Existing localStorage key and version2 completed/introSeen migration remain. Optional session and preferences extend that payload. Current layout, level, sandbox size, control mode and reduced motion survive reload. Loaded placements are validated against current pieces/terrain; corrupt, out-of-field or overlapping pieces are discarded. Prior published builds did not persist unfinished placements; missing session starts the appropriate unlocked level. Storage denial retains session play with an on-screen notice.

One pause clock covers all modal/orientation blockers, including overlapping portrait + pause panel. Ruta uses the approved static PNG translated by her feet along the projected path; animated walking sprites are not in the package. Reduced motion skips travel and disables decorative animation. The painted mill wheel stays static; no duplicate wheel is overlaid.

## Art differences and remaining limits

The full background is contained, with dark green free edges. Gates and buildings are baked in; no separate duplicate sprites. Short walks to actual thresholds are not invented: endpoints remain on nearby valid ground, approximately one cell away from some painted entrances. Long permanent approach paths have not returned.

Water banks are curved illustrations versus discrete water hexes; a translucent blue tint and ≈ explicitly identify game water. The outline can extend slightly onto bank plants. Exact bank-to-hex artwork, separate foreground masks and a mill wheel layer remain future art work. No route travels through the blocked apple crown or flowerbed. The projection is an affine approximation of the painted camera.

UI is implemented in CSS/SVG; it does not reproduce every leaf/corner from the baked mockup. Sound/music assets and audio logic are absent, explicitly labelled in settings. PNG backgrounds are about24MB combined and can load slowly on a mobile network; screenshots do not validate physical touch ergonomics or Safari.

## Verification

`npm test`, `npm run build`; browser suites `tests/art_browser.py` and `tests/chapter_browser.py`.

Eight reference solutions placed using actual projected cell screen coordinates on1280×720,1920×1080,844×390,1024×768. Screenshots of all eight solved boards on1280×720 and844×390 are in `docs/screenshots/art-v6/`. Separate UI suite covers sequential unlock/next/finale, reload/session, restart confirmation, reset, sandbox drag/undo, modal + orientation pause, touch bridge cancellation/invalid drop and four-cell piece dragging.

Historical `road_v5_browser.py`, `art_fixture_browser.py`, `orientation_browser.py` and `browser_check.py` still describe pre-v6 scene IDs/UI and should be run against their historical commits, not as current-v6 visual assertions. The current suites cover the changed flows.
