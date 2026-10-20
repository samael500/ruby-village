# Rejected sources

rabbit-left-v1-ear-swap-clipping.png — Builtin imagegen output. New left-facing pose and preserved clothing/pockets, but upright/drooping ears swapped across the face; source touches canvas top/bottom. Not eligible for runtime.

Correction attempt v2 (two references) returned HTTP400 output moderation `other`, request43537b32-1a9d-4ea9-826d-8d8095b1a59a. No image artifact returned. Kept prompt; repeated with one approved reference and shorter plain sprite description. No fallback/API/external service used.

rabbit-left-v2-ear-swap.png — Single-reference retry gave contained figure but repeated swapped ears. Not runtime eligible. Technical packing was tried for measurement then removed; no rejected runtime asset retained.

baker-left-v1-wrong-apron-tie.png — left-facing but apron knot changed side; targeted knot-only edit requested.
squirrel-left-v1-wrong-bag-side.png — left-facing but bag/strap/scarf fringe switched side; targeted accessories-only edit requested.
miller-left-v1-wrong-sack-arm.png — left-facing but sack switched arm; targeted arm/sack correction requested.

baker-left-v2-wrong-apron-tie.png — direct knot-only correction merely shortened wrong-side tail. Two-step remove+insert then succeeded; remove intermediate retained.
miller-left-v2-wrong-sack-arm.png — direct arm/sack edit ignored target side.
miller-left-v3-wrong-sack-arm.png — two-step remove succeeded, insert put sack back in wrong arm. Intermediate retained. No further generation by facing agent; coordinator's original-reference localized head edit produced correct final source instead.
