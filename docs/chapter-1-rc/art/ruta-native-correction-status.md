# Ruta correction checkpoint — 2026-10-20

Current acceptance: youthful painted appearance and head-registered E-pilot movement accepted. Image clarity/flicker remains rejected. Earlier checkpoints below are historical; do not promote rejected #77 or infer runtime acceptance.

| Work | Actual status | Owner | Evidence / dependency |
|---|---|---|---|
| Child proportion rest mesh + rig | Technical audit passed; art not accepted | proportion author, independent QA | `qa/retarget-b-e6ab193`; cold-open saved actions; source B a4215f55… |
| Authored face/hair | One Ellie CC BY4.0 candidate, native blue eyes/copper loose locks | npc_facing | `art/ruta-ellie-head-v1/layered-locks-pilot`; source topology/UV and matrices retained |
| Costume | Frozen v2 candidate; art not accepted | root | e18d727; source SHA bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706 |
| Boot laces | v1 defect reproduced; v2 corrected in rest geometry + skin weights | root, independent regression reproduced | `art/ruta-native-layered-style-v2/lace-check`: 48-phase max distance 42.065 mm before / 1.532 mm after; real E04 regression render |
| Export/pack | Fixed camera, Root, full canvas; fail-closed evaluation guards; actual v2 render/pack complete | compact_view_qa; independent stream_road_finish | exporter 24129ad / root de838ea; 19 negative/positive guard probes; actual pack still pending |
| First loop | 48 actual phases, 1.666667 s (28.8 fps); independent browser controls/anchor checks passed, visual closure being reviewed | exporter author, independent browser reviewer | new output `art/ruta-native-layered-walk48-v2`; actual delivery e70d049; old 17 frames explicitly rejected wardrobe proof |
| World distance curve | B experiment independently reproduced, final sole re-sampled; max curve path discrepancy 0.301 mm (author diagnostic) | curve author; npc_facing final-sole probe | `art/ruta-b-contact-forward-v1`, `qa/contact-forward`; no no-slip claim |
| Runtime | Unchanged, new character NOT enabled | root #46 | integration remains e32cad4 / PR55; new source PR78 is draft |

Next gate: independent visual loop closure → artistic review against accepted Ruta → six headings/cameras and actual game short/long/bridge/turn/stop checks. No per-frame raster warp, size fit or registration. Physical phone/family NOT RUN.

Separate worktrees/owners: head author `ruby-village-36-ellie-head`; exporter ` /tmp/ruby-ready-sprite-export`; independent QA `/tmp/ruby-export-pack-qa`; root costume/integration `ruby-village-36-ruta-render-style`. No concurrent runtime writes. Main is neither merged nor published.

## Runtime integration constraints (pending, not implemented)

- Do not fill native `start`/`stop-L`/`stop-R` clips with the rejected painted frames or freeze one pose while the actor translates. New source-native transitions and their contact behaviour require actual route review.
- Native Walk duration is 40/24 seconds; sample source phase and forward-distance curve from one continuous clock through headings. Old painted half-step assumptions and `.72` world distance are not evidence of native sole contact.
- A final-sole compatibility probe is necessary: costume tailoring/welding changed mesh IDs; raw B contact vertex IDs cannot simply be applied to the final model.
- The pilot intentionally retains the full 256×320 delivery canvas. A complete 24-atlas set (six headings × two camera variants × Walk/Idle48) would decode to roughly 377 MB (360 MiB) before other resources. Measure memory/loading before activation; an explicitly recorded single constant crop over the entire resource set could remove transparent margins without per-frame fitting, but is not implemented or claimed here.
- Browser landscape emulation is separate from a physical-device check. No promotion from static six-heading views to six-direction walk acceptance.

## Latest direction and painted experiment (2026-10-20)

Maksim: native 3D is better and the walk can serve as a pose base; now make illustrated sprite frames matching approved Ruta. Native appearance is not final art acceptance. Root used built-in imagegen for a12-pose style study, then full48. Exact prompts, ordered reference hashes, immutable raw PNGs and source sheets are in `art/ruta-native-painted-sprites-v2/`; independent static review in `qa/painted-native-style-v2/`.

Current painted baseline: c2e1d05 (author a983198), comparator-only revision88d4411 (author1a16d10). Preview `http://localhost:5311/art/ruta-native-painted-sprites-v2/packing/full48/review.html`. Shared measured raw grid origin(0,30), cells162×200,8×6; padded raw canvas1296×1230 preserves original1295×1215RGBA. Fixed asset-level similarity calibration is diagnostic, not certified physical Root/foot contact. Original raw outputs and every whole frame remain unchanged. Native comparison rebuilt exactly from actual48 source PNGs. Reference uses exact approved463×970PNG, now drawn at the native actor height/anchor instead of an unfair larger display.

**Open defect:** independent reviewer sees suspected upward pop39→40 (crown proxy17→9 rawpx). A blind last-row+8px shift is NOT authorized: raw crown47→0 is9→10px, so it could create a new loop pop. Paired pose16↔40..23↔47 shows shape differences as well as possible placement differences. Row compression is plausible but not proven to be a whole-block translation. Read-only Chest bow / hip satchel clasp landmark diagnostics are being collected to separate actual atlas placement from internal drawing changes. Do not register by crown/foot bounding boxes or silently warp frames. No smoothness/game/no-slip acceptance transfers from the native source.

Owners: root generation/raw/prompts/provenance; compact_view_qa fixed-grid packer/comparator in `/tmp/ruby-painted-native-pack` branch`art/36-painted-native-pack`; npc_facing static painted review and semantic landmark probe; stream_road_finish independent painted browser/jump audit. Gameplay/runtime still unchanged. Current work is a painted E-direction pilot, not all six headings or release acceptance.

## Painted temporal diagnosis and next candidate

Independent actual browser audit `36b90c6` (author f37a5fe) confirms visible39→40 upward pop with static draw destination, exact raw/atlas RGBA and all48 actual source rectangles. Controls, clock and decode pass; painted motion fails. Evidence is under `docs/qa/painted-native-walk48-browser/`, including corrected-reference repeat and actual silent videos. No acceptance inherited from native.

Read-only layout analysis `15cf2bf` finds no proven alternate shared row origin. Blind last-row+8 improves one crown boundary but damages47→0. Semantic probe then measured visible front clasp39→40(+2,−10)rawpx vs exact native(0,+0.0605), and partly obscured knot(+3,−10) vs native(−0.0735,−0.2825), within annotation uncertainty. These two upper-body features agree with whole-sprite displacement at that boundary; they do not prove internal pose deformation or a correct global last-row shift. Root's preliminary wide-step impression is not treated as a demonstrated phase error.

Next is a **separate metadata-only sprite-pivot trial**, retaining immutable raw whole frames, one fixed scale and the exact native Hips/clasp trajectory. Explicit per-frame translations are permitted as diagnostic sprite pivots derived from semantic points; this is a deliberate change from the baseline's one common translation, not a silent modification of the exporter or raster pose. No contour/bbox fitting, individual scale, limb warp or redraw is applied. Five occluded clasp phases need explicitly estimated pivots; their uncertainty is not certified. Bow points are held out for cross-validation. A pivot trial must be compared against baseline on all row boundaries and loop closure in actual browser video; it cannot certify correct anatomy, physical foot contact or game routes.

Root prepared but did not invoke another generation call: semantic evidence is being tested before potentially introducing new drawings. Baseline and native/game resources stay unchanged. Compact owns new trial pack/player, NPC owns semantic annotations, stream reviewer owns independent trial browser acceptance.

## User art acceptance; motion remains rejected

Maksim reviewed the semantic-pivot trial at5322: «Да, хорошо, почти идеально -- только изображение дребезжит и дёргается». **Illustrated appearance/style is accepted. Animation smoothness is NOT accepted.** Do not ask appearance approval again or change approved identity/outfit while fixing jitter. The current trial does not solve the user's motion complaint. Next diagnosis separates actual browser cadence, uncertainty/high-frequency pivot noise, whole-head registration and internal drawing/scale changes. No body/limb warp or source-pixel edit is authorized by this diagnosis. Runtime still unchanged; no game or release acceptance.

## Next motion candidates, not yet accepted

- Head-translation-only trial `34f8384` (author bb845ed): same raw48/fixed scale/clock, loop-constrained common-template registration plus exact smooth native Head trajectory. Root regenerated manifest without a diff. Frozen preview: `http://localhost:5311/art/ruta-native-painted-sprites-v2/packing/head-pivot-trial/review.html`. Author desktop/CDP touch controls pass; independent actual motion comparison pending. Lower-face correspondence remains imperfect, no physical-anchor claim.
- Independent eye-patch annotations `7a323fa` (46 visible / 2 null, approximate), author cross-check `d5ee2b8`: adjacent eye-minus-nativeHead vector RMS clasp2.307 vs head0.935 native-half px; seam5.055 vs1.742. These descriptive metrics have annotation/systematic uncertainty and partly shared image evidence; they do not prove user-visible jitter fixed. Native projected Head bone length varies by1.086 due to orientation, not growth.
- Isolated cadence study `ff5ee32` keeps cycle40/24s and phase-faithful source pixels; 48/24/16 unique phases are explicitly distinguished. No arbitrary reordering/blending or invented poses. Not a recommended setting until actual comparison.
- Bounded deterministic native shader fallback `751cacf` (three actual poses only) preserves source geometry/weights/rig/actions after cold open, but visibly does **not** match the accepted painted appearance. Kept as a study, not substituted for approved art and not expanded to48.

Current user motion verdict remains FAIL. Runtime still uses the previous set. No six-direction, in-game, no-slip, full-chapter or release acceptance is inferred from these studies.

## Latest user distinction: movement accepted, image flicker/blur rejected

Maksim on head+48: «да хорошо -- движения нормально, но само изображение МЕРЦАЕТ, и плывёт -- картинка не чёткая и дребезжащая». Preserve the accepted gait, phase, head registration and appearance. The outstanding complaint is rendered-image clarity/flicker, not another invitation to tune gait speed or pivots. The pilot is still not game/release accepted.

Actual Chromium baseline uses backing256×320 at CSS320×400 (and the same small backing atDPR2), ctx smoothing low. Source162×200 is first filtered to≈188×233 inside backing then compositor-upscaled. A same-frame controlled drawImage experiment shows lower gradient-energy proxy and stronger offset-dependent sharpness in two passes vs direct; this is evidence of a sampling contribution, not proof the compositor or all temporal art defects are solved. A separate DPR-aware single-pass renderer study is now assigned to NPC; stream independently checks it. Original pixels/clock/pivots stay frozen. Native transition inventory is complete, no new IK/actions/render were started; source five-direction pose batch continues independently.

## Image-quality checkpoint: renderer audited; larger source pending full-loop QA

Single-pass DPR-aware renderer `fb28719` was independently compared against the exact baseline (`6d8b991`, `docs/qa/painted-image-sampling/renderer-ab/`). Actual DPR1/2 browser recordings show moderately clearer detail, especially at DPR2, while the same internal hair/face changes remain. This is a verified sampling improvement, **not** a flicker fix or user acceptance. No gait, phase clock, raw source, registration or game runtime changed.

Four larger painted sheets now cover consecutive phases0..47 (`b811d63`, `d05eb76`, `art/ruta-native-painted-production-v1/`). Actual outputs are1295×1214/1215, not the requested2048×1920. Exact accepted pose excerpts, canonical reference, prompts, ordered inputs, immutable raw RGBA and provenance are retained. Independent static identity review `5e9906e` (`docs/qa/painted-hires-identity/`) finds no major age/identity/bag/whole-pose regression. It explicitly observes changing internal detail and does **not** establish temporal stability.

NPC owns lossless whole-frame packing and the separate full48 DPR preview; root owns source/provenance. One measured grid per source sheet, no per-frame resizing/warping, one global display scale. Full loop and quarter boundaries11/12,23/24,35/36,47/0 require independent actual browser review before recommending the larger source. Partial12-frame forward playback is not a full cycle. Existing accepted appearance/movement and unchanged runtime remain the comparison baseline.

## Frozen full48 larger-source checkpoint

`cd1d389` (author `3cd0973`) freezes all48 exact whole larger frames and the separate translation-only head trial. Preview: `http://localhost:5311/art/ruta-native-painted-production-v1/full48/review.html`. Original source pixels, ONE global scale and40/24s cycle preserved. All four measured grids fit; full atlas2640×2556, cells330×426 with identical transparent padding. Actual author desktopDPR1/2 and landscape844×390DPR2 controls/viewport checks pass. Independent temporal review is pending.

An important measured limit remains: held-out lower-face-vs-upper-head residual changes roughly(−3.267,−3.389)logicalpx at11/12 after rigid head registration. Larger source is visibly crisper on actual same-size screenshots, but whole-sprite translation cannot fix this internal disagreement. Do not call source flicker fixed. No game install or user re-approval of appearance.

Native guide batch completed separately in `b37e0a9`:240additional actual frames forSE/SW/W/NW/NE, plus existingE48; fixed source/camera/Root/height, lossless atlas readback and source before/after SHA preserved. These are technical pose guides, not six-direction painted art. No further native camera/Idle/transition renders started. Read-only stable-UV fallback feasibility is saved in `9c7249c`; it is unproven for accepted likeness and not a selected replacement.

## Independent larger-source temporal verdict

`7b1e4e2` (author `b80237a`) verifies frozen `cd1d389`/author3cd0973: actual desktopDPR1/2 and landscape CDP-touch844×390,4.2s simultaneous recordings,48low+48high actual draw calls per context, equal phase/scale contracts, no request/page errors, full actors within landscape viewport. Evidence: `docs/qa/painted-hires-temporal/`.

The larger source is substantially clearer at equal screen size; **flicker remains open**. Actual paused pairs/decoded sequences show lower face/fringe/shoulder-hair changes11/12 and satchel/local drawing changes35/36. No whole-actor zoom or gait failure is inferred from these local differences. Do not request appearance re-approval or present this as a finished image-quality correction. The frozen comparison is retained for inspection.

Next bounded work is a separate stable-UV-textured whole-3D-actor pilot (NPC owner, new worktree/art directory), materially different from the failed grain/outline study. First texture/UV constraints and only actual poses0/30/40 plus a front/three-quarter view; no48/six-direction expansion or runtime install until likeness is demonstrated. UV texture cannot fix silhouette/heading differences; those remain explicit potential blockers. Integration game remains e32cad4.

## User review of larger full48: improved, still rejected

Maksim: «лучше уже меньше мерцает, но картинка всё ещё дергается. "неизменная разметка" -- очень прыгает, "хед" -- немного дрожит.» Image-quality improvement is acknowledged; stability is still **not accepted**. Keep baseline only for diagnosis, retain head as the closer comparison. Do not retime gait or claim closure from DPR/packing checks. Stable-texture pilot continues in isolation.

Early derivative UV audit finds body/feet/trousers stock UVs are palette points (zero-area faces), despite UVMap existing. Genuine surface painting needs explicit derivative unwrap; native head/cap have usable area, repeated locks overlap across objects. No source geometry/rig/weights/Walk edits are authorized by this unwrap.
