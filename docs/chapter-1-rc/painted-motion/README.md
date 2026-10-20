# #36 painted motion experiments — 2026-10-17

Status: reproducible east rigged-painted pilot, **not a finished six-direction walk set**. Approved Ruta appearance preserved; production disabled. main.ts and character-animation.ts untouched.

## Actual attempts

1. Built-in imagegen paint-over of a registered 6×8 sheet sampled from one existing Blender cycle, frames1,3,...15. Actual rig input and accepted identity were referenced. Source/prompt preserved. Recognizable appearance; phase geometry unreliable. Original1448×1086 output normalized uniformly to requested grid. Raw offsets alone are not a gait rejection.
2. Native-mask cleanup/repacking: remove alpha<32 and isolated components, whole-cell translation into320px padding. No framewise scale/mirror/pose painting. Makes review sequence; not proof of stance. First48frame runtime is reject/review evidence.
3. Targeted8phase east edit: first connection failed, built-in retry succeeded. Source/prompt saved. Passing/contact phases still unreliable; boot/satchel drift. No further directions generated from failed targeted pilot. No CLI fallback.
4. Deterministic alternative: ONE east painting split by explicit masks into body/thigh/shin/boot parts. Existing Blender IK action evaluated in16phases; actual projected hip/knee/ankle/toe joints drive textured meshes. Soft arm deformation from same action; face/torso/hair/satchel ONE stable texture. Blend/masks/evaluated joints/16RGBA frames retained. Genuine relative knee/foot motion, not whole-body bob.

## Results / limitations

East mesh has true stance exchange and800ms loop. Initial wrong physical L/R binding preserved as rejected sheet, fixed using projected joints. Generated rear boot had ambiguous toe direction: current experiment reuses ONE unmirrored forward-facing boot texture on both physical feet, explicitly not authored inner/outer boot art. Cuff/knee seams and occluded-leg paint need cleanup. Five other directional rigs, clean boots, idle, turns, start/stop and production occlusion incomplete. **Does not close #36.**

Next useful step: clean articulated parts/overlap masks over canon, then same evaluated-action export for all six views; not another independent phase batch. East technical exchange demonstrated; artistic gait still needs review before expansion.

## Contract

Unchanged source rig: art/blender/characters/ruta-motion-prototype.blend. .72worldunits/cycle,800ms, ortho2.65 at256px, nativeheight210. At displayheight136: e/w stride45.045px, diagonals21.662px (yaw from rig manifest). Mesh maps rig pixels*224/210 into320canvas, anchor160,256. Display136/224 cancels intermediate scale. East45.045/.8=56.306px/s; diagonal27.0775px/s. Shared800ms phase continuous at turns; camera scale applied once.

Delivery east-mesh-pilot/manifest.json +16PNGs under public/assets/characters-walk-v1:320×320, anchor160,256,50ms,looptrue,productionEnabled=false. Contacts0/8 declared from actual rigL/R; final painted ground-contact review pending. Top-level manifest is disabled first48frame experiment.

## Evidence

- mesh-east-contact-sheet.jpg / mesh-east-runtime.webm: deterministic east pilot, actual CharacterPlayer/CharacterRoute on accepted courtyard; isolated review, not production gameplay.
- attempt-01-six-directions-runtime.webm, desktop/844×390 screenshots, runtime-checks.json: actual six-direction first-attempt playback, pause/completion checked; not final art.
- alpha-registration-audit.json / repacking.json: unmodified first sheet metrics and native transforms; not anatomical approval.
- mesh-audit.json:16RGBA transparent frames, canvas bounds, IK stance exchange and plant speed within0.01px/s of56.306. Does not certify seams/anatomy.

Scripts character-paint-input → extract(source/paintover-attempt-01.png) → register → mesh-input → Blender original rig with character-paint-mesh.py → audit. Browser preview requires Vite/Playwright. Source .blend includes packed textures; scripts reproduce from repository parts.

Not-run: finished six-direction production traversal, physical phone/iOS, family and artistic acceptance. No merge/publish.

Verified: 74/74 existing Node tests, TypeScript and Vite production build pass; diff check pass. Mesh source/textures packed for portable review. Final east browser pause/reduced-motion/completion checks are in mesh-runtime-checks.json; all-six first attempt checks remain runtime-checks.json.

Stacked PR base is #59 (9c0911e). Browser evidence was captured on integration73c33bb, including approved courtyard source from #45 commit1d0dad5. Reproducing the pictured background therefore additionally requires that scene asset; rig extraction/export itself needs only #59 and this package.
