# Manual painted registration dataset (#36)

Native `native-landmarks24.json` has24 actual Walk phases, Root/Hips/Foot.L/Foot.R bone-head projections and source boot sole/toe/heel features. Root is native world0 after rest-ground normalization. Sole features are means of evaluated source vertex regions selected once in rest geometry, with exact source indices preserved; they are geometric landmarks, not guaranteed stance/contact points. No bbox-based native joints.

`foot-grid-*.png` and combined `foot-registration-contact-sheet.png` are diagnostic copies. Grid labels reference original whole packed384×416 frame coordinates (crop y176…416). Original painted RGBA remains untouched in whole24 folder. `manual-painted-landmarks-template.json` deliberately has null landmarks, visibility/uncertainty fields and anatomical L/R. Annotator must not guess occluded joints.

`scale-study.json` suggests initial common painted source-pixel→native guide-delivery-pixel scale0.9389975 (approximately0.94). It is the median of all24 whole silhouette height comparisons, not individual correction. Hair/head/boot silhouette differences limit anatomical validity. Source-pixel art at this common scale is comparable to guide256×320; this scale has NOT been applied.

With manually verified ankle correspondences, compute tL=nativeAnkleL−s*paintedAnkleL and tR likewise. Their common translation estimates drawing-origin drift; tL−tR is translation-independent leg-pose residual. A large residual indicates changed leg placement or uncertain annotation, not something an origin shift fixes. Add hip/heel/toe residual checks and per-point visibility/error. FootAnchor can subsequently encode a verified origin, with one unchanged global scale; no painted FootAnchor is claimed in this dataset. Original/corrected loops and residuals must remain reviewable before acceptance.

Reproduce native dataset with Blender scripts/painted-ruta-native24-landmarks.py; grids/scale study with python3 scripts/painted-ruta-registration24-sheets.py. Neither modifies source rigs, poses, images or runtime.
