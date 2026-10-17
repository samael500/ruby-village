# Rapid touch after an invalid drop

The coordinator reproduced the author's intermittent report on the current game: six identical native CDP touch workflows,80ms presses and120ms gaps. Three passed and three failed. Failure traces show five right-button pointerdown/up pairs but four compatibility clicks, leaving the selected composite at the wrong rotation. This was not fixed by requiring a slower user.

The action buttons now activate a deliberate touch release once. Matching trusted compatibility clicks are suppressed by pointer ID before they can hit a rearranged dock. Mouse and keyboard retain native clicks. Movement outside a tap, cancellation and disabled controls do not activate. No timing delay is added to gameplay.

The same six workflows passed6/6 after the change. The complete ten-case mouse/touch × select/drag × compound/bridge plus cancel/undo/switch/system-cancel/pause/reload suite also passed with120ms gaps. Source reports/screens/videos are in `fast-after-drop-repeat`, `fast-after-drop-fixed` and `fast-full-fixed`; raw recordings remain on disk under ignored `raw-video/` directories.

`scripts/qa/fast-touch-buttons.py` separately exercises48 native touch taps with100/150/250/500ms gaps, then Enter, Space and mouse input. Its exact result is in `fast-touch-buttons/report.json`. Native Chromium input is not a physical phone test. The changed input adapter must be independently rechecked during final #37; earlier independent #61 results predate this additional fix.
