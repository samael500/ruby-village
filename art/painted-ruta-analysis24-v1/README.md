# Painted E24 v1: unregistered fixed-cell analysis (#36)

Candidate only, no runtime changes. Source1374×1145 preserved byte-identically. Native cell boundaries are round(col*1374/6),round(row*1145/4). A single whole-sheet resize1536×1280 produces fixed256×320 cells; no individual height correction, crop, shift, warp, anchor correction or image editing.

Open `index.html`: 24phases/1666.667ms, enlarged view and game-scale view. Game scale136/209.6587226 is the existing native body-reference scale, deliberately not an individually fitted painted height. Toggle original native guide or guide ghost. `registration-diagnosis.png` alternates painted/guide rows; red=root reference, blue=all alpha≥16 bounds.

Metrics in `analysis.json` retain all-alpha16 bounds AND largest connected alpha16 component bounds. All-bounds ratios can be inflated by fragments of adjacent-row poses, so they are not equivalent to body size. Largest-component silhouette/guide height ratios1.126–1.223. Painted bottom differences+24…56pixels. First six cells reach bottom boundary; previous-row boot fragments appear at the top of subsequent cells, visible at alpha≥16. A fixed-cell export therefore retains source cell-boundary contamination/clipping rather than hiding it. Final row local top40…44 versus first row60…62 and lower body extent show registration variation. No claim these silhouette measures identify anatomical head/ankle/contact landmarks.

Raw bright-red speckles at alpha1…3 are not treated as visible red defects. The visible-cell overlap issue is measured independently at alpha≥16. RGBA composites are preserved normally.

## Per-frame anchor proposal

Per-frame footAnchor is a legitimate sprite representation of an artist's varying canvas origin **when a source-verified semantic support point is available**. It can recover translation while preserving a deliberately registered gait. For a walking airborne foot, the lowest silhouette pixel is not the support point; shoe shape/heel/toe and projected contact plane differ. Selecting each frame's bbox-bottom or centering its feet would conflate pose with origin and can invent contact.

This source currently has no verified painted joint/contact correspondences; native root/ankle guide coordinates alone do not prove where that semantic point landed in the repaint. Translation cannot repair differing body scale, changed foot pose, or missing/cross-cell pixels. Thus no corrected anchors are proposed/applied here. A future proposal must publish original/corrected loops, source-visible correspondence annotations and contact residuals, with one unchanged scale across all frames.

Reproduce: `python3 scripts/painted-ruta-analyze24.py`. Runtime/source rigs/actions untouched; no NPR continuation.
