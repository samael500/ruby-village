# Independent four-scene candidate audit — #45 / #46 / #62

Baseline integration `36912d2`; own private review commit `acc2db5`, separate worktree/build. **Art/runtime scope needs fixes B1 and B2 below.** Gate/post/forest and bakery environments otherwise pass the described scoped checks. No user artistic acceptance, global activation or RC is claimed.

The private patch sets layout2, checks only gate/bakery/post/forest and waives **only pending full-polygon visual-audit status**. Camera/endpoints/required resources/anchors stay checked. Watermark says NOT RC; map/next navigation is hidden. `review-only.patch` is evidence, **must not be applied to production**. Coordinator integration/global gate unchanged. Production build passes; actual served bundle hashes recorded. Only earlier progress is seeded to enter each target, never a layout, solution or win.

## Findings requiring correction

**B1 — Bakery arrival overlaps Baker.** Actual anchor1290,405 is too close to Ruta's accepted goal1231,456. All three after-dialogue pages show visible overlap at the Baker's left/loaf/arm side. Independently reconstructed any-alpha overlap:277 viewport pixels at1280×720,120 at844×390; result228/91 respectively. `bakery/1280/08-arrival.jpg`, `bakery/844/08-arrival.jpg`, actual videos and `pairwise.json`. Coordinator notified early; later staged1360,405 fix is **not part of this frozen audit** and needs its own repeat.

**B2 — Gate landscape arrival obscured by dialogue.** At844×390 the after-win dialogue panel covers most of Ruta and the gate interaction; only part of her head remains above the panel. Actual `gate/844/07-arrival.jpg` and08 show this. Desktop arrival and the completed-result composition show the scene normally. This is a staging/camera/panel-layout issue observed in the real game, not an inferred source-mask fault. Do not alter the puzzle goal to solve it.

## Actual game checks performed

Eight normal-motion real UI runs: four scenes × desktop1280×720 and emulated landscape phone844×390, with mouse or native CDP touch. Each covers introduction, activity, replay, reload, accepted-solution placement through actual inventory/rotate/cell/place controls, normal route walk, all after-dialogue pages and the result. Every completed run has no page or HTTP errors. The eight actual silent browser videos and90 state screenshots are retained; gate additionally has twelve actual prologue-frame captures across the two viewports. No physical phone/family/audio acceptance.

Story checks assert grid/tray `display:none`/absence of render rectangles, and the whole technical field hidden during ordinary narrative; won narrative retains the player's actual restored road. Prologue canvas has no technical grid/cell DOM and keeps the scripted loose stones. Results show four different current places with actual player roads and relevant actors, not one shared ending.

Post Hedgehog remains present in scene and every dialogue/result/replay/reload state; actual pairwise visible alpha0 at arrival/result on both viewports. Bakery Baker likewise remains loaded/visible but fails B1 overlap. Gate/forest intentionally have no resident actor in this delivered scene contract; forest dialogue portrait alone is not described as a scene NPC. Full-nonzero alpha against accepted playable ground/water is0 for **one delivered new conversation-left facing plus the actual optimized legacy-idle fallback per Baker/Hedgehog**. These are two resource poses per resident, not eight directions; exact entries in `geometry.json`.

Some instant screenshots caught the Hedgehog portrait before decoding; a separate actual delayed capture `post/portrait-loaded.png` verifies it decodes340×384 at its real URL. No persistent missing-portrait defect is asserted from those transient captures.

## Environment / map / wide review

Viewed current map raster and all four native/game environments. `map-native-object-comparison.jpg` explicitly compares source crops (not a synthetic game capture): actual game evidence is separate. Gate's warm plaster/stone cottage, red multi-gable tiled roof/chimney and flower details relate to the map home; bakery has the characteristic red/cream striped awning, bread display, red tiled roofs and stone doorway; post has matching red mailbox, warm cottage, roof and parcels; forest has the paired wooden arrow sign and conifer setting. These are painted scene candidates, not the old technical layout stand. No extra duplicated foreground building/gate was observed in the actual scenes.

All four native1672×941 images match their registered3272×1200 wide crops exactly. Desktop/phone activity/dialog/result frames show painted coverage without abrupt flat/black side or top/bottom bands. Forest grade visibly applies to the scene/actor/road together while HUD stays readable. Artistic approval remains pending.

Accepted layout-adjustments SHA-256 remains `6baed82d3dea0e1b6472582751bcd0ccb9d41c872f50c9b865838b17e7b1cf6e`. No cells, logical rules, placements or save migration changed for this review. Individual old tile styling remains visible here; the independently developed connected-road pilot has **not** been claimed rolled out across these four scenes.

## Harness / environment notes

Own5298 process unexpectedly exited143 partway through; completed case reports were preserved and unfinished cases rerun after restarting only the reviewer-owned server. This is recorded as environment interruption, not game failure. A first gate-touch attempt tapped the partly offscreen eighth inventory chip and correctly failed to complete; harness was corrected to scroll the target into view before real native tap and assert each placement's owner. No invisible/forced input is counted as passing evidence. Completed gate touch then passed normally. Scripts/logs preserve the reproducible method.

Eight per-case reports, `pairwise.py/json`, `geometry.py/json`, build hashes/log and the review patch are retained. No source author edits, main merge or publication. B1/B2 plus integration of new road/character resources and final independent whole-chapter acceptance remain outside a passing RC claim.
