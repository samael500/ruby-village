# Independent alpha-volume hair RGB bake audit

Author6bd1daf alpha-aware study under /tmp/ruby-combined-loop/art/ruta-native-hair-volume-study-v1/alpha-aware/. Parent source b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7 frozen. Read-only blend/code/data audit, no render/rebake/48 or material/brightness edits.

**No evidence that the bake introduces global brightening, baked lighting, or double gamma.** Actual original fixed painted image and actual final baked image both have sRGB ColorSpace. Original packed image SHAab0a4713e0bb9f8f98ee437cd787190557b47567a7e5199584bbc5d09244d0f7 is unchanged. BakedPNG SHA b1e3736fba154829675a8351acca1e1b5f74cabce410ee3ca270feeaba634fa1 matches the packed target image. Code/actual final nodes show NativeSourceUV→original RGB→Emission(strength1) for bake; Cycles EMIT only, then VolumeBakeUV→single baked sRGB image→Diffuse(.8). Source diffuse lighting/normal shading are not connected into the EMIT color path. This does not imply identical final lit appearance.

Independent deterministic10,000face-centroid sample pairs from actual saved volume NativeSourceUV/VolumeBakeUV, bilinear source and baked PNG sampling after explicit sRGB decode:

- Source mean linearRGB [.430821,.118822,.036735]; baked [.425824,.117413,.036322]. Mean luma difference−.002100: slightly darker in this sample, not brighter.
- RGB mean absolute difference [.039223,.013215,.004113]; median absolute difference [.019284,.006604,.002264]. Correspondence/bake is not numerically exact.
- Explicit erroneous double-gamma hypothesis gives much larger RGB MAE [.252764,.253669,.171123] and mean luma error−.247394. Observed data does not fit that explanation.

Meaningful actual shading difference: original hair Diffuse Normal receives daisyhair1_normals.png through tangent NormalMap strength.25; new volume Diffuse Normal has no such normal-map link. New closed/remeshed geometry also has different surface normals, occlusion and opaque coverage. Consequently a brighter orange lit appearance can occur independently of a brighter baked albedo. This audit identifies these real differences but does not apportion their visible contribution by matched renders; no corrective tint/gamma patch is justified here.

Limits: face-centroid samples are deterministic/unweighted, not visible-front-area or texel-area weighted. Tiny targetUV islands/bleed/filtering can affect sample values. Closest-original-triangle/per-vertex sourceUV followed by interpolation can cross original chart/material correspondence discontinuities; author source-distance ambiguity remains. Smart-project chart count/coverage was not independently certified. Thus small mean color difference does not prove every visible strand preserves its RGB detail or that all local errors are harmless. No temporal/art acceptance or front-face flicker conclusion follows.

Evidence: actual material-inventory.json (including both blend hashes/node links/ColorSpaces), uv-centroids.npz, original extracted packed RGB, independent sampling code and sample-comparison.json. Inputs remained untouched. Audit stopped at this color checkpoint before any additional source renders.
