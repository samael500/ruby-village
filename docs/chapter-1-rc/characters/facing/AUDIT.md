# Resident facing pilot — #35 / #46 / #62

Base: integration 43e64bd, 2026-10-17. Read AGENTS.md, LATEST-REQUIREMENTS.md and latest Issue #62 comments before work. This is an asset-only pilot; runtime integration and actual-scene review belong to coordinator.

## Observed PNG audit

Reviewed actual six full-body `public/assets/characters-v1/residents/*-idle.png` together (idle-audit.png). All face screen-right; no matching screen-left full-body alternative exists in residents manifest. Portraits are separate cropped pictures and cannot replace full-body dialogue views.

| Resident | frame px | existing foot anchor | scene height |
|---|---|---|---|
| Rabbit |508×981|302,977|108|
| Teacher |522×1008|239,1004|174|
| Baker |537×999|258,995|165|
| Squirrel |692×904|438,900|92|
| Miller |431×1000|231,996|181|
| Hedgehog |639×844|319,840|74|

All PNGs RGBA, with real zero-alpha pixels; maximum alpha254 rather than255. Alpha bounding boxes fill the tight cropped canvases. Do not infer an opaque backdrop from a viewer's checker/dark presentation.

Rabbit identity: beige fur, cream shirt, green apron, botanical cup in both paws; anatomical right ear droops, left upright; anatomical right pocket flowers, left pocket tools. Simple horizontal flip would reverse these asymmetries. Scene presence remains garden Rabbit; well Teacher; bakery Baker; stream Squirrel; mill Miller+Squirrel; post Hedgehog. Existing runtime feet positions and clearance remain untouched.

## Pilot policy

Builtin imagegen with approved idle as identity reference. No external service, paid API, upload or CLI fallback. Source preserved whole with generated transparency. Only alpha crop, uniform resize and transparent packing may be performed afterward. Original characters-v1 assets are untouched. Other five residents wait until coordinator compares this pilot in actual garden dialogue.

## Selected pilot v3

`rabbit-left-source-v3.png` is the whole generated transparent1024×1536 output. The final targeted edit preserves the left-facing pose and restores original drooping-left/upright-right ear arrangement. Flowers remain left-of-image, tools right-of-image; this is not a global horizontal flip. Cup stays in both paws. New perspective changes tail/bow visibility and stance naturally.

Packed output604×981, unchanged foot anchor302,977, sceneHeight108. Measured source alpha≥8 bbox176,25,841,1499; uniform resized subject height969, transparent packed offset82,8. Alpha range0..255. No feature drawing, mirroring, separate limb transforms or anisotropic resize. Original idle SHA2564378b6eddaf758ea2a19aa6fc821c442c35159a7686583fde68f756f11fbd1fd unchanged.

`rabbit-comparison.png` shows shared ground/scale and108px thumbnail. This is an asset comparison, not actual gameplay evidence. Technical output size/alpha/bottom margin assertions PASS. Actual garden, dialogue orientation alongside Ruta, transitions and clearance review pending coordinator; all five other residents remain unchanged. No production approval claimed.

## Teacher conversation-left

Approved original reference used directly in builtin imagegen. Preserved cream blouse/rust knit cardigan, olive botanical skirt, glasses, green botanical book in left-of-image arm, brass watering can in right-of-image hand. New face/gaze/body/feet view toward left; no horizontal flip. Native frame532×1008, foot239,1004 and sceneHeight174 unchanged. Source whole PNG retained. Activity metadata: well+flowerbed, idle original right-facing; encounter/dialogue entry selects authored facing once, no continuous tracking; caller world feet retained. Asset-only review complete; actual-scene review pending coordinator.

## Hedgehog conversation-left

New whole fullbody left-facing view from original reference. Preserves one postal strap, satchel on left-of-image hip, envelopes/red seals, raised letter in right-of-image paw, olive vest and postal cap. Cap tilt/button visibility differs with pose; not an automatic rejection. Dense spine silhouette and feet complete. Source preserved, sceneHeight74 and nativeHeight844 retained. Pixel frame/anchor in manifest control stable caller world feet. Activity post/postal-work, original idle unchanged; meeting policy as above. Actual-scene review pending.

## Squirrel conversation-left

New fullbody view with left face/gaze/torso. First generator output changed accessory side, rejected. Targeted edit restored brown satchel at original left-of-image hip, one strap from right shoulder and olive fringe on original side. Two paws keep one acorn. Tail naturally moves behind the right side of the new pose rather than swapping bag with it. Whole source preserved. Packed893×904 (includes transparent area needed to retain old pixel foot anchor438,900), native904/scene92 unchanged. Activity metadata includes both stream and mill. Actual-scene review pending; coordinator identified a separate near-front arrival view needed for the second mill placement.

## Near-front arrival views: Teacher + Squirrel

Coordinator's actual runtime geometry audit: well Teacher feet1225,405 (final1195,405) vs Ruta goal1231,456; mill second Squirrel1330,405 vs goal1352,466. A left-only conversation view points away after arrival. New authored near-front/slight-right fullbody poses address nearby partner with fresh front torso/feet perspective; book/can and bag/scarf/acorn ownership retained. Original approved refs used, not horizontal flips or eye-only edits.

Teacher front532×1008, anchor272,1004, scene174; Squirrel front893×904, anchor448,900, scene92. These frame-pixel anchors differ to accommodate new silhouette, while runtime's caller world feet and canonical scale stay fixed. Manifest marks `arrivalFrame: conversation-front` with scene rationale; intro still uses left. Whole source PNGs/prompts preserved, source alpha retained in technical uniform packing. Actual scene acceptance remains coordinator's check.
