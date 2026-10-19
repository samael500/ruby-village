# One ready hair-geometry donor: Victoria / Sprite Fright

**Recommendation: Victoria's solid hair mesh as a source donor for a deliberate fit study; NOT a ready matching Ruta hairstyle.** The official thumbnail and actual geometry show a tall 1980s bouffant, thick swept side lobes and curled ends. There is substantial loose hair, no ponytail, but the high crown and silhouette differ from long natural waves. Do not silently import it as accepted art. No new sculpt, character/head adaptation, rig transfer or runtime changes were made.

## Official source and rights

- Character/source: https://studio.blender.org/characters/victoria/v1/
- Official download: https://studio.blender.org/download-source/files/f3/f399fb2523e10448b6d6e7b77d2eaa26/f399fb2523e10448b6d6e7b77d2eaa26.blend
- License explicitly linked by the official page: **CC BY 4.0**, https://creativecommons.org/licenses/by/4.0/
- Attribution for the extracted donor: **Victoria hair, from Victoria / Sprite Fright — Blender Studio / Blender Foundation, CC BY 4.0. Hair meshes isolated from the original character; original rig, particles and modifiers omitted.** Preserve source/license and indicate any later fit/recolor/remesh changes. No claim this is CC0.
- Official thumbnail URL: https://studio.blender.org/files/public/thumbnail/f3/99/f399fb2523e10448b6d6e7b77d2eaa26_m.webp

`source-hash.json` identifies the actual downloaded .blend. It was cold-opened using Blender4.5.3 with **auto-execution disabled**, and was not saved over. Whole official source is retained only in local ignored `sources/victoria.blend`, for audit/reproduction; only the extracted two hair objects are delivered, never the full character or rig.

## Actual geometry, not inferred from a picture

Cold inventory in `mesh-inventory.json` distinguishes the real solid mesh from scalp particles and hair-guide helpers:

- `GEO-victoria_hair_main`: **2699 vertices, 2691 faces**, every edge has exactly two incident faces. No particle system. Native dimensions ~.486×.405×.607m before fitting.
- `GEO-victoria_hair_bangs`: **2110 vertices, 2050 faces**, solid-shaped bang clusters with separate openings; consult inventory for exact boundary count. No particle system.
- `GEO-victoria_hair.scalp`: seven particle systems, deliberately excluded.
- Scalp-back/front/side/top guide objects and their lattices are also excluded. Several have zero faces: they are not a replacement hair asset.

`victoria-hair-only-raw-rest.blend` is a library containing only copies of the two named mesh objects/data, original raw rest vertex positions and object matrices; no skin/rig/modifiers/particles. It is **not** a fitted/head-compatible/shaded final export. Four `actual-hair-rest-*.png` views are actual Workbench renders of those vertices with one uniform orthographic camera, neutral clay. Original production silhouette is separately visible in `sources/official-thumbnail.webp`. Removing production rig/lattice/subdivision can change smoothing/pose; raw views intentionally prove geometry only.

## One fallback checked, rejected at thumbnail stage

Official Spring https://studio.blender.org/characters/spring/v1/ was the only fallback examined. Its official preview shows short swept-back hair, not long loose waves; no 406MB character archive was downloaded. The page also links CC BY4.0. `sources/spring-thumbnail.webp` retains this real preview. No catalogue or second speculative recommendation.

**Decision:** there is a verified, legally reusable solid donor (Victoria), but no verified ready-to-use Ruta-matching long-wave hairstyle among these two. If the requirement means zero shape adaptation, the search result is **not a suitable asset**, rather than pretending the bouffant matches. A donor-fit visual pilot needs separate approval before implementation; NPC head work stays separate.

Reproduce with the official file at `sources/victoria.blend`, then `blender --background --threads 2 --disable-autoexec --python inspect-source.py` and `render-geometry.py` (paths relative to each script). No image generation was used.
