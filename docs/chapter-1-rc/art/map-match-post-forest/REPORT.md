# Post and forest map-match candidates — #45/#62

Built-in imagegen precise-object edits of existing v9 scenes, with the accepted map as the explicit reference. Original targets, generated sources, exact prompts, masks and native PNG candidates are retained under `art/chapter-1-map-match/{post,forest}`. Generated source and delivery are1672×941; no resizing or camera change.

Post: upper-right postal cottage now cream stucco, terracotta gable/chimney, brown wood door/windows and red freestanding mailbox. Existing left start cottage remains intentionally present: it is the start landmark and blocker, not a duplicated postal facade. The old right stone facade/green door/wall-mounted mailbox is fully replaced.

Forest: conifers mixed with shrubs, dusk light, two opposing blank wooden arrows at the existing landmark; no water or river.

Both deliveries use a full free-polygon mask dilated by3pixels. All original free-polygon pixels are unchanged, not only centers or the reference solution. Camera, start/goal anchors, engine layouts and layout-adjustments remain unchanged; manifests record source/geometry hashes. Actual full-polygon overlays and map/object pairs were inspected. This guarantees no new intrusion; it does not independently certify the original underlying illustration.

Status: source/core candidate, artistic and integrated game review pending. Wide delivery is a separate next commit. No runtime paths, common manifest or other scenes edited. No remote push, merge or publication.

Reproduce core registration: `python3 scripts/art-map-post-forest-core.py`.
