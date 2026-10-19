# First painted E8 source: registration diagnosis

Candidate only; not runtime approved. `painted-source.png` is byte-identical preserved source. Eight native cells use `round(i*width/4)` and `round(j*height/2)` boundaries, without pose crops or shifts.

`global-normalized.png` resizes the entire1586×992 canvas once to1536×960 (x.9684741488,y.9677419355). The tiny aspect adjustment is global, not pose fitting. `frame-*.png` are fixed384×480 cells from that whole-canvas result. `index.html` displays these frames at the original eight-phase cycle1666.667ms, no interpolation, optionally with native guide ghost. Open directly in a browser.

At alpha≥16 painted/guide bbox height ratios range1.174–1.223; painted bottom differs+24…37px. First-row local top46…50px versus second-row33…37px indicates inter-row registration drift. These are silhouette measurements, not anatomical height or stance/contact estimates. Long painted hair affects silhouette width and height. A single global normalization cannot prove contact preservation.

`registration-diagnosis.png`: each painted row followed by corresponding guide row. Red cross=fixed native root, blue=bbox(alpha≥16), green=painted low95px connected-component bounds(alpha≥128). These components are **foot candidates, not anatomical ankle landmarks**; nearby legs may join. Native guide ankle joint projections are copied into `analysis.json`. No invented painted joint coordinates, per-pose correction, warp, repaint or source mutation.

Reproduce: `python3 scripts/painted-ruta-analyze.py` (source path currently points to root-owned painted-ready worktree). Output hashes and exact source rectangles are in `analysis.json`.
