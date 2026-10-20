# One fixed painted RGB on native Daisy geometry

Actual Eevee128sample renders: `e-walk00.png`, `front-diagnostic.png`, `threequarter-diagnostic.png`, and `e-walk30.png`. The last is source48phase index30, i.e. actual Walk sourceFrame25, not an extra animation or independently redrawn pose. `original-painted-threeview-comparison.jpg` compares complete unchanged render canvases before/after the material change. Artistic likeness/style and temporal quality remain pending; file count is not acceptance.

## Exact material split

Source geometry: frozen scalp-protected refinement `96a5ab7`, blend SHA421912859b4190f5c04fa681523782b6f7053adbb1cd46a4e2b18712130c0ff8. New root-generated RGB: `0be2713`,1254×1254 RGB, SHAab0a4713e0bb9f8f98ee437cd787190557b47567a7e5199584bbc5d09244d0f7. Exact prompt, generation provenance, ordered-reference metadata and raw PNG are retained in `inputs/`; no image generation or pixel editing occurs in this material assembly.

Native `UVMap` feeds one new image node. Its **Color** connects directly to the diffuse shader Color, bypassing the previous warm tint multiplier. Its **Alpha is unconnected**. The original `daisyhair1.png` stays packed, unchanged, in a separate image node; its original Alpha still drives the same alpha>.5 threshold and Transparent/Diffuse mix. The generated RGB does not replace or clean the source alpha mask. Source image alpha hash a434a5b22dfaf8e658742ce1e91a531e4e626a868731c37fb04c2fcb60d3ae9c.

Diffuse roughness.8, normal strength.25, BLENDED surface and128offline AA are retained. No specular/glint shader, new shape, face/camera offset, per-frame texture, crop, scale, warp or pose fit is introduced. E uses the unchanged base heading; front/three-quarter are explicitly diagnostic views. All source body/face/eyes/rig/bones/Walk/native footRoot remain unchanged. Existing broad cap/panel geometry and E rear-three-quarter visibility do not disappear merely because the colour becomes painted.

## Actual technical evidence

Cold reopen verifies every mesh coordinate/topology/UV/weight/parent binding, non-hair material, bone/action curve and camera/canvas exact; all original packed images remain byte-identical. Exactly one packed image is added (9→10), matching the new raw RGB hash. Generated-alpha output link count is0; original Alpha socket/threshold/source image are checked explicitly. Source and output hashes remain unchanged by readback. Saved self-contained derivative SHA350c96cdacb9c413dac120cb57de695e94d1a9dd2b7c4cbfd8672ed7115ee5d8.

Additionally, actual saved alpha channels of E0/front/three-quarter match their previous geometry-render counterparts byte-for-byte:327680pixels per view,0 changed pixels, maximum difference0. This checks the output silhouettes, not just node presence. Two E poses demonstrate one fixed mapped colour surface under different source poses; they do not certify the complete loop, shoulder intersections, alpha sorting or absence of shimmer.

No48 export, runtime/common-script change, publication, real-game/physical-phone test or artistic PASS is claimed. Parent compares actual stills with the approved Ruta style. Daisy Hair remains Elvaerwyn's CC-BY asset; original source/rights and modification notice are inherited from [the asset attribution](../daisy-native-pilot/ATTRIBUTION.md). This fixed RGB repaint is an additional recorded modification, not a replacement of those rights.
