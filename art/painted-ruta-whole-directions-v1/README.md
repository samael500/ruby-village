# Five additional whole-actor Walk24 extractions (#36)

SE/SW/W/NW/NE each contain exactly24 separate8-connected alpha≥16 actor components, minimum500pixels. Each actor bbox is checked against all other actors: no neighboring actor alpha16 pixel is included. Small disconnected components are recorded separately, never merged into actors.

Actor bbox rectangles retain original RGBA bytes, exact equality checked. Source/crop/frame PNG SHA256 hashes are recorded; complete original sheets are preserved. No recoloring, alpha cleanup, per-frame scale, pose deformation or fitting.

Common canvas512×512, original source scale1. Placement preserves bbox offset relative to rounded rational nominal6×4 cell origin, plus common padding128,96. Exact and rounded origins and source→packed translations remain in manifests. Drawing-origin drift remains; footAnchor=null.

Every direction has index.html24phase/1666.667ms unregistered loop, whole24-sheet.png,24frame PNGs, preserved source.png and manifest.json. Top manifest links all6directions, including existing E (distinct384×416 canvas). Technical canvas is not a body-height/physical-anchor contract. Root review.html, native source/rig/actions, image generation and runtime untouched. No art/physical/no-slip acceptance claimed.

Reproduce: python3 scripts/painted-ruta-extract-directions.py (originals also copied here).
