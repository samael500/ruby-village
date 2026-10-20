# Independent stream correction review — 14b1f6f

**Functional regression PASS; P2 corrected sufficiently for this pilot; P1 improved but residual painted-bank clipping needs review. Not finished art, not RC or production activation.**

New isolated worktree `/tmp/ruby-qa-stream-14b1f6f`, branch `qa/37-stream-road-14b1f6f`, immutable review checkpoint14b1f6f. Read repository instructions and stream source contract. Actual TypeScript/Vite production build passed (89.3MiB exports), own5298; root5306/user5180/integration5286 untouched. Only QA artifacts changed. Non-release watermark and pending visual gate remain explicit. The inherited review gate patch is preserved as evidence, not an integration source edit: stream layout2/road pilot only, full-polygon visual audit pending, metadata/camera/endpoints still gated. No all-eight or normal-production activation approval.

## P1 visual verdict — meaningful improvement, residual trim remains

Actual clean desktop1280×720 and native-touch landscape844×390 views show a visibly curved, flowing channel rather than the former complete polygon-shaped water silhouette. The exact-water overlay demonstrates that the smaller **visible artistic body** sits inside the unchanged full logical zone. These are distinct contracts and were measured separately.

The painted bank support still has some hard straight cut lines at logical hex boundaries around the5,3/5,4 bends: parts of the outer stone/grass trim terminate abruptly while the water itself curves. This remains apparent in the actual enlarged `mouse1280-bank-road-crop.png`; view it with the full clean screenshot and exact overlay to distinguish grid lines from the painted-edge termination. It is substantially better than c64b249, but I do not call the whole bank finished solely because its centerline is smooth and mask tests pass. Root was notified of this residual P1 review finding.

## P2 visual verdict — corrected within scoped pilot

The worn stone perimeter now has a visible subdued earth edge and soft ground contact rather than the old single uniform painted stroke. It remains clipped to the actual union. The inspected screenshots/crops show continuous stone material, no raised ownership-hex rims and no eroded gap where land meets the bridge. Returning the neighboring composite opens the correct external edge; undo closes it. This addresses the prior flat-stroke P2 in this scoped candidate; it is not approval of every scene/material or a final artistic signoff by Maksim.

## Independent actual gameplay and geometry

`review.py` repeats both accepted solution runs: actual mouse1280×720 and native CDP touch844×390, tray→rotation→cell→Place, no forced actions or browser layout injection. Source manifest solution skips null stream-b. Whole three-cell reselect/outline, pending rotation, invalid preview, combined valid move/rotation, return, undo and reload all run through UI. Preview does not change surface, edge or byte-identical saved state. Confirmed movement/return changes union/edge; undo and reload restore it. Check completes the real route to arrival/result. No page/HTTP errors.

Every state compares actual SVG clip polygon coordinates with confirmed non-bridge ownership plus fixed endpoints1,3/9,1. Solved land clip is six cells; all three bridge cells are excluded. `edge-audit.py` independently derives polygon edge multiplicities and compares actual road and bridge path topology across all bridge-bearing states: no internal land rims, internal bridge rims or shared land/bridge cap rim, correct exposed edge after neighboring return. It also checks the selected outline is exactly the whole selected composite.

`visual-water-audit.py` independently confirms:

- logical truth mask bytes unchanged from c64b249;
- actual visible body alpha255 at all seven accepted water centers, all in the same4-connected component;
- bridge middle6,1 alpha255; dry ends5,1 and7,1 alpha0;
- both actual shared water contacts above/below the bridge middle alpha255;
- actual body opaque leak0 in the conservative1px free interior;
- native RGB changes0 inside that free interior against canonical dry source `stream-dry-v1.png`.

An initial comparison against exported dry-background.webp gave55 tiny≤2RGB differences near the board boundary. That export includes the pre-water board/continuation composition and is not the canonical dry-source RGB invariant. The corrected audit compares the actual canonical dry PNG, yielding0, matching the stated contract. This is a QA reference correction, not a claimed game fix. `water-audit.py` additionally retains the independent full-truth-mask boundary analysis; all original raster boundary candidates are within documented1px tolerance.

## Evidence and A/V

Paired technical/clean/exact-water-overlay screenshots plus enlarged real-image crops retained for both inputs. Clean view hides only technical water polygon fills and≈glyphs, not art, road or watermark. The temporary overlay uses accepted source polygons in the actual painted-world transform and is removed before interactions resume.

Both actual input/walk videos include original single-AudioContext WebAudio capture, raw Opus audio and muxed MP4; raw silent input videos remain available. No added soundtrack. Audio/video alignment uses reported performance/monotonic construction-time estimates, not a hardware-sync event; stream starts/durations are recorded in media.json and audio/video lengths differ. No sample-exact synchronization or human-listening claim. Physical phone/family/Safari/iOS NOT RUN; CDP touch is emulation.

Final art/layout2 integration, MPFB gait, full chapter and other seven road scenes remain pending. Source runtime/vendor/camera/logic untouched by QA. No main merge/deploy. Reproduce with own production preview5298 and the scripts here using `/tmp/ruby-rc-tools/bin/python`.
