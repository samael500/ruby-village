# #35: painted resident and prologue asset package

Assets commit d82566b follows pilot1094c56 on art/35-characters / PR #54. The coordinator relayed Maksim's acceptance of Ruta's appearance; no repeated appearance approval is requested. Six resident designs and new acting poses are concrete finished illustration candidates for review, not technical Blender substitutes. Their individual art acceptance is separate from this delivery.

## What is delivered

| Character | Available reference | New source and exports | Manual anatomy review |
|---|---|---|---|
| Ruta | accepted pilot sprite/bust | one coherent four-pose sheet: held basket, adjusting satchel, surprise, crouch with ground basket; separate apple basket | same loose hair/neck scarf/vest; single diagonal satchel strap, bag stays at character right; two hands/legs |
| Rabbit | original pencil animal + accepted Ruta style | coherent idle/bust source sheet; separate identity-preserving baking group with table/bowl/spoon | exactly two ears, one upright/one floppy; animal paws, no human trousers; bowl/spoon placement coherent |
| Squirrel | original pencil animal + accepted Ruta style | coherent idle/bust source sheet | one bushy tail; animal legs; scarf does not form another tail |
| Hedgehog | original pencil animal + accepted Ruta style | coherent idle/bust source sheet | rounded quilled silhouette, tiny short paws/legs, postal satchel/envelopes |
| Teacher | story function and historical notes; original approved color PNG unavailable | new individual adult design, full sprite and true bust | book/watering can, glasses/cardigan; consistent identity and two hands |
| Baker | story function and historical notes; original approved color PNG unavailable | new individual adult design, full sprite and true bust | stocky baker with tray/two rolls/apron; two arms/hands, distinct face |
| Miller | story function and historical notes; original approved color PNG unavailable | new individual adult design, full sprite and true bust | lean older bearded miller with flour sack; distinct from baker |

No historical ZIP was recovered. All nine new source sheets/images are identified as new built-in imagegen work; exact prompts are `art/characters-v1/*-prompt.txt`. Animal sources use the repository pencil reference and Ruta style reference; adults are new designs, not claimed to reproduce lost approved originals. Positional acting figures came from ONE shared Ruta sheet, not independently regenerated animation frames. Baking Rabbit explicitly used the new rabbit source sheet as identity reference.

`extract-sheet.py` isolates connected alpha components and crops transparent margins while preserving source RGB and alpha, with sourceRect extraction metadata. `build-character-manifests.py` rebuilds both resource contracts. No main/style/camera/prologue logic changed in this branch.

## Exact runtime contract

All image paths are relative to assets/characters-v1. `residents-manifest.json` contains characters keyed rabbit/squirrel/hedgehog/teacher/baker/miller, each with speaker, nativeHeightPx, sceneHeightPx, scale, frames.idle and frames.portrait. A frame has image/sourceRect/frameSize/footAnchor; portrait footAnchor=null. Idle scene heights:108/92/74/174/165/181 pixels in the1672×941 native scene.

`poses-manifest.json` contains six frame entries: ruta-basket, ruta-adjust-satchel, ruta-surprised, ruta-crouch-basket, rabbit-baking, basket-ground. Four Ruta poses share **one scale136/768**, rather than stretching each pose independently to full standing height. Crouch frame490×526 has anchor[155,516], sceneheight93.146; its baked ground basket anchor[420,461] and reaching hand[355,485] are also recorded in native frame pixels. Do not add a duplicate basket to that pose. Rabbit baking includes the table/bowl/spoon, also do not duplicate them. Source standing equivalent768px calibrates to136px standing Ruta. The separate basket is27px high in-scene.

Six proposed staging entries map directly to zero-based prologue indices, with semantic pose ids, scene-native foot positions, and optional camera review crop. These are concrete positioning suggestions for integrator #46/#47, who owns final production framing. No resident walking or portrait mirroring is used.

## Visual evidence and alpha diagnostic

- `alpha-light/dark/green.jpg`: every resident sprite and actual large bust on three real RGB backdrops.
- `poses-alpha-light/dark/green.jpg`: every pose/prop on those three backdrops.
- `ruta-poses-scale-review.jpg`: accepted original at left plus all four acting poses, common standing scale and foot baseline.
- `scale-in-accepted-courtyard.jpg`: relative heights over the accepted courtyard with actual foreground masks.
- `prologue-01..06-scene-composite.jpg`: offline scene composites, **not production screenshots**. They inspect silhouettes/camera/alpha; no claim of full prologue staging or actual puzzle geometry. Crouch composition omits stones (actual game adds them); orchard still uses previous v8 background pending new environment package.
- `composite-provenance.json` identifies accepted courtyard input/SHA and exact foreground/orchard sources.

A PNG viewer reported brown rectangular background and yellow/red fringe. This was a verified **false alarm**: the tool exposed underlying RGB at alpha0. E.g. crouch empty gap pixel[380,300]=(159,86,39,0), empty right[480,100]=(71,38,16,0). Real composites on white/dark/green have no opaque rectangle or colored fringe. The coordinator confirmed the real composites and withdrew the diagnostic. `alpha-integrity.json` records all21 PNG alpha ranges/fractions/corner values and those samples. Source RGB at alpha0 is intentionally not color-keyed: removing brown by hue would damage hair/clothes. No unnecessary regeneration or destructive color keying was performed.

## Checks and remaining gaps

55/55 branch tests, tsc and Vite build pass. New resource validation checks image existence/dimensions, sourceRect and valid anchors; alpha checks require real RGBA with transparent pixels and opaque subject regions. Full sources and source/export SHA are retained.

These are static scene/portrait/acting resources. They do not complete final coherent painted six-direction walking; technical rig prototype remains separately in PR #59. Resident .blend rigs/idle motion/blinking are not created here. Actual production six-frame screenshots, speaker mapping, phone layout, gate/bridge occlusion and video with game audio remain integrator/QA checks. No physical phone or family test is claimed.
