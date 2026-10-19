# Painted sprite candidate status

The user accepted the ready 3D gait, not this generated repaint. Rendering that gait into painted Ruta sprites remains in progress. This pilot is suitable for a focused style review only.

- E: 24 complete actors; independent Chromium page load, animation, pause and phase controls checked. Manual contour-based origin proposal is not an approved physical foot anchor. Browser QA found a visible body dip across frames17→18; do not enable in game.
- SE: alternating phases exist, but recovery/passing leg readability is weak.
- W: static whole-cycle alternating poses and the far-side bag are readable. Actual movement/camera registration remains unverified.
- NW / NE: promising static 24-pose direction, alternation and single right-hip bag. Runtime acceptance not performed.
- SWv1: rejected wrong heading.
- SWv2: rejected bag moving from hip toward chest and altered near-arm pose. Do not enable.

No per-frame height normalization, limb deformation, mirroring of an asymmetric bag, or runtime smoothing was applied to conceal these faults. Whole-actor extraction has exact RGBA provenance; packing checks are not gait acceptance.

Next source corrections: E17–18 body/pose continuity, SW bag/arm consistency, SE passing readability. Then explicitly register painted origins, check a loop at actual game scale, turns, short and long routes, and bridges. A second camera group and painted Idle are not complete. The existing game sprites remain unchanged.

Source branch: art/36-painted-ready-sprites, draft PR #77. Source rig/gait PR #74; guide/packing PR #75. No merge or publication.
