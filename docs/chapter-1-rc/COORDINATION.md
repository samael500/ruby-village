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
Courtyard and Ruta artistic acceptance pending. Do not mass-produce unaccepted style. Continue independent work while awaiting review.
Physical phone, iOS/Safari and family playtest: NOT RUN; browser emulation does not satisfy them.
No RC claim until integrated browser playthrough, audiovisual evidence, independent QA and release checks.

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
