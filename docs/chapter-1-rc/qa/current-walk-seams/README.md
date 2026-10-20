# E-view seams: current temporary walk, 2026-10-20

Base main f046889; read-only diagnostic, **not an animation fix**.
Reproduce: `/tmp/ruby-rc-tools/bin/python scripts/audit-current-walk-seams.py`.
`review.html` draws immutable `export-v2/renders/e/walk/00..15.png` at 2× nearest,
with projected hip/knee/ankle probes from the actual saved evaluated joints.
`actual-browser-all16.png` is a real Chromium screenshot, all16 images decoded,
page errors0. No image crop, source rescale, per-frame pivot or raster edits.

## Confirmed

- Every projected knee center in both legs is alpha255 in all16 source frames.
- At alpha≥128 the full figure has one significant connected component in every
  frame; there is no second disconnected component of12pixels or more.
- Static thigh source hip endpoints have alpha0, and shin source ankle endpoints
  alpha0. Other layers cover these points in the final composite. An individual
  transparent part endpoint does not prove a hole in the assembled character.
- Both thigh source knee-end pixels and shin source knee-start pixels already have
  alpha251/252. Enlarging the knee alpha as an automatic fix is unsupported.
- Existing v3 release-pack script asserts exact alpha against v2. Repacking the
  runtime atlas cannot change these masks or the rendered contour.

This narrows the defect: the perceived cut knee is not a missing alpha center or
fully disconnected leg in this E-view. The exporter uses separate flat textured
thigh/shin/foot objects, independently remapped by source bone endpoints; round
knee-cap/shin-top masks and white ankle cuffs remain visible as independently
moving graphic shapes. This implementation explains why it cannot provide newly
drawn folded-cloth poses. The alpha test alone does **not** identify one uniquely
correct art edit or rule out a thin contour notch; coverage thresholds are stated
so the result is not overclaimed.

## Decision

No blind dilation, body warp, source scaling or rejected native-character swap.
A safe final fix requires an artistic revision of the actual cutout overlap/detail,
or a coherent new whole-character sequence matching accepted Ruta. Current16
whole frames cannot recover missing cloth/anatomy detail from new viewpoints.
A limited source-overlap pilot remains possible, but must demonstrate visible
improvement before replacing assets; passing this diagnostic is not that proof.

No after-loop is supplied because no asset changed. Existing before-game AV and
full-route evidence: `../final-temporary-walk/`. No new game/physical phone/family
claim. Runtime/UI untouched; future integration belongs to #46 and requires
independent browser/game review.
