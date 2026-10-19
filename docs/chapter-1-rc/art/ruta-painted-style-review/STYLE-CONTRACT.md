# Ruta painted sprite style contract — #36

The accepted painted Ruta is the appearance authority. The ready3D Walk/Idle is the pose/timing/camera authority, **not final art**. Maksim accepted the ready gait and requested sprites in Ruta's accepted style; that does not approve the stock adult adventurer likeness.

Appearance references inspected: `public/assets/characters-v1/optimized/ruta-idle-pilot.webp`, `ruta-portrait-pilot.webp`, `ruta-adjust-satchel.webp`, `ruta-surprised.webp`, `ruta-crouch-basket.webp`, plus `public/assets/characters-v1/ruta-back-study.png`. Idle and portrait lead identity; story poses confirm costume consistency. Back-study supports rear hair/strap/bag continuity. Story baskets/apples are action props and are not part of ordinary walking/idle.

|Feature|Required appearance|
|---|---|
|Identity|Friendly young Ruta, large clear blue eyes, warm peach skin/rosy cheeks, soft brows/small nose, gentle expressive mouth; consistent face across front/three-quarter/profile. Avoid stock adult angular face.|
|Hair|Long loose chestnut/copper-gold waves, warm painted highlights, side-swept fringe; layered volumes around shoulders and down back. No short stock red hair or ponytail. Rear silhouette remains recognizably the same hair.|
|Top|Cream collared blouse with sleeves rolled near elbows; dark olive sleeveless fitted vest, brass/gold buttons; burgundy/red neckerchief tied at collar. Stock flat green shoulder cape is not the costume reference.|
|Lower body|Loose warm brown cargo trousers gathered above boots, stable side-pocket details; cream sock cuffs; brown leather lace-up ankle boots with clear soles, brass/warm stitching details. No bare adult legs, tights or tall featureless stock boots.|
|Bag|Exactly one warm brown leather flap satchel, one main buckle, one diagonal shoulder strap, attached to the same anatomical right hip across all views. Accepted front image places it screen-left; accepted rear image screen-right. Occlusion can hide part/all of the bag naturally; do not invent a second bag or mirror anatomy.|
|Paint|Warm storybook painted sprite, rounded readable forms, dark warm outlines/contact accents, soft layered brush shading and restrained highlights. No flat lowpoly facets, photoreal skin or glossy plastic. Keep saturated blue eyes/red scarf as small identity accents; foliage-green vest and leather-brown lower body remain balanced.|

## Geometry and motion that repaint must preserve

Use the exact supplied whole-pose guide for each indexed frame, not a newly imagined walk. Keep feet/sole contact points, ankle/knee/hip/shoulder/elbow/wrist centres, head centre/orientation, limb lengths and pose phase; camera/elevation, direction and occlusion order remain that guide's. Do not replace bent recovery legs with straighter decorative poses, change stride width, rotate a foot to suit the illustration, or create extra fingers/limbs. Hands must retain guide placement and swing. A more youthful face is painted inside the stable head registration; do not solve adult proportions by moving skeleton joints or scaling each frame independently.

Styling may replace colours/materials/outlines, add the accepted vest/scarf/cuffs/pockets/laces and soften facial/clothing forms. Hair can become the accepted longer waves while retaining a consistent registered head and controlled silhouette; new waves must not erase arm/hand articulation or fluctuate frame-to-frame. Garment thickness/looseness and bag contours may be painted consistently around existing guide structure, without changing body centre or foot geometry. Stable highlights/folds follow rotating volumes and gait rather than random texture regeneration. If costume cannot fit without altering pose, flag that frame for guided correction instead of silently changing the motion.

Native frames remain512×640, one fixed foot anchor256,516.859314; uniform.5 delivery canvas256×320, anchor128,258.429657. Body reference is419.317435native/209.658717delivery pixels, **not canvas640/320**. No per-frame crop, recenter, warp, perspective correction or independent screen offset. Preserve exact joint/sole guides even when the painted visible outline changes slightly with cloth/hair thickness.

Six directions E/SE/SW/W/NW/NE must be genuine corresponding views, not mirrored substitutes that swap bag/strap/costume asymmetry. Both accepted camera-angle groups0 and.04494904935533156 already have calibrated guides; use the correct group/index directly, never derive fresh screen60° diagonals. GroundScale.65 and source root normalization remain unchanged. Walk24 phases and Idle24 phases retain their original indexed timing and loop order. No basket, added prop, bag duplication, decorative ground or new shadow may obstruct the exact feet.

## Independent temporal review to perform after painting

Review all frames at native/body delivery size and real loop timing: identity/wardrobe/bag count and side stable; no face/hair/boot/hand flicker; motion remains the supplied leg/arm sequence; projected sole/joint/anchor matches frame guide; silhouettes neither clip canvas nor pop at23→0. Inspect front/side/back and both camera variants, then actual translated ground contact and walk/idle transitions in integrated runtime. Source gait's known stance residual remains a separate contact issue; attractive repaint does not establish slip-free walking.

This document is a style/constraint review, not generated art approval or a576-frame audit. `native-six-heading-reference.jpg` is a diagnostic sample of base3D phases0/6 across six headings, inspected for guide roles; it is not the approved visual style. Runtime and final painted-loop acceptance remain pending.
