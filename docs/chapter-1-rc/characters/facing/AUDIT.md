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
