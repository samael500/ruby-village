# Ruta correction checkpoint — 2026-10-20

Latest user acceptance: ready gait accepted; painted pilot rejected because adult/long-limb proportions and visible frame jerks. Do not promote #77. Correct proportions on the source rig and render whole sprites from one native actor.

| Work | Actual status | Owner | Evidence / dependency |
|---|---|---|---|
| Child proportion rest mesh + rig | Technical audit passed; art not accepted | proportion author, independent QA | `qa/retarget-b-e6ab193`; cold-open saved actions; source B a4215f55… |
| Authored face/hair | One Ellie CC BY4.0 candidate, native blue eyes/copper loose locks | npc_facing | `art/ruta-ellie-head-v1/layered-locks-pilot`; source topology/UV and matrices retained |
| Costume | Frozen v2 candidate; art not accepted | root | e18d727; source SHA bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706 |
| Boot laces | v1 defect reproduced; v2 corrected in rest geometry + skin weights | root, independent review pending | `art/ruta-native-layered-style-v2/lace-check`: 48-phase max distance 42.065 mm before / 1.532 mm after; real E04 regression render |
| Export/pack | Fixed camera, Root, full canvas; fail-closed evaluation guards; actual v2 render in progress | compact_view_qa; independent stream_road_finish | exporter 24129ad / root de838ea; 19 negative/positive guard probes; actual pack still pending |
| First loop | 48 phases, 1.666667 s (28.8 fps); not completed/reviewed yet | exporter author, independent browser reviewer | new output `art/ruta-native-layered-walk48-v2`; old 17 frames explicitly rejected wardrobe proof |
| World distance curve | B experiment independently reproduced, final sole compatibility pending | curve author; npc_facing final-sole probe | `art/ruta-b-contact-forward-v1`, `qa/contact-forward`; no no-slip claim |
| Runtime | Unchanged, new character NOT enabled | root #46 | integration remains e32cad4 / PR55; new source PR78 is draft |

Next gate: complete actual render → lossless atlas/alpha checks → real browser loop, desktop and landscape viewport → artistic review against accepted Ruta → six headings/cameras and actual game short/long/bridge/turn/stop checks. No per-frame raster warp, size fit or registration. Physical phone/family NOT RUN.

Separate worktrees/owners: head author `ruby-village-36-ellie-head`; exporter ` /tmp/ruby-ready-sprite-export`; independent QA `/tmp/ruby-export-pack-qa`; root costume/integration `ruby-village-36-ruta-render-style`. No concurrent runtime writes. Main is neither merged nor published.

## Runtime integration constraints (pending, not implemented)

- Do not fill native `start`/`stop-L`/`stop-R` clips with the rejected painted frames or freeze one pose while the actor translates. New source-native transitions and their contact behaviour require actual route review.
- Native Walk duration is 40/24 seconds; sample source phase and forward-distance curve from one continuous clock through headings. Old painted half-step assumptions and `.72` world distance are not evidence of native sole contact.
- A final-sole compatibility probe is necessary: costume tailoring/welding changed mesh IDs; raw B contact vertex IDs cannot simply be applied to the final model.
- The pilot intentionally retains the full 256×320 delivery canvas. A complete 24-atlas set (six headings × two camera variants × Walk/Idle48) would decode to roughly 377 MB (360 MiB) before other resources. Measure memory/loading before activation; an explicitly recorded single constant crop over the entire resource set could remove transparent margins without per-frame fitting, but is not implemented or claimed here.
- Browser landscape emulation is separate from a physical-device check. No promotion from static six-heading views to six-direction walk acceptance.
