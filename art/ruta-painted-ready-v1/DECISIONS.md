# Painted Ruta from accepted ready-rig motion

2026-10-19: Maksim explicitly accepted the ready-character gait and requested sprite rendering in approved Ruta style. This branch owns painted assets only. Source ready-rig3dbe699 and all motion/pose registrations stay unchanged. Reference is public/assets/characters-v1/optimized/ruta-idle-pilot.webp plus portrait/approved poses. Native low-poly output is a motion guide, not final artwork.

Root owns imagegen painting; npc_facing owns separate deterministic guide/pack tree; stream_road_finish independently reviews style/temporal consistency. No concurrent edits. Start with8 distinct E gait poses (0,3,6,9,12,15,18,21), a real loop and anchor/silhouette check before the complete24-phase/6direction/2camera export. No cutout warping, mirrored bags, per-frame height normalization or automatic production replacement. Whole-frame generative repaint must preserve actual native motion; if it drifts, reject rather than claim technical checks passed.

Generated sources/prompts/registrations and rejected trials are versioned. Any atlas extraction is fixed-cell packing only, not pose correction. Main merge/publication forbidden.
