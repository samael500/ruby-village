# Independent MPFB motion technical pilot review — 24315ea

**Result: contact/loop engineering baseline passes; natural motion needs correction before six-direction expansion.** M1 rigid elbows and M2 hand/satchel intersections remain. This is a technical mannequin study with explicitly rejected generic appearance, not final Ruta, not a game-walk acceptance and not RC.

Read `docs/chapter-1-rc/mpfb/motion/README.md`, motion sources and repository AGENTS.md. Separate worktree `/tmp/ruby-qa-mpfb-24315ea`, branch `qa/37-mpfb-motion-24315ea`, immutable source24315ea stacked from appearance25690fa. Only this QA directory changed. Source `.blend`, rendered frames, body and runtime were not edited or saved. `summary.json` records exact source commit and SHA256; blend hash matches before/after Blender evaluation.

## M1 — rigid nearly straight elbows / restrained upper-body motion

Actual side/front/three-quarter strips, all24 temporal frames and repeated browser playback show a mechanical, stiff-armed quality. Arms are **not static**: fresh evaluation gives0.28rad (16.04°) total upper-arm swing and95.7mm rig-relative wrist displacement. The elbow angle nevertheless stays7.19776–7.19778° on both sides across97 samples, effectively fixed and almost straight. That supports the visible rigid-pendulum impression. The knees remain flexed throughout (15.75–53.05°), giving a slightly crouched/stepping impression in the side sequence; treat that as visual feedback rather than a universal biomechanical threshold. Contact accuracy alone does not establish naturalness. Rework upper-body/arm phrasing with actual bag clearance before cloning six views.

## M2 — actual right hand intersects satchel

`accessory-check.py` independently tests actual evaluated meshes in a fresh Blender process. Body MASK modifiers are temporarily disabled only inside the measuring process to retain original source vertex/group correspondence; no file is saved. It selects vertices >0.5 weighted to right lowerarm/wrist/finger/thumb, builds the corresponding surface and compares it with the evaluated satchel using BVH triangle intersections. All24 poses intersect on the right (70–102 triangle pairs), left0.

To exclude sleeve/forearm coverage as the explanation, `hand-bag-check.py` repeats with **hand-only wrist/finger/thumb** weights:1569 vertices each side. Actual right-hand surface intersects satchel in **21/24 poses**, with3–24 overlapping triangle pairs when present; frames18–20 clear. Left hand remains0. This is a real geometry collision, not merely visual overlap of projected boxes. `actual-arm-bag-crops.jpg` enlarges unchanged actual source E07 and three-quarter09 renders; occlusion makes precise penetration hard to judge at native384px, hence the evaluated-mesh check. No all-garment collision-free claim is made.

The satchel is genuinely skinned and follows the rig; it is not an unattached floating object. Its wrong interaction with the arm remains a motion issue. Satchel/strap/flap/buckle/scarf/buttons all have actual armature modifiers and rig-relative evaluated vertex changes; full counts are in fresh-blender-measure.json. Waistcoat, shirt/trousers, boots and body deform rather than remaining rigid render cutouts.

## Independent contact/loop measurements

`measure.py` opens the packed blend in a **new Blender4.5.3LTS process**, CPU2 threads, own config/scripts/data paths under `/tmp/ruby-mpfb-qa243-*`. Shared MPFB vendor stays read-only. The mesh has19158 source body vertices and167 rig bones (standard163 plus four native helpers). No author verification report is used as input to the measurement.

97 samples at quarter-frame spacing cover frames1…25. Source-bottom indices are independently derived from each shoe's rest bounds (bottom4mm, forefoot/heel20% of length), instead of copying author's marker lists. Actual armature-evaluated points are measured in **world coordinates**. Shoe subdivision is temporarily disabled only for persistent source-index contact markers; a separate evaluated **render-level1 subdivided boot mesh** is measured before that change at every sample for floor penetration. Every modification is transient; no source save occurs.

- Physical root translation:0.56875455m per cycle, linear world advance. Actual24 different root-relative poses; frame25 endpoint closes bone matrices within3.055e−7.
- Flat stance phase0.125…0.45: toe/heel world drift about0.0182mm on both sides. Push-off phase0.49…0.59: toe-marker drift about0.669mm per individual support cycle. This smaller window/independent marker set is deliberately stated; it is **not** a claim to beat the author's1.198mm broader-window number. Support-cycle grouping prevents incorrectly comparing different world plants across the loop boundary.
- Knee flex15.75…53.05° including subframes. Mid-swing bottom clearance17.14…46.53mm in measured phase0.65…0.95. Pelvis world Z spans0.615625…0.647625m (32mm).
- Actual **render subdivision level1** shoe minimum Z is+0.00034468m at frame24 (~+0.34468mm): no floor penetration at the97 tested samples. No visible stance sliding was apparent in the fixed-world six-frame sequence; numeric world stance points support that observation. This is sampled evidence, not a continuous-time collision proof.

A measurement correction is recorded explicitly: the source shoe modifier has viewportlevel0/renderlevel1. The initial draft evaluated viewportlevel0, found−0.01975mm and incorrectly called it full subdivision. That was a QA labeling/method error, not a game defect. The final own script explicitly switches the transient modifier to renderlevel1 for the complete boot floor probe, then disables it only for stable source marker indices. Fresh reopening produced the positive+.34468mm minimum reported above. Source file/hash stayed unchanged.

`browser-review.py` independently hashes42 actual PNG renders (24E plus6front/6three-quarter/6fixed-world), all unique. Actual E alpha maximum height251px independently reproduces69.6101 scene-pixel stride at136px target height and1.70m orthographic scale. This calibration is appearance-dependent and must be repeated after accepted body/clothing/scale.

## Actual frame and browser loop proof

Actual `actual-three-view-strip.jpg`, `actual-fixed-world-strip.jpg` and individual E/front/three-quarter PNGs were inspected. `all24-temporal-sheet.jpg` and `loop-boundary-23-24-01-02.jpg` derive only from unchanged whole rendered frames. No interpolation, mirroring or new pose synthesis is used. The boundary looks continuous in those frames and numeric root-relative endpoint check; this does not prove every joint's velocity is C1 continuous.

The browser page plays original `E-actual-cycle.gif` plus a canvas sequence of actual PNGs. Source GIF has24 frames×30ms=720ms. Playwright records seven browser cycles, observes all24 indices and repeated24→1 boundaries; logs/screenshots and `actual-source-loop-browser-silent.webm` are retained. Front/three-quarter/fixed-world diagnostics have only six source samples, held120ms each; they are not falsely presented as24 newly rendered poses. The fixed-world diagnostic sequence resets when replayed; it is a contact-review sequence, not an infinite world-path animation. Actual world root travel is measured separately in Blender.

## Limits and decision

M1/M2 should be addressed and independently rechecked before six-direction/start-stop rollout is called motion-ready. Existing contact/stride/loop source is useful engineering evidence; numerical contact success does not waive naturalness or collision findings. Generic face/hair/wardrobe are already rejected and were not relabeled accepted. No actual production game walk, final body likeness, six-direction set, start/stop controller, phone, Safari/iOS or family test is certified. Physical phone/family: NOT RUN. Browser loop proof is silent; no audio claim. No main merge or deploy.

Reproduce: Blender with `--threads 2 --python` on measure.py, accessory-check.py and hand-bag-check.py using separate BLENDER_USER_CONFIG/SCRIPTS/DATAFILES under/tmp. Serve this worktree read-only at5298 and run browser-review.py with `/tmp/ruby-rc-tools/bin/python`. Only QA outputs are written; source blend/hash stays unchanged.
