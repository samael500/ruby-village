# #49 native sprite decode/resource budget: independent static audit

Pinned runtime e32cad4 (full commit and file SHA256s in report.json), /home/mskorokhod/life/ruby-village. Read-only code/manifest accounting. No runtime edits, profiling, browser session, build, global asset loading or physical-device measurement. **Not final native performance PASS.** Current runtime uses animated-v3, not these new native prototypes.

## Known accounting versus illustrations

RGBA8-equivalent = sum of width×height×4 for **unique decoded image resources**. For independent frame PNGs this sums frames; for an atlas count its full dimensions ONCE, including padding, not each sourceRect again. These are exact logical byte counts under full RGBA8 materialization, a baseline excluding overhead/copies; not a universal physical RSS lower bound. Browsers can retain, discard, tile, share or duplicate internal decode/raster/GPU resources.

| Resource/model | Encoded bytes | RGBA8-equivalent bytes | MiB |
|---|---:|---:|---:|
| Known native E48 global crop260×434 | PNG sum4,715,045 |21,665,280|20.6616|
| Known native E48 whole512×640 |not measured here|62,914,560|60|
| Illustration:6×same crop Walk48 |unknown|129,991,680|123.9697|
| Illustration:6×same whole Walk48 |unknown|377,487,360|360|
| Illustration:2crop Walk48 bundles |unknown|43,330,560|41.3232|
| Illustration:2whole Walk48 bundles |unknown|125,829,120|120|

Known encoded crop PNG sum is4.4966MiB; encoded size is not decoded memory. CSS shrinking/low display height does not change source dimensions. Illustrations assume each heading has the same E dimensions/count, which is **not a measurement of final six-heading art**. Final native Idle/Start/Stop resources, camera groups, padding and delivery encoding are unknown. Add their actual unique resource dimensions when exported. A second hypothetical six-heading camera group would double the illustrated Walk-only totals (crop247.9395MiB/whole720MiB), not establish a real allocation. Extra scene/background/resident/portrait buffers, network/decode temporaries, GPU textures and compositor surfaces are excluded.

Current animated-v3 manifest has6unique1152×1728images per camera group, each7,962,624RGBA8bytes. Base group47,775,744bytes=45.5625MiB/encoded2,716,668; calibrated-1sameRGBA/encoded2,706,170. Visiting both groups exposes12unique resources=95,551,488RGBA8bytes=91.125MiB. It is not8scenes×6: five scenes share base files, three share calibrated-1. These are pinned manifest metadata, not observed live memory or measured final native assets.

## Existing ownership and retention risks

- `src/ruta-motion-view.ts:13–18`: module-scoped decoder; `prepareMotionAtlases` enumerates every direction/clip in selected camera set, deduplicates files, then `Promise.all` decodes all6headings eagerly. JSON manifest loading itself does not decode all images.
- `src/image-decoder.ts:2–12`: Map stores `Promise<HTMLImageElement>`; successful resolved promises keep the image reachable for module lifetime. Failed loads are correctly removed for retry. No release/eviction or concurrency bound exists. This is a strong JS-reference fact, not a guarantee that all decoded pixel buffers stay physically resident.
- `src/main.ts:110–113`: scene entry starts all-heading decode before the winning route is known. Generation prevents old result publication when a newer scene entry exists, but does not cancel/evict old decodes. `showMap` around679 cancels animation yet neither increments motionGeneration nor clears motionSet/motionAtlases/rutaJourney; a pending same-generation load may still publish after leaving. Nulling the dimensions Map alone would not clear the module decoder.
- `src/ruta-motion-view.ts:20–29`: SVG frame renderer retains image href; decoded HTMLImage is used for dimensions, while SVG refers to the resource separately. Browser sharing/redecode behavior cannot be assumed; releasing JS cache alone is not proof of release while a visible/hidden SVG still references the atlas.
- `src/resident-scene.ts:22–30`: scene request prepares ALL authored resident facing views, not only selected view. ready/loading collections have no lifecycle removal. Promises resolve void, so unlike the motion decoder they do not explicitly return/strongly retain HTMLImageElement; do not count them as a proven image-object retention cache. Browser/DOM resource retention remains outside this audit.
- `src/prologue-scene.ts:13–14,47`: independent module readiness cache; all image hrefs in the constructed story SVG are decoded. Promise resolves void and catches failure as success, so retry/readiness semantics differ from shared decoder. No eviction contract. HTML `loading=lazy` portrait/map img attributes in main do not govern these explicit `new Image().decode()` or SVG loads.

## ONE minimal integration contract: scene-owned active+next motion leases

Keep current SVG/player architecture; introduce one shared `acquire(resource, ownerGeneration) → {ready, release}` owner-aware decode service at the existing decoder boundary. Key by versioned file/hash and dimensions from delivery manifest. Share in-flight requests, retain failure retry; reserve `w*h*4` once per unique resource before decode. Admit only current heading's required resource bundle plus ONE next heading bundle for this Ruta instance (ready OR pending), decode concurrency1. Evict zero-owner ready entries immediately; do not accumulate every visited heading/camera group. This is a logical retention policy, not a claimed device-safe byte cap. Final native manifest determines bundle sizes; illustrative two-Walk numbers above exclude unexported clips and decoder overhead.

Concrete ownership:

1. `image-decoder.ts` owns request deduplication, queue, byte reservations, lease counts and zero-owner eviction. A stale result must release on settlement; a canceled generation is not allowed to pin an image merely because its decode cannot be aborted reliably. No promise of browser cache flush/GC timing.
2. `ruta-motion-view.ts` owns manifest→resource mapping and direction-specific preparation, replacing eager ALL-direction enumeration. `loadMotionSet` may retain small metadata for all directions; only selected resources get leases. `drawMotionFrame` consumes a ready lease and owns its SVG href reference; detach/replace href when that actor is removed or resource released.
3. `main.ts` owns scene-generation lease lifetime. `prepareRutaMotion` acquires only actual initial idle/facing resources; solved-route code around493–498 plans from metadata, then acquires the first needed heading and prefetches only the next planned heading. Direction changes/meeting idle must request the actual next required direction, not silently decode six. Do not draw/advance an unavailable resource; use the existing paused/unavailable path without changing logical victory state. `enterLevel`, sandbox entry and `showMap` invalidate generation, stop the old player, remove old actor references and release old scene leases. Existing `RutaJourney`/`CharacterPlayer` remain clock/route owners, not image caches.

Resident/prologue are separate consumers if later put behind the same service: their render entrypoints own/release scene leases. Do not expand this scoped native Ruta integration into a game rewrite or claim unrelated existing caches solved. A direction-wide atlas may necessarily contain multiple clips; an idle request cannot decode only one sourceRect from an indivisible atlas. Budget actual manifest resources rather than imaginary frame-level savings.

## Remaining acceptance

No physical-phone capacity, GC, frame-time, orientation performance, final six-heading/transition-size or whole-game performance claim. Needed later: final versioned native delivery dimensions/encoded bytes plus targeted actual integration/profile under this bounded ownership contract. Current artifacts do not support a final #49 performance PASS or a fabricated native six-direction memory measurement.
