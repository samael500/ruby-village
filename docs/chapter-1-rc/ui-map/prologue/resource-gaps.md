# #47 six-frame resource audit — 2026-10-17

This is a resource/staging handoff, not a claim that the prologue is finished. Source: current `src/prologue.ts`, `src/prologue-staging.ts`, HANDOFF and original `docs/prologue/report.md`. The six lines match HANDOFF; before/after lines in chapter-1.story.json already explain Rabbit, school flowers, baker's flour, Squirrel, Hedgehog and old invitation. Do not rewrite these or reveal the cause/Domovoy.

Ruta's appearance was accepted by Maksim on 2026-10-17 (coordinator handoff). Available assets: characters-v1/ruta-idle-pilot.png and ruta-portrait-pilot.png. The static back study is not a walking animation. Appearance acceptance does not create any missing poses. Existing v6 courtyard/orchard provide coherent staging references; The courtyard style was also accepted on 2026-10-17: gate-v3-base plus registered layers/manifest from #45 commit 1d0dad5 (integrated as 9ffcfd6). Acceptance of style does not replace production camera/geometry verification.

| Frame | Existing resources that can actually be used | Missing finished resource / contract | Honest status |
| --- | --- | --- | --- |
| 1. Morning courtyard | Same courtyard background, accepted Ruta identity/idle | Real basket-hold pose, drawn apple basket; intact-road layer for yesterday's familiar route | Static blocking reference only |
| 2. Apples for Rabbit | Same courtyard/camera, exact Ruta dialogue and portrait | Same basket-hold pose; optional small settling motion from actual pose frames | No fake scaling or shaking as action |
| 3. Rabbit preparing pie | Existing orchard composition includes table; narrator has no portrait | Approved Rabbit model and actual baking pose with bowl/spoon; exact table/action anchor | SVG Rabbit remains placeholder and must not appear in final review |
| 4. Road has vanished | Same courtyard, accepted Ruta identity | Surprised pose, loose-stones art and semantic anchor, basket beside Ruta; missing-road layer | Actual disappearance must be a changed road layer, not hex markers |
| 5. Ruta crouches | Courtyard and accepted identity only | Actual crouch pose, basket-ground art, one stone and subtle highlight tied to action | Standing sprite resized is expressly insufficient |
| 6. To the gate | Accepted Ruta idle; game scene start projection | Same final camera/crop/foot anchor as gate gameplay; final gate state and basket/stones layers | Handoff can be exact once #46 camera is connected |

Common missing runtime layer: use one scene asset/camera for five courtyard frames, same light and model scale; no six independent generated scenes. Narrator portrait is absent. Text and >=44px controls remain DOM; no forced reading timer. Reduced motion selects held final pose. Grid/tray are hidden until final click. Do not render invented stand-ins in place of missing resources.

Existing src/prologue-staging.ts expresses poses/props/road states and semantic anchors; `loose-stone` needs scene-manifest binding. `start`/`goal` resolve through the game camera, never percentages invented independently. Basket and crouch assets should share Ruta's ground-plane scale; foot contact follows pose-specific local anchor. Camera=gameplay in frame 6 must be exactly the first puzzle camera. Replay must leave puzzle session untouched.

Pending acceptance evidence: six finished frames at 844x390 and 740x360, portrait correctness, full production before/after story traversal, resume/reload/skip/replay/storage failure, and transition video. Existing old prologue screenshots prove old functional flow only, not final resources. Phone, iOS and family: not-run.
