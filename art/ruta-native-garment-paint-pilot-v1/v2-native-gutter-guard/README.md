# Brown UV gutter guard: bounded shader trial, visual FAIL

Source v1 and both immutable painted maps retained. No semantic bitmap editing, UV movement, geometry, rig, action or weight edits. Only brown painted material node graphs changed. Cream, olive, brass, bow, native skin/eyes/hair untouched.

Shader: image sRGB decoded to linear RGB by Blender; distance from measured raw beige border median: mixed(234,227,211), trousers(232,225,210). Smootherstep fallback weight1 below linear EuclideanRGB distance.30, weight0 above.60, between smoothly interpolated. Fallback brown sRGB(141,77,35), trousers(127,80,46). This is one static surface shader, not a pose/image correction. Trousers additionally mix12% of constant canonical brown into the guarded painted color to restrain fold contrast. Nodes explicitly bind RutaPaint, no input image changes.

Initial stricter threshold.045→.20 did not visibly remove lines; one bounded refinement to.30→.60 used measured separation from legitimate brown interiors. `collateral-check.json` reports0% eroded-interior texels affected for every guarded material at final thresholds. This does not establish subpixel filtering/edge behavior or semantic stitching identity. Hardware and cream are excluded categorically.

Actual `e-00.png` and `front-neutral.png` show the material contrast is slightly restrained, **but conspicuous pale UV contour seams remain on trousers/boots**. Therefore this shader guard does NOT solve the visible defect and must not be promoted as a fix. No further threshold broadening: it would eventually alter genuine cloth/highlights. Source texture authoring/UV padding needs a different verified treatment, rather than hiding seams with a broad palette clamp. No5/48 expansion.

`cold-open-check.json` checks unchanged rest mesh/topology/weights, rest bones,50actions and protected head/hair UV/material assignments; these invariants are independent of artistic failure. Compare before files `../renders/{e-00,front-neutral}.png` at the identical camera/pose/size.
