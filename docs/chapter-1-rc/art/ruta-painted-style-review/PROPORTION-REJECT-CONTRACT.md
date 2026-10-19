# User rejection and proportional correction contract — Ruta

**Maksim rejected the painted pilot: too adult, arms/legs too long, with jerky movement.** Previous “promising source” reviews are observations of identity/gait readability, not acceptance, and are superseded by that explicit user verdict. Stop mass generation. First change the3D source proportions toward accepted idle, then inspect a short motion pilot. This document changes no source pixels, mesh or runtime.

Measurement authority: accepted `public/assets/characters-v1/optimized/ruta-idle-pilot.webp`,244×512. Not portrait. `proportion-grid-accepted.jpg` overlays20px rulers for reproducible manual landmarks; nativeE06 and paintedE06 ruler images show how the same comparison is affected by gait/view. Landmarks are hand-selected visible ranges, not automatic anatomical ground truth.

## Accepted standing sprite measurements

|Visible landmark|Approximate image coordinates/range|Normalized against crown-to-sole493px|
|---|---|---|
|Crown top|y4–8, nominal6|0|
|Chin|y141–148, nominal146|Head140px≈.284H; plausible.27–.29H|
|Shoulder centres|y160–174, nominal166|Height above sole333px≈.675H|
|Waist/belt|y247–257, nominal251|Above sole248px≈.503H|
|Clothing crotch/inseam|y320–338, nominal329|Above sole170px≈.345H; baggy trousers hide true pelvis|
|Boot soles|y491–506, nominal499|Reference floor; different feet/perspective produce~15px spread|
|Visible head skin/cranial width|x85–196≈111px, uncertainty±10px|~.225H|
|Shoulder joint span|x83–183≈100px, uncertainty±12px|~.203H; head/shoulder≈1.11, practical1.0–1.25|
|Hair envelope width|~170–215px depending row|Not skull width; may exceed shoulders1.5–1.9×|

Shoulder→waist≈85px(.172H); waist→garment crotch≈78px(.158H); garment crotch→sole≈170px(.345H). Do not convert the low trouser crotch into the actual hip-joint height. The relaxed far arm suggests upper-arm length~65–80px(.13–.16H), elbow→wrist~45–60px(.09–.12H), with shoulder/elbow hidden by blouse. Near arm is flexed/foreshortened and cannot provide an independent exact forearm length. These are projected garment/skin landmarks, not a rig skeleton recovered from a portrait.

## Native adult source and painted E comparison

Independent Blender REST bone readback is retained in `proportion-source-bones.py/log`. Adapted body worldZ span is1.810531917m. Shoulder jointZ1.4432137≈.797H; true upper-leg jointZ1.0369302≈.573H. Thigh/shin each.4818153m≈.266H; upper arm.2170078≈.120H, forearm.2356668≈.130H. Source Neck baseZ1.510533 to adapted crown1.810024 spans~.29949m≈.165H: this is a neck-to-crown anatomical proxy, **not exactly accepted chin-to-crown**. All figures refer to REST geometry, not camera canvas height.

Thus high shoulders/small cranial volume and long legs are concrete adult-source differences. In the accepted sprite shoulders lie around.675H above floor, compared with stock.797H; the gap is too large to solve by recolouring or changing facial expression. Leg bones account for~.532H before feet. Their proportion is a stronger rig diagnosis than a low clothing crotch.

PaintedE06 (cell229×286) has visible crown~49, chin~98, soles~274: head~49/225≈.218H, still materially below accepted~.284H. Shoulder~108–116, belt~151–162. Hanging upper arm projected~35–45px(.16–.20H), forearm~30–38px(.13–.17H), hand~13–18px. Those apparent lengths support the user's long-arm impression, but stride, camera depth and sleeve placement prevent converting them directly to3D bone scale. Passing/crouched crotch~190–205 is especially unsuitable for leg proportion measurement.

NativeE06 has crown~98 and lowest sole~535; face/chin is hidden by view/hair, so a reliable independent cranial head-height cannot be selected on that image. The REST3D proxy above is used instead. Gait silhouette height changes with knee bend, while depth contributes through camera foreshortening; neither a raw walking bbox nor canvas640/320 should define constant anatomical body height. Origin registration errors move the drawing; they do not explain a systematically small head relative to shoulders/limbs.

## Proposed3D trial targets, not an accepted new body

Use one total REST body heightH and compare an actual front/three-quarter/E neutral pose against accepted idle before rendering a batch. Trial head/chin-to-crown.25–.28H; shoulder joint height.68–.72H; belt~.49–.52H. True hip-joint height.44–.48H is an informed starting range, **not directly measured** from the baggy accepted trousers. Trial thigh and shin~.20–.22H each (roughly18–25% shorter than stock proportions), preserving plausible knees/boot placement. Enlarging the skull and redistributing vertical proportions is needed; adding longer hair alone does not enlarge the head.

Use skull/skin head width~1.05–1.20 shoulder span, with shoulder width~.20–.23H; hair may expand beyond it. Trial upper arm.11–.13H and forearm.10–.12H; hand~.055–.065H. Stock upper-arm ratio is already near that range, so do not blindly shorten every arm bone25% based on a projected E image. Check shoulder width/torso and projected hanging wrist at accepted proportions; forearm length, hands, posture and clothing can dominate perceived reach.

These targets are for a deliberately childlike stylized model, not real-child anthropometry. Retain identity/costume/one right-hip bag. Recompute retargeted contact after proportion edits: shorter legs change stride and reach, so the accepted old cycle cannot be promised unchanged merely by keeping action names. Preview a few key poses and one complete loop at136px; solve jerk/contact/registration separately. No per-frame image warping, mass generation or runtime activation follows from this draft contract. Shared with npc_facing and root for the source correction.
