# v3 trousers native UV padding preparation

One new UV layer `RutaPaintPaddedTrousers`,11 independently positioned existing charts, constant1450px/nativeUV-unit scale, explicit source-face mapping in actual-UV-faces.json.gz. Existing `UVMap` and old `RutaPaint` retained as backups. Original mesh vertices/faces/weights/rig/actions unchanged. Tiny charts (<20faces) stay uniform original cargo cloth material; the11 paintable charts use a new placeholder material slot pending root generation.

The flat target is freshly rasterized from the **new actual model UV polygons**, with16px exterior brown painted region using segment/vertex coverage. It is NOT dilation/cleanup of any generated image. `trousers-actual-UV-wire-guide.png` overlays the real mesh chart edges inside the brown region. Generator input is `trousers-padded-flat-target.png`; wire guide is diagnostic only. One brown cloth-only prompt provided. No canonical person reference is needed.

Conservative minimum actual chart bounding-box distance150.43px; after both16px bleeds118.43px empty spacing remains. Minimum actual atlas border68.94px. See padding-contract.json for exact transforms/chart source face IDs/bounds. This deliberately fixes the texture sampling contract before painting, not through per-pose corrections.

No generated texture yet. Before any actual front/E40 pair, validate ALL actual boundary samples (including noneroded edges) against beige/background and measure minimum outward painted padding at output resolution. An eroded-interior test alone is insufficient. No boots/bag changes, no48, no runtime. Previous shader guard remains a rejected trial.

## Frozen generated-material pair

Root9e849b7 raw1254² copied immutably to generated-v1/ with provenance/prompt. Actual UV coverage tested without erosion:109387texels and7962boundarytexels,0% creamlike/olive. Minimum boundary-to-background Chebyshev distance7outputpx; conservative Euclidean lower bound6px. Diagnostic labels rely on declared color thresholds; actual two renders are the visible validation.

`front-neutral.png` and `e-40.png` are actual Eevee renders, same source camera/poses, no filtering/guard/contrast workaround. Shader is explicit new UV→immutable raw RGB→Diffuse(.8). New UV only selected11charts; tinycharts keep original uniform material. Other painted materials unchanged.

Author inspection: old pale trouser contour/wire seams are no longer visible in these two views. Painted fold directions/contrast remain stylized and may differ between panels; no claim of final canonical likeness or temporal consistency. Boots and cargo pocket retain their earlier materials/edge defects, visibly outside trousers-only scope. No boots/bag/48 changes. Cold open verifies unchanged rest geometry/topology/weights, rig,50actions and head/hair UV/materials. Independent visual review pending.
