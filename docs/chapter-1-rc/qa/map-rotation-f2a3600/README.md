# Independent map and rotation QA — f2a3600

Result: PASS within the production Chromium scope below. No runtime or art changes.

Checkout: `qa/37-map-rotation-f2a3600`, isolated worktree `/tmp/ruby-qa-map-rotation`. Production `tsc --noEmit` and Vite build passed. HTTP preview served own `dist` at `127.0.0.1:5297/ruby-village/`; 5180 and coordinator servers untouched. `d9e34ec` was not included.

## Verified

- `map.py`: 15 combinations, five viewports (1280×720, 1920×1080, 844×390, 740×360, 1024×768), no/partial/all completed progress. Native painted layers, no SVG paving shapes, all eight level targets ≥44px and inside viewport, labels inside, correct unlock counts, no page/HTTP errors. Full screenshots retained. Visual inspection of representative desktop/landscape/new/partial/all screenshots found dense painted paving and no abrupt solid bands.
- `navigation.py`: independently decoded actual WebP files; wide 1400×800 crop at (200,200), 1000×400, is pixel-exact to base. Real map → gate scene → pause/map → reload/menu/map on desktop and landscape. Scene screenshots and two silent recordings retained.
- `rotation.py`: eight real UI cases: garden composite and stream bridge × mouse/native CDP touch × drag/select. Invalid released drop remains red/unplaced; right rotation auto-confirms only drag; select requires explicit Place. Saved anchor/orientation exact; one undo removes whole instance. Tray rotation before any drop does not place. Active native touch consumes keyboard button activation; native touchCancel restores invalid preview, then valid rotation places.
- `rotation-extra.py`: additional eight cases whose first right rotation remains invalid and second becomes valid. Invalid rotation leaves localStorage byte-identical and no owners; valid rotation commits expected anchor/turn. A second real click/tap at former rotate-button coordinates creates no second placement; one undo removes it. No renderer or layout injection, only progress fixtures.
- `rotation/*-native-events.json` records native pointerdown → pointercancel → lostpointercapture on the same pointer for both composite and bridge. Native touch is browser CDP emulation, not a physical device.

## Harness diagnosis and limits

Initial baseline harness intermittently failed at `center(cell)` (`Locator.bounding_box()` returned None) in stream native touch, after invalid drop but before starting the separate active-touch gesture. Replacing it with `#placement-preview` reproduced the same failure. `rotation/failure.jpg` and `failure-state.json` retain the observation: invalid preview exists, no open dialogs, upper-edge anchor has partly negative preview polygon coordinates; feedback overlaps that region. This is a harness coordinate-selection failure, not evidence that the actual drop/rotate failed. The first complete rerun alone was not treated as a fix. Final harness starts the separate active gesture on the visible selected tray piece and records native pointercancel/capture events; it uses no visibility override or sleeps for this correction. Both final matrices pass.

The left button is unconditionally hidden by existing UI (`src/main.ts`, updateControls); there is no exposed native left control to exercise. No forced click/unhide was used. Only the exposed right control was tested. Cancel button and physical device testing were not independently added here; pointercancel is covered. No physical phone, family playtest, or audio listening was performed. All WebM recordings contain actual browser input and are silent. This is scoped map/#61 integration QA, not final chapter acceptance after subsequent art/gait changes.

## Reproduce

Run from checkout with production preview at port 5297:

```sh
RUBY_QA_URL=http://127.0.0.1:5297/ruby-village/ /tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/map-rotation-f2a3600/map.py
RUBY_QA_URL=http://127.0.0.1:5297/ruby-village/ /tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/map-rotation-f2a3600/rotation.py
RUBY_QA_URL=http://127.0.0.1:5297/ruby-village/ /tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/map-rotation-f2a3600/rotation-extra.py
/tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/map-rotation-f2a3600/navigation.py
```
