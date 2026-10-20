# v3 trousers native UV padding preparation

One new UV layer `RutaPaintPaddedTrousers`,11 independently positioned existing charts, constant1450px/nativeUV-unit scale, explicit source-face mapping in actual-UV-faces.json.gz. Existing `UVMap` and old `RutaPaint` retained as backups. Original mesh vertices/faces/weights/rig/actions unchanged. Tiny charts (<20faces) stay uniform original cargo cloth material; the11 paintable charts use a new placeholder material slot pending root generation.

The flat target is freshly rasterized from the **new actual model UV polygons**, with16px exterior brown painted region using segment/vertex coverage. It is NOT dilation/cleanup of any generated image. `trousers-actual-UV-wire-guide.png` overlays the real mesh chart edges inside the brown region. Generator input is `trousers-padded-flat-target.png`; wire guide is diagnostic only. One brown cloth-only prompt provided. No canonical person reference is needed.

Conservative minimum actual chart bounding-box distance150.43px; after both16px bleeds118.43px empty spacing remains. Minimum actual atlas border68.94px. See padding-contract.json for exact transforms/chart source face IDs/bounds. This deliberately fixes the texture sampling contract before painting, not through per-pose corrections.

No generated texture yet. Before any actual front/E40 pair, validate ALL actual boundary samples (including noneroded edges) against beige/background and measure minimum outward painted padding at output resolution. An eroded-interior test alone is insufficient. No boots/bag changes, no48, no runtime. Previous shader guard remains a rejected trial.
