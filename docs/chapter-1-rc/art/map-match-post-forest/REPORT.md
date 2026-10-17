# Post and forest map-match candidates — #45/#62

Built-in imagegen precise-object edits of existing v9 scenes, with the accepted map as the explicit reference. Original targets, generated sources, exact prompts, masks and native PNG candidates are retained under `art/chapter-1-map-match/{post,forest}`. Generated source and delivery are1672×941; no resizing or camera change.

Post: upper-right postal cottage now cream stucco, terracotta gable/chimney, brown wood door/windows and red freestanding mailbox. Existing left start cottage remains intentionally present: it is the start landmark and blocker, not a duplicated postal facade. The old right stone facade/green door/wall-mounted mailbox is fully replaced.

Forest: conifers mixed with shrubs, dusk light, two opposing blank wooden arrows at the existing landmark; no water or river.

Both deliveries use a full free-polygon mask dilated by3pixels. All original free-polygon pixels are unchanged, not only centers or the reference solution. Camera, start/goal anchors, engine layouts and layout-adjustments remain unchanged; manifests record source/geometry hashes. Actual full-polygon overlays and map/object pairs were inspected. This guarantees no new intrusion; it does not independently certify the original underlying illustration.

Status: source/core candidate, artistic and integrated game review pending. Wide delivery is a separate next commit. No runtime paths, common manifest or other scenes edited. No remote push, merge or publication.

Reproduce core registration: `python3 scripts/art-map-post-forest-core.py`.

## Wide delivery and dusk profile

`delivery-contracts.json` and each public manifest contain the current full contract. Wide canvas3272×1200, originalRect `{x:800,y:129,width:1672,height:941}`. Both the old painted v8 surround reference and the built-in seam-edit output have an actual native size2070×760; they are registered with Lanczos to the existing logical wide canvas. This is not a claim of native3272px generation. No source was overwritten or deleted.

The first exact-core paste exposed a rectangular seam, and the old v8 postal ring had a cropped roof remnant above the core. The built-in seam edit removed that roof and joined a single painted outer landscape without additional cottages/mailboxes/signposts. A72px decorative perimeter band inside the core joins the registered paint to the fixed native core, with complete free polygons plus3px guard excluded. `core-before-wide-join.png` preserves the pre-join version; `wide-core-join-mask.png` records every allowed changed pixel. The resulting native core is reproduced byte-for-byte inside the lossless wide WebP. A native `background.webp` update accompanies the wide delivery. There is no mirrored/replicated edge or empty padded surround.

Forest paint alone remained too bright for the dusk requirement. `recommendedWholeSceneGrade` proposes one sRGB SVG `feColorMatrix` for background,wide,characters,road,props together (HUD excluded):

```
0.76 0    0    0 0.018
0    0.78 0    0 0.026
0    0    0.86 0 0.065
0    0    0    1 0
```

That is `R'=.76R+4.59`, `G'=.78G+6.63`, `B'=.86B+16.575` in0–255 sRGB, alpha unchanged. Deliveries remain ungraded, so the coordinator can apply the profile once to all scene layers. The actual Chromium preview applies the same matrix to the wide background and accepted Ruta sprite together. `forest-dusk-before-after.jpg` is the real browser comparison; the profile is a candidate for review, not a claimed new artistic approval.

Actual Chromium captures for both scenes:1280×720,1920×1080,2560×1080,844×390,932×430,1024×600. All12 page loads had0page errors. `wide-six-viewports-contact.jpg` and full-size captures were inspected for perimeter continuity and duplicated objects; no visible rectangular join or extra postal house/sign was found. The preview uses the production `fitScene` formula but is explicitly standalone art evidence, not an integrated game/physical-phone check. Root integration must still check the actual scene layers, NPC staging, HUD and puzzle.

Reproduce: core script, wide script, browser script (HTTP root on5201), then review script. The common v9 manifest and runtime remain coordinator-owned. No merge or publication performed.
