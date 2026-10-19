# Six-heading native resource handoff

Resources live under art/ready-character-six-v1, outside production/runtime/public registries. Source remains the adapted native .blend; all stock local geometry/weights/rest/actions are preserved except the explicitly assembled accessory/ready-part changes. World view transform alone is Rz(yaw) @ Translation(−native Root rest ground).

Two accepted camera variants base(angle0) and calibrated-1(angle0.04494904935533156), six actual projected hex headings each. The renderer reads accepted heading-contract.json, not artificial screen60° sectors. Native orthographic elevation asin(.65), fixed512×640 viewport, true projected horizontal304.761902px/m. Root world point0 projects to[256,516.859312]; no per-frame crop/shift. Static Root projection checks cover all12 headings, Walk/Idle start/half/end with maximum error0pixels.

Delivery is one uniform.5 resize of every entire source canvas: frameSize[256,320], footAnchor[128,258.429656]. Body reference comes from native REST world Z bbox1.810531917m × actual camera vertical Z231.599035px/m =419.317445nativepx,209.658723deliverypx. Set.nativeHeightPx uses209.658723, never canvas height320, with desired display136. One common body reference and anchor for all directions and variants.

Each direction atlas combines Walk24(top4rows) and Idle_Neutral24(bottom4rows),6columns. Lossless WebP decoding is compared byte-for-byte against the uniformly resized atlas. Native512×640 RGBA frames remain available for source audit. Walk cycle1666.666667ms, neutral Idle2083.333333ms. All original24 native actions remain available in the .blend. No start/stop/turn action is invented.

Manifest follows cameraVariants[variant].directions[name].clips[walk|idle].frames with sourceRect/frameSize/footAnchor/durationMs, directions alias base. File paths are resource-relative assets/*.webp; root chooses production URLs and owns runtime adapter/installation. Frames already include camera projection: do not apply a ground transform to sprite pixels. Route position still uses the scene projection normally.

Stride1.749205515native meters/cycle is measured from inferred stance motion, not game hex units. Per-direction projectedStridePixels measures that stride after camera projection and delivery resize; projectedStrideDisplayPixelsAt136 includes136/nativeHeightPx display scale. Source stance-speed RMS residual0.192322m/s remains disclosed. Root should validate actual route video and cadence, preserving source cycle until observed.

Stock low-poly adult face/proportions/green shirt remain an unapproved likeness variant. This package is a source-resource delivery, not actual-game acceptance or permission to merge/deploy.

## Completed delivery

576/576 native renders complete:12 headings × Walk24 + Idle_Neutral24. All source any-alpha within512×640 (minimum margin41px); all576 delivery cells also fully contain any-alpha after uniform resize.12 lossless1536×2560 WebP atlases total9,340,716bytes,188,743,680decodedRGBAbytes. Exact decoded pixel equality verified against packed RGBA. Five-second all12-view MP4 and animated WebP plus four-phase sheets for both cameras are delivered.

Source local rig/actions remain unchanged; all10407 evaluated vertices match at Walk0↔40 and Idle_Neutral0↔50 (maximum/RMS endpoint displacement0m). This loop closure check does not replace stance-speed analysis or actual-game review. Native Root projection maximum error0pixels over12heading proof. Source-origin draft and camera-PPM metadata errata remain documented; current package uses measured camera coefficients and worldtransform normalization.
