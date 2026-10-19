# Independent observed loading/performance — #49 / source `7244fb2`

**Four actual local samples completed; no asset 404, failed request or page error observed.** This is the ordinary layout-2 build, source/runtime/assets unchanged, served bundle `index-Booi3P-Q.js` SHA256 `d6f9e80949b87752e1eee897a8ca2d49d08e591aa9c92f22c961ba0e2b7aca28`. Total release export is 103.7 MiB; it is **not** the initial download.

Fresh Chromium contexts cleared/disabled browser cache through the cold-ready snapshot. Gate starts with genuinely empty storage and actual six-frame prologue; mill enters through the real map using a save genuinely earned by the completed clean chapter run. No layout or win injection, no private activation. Cache was restored for subsequent real drag inputs, accepted UI solution and normal walking.

| Scene / viewport | Cold requests | Encoded MB | Nav → motion ready, ms | Final entry input → ready, ms | Visible raster RGBA estimate, MiB |
|---|---:|---:|---:|---:|---:|
| gate / 1280×720 | 45 | 31.62 | 1244 | 300 | 36.46 |
| gate / 844×390 | 45 | 31.62 | 1264 | 214 | 36.46 |
| mill / 1280×720 | 46 | 28.42 | 595 | 417 | 32.23 |
| mill / 844×390 | 46 | 28.42 | 577 | 330 | 32.23 |

Encoded bytes are CDP `Network.loadingFinished.encodedDataLength` (HTTP representation/headers), not uncompressed decoded pixels or a mobile data bill estimate. `nav → ready` includes automated real UI progression, including the prologue; it is not an isolated bandwidth latency. Goto-return menu timing is an early load event: asynchronous menu images can still finish later.

## Exact request-initiation phases (additional network-only cold samples)

Both desktop and touch produced the same final phase budgets. Phase tags were set **before** real UI actions; raw reports retain request, response and finish phases because downloads initiated earlier can finish later.

| Request-initiation phase | Requests | Encoded bytes | Main content |
|---|---:|---:|---|
| Menu | 7 | 3,947,527 | Old v6 courtyard PNG 2,989,416; UI materials 891,338; HTML/JS/CSS 66,773 |
| Six-frame prologue | 26 | 20,972,410 | Painted garden 8,710,886; gate layers 7,914,166; old inventory tile PNGs 2,726,222; audio 1,211,704; character poses 409,432 |
| Entry into playable gate | 12 | 6,700,279 | Six Ruta atlases/manifest 2,741,834; road material 1,573,190; UI/header 1,171,699; audio 1,213,556 |

This distinguishes when a request began from the asset purpose: gate layers are also used by the prologue. The old inventory tiles are requested during prologue presentation even though the technical board/tray are hidden. These are observed optimization opportunities, not declared rule/rendering regressions.

## Ten largest encoded requests per cold route

### gate

| Asset | Encoded bytes |
|---|---:|
| `assets/chapter-1/v9/garden/wide.webp` | 6,002,204 |
| `assets/chapter-1/v9/gate/wide.webp` | 5,234,518 |
| `assets/chapter-1/v6/01-courtyard.png` | 2,989,416 |
| `assets/chapter-1/v9/garden/background.webp` | 2,708,682 |
| `assets/chapter-1/v9/gate/background.webp` | 2,273,524 |
| `assets/road-v1/charoite.webp` | 1,573,190 |
| `assets/audio/music/day.ogg` | 1,206,907 |
| `assets/audio/music/village.ogg` | 1,192,598 |
| `assets/ui/v8/level-header-v1.webp` | 1,153,288 |
| `assets/ui/v7/leaves.png` | 857,012 |

### mill

| Asset | Encoded bytes |
|---|---:|
| `assets/chapter-1/v9/mill/wide.webp` | 5,703,484 |
| `assets/chapter-1/v6/01-courtyard.png` | 2,989,416 |
| `assets/chapter-1/v9/mill/background.webp` | 2,542,460 |
| `assets/chapter-map-v2/map-wide.webp` | 2,193,518 |
| `assets/road-v1/charoite.webp` | 1,573,190 |
| `assets/audio/music/water.ogg` | 1,236,188 |
| `assets/audio/music/village.ogg` | 1,192,598 |
| `assets/ui/v8/level-header-v1.webp` | 1,153,288 |
| `assets/characters-facing-v1/residents/squirrel-conversation-left.png` | 900,992 |
| `assets/characters-facing-v1/residents/squirrel-conversation-front.png` | 866,030 |

## Actual input / frame cadence

Each of the four samples performed three real drags through the visible tray, then a UI-entered accepted layout and normal runtime walk to the actual arrival dialogue. Native touch lifts vertically before crossing the horizontally scrollable tray. The normal-motion path uses the existing runtime gait; the separate MPFB appearance is not activated or accepted by this measurement.

Across the four drag samples: 126–134 measured RAF intervals each, p95 16.7–16.8 ms, max about 16.8 ms. Across the four walks: 1,314–1,407 intervals each, p95 about 16.7 ms, max about 16.8 ms. There were no sampled intervals above 50 ms and no observed long tasks starting within these phases. Raw frame timestamps and long-task records are retained. These are **RAF scheduling intervals**, not measured GPU frame presentation or a universal FPS guarantee.

## Decoding and limitations

After freezing cold-request measurements, a separate real browser `Image.decode()` probe obtained natural dimensions for distinct raster URLs whose DOM boxes intersected the viewport. All probes succeeded. The RGBA column is only width×height×4 summed over these images; it excludes offscreen/preloaded atlases, mipmaps, compressed surfaces, GPU/browser copies and allocator overhead. It is **not a measured process/GPU memory value**. Probe requests are excluded from the cold snapshot.

Single observed sample per scene/viewport, headless Chromium 156.0.8078.4 on localhost, no network or CPU throttling, shared 16-logical-CPU development host. `host.json` records concurrent-host conditions; no other sessions/processes were stopped. Browser cache cold does not imply cold OS filesystem/server caches. No physical phone, WAN, low-memory device, thermal/battery assessment, family test or universal performance budget was tested. No audio listening or artwork acceptance is implied.

Raw per-sample JSON includes every cold request, Resource Timing entry, viewport decode dimensions, RAF/long-task timestamps and screenshots. `network-phases-*.json` preserves the extra initiation-phase runs. `summary.json` and `summarize.py` provide the reproducible aggregation. No runtime files were edited.
