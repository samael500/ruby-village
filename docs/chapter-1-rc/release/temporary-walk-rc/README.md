# Chapter 1 review candidate — temporary walk

Production source: **8bb08fbcb747ccc43cf8e24c8b627acb8d65b099**.
[Integration PR #55](https://github.com/samael500/ruby-village/pull/55), Issues
[#43](https://github.com/samael500/ruby-village/issues/43),
[#37](https://github.com/samael500/ruby-village/issues/37),
[#49](https://github.com/samael500/ruby-village/issues/49),
[#62](https://github.com/samael500/ruby-village/issues/62).
Later evidence/documentation commits do not change this frozen runtime.

Local production preview: http://localhost:5390/ruby-village/ . No main merge or
publication has been performed. This is a candidate for Maksim's review, not a claim
of physical-device, family or final artistic approval.

**Ready for review within the documented temporary-art scope.** Independent final
desktop and landscape runs both completed all eight scenes; no new functional
blocker was reproduced. Tested runtime remains8bb08fb after documentation updates.

## Scope and temporary animation

All eight illustrated layout2 scenes, connected roads/bridges, residents, staged
prologue, map, scene-specific results, saves/migration, music and effects are active.
Maksim permits temporary walking: «сделай хоть какую анимацию походки — это мы исправим
потом». The existing `animated-v3` set stays installed: six directions, 16 walk phases
per direction, 800ms cycle. Knee/cut defects are explicitly deferred; no final
character-art or no-slip approval is inferred. Native appearance experiments are
not enabled or included in the playable export. See the [asset audit](../../qa/temporary-walk-assets/README.md).

The release audit found music notices inaccessible in the export. The frozen fix
adds a menu link, static credits, the GPL text and an optional editable music-source
download. The archive is not automatically loaded by gameplay. Its eleven entries
match the score/MIDI/instrument/license originals; no lossless masters are included.
[Independent credits review](credits-review/README.md).

## Checks and evidence

- Fresh separate checkout, fresh npm cache, locked `npm ci`; Node v24.15.0.
- 90 application tests plus 6 route-planner tests: **96 PASS**, zero failures.
- TypeScript and clean Vite production build: **PASS**. [Build log](build.log), [TAP](tests.tap).
- [Independent landscape full chapter](../../qa/final-temporary-walk/landscape/README.md):
  clean profile, native CDP touch 844×390, eight actual UI solves/walks/dialogues/
  results/replays/reloads, final map; zero page/HTTP errors. This is emulation.
- [Independent desktop full chapter](../../qa/final-temporary-walk/desktop/REVIEW.md):
  eight actual mouse-input solves, normal start/walk/turn/stop, dialogues, results
  and earned-save reloads; zero page/HTTP errors. Both full runs total16 routes.
- [Independent save/input regression](../../qa/final-temporary-walk/placement-save/README.md):
  legacy migration/reload, mouse/touch invalid release → rotate → auto-place,
  composite/bridge ownership, cancel/undo/reload and native touchCancel.
- [Eight actual result screens](eight-results.jpg); [original screenshot hashes](eight-results-sources.json).
- [Both installed bridges](../../qa/final-temporary-walk/bridges/README.md):
  desktop/landscape clean frames and exact water-polygon overlays; dry/water/dry
  terrain ownership verified with no geometry or camera shifts.
- [Actual audiovisual movement, pause and reduced motion](../../qa/final-temporary-walk/targeted/REVIEW.md):
  [gate](../../qa/final-temporary-walk/targeted/gate/actual-audio.mp4),
  [stream](../../qa/final-temporary-walk/targeted/stream/actual-audio.mp4),
  [mill](../../qa/final-temporary-walk/targeted/mill/actual-audio.mp4).
  These contain actual captured WebAudio; pause freezes the route clock and resume
  reaches victory. Reduced motion intentionally uses a still and completes.

Full-chapter videos in the landscape report are silent; audio evidence is recorded
separately and must not be inferred from them. Full chapter tests enter known
solutions through the actual UI; they are not uncoached family playtests.

## Package and reproduction

[Package manifest](package-manifest.json) records every exported file, SHA256 and
archive digest. Export: **114,346,714 bytes**, 148 files (about109.0MiB).
The optional5.58MB source archive contributes to total package size, not initial
gameplay transfer. The build excludes128.9MiB of archived candidates. This is static
file accounting, not measured browser RAM or WAN/physical-phone performance.

Local archive: `/home/mskorokhod/life/ruby-village-rc-8bb08fb.zip`.
SHA256: `02cf3876c2ad861c69c8f5f96beab9a8c5860219f2b0a1b6e54c853f0fa9020d`.
It contains a `ruby-village/` directory suitable for an ordinary static HTTP server.

```sh
git checkout 8bb08fbcb747ccc43cf8e24c8b627acb8d65b099
npm ci
npm test
node --experimental-strip-types --test scripts/character-paint-route-planner.test.ts
npm run build
npm run preview
# Open the printed URL with /ruby-village/.
```

## Outstanding human review and limits

- Temporary knee/cut defects and final character animation remain in #36 for later replacement.
- Maksim's review of the integrated scene/bridge presentation is still required.
- Physical landscape phone, physical Safari audio interruptions and family comprehension: **NOT RUN**.
- Human listening to every full music loop twice: **NOT RUN**; captured audio and automated checks do not replace it.
- Mouse OS-generated pointercancel was not reproduced; native browser touchCancel was.
- Historical local load/frame-cadence measurements remain scoped to their original
  checkpoints; no new physical-device RAM/FPS guarantee is made here.

## Rollback and publication

Main remains `add76709d66ab6a138014886642f045e658f53bf`. There is nothing to roll back
on the published site because this branch has not been merged/deployed. For local
review rollback use the earlier `e32cad4` checkout; it has the same temporary motion
and gameplay but lacks the new credits delivery. Keep saved progress before resets;
layout2 migration is documented in the save/input report. The final merge, Actions
and published-site smoke require Maksim's separate authorization.
