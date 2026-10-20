# Rejected wardrobe proof — interrupted E/Walk48 render

**REJECTED. Not a complete pilot, atlas, seamless loop or art/game acceptance.**

Frozen input at verified smoke SHA256 `d33699efbf0a09dbedb3254c30ea645ee60ef2abd046ac73da21106cc659a3ae`, canonical source `art/ruta-native-layered-style-v1/ruta-native-style.blend`. Actual source read was in root's worktree; it was never saved by the exporter. Smoke passed visibility/geometry/camera checks, but those checks do not establish wardrobe quality.

Root and the independent head author inspected actual E04/E08 and found white boot laces outside the lifted boot surface. Root requested stopping the render to repair native geometry/weights. Only our verified Blender PID634665 received SIGINT; it stopped on phase17, whose PNG was not produced. The exporter consequently reports a missing cancelled-frame file and writes no complete source-contract. This is a deliberately interrupted render, not a successful batch.

**17 complete actual source PNGs00..16** are preserved unchanged, with hashes in rejected-partial-render.json. Source range/time/anchor/camera and geometry-only smoke evidence remain in dry-run-contract.json. rejected-wardrobe-contact-sheet.png is an ordinary6×3 assembly of full source canvases uniformly resized. It retains the defect. No pack was attempted; no atlas/loop exists. make-review.py was prepared but not executed because it requires a complete packed manifest.

Rendering used inherited EEVEE64samples, fixed512×640, base/E, source Walk_ProportionProposal48phases over40/24seconds. Render elapsed182.28s before interruption. No per-frame crop/fit, warps, changed timing, model save or runtime installation. The post-render source hash is deliberately not asserted after interruption because root announced a source revision; frozen v2 will use its own hash and a new output directory.
