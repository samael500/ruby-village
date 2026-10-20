# Native Ready/Ruta transition inventory — no new animation yet

**No ready source-native start/stop clips exist in this frozen file.** Cold read finds50actions:24 distinct original named clips,24 exact `.001` fcurve duplicates, and2 child-proportion adapted copies. Actual names/ranges/hashes/bone channels/slots are in action-inventory.json. The usable current pair is `Walk_ProportionProposal`0..40 at24fps (1.666667s) and `Idle_Neutral_ProportionProposal`0..50 (2.083333s). Run/Run_Back/Run_Left/Run_Right/Run_Shoot, weapons/hits/roll/kicks/punches and Interact/Wave are not authored locomotion start/stop clips. Original unadapted Walk/Idle names must not replace the proportion-adapted actions.

All probes open the original SHA bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706 without autoexec, perform no saves/renders and verify its bytes unchanged. New worktree branches from0f3d33a; only this directory is owned. No runtime/main/shared scripts are edited.

## Actual phase/sole findings

pose-contract-samples.json contains actual evaluated final-boot sole/heel/toe surfaces and bone endpoints at9Walk +5Idle times. Both idle soles remain at native minZ−.3555mm. Walk0 instead has sole minima L+30.83mm/R+14.69mm, Walk20 L+23.65/R+30.83mm. These are not flat planted idle/heel-strike joins. Walk0 Foot-bone heads differ from Idle0 by260.30/322.79mm; maximum bone-head displacement425.53mm at a finger reflects the arm-swing pose. An immediate switch cannot be justified by both actions existing.

Final-source480interval contact-inference measurements are reused by hash rather than duplicated: left confidence>.01 samples22..174 (phase.045833..3625), right262..413 (.545833..860417). This is an inferred min-z soft17.5mm-band candidate, **not physical ground-contact truth**. Neutral Idle is a real source pose/action, but no source clip bridges it to Walk. Pose0/.5 do not carry the old PR71 support meaning.

## Existing PR71 reuse

Read actual [PR71](https://github.com/samael500/ruby-village/pull/71), committed native transition docs/code at b3e5ec2. Their readonly copies are pr71-transitions-readonly.md and pr71-transitions-reference.py (reference only; **do not execute here**, it expects/writes an old MPFB tree). This is genuine native MPFB IK work, separate from older painted cutout exports. It already supplies useful principles: queue stop to a measured support phase; complete the shortened swing; settle with both feet planted; consume Root translation once; check actual skinned sole/render boots and carry clearance; retain action bundles/fakeusers and verify saved-file joins.

It does **not** provide drop-in actions for this Quaternius62-bone FK source. MPFB leg/thumb IK controls,0.5687545573m/720ms stride,360ms starts/stops and180ms settle are different authored contracts. Reusing those numeric constants or rejected painted body pieces would be wrong. Preserve the ideas and adapt their measurable interfaces, not the old motion/artwork.

## Bounded proposal only

transition-contract.json records a limited next probe; implementationStarted=false. Try one lead start+matching stop, source-only. Candidate join phases Walk5(.125,left low-sole window) or25(.625,right) are more grounded starting hypotheses than0/.5, **not validated optimal phases**. First400ms duration is an explicit engineering trial, not an already authored/accepted transition. A queue restricted to those two phases can wait up to.833333s; do not inherit PR71’s360ms queue bound.

On a copy, interpolate existing local poses with smooth quaternion/translation weights and solve the existing two-bone leg FK to hold a selected actual sole support point while the other foot finishes its swing. Derive root travel from the same support trajectory, never freeze a sprite and translate it. New actions may be created separately; original Walk, mesh, rest rig and weights remain immutable. Endpoint pose and one-sided velocity, full sole drift/floor uncertainty, Root/Hips/Head acceleration and bag/hand/body/boot clearance must be measured before a tiny E demonstration. No large render or new IK action has been started. No contact/no-slip or runtime approval is claimed.

Reproduce inventory.py and pose-contract-probe.py using Blender4.5.3 `--disable-autoexec --python-exit-code 1 -b -t 2 --python <script>`. Initial unsupported ActionSlot.name inspection was corrected to identifier before the successful inventory; output JSON is from the successful cold run, not guessed action names.
