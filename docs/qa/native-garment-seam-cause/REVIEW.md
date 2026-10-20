# Independent cause audit: native garment pale seams

Root worktree baseline bfc3747; derivative diagnostic work only under this folder. Shared original/guard blends opened read-only and unchanged (inventory.json, albedo-contract.json and source-hashes-after.json). Actual Blender4.5.3 Eevee renders,512×640, front Idle_Neutral_ProportionProposal,16samples,threads2. No Cycles, full48, semantic bitmap cleanup, pose fit, source promotion or runtime changes.

## Finding

Dominant front trouser/boot wire-like pale boundaries are supported as a **painted UV-island coverage/filtering problem in the bound color path**. They are not fixed by the current beige color-distance guard. This is a cause diagnosis for the inspected front pose, not certification of every E40 pixel or all possible overlapping garment geometry.

Controlled actual evidence, see controlled-front-comparison.jpg:

- Baseline retains the pale polygon-like paths.
- Replacing brown painted material Color inputs with one constant brown removes those paths on trousers/boots, while true cream boot-lace geometry remains. Geometry, rig, lights and underlayers unchanged.
- Hiding Adventurer_Body in a separately reopened baseline leaves the same trouser/boot paths. Underlying body visibility is therefore not their necessary cause.
- Texture Color through Emission still shows them: ordinary diffuse illumination/specular is not necessary. Guarded final albedo retains them too.
- Changing only image interpolation Linear→Closest visibly reduces many thin fringes, but leaves remaining edge discontinuities. Nearest is diagnostic, not the proposed production fix.

Material/UV-ID pass identifies trouser regions as actual `Ruta painted garment Ruta warm loose cargo cloth`, boots as actual painted Brown_02/Brown2. Inventory shows explicit RutaPaint nodes and expected image bindings; not merely a guard applied to an unused material. Packed mixed/trouser image hashes exactly match external PNGs. Actual images are RGB, sRGB and no image Alpha output drives these materials. There is no evidence here of an alpha-blend fringe or accidentally stale packed image. Stock body/cargo/feet layers do exist; this audit does not claim every possible layer-intersection defect absent. The controlled underbody/constant/albedo tests localize the dominant inspected lines without needing that broad claim.

## Why another beige threshold does not solve the contract

Actual bound UV polygons were extracted from the blend and overlaid on the immutable generated textures (cyan boundaries in *actual-island-boundaries.png). Brown paint generally stops on the geometric UV island edge with effectively no padding; some generated edges retreat from that edge. At native1254texel raster resolution,608 beige-like texels lie inside trouser UV polygons and125 inside foot UV polygons (distance<.15 in linearRGB; edge rasterization is approximate). Even exact interior coverage would not protect an unpadded edge from image filtering/minification across the neighboring beige.

The guard measures distance **after image sampling**, against beige, with full fallback below.30 and none above.60. Brown/beige mixtures can already be conspicuously lighter than cloth yet remain far from beige, so are not reliably selected. Actual seam-pixel examples in seam-pixel-samples.json have original albedoRGB and guarded albedoRGB plus distances. These are rendered filtered/MSAA pixel values, not proof of a single precise texture-ray/guard weight; UV at discontinuous seams can itself average in the UV-ID pass. They demonstrate the surviving pale color in the correct material. Current guard does not provide UV-aware coverage or bleed. It cannot be treated as a validated seam fix merely because pure beige would be replaced.

## Scoped recommendation

Fix the atlas/UV coverage contract first: ensure intended brown garment color extends beyond every real island boundary by a filter-safe margin and verify continuity across paired physical seams. Source repaint/repacking or a deliberately UV-aware material design should be assigned separately; preserve intended cream lace/cuff regions. Choose padding against actual atlas resolution/minification, then verify the same small front/E40 actual renders. Do not tune another global RGB-distance threshold as the primary fix: it confounds intended paint highlights with missing border coverage. Do not ship constant brown or Closest from this diagnostic as a style solution.

Boundaries: no universal claim that all local irregularities have one cause; no final art acceptance. All outputs are diagnostic, not replacement source. Inputs/geometry/source images were not edited. Audit stops after bounded causal probes; root assigns any fix.
