# Independent v4 padded accessories / transfer audit

Author0f9ac3c. Scoped PASS for boot/satchel UV coverage and the existing actual front/E40 pair, with pantsv3 retained. No whole-loop, final character art, game or physical-phone acceptance. No source edits, rendering or integration performed.

Independently cold-opened frozen pantsv3 and final donor. Rest geometry/topology/weights, rig,50actions including keyframe handles, and the full pants UV/material-slot/per-face-assignment state match exactly. Actual33accessory material nodes explicitly bind newUV→packed immutable sRGB image/Linear→Diffuse(.8)→Surface, without a color guard/contrast path. Actual1229painted faces were extracted from the donor.

All999actual UV boundary segments sampled≤.25texel including endpoints:71,636samples. No cream/background classification on boundary;0cream/olive across all285,717noneroded UV polygon texels. Minimum boundary-to-classified-background distance7outputtexels (both sampled segments and separate boundary raster). Threshold and raster/sample limits remain explicit in padding-results.json; not a guarantee for arbitrary minification. No generated bitmap alteration.

Viewed actual v4front-neutral/e-40 against v3 pair: previous pale wire contours on boots and satchel no longer visible; pantsv3 remains. Original cream lace/cuff geometry is still present. Brown leather reads more mottled and less outlined; this bounded seam result is not final leather-style/texture-temporal approval. Paired screenshot and exact render hashes retained.

Transfer safety readback: donor blend SHA57d6668cb8ae2b81b5709b83a608f3ad435de4c39d711aa378b4e6ccf6d9a214 matches manifest. Every transfer object topology/vertex/loop count, material slot name, sparse face assignment and named per-loop paint UV matches actual donor. No head/hair object included. All1932Skin faces in Adventurer_Body carry−1 preserve sentinel. Data/manifest hashes are retained independently in invariants.json. Transfer is safe **under its stated importer rules**: validate target rest topology first; append/remap named material datablocks; use donor indices only through that mapping;−1 preserves current target; copy only named paint UVs and preserve palette/unrelated UV layers. This is schema/donor verification, not an actual importer execution or target skin readback.

Documentation nit: README says “positive indices”; the precise valid set is **nonnegative indices**, because donor slot0 is valid and only−1 means preserve. Parent reports assembler supports0 by mapping membership; that implementation was not independently tested in this audit. No author README overwritten. Pin both manifest and compressed transfer-data bytes for a reproducible import.

Recommendation: retain the scoped accessory fix and perform separate combined-target source readback before any new render. No broad acceptance inherited from pants or source guides.
