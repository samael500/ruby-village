# Chapter 1 coordination — 2026-10-17

User authorized parallel implementation, draft PRs and local integration. No main merge or publication.

## Verified baseline
- main / origin/main: add76709d66ab6a138014886642f045e658f53bf.
- PR41 merged d7adcf9; PR42 merged add7670, source head 740012750bc427c41687cf04e692c9ec18766f4e.
- PR38 open, not accepted; production docs must be read from its branch.
- PR52 draft #44: af615983125eb3934d500980218220b10e7f2aef; reuse, do not duplicate.
- Accepted layout SHA256: 6baed82d3dea0e1b6472582751bcd0ccb9d41c872f50c9b865838b17e7b1cf6e. Metadata source head inside JSON describes annotation ancestry, not current PR head.
- Existing untracked candidates preserved; generated candidates are not accepted final assets.

## Ownership and queue
Four slots total including coordinator. Each executor has its own worktree.

| Owner | Worktree / branch | Files | Status |
| --- | --- | --- | --- |
| coordinator #46 | ruby-village / integrate/46-chapter-1 | main.ts, style.css, scene-camera.ts, scene-art.ts, integration docs | active |
| data_ui #44→48→47 | ruby-village-48 / feat/48-ui-prologue; reuse PR52 | chapter-ui.ts, prologue-staging.ts, own tests/docs | active |
| art_scenes #45 | ruby-village-45 / art/45-final-scenes | art/chapter-1-v9, public/assets/chapter-1-v9, art-v9 scripts, scene-v9.json | courtyard pilot |
| characters #35→36 | ruby-village-35 / art/35-characters | art/characters-v1, public/assets/characters-v1, character-animation.ts, own tests/docs | Ruta pilot |
| next available executor #50 | separate worktree to create | audio.ts, audio effects assets/manifests/tests | queued |
| next available executor #51 | separate worktree to create | music assets/source/cue sheet | queued |
| independent executor #37 | separate integration worktree | QA evidence/report only | after integration |

## Shared contracts
- Scene coordinates: 1672×941, camera/crop/origin from accepted engine export. Layers share exact canvas; no cover crop; alpha foreground and gate states separate. Manifest records source commit/hash, paths, anchors, camera and review status.
- Data/scene switch atomic. Staged #44 data must not replace production while matching final scenes unavailable.
- Character frame manifest: sourceRect/frameSize, foot anchor in native pixels, duration/loop, character/state/direction, native display scale, source/reviewStatus. Direction from projected path vector; no independent six-direction projection.
- Animation emits foot-contact(surface earth|stone|wood), never render-based step timer. Unaccepted sprites do not activate production walking.
- Audio: one AudioContext, master/sfx/ambience/music buses. Export createGameAudio(baseUrl, storage), unlock(), play(event), setScene(scene), setMusic(cue), setPaused(bool), setDucked(bool), setPreferences(patch), dispose(). Audio initialization only after gesture; failures never stop puzzle. Separate effects and music manifests, source URL/license/master hashes.
- Coordinator alone wires app events/settings/pause. Modules do not replace main.ts in parallel.

## Acceptance gates
Courtyard style, Ruta appearance, map drawing and residents/poses inclusion in integration review are explicitly accepted by Maksim. This does not waive geometry, motion or integrated runtime checks.
Physical phone, iOS/Safari and family playtest: NOT RUN; browser emulation does not satisfy them.
No RC claim until integrated browser playthrough, audiovisual evidence, independent QA and release checks.

## Handoff refresh — 2026-10-17

This supplements earlier checkpoints; historical pending statuses below describe their original commit, not current approvals. Live GitHub main remains `add76709d66ab6a138014886642f045e658f53bf`; PR41/42 verified MERGED again. Integration baseline before this refresh is `09bd4667dc00f872ea0c03975df99ce5fb429ef6`. PR38 remains open. No main merge/publication.

| Task | Actual readiness | Executor / exclusive files | Dependency | PR |
| --- | --- | --- | --- | --- |
| #44 | accepted layout2/migration tested; production still coherent layout1+legacy art | completed data_ui, coordinator production gate | matching audited #45 | #52 |
| #61 | defect located, implementation queued after cleanup | characters next, separate worktree; main.ts temporarily reserved | cleanup handoff | pending new task PR, integration #55 |
| #45 | all8 painted candidates staged; stream/mill geometry fail, wide and map architecture matching pending | art_scenes, ruby-village-45, chapter-1-v9 assets/scripts | accepted layout/hash; map is artistic reference | #56 |
| #35 | accepted portraits/poses active; full scene residents pending | source assets delivered; coordinator scene composition | safe scene anchors and one garden table | #54/#55 |
| #36 | full6 browser trial exists; final source normalization/knee caps rendering; production disabled | data_ui ruby-village-36-paint exporter/controller; characters ruby-village-36-parts masks only | cap handoff, final render/runtime QA | #59/#60 |
| #47/#48 | map/prologue/UI active; #62 scene hiding, stone scale, painted roads and per-scene results pending | coordinator modules/style, main wiring after #61 handoff | compatible scene assets and residents | #53/#55 |
| #50/#51 | recommended effects+music integrated, rights/sources retained | completed audio/music branches | final motion foot contacts and final mix QA | #57/#58 |
| #37 | earlier independent legacy-runtime pass; final pass queued | independent_qa, separate ruby-village-37 | all final production resources integrated | report in #55 |
| #49 | preliminary load audit only | coordinator then free executor | final #37/fixes | #55 |

Four real slots: coordinator + art_scenes + data_ui + characters. No additional executor is claimed. Prior worktrees are preserved; no author is relabeled independent. Exclusive main.ts ownership is temporarily handed to #61; coordinator works in separate modules/docs until its commit is integrated.

Integration order: preserve audited source/candidate commits inactive → #61 behavior → #36 final controller/assets → #45 complete geometry/map-reference audits → atomic layout2+matching art switch → scene residents/prologue/map/results wiring → final independent #37 → fixes → #49. Independent modules and source checks proceed in parallel. #62 is mandatory, tracked in ACCEPTANCE-61-62.md. Do not mark atlas presence or isolated rig tests as final game acceptance.

## Live checkpoint 2026-10-17 (after first integration)

- Integration PR55 is draft; #52 data, #53 UI, #54 Ruta, #56 scenery, #57 audio, #58 music remain separate review records. Nothing merged/published by this session.
- Ruta appearance explicitly accepted by Maksim; courtyard style explicitly accepted by Maksim. Acceptance is recorded in their reports/manifests; technical motion/game integration still require checks.
- #50 effects and #51 score are integrated: 29 processed effects/ambiences, four ~107s sampled-instrument loops and ending, shared graph with persisted music/sfx/mute, pause offset retained. Rights/source projects/masters committed.
- Active slots: characters → #36 rig/motion; data_ui → #48 painted map; independent_qa → initial #37 runtime audit. art_scenes queued for seven accepted-style scenes as next slot releases.
- Production retains matching layout1/legacy backgrounds behind explicit atomic gate. All accepted layout2 data/migration code are retained and independently tested. No new endpoints are painted over old scenery.
- Initial static production traversal: six prologue frames, all eight solutions through actual tray/rotation/cell/place/check clicks; no page errors. Evidence precedes final music/Ruta refresh; final audiovisual capture running.
- 71 tests pass before latest purely visual hookups; tsc/build pass. Independent review is in progress, not an approval of unfinished artwork.
- First independent finding: stale three-puzzle description in index.html, fixed to eight.
- Family/physical phone/iOS listening remain NOT RUN. Final art, villagers/poses, rig-polished walking, map/choreography and final QA/release remain incomplete.

## Subsequent production checkpoint

- Map artwork accepted explicitly and active in review runtime; six viewport labels/hit targets verified. Native touch drag/swipe, keyboard/restart/replay/reset/letter/reduced-motion checks independently passed. 74 unit tests pass.
- Mixed author walkthrough is 123.6 seconds of all eight legacy-scene puzzles with accepted Ruta and the recommended complete music/SFX. It is genuine browser video plus captured WebAudio, not an added soundtrack. Source and scope are in evidence/browser-report.json.
- Six residents, portraits and Ruta acting poses are delivered (d82566b; evidence745b077). Real composited JPGs verify alpha; native PNG viewer exposed hidden RGB and produced a false alarm, documented and corrected. Runtime activation is currently held: automatic approval review rejected it because these new resources remain review-pending, despite draft branch and explicit integration request. One bundled user approval question is pending. No bypass or publication.
- #45: six of seven new base paintings produced; forest and wide surrounds/layers pending. Coordinator overlay found stream water shifted into free cells; owner independently confirmed. Geometry corrections are required before activation; accepted style is not a geometry pass.
- #36: independent generative phase paint-over failed gait/registration; automatic repacking fixes position but cannot prove stance. Owner is testing rig-driven painted cutout mesh using the saved IK cycle, beginning with east. Technical or failed art remains separate from active sprites.
- Current executor slots: art_scenes final geometry/art; data_ui painted motion; characters optimized WebP delivery variants. Independent QA is queued for integrated final resources.
- #49 preliminary local build: ~64MiB exported, ~10MiB through first puzzle after deferring hidden illustrations; local FCP ~216ms is not a network/device benchmark. Original masters and SF2 are outside browser exports. Repeat after final resources and optimize delivery; not RC ready.
