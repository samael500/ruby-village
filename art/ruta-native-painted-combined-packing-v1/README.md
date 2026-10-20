# Global union-ROI pack scaffold

NOT RUN until root confirms all48 actual source renders complete. `pack.py` defaults to preparation-only; `--run` requires complete source-contract pinned b14cfb5… and all48 matching PNG file hashes, exact512×640RGBA, sourceframes40*i/48 and one fixed original anchor.

One union of alpha>0 bounds over ALL48 plus8pixels on every side. No per-frame crop/fit/scale/warp or filtering. Crop margin crossing originalcanvas fails closed. One PNG atlas,8columns when legal, both dimensions≤4096 or fail. All retained RGBA bytes round-trip exactly, including lowalpha edges; every discarded pixel must have alpha0. TransparentRGB outsideROI is discarded and NOT falsely claimed fullcanvas-byte-identical. One global anchor offset only. Original source PNGs untouched. Reports original/cropped48-frame and atlas decoded bytes separately from encoded PNG bytes.

No runtime installation, lowerFPS, resampling, artistic acceptance or performance benchmark. Actual packing/roundtrip verification awaits explicit root trigger.

## Actual run after root trigger

All48 actual frame hashes and source-contract verified before/after. Global ROI **(123,110,260,434)** with8pxmargin; atlas **2080×2604** (8×6), under4096, PNG lossless. All48 decoded atlas ROI RGBA bytes exact, all48 restored fullcanvas alpha bytes exact. One originalRootanchor→croppedanchor offset(−123,−110), recorded precisely in manifest. Full48 decoded62,914,560bytes→21,665,280bytes (65.56% reduction); atlas decoded equals that crop budget. Encoded file bytes reported separately, not initialdownload/frame-time measurement. No runtime installed/artPASS.
