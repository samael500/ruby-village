# One native likeness proposal: incomplete artistic result

This is a bounded same-topology 3D REST-geometry experiment, not accepted Ruta likeness, final hair, a new rig, runtime installation, or a completed animation. Actual three-view renders are `e-walk00.png`, `front-diagnostic.png`, `threequarter-diagnostic.png`; `source-proposal-threeview-comparison.jpg` places unchanged full512×640 source and proposal renders in columns, without fitting or altering character pixels.

## Actual result and remaining mismatch

The forehead is more open and the existing side-lock surfaces have continuous bends. However, the crown/fringe still reads as a bulky cap; the eighteen lock volumes and existing bright texture strokes still read segmented/rope-like, rather than the accepted broad loose waves. The E camera continues to expose a rear-three-quarter head and obscure the face more than the accepted painted profile. The native expression/gaze and face likeness are not established as the approved youthful Ruta. This proposal therefore does **not** achieve the requested canonical likeness. Do not run48 renders or promote it to final hair on the basis of technical checks.

Reference files/hashes are in `reference-inputs.json`: exact canonical `public/assets/characters-v1/ruta-idle-pilot.png` and the approved high-resolution painted E source/phase00. Both canonical and extracted highres phase00 were actually viewed; unavailable user attachments are not claimed viewed.

## What changed

Read-only NPC source `15dfd4c`/hair texture `e769a7b`, blend SHA `a60a9601d6a8daa3dfc271b5152d41a361f9397847e111d80c08b3ae05e6d754`. Output SHA `192d170bccfa10edb4d165277bc1dd254cc93c73a96951d7ed3346202a7ff94a`.

Only existing visible `Ellie ready ` head/hair REST vertices changed. Existing cap-front vertices receive a smooth asymmetric fringe lift/sweep; eighteen original full3D lock meshes receive a smooth S-wave rest displacement. No primitives, hair cards, new topology, per-frame AI imagery, skeletal image warps, or UV edits were introduced. Every native UV layer, vertex binding, modifier/material assignment and packed image remains exact. The fixed copper diffuse UV texture remains usable; this does not imply its visual highlights match the new hairstyle.

There is an **explicit**−10° localX REST-geometry gaze/head lift around the unchanged Head-bone pivot, blended to zero below original REST Z1.18. It is not a camera tilt, global character yaw adjustment, or change to Head bone/actions. Consequently the original heading contract is not silently replaced by painted profile framing. Front yaw0 and three-quarter yawπ/4 are labelled diagnostic views; only E yawπ/2 uses the existing game heading. All retain the existing base orthographic camera,512×640 canvas and unmodified actor scale/footRoot. Head/hair geometry can change visible rest height; no scale correction is applied.

## Reproducibility and checks

`make-proposal.py` opens the exact pinned source read-only, transforms the existing geometry, preserves all actions with fake users, packs unchanged native images, saves the derivative, and renders precisely three Eevee32sample stills. Actual Eevee is retained because native ShaderToRGB materials are unsupported in Cycles. Hair uses NPC's diffuse fixed painted texture, not SH-Hair glints. No body/garment material replacement occurs.

`cold-check.py` reopens source and saved derivative in a new Blender process. It verifies all non-head mesh coordinates, all UVs/weights/packed images, bone rest fingerprint and all action curves exactly. Original protected neck vertices (2946 vertices selected from REST Z≤1.18) remain exactly unchanged both at REST and evaluated Walk endpoints0/40. Actual three stills show no newly detached eyes, eyebrows or ears; this is not a fullcycle collision/surface certificate.

An initial QA probe selected vertices by **posed** Z≤1.15, which includes intended changed vertices from higher REST regions after pose deformation, yielding1.118mm. The retained failure log records that methodological mismatch. The final check selects original protected REST indices consistently and requires exact zero change; it does not assert that every posed low-head vertex is unchanged.

Run commands, process logs, source/output hashes, complete before/after mesh fingerprints and explicit limitations are preserved. The source blend and NPC worktree remain unchanged. No48 export, game validation, physical-phone test, external service or artistic acceptance is claimed. A substantially more deliberate hair-volume/face asset design may be needed rather than further blind rest bending of the current donor cap/locks.
