# #50 recommended effects / ambience set

One recommended local set: warm Kenney CC0 recorded taps, softened impacts, paper/cloth-like foley and three variants of each earth/stone/wood step. Original synthesized short chime/victory and five low-level twelve-second beds cover all eight scenes. The bakery is a quiet low wooden-room texture, water is gently turbulent, village/forest/leaves include sparse birdlike phrases. These are generated ambience, not field recordings. No voice, punitive buzzer, hover sound or step metronome.

## Integration API

`createGameAudio(import.meta.env.BASE_URL, storage)` returns unlock, play, setScene, setMusic, setPaused, setDucked, setPreferences, dispose and read-only snapshots preferences/metrics. Only `unlock()` creates the single context; invoke directly during a meaningful click/touch (do not await unrelated work first). Call it on later gestures too so interrupted contexts can resume. play returns an awaited-safe promise; effects before gesture or during pause are dropped, not queued.

SoundEvent is exported: ui-click, modal, dialog, tile-select/place/rotate/return/reject, check-incomplete, path-connected, victory, gate-open, paper, basket, stone, foot-earth/stone/wood. No hover. Foot events only at #36 foot contacts. Basket/gate/paper only when corresponding visible action exists; unsupported choreography remains unwired, not represented by timers.

`setScene('gate'|'garden'|'well'|'bakery'|'stream'|'mill'|'post'|'forest'|null)`; null stops ambience. `setMusic('village'|'day'|'water'|'evening'|'ending'|null)` uses lazy optional `assets/audio/music/manifest.json` with `{version:1,cues:{name:{file,gain,loop}}}`; file relative to music directory. Absence/fetch/decode failure safely skips sound. One master/sfx/ambience/music graph, no second context.

`setPaused(true)` for pause or portrait; false when both resolved. Document visibility is handled separately inside module so visible-page events cannot unpause a game paused by UI. Pause immediately frees sources and invalidates in-flight effects. Scene changes discard old footsteps; latest scene/cue wins async races. Switching/replaying same scene does not duplicate loops; transitions fade and old transition tails are bounded. Eight simultaneous effects maximum, per-event rate limit, cyclic step variants. `setDucked(true)` during dialog lowers ambience/music, retains UI. Do not send the same click both globally and in its handler.

`preferences` defaults: muted=false, music=.35, sfx=.65, master=.7. Controls: master mute plus numeric [0,1] music/sfx, ambience tied to sfx. Persisted before unlock in `ruby-village:audio:v1`; malformed/denied storage safe. Keep textual gameplay feedback regardless of mute. `metrics` gives played/dropped/loadErrors, activeVoices, cachedFiles, unlocked/paused/contextState for independent QA.

## Rebuild / rights / checks

`python3 scripts/audio-effects-build.py` requires ffmpeg and uses committed untouched selected recordings plus seeded original synthesis. Ogg Vorbis mono 24 kHz, high/low pass on foley, short edge fades; ambience master starts/ends at zero with 300 ms fades for click-free loops. Quiet beds are not normalized to foreground effect loudness. See art/audio/sfx/THIRD_PARTY_NOTICES.md and included licenses. Manifest has per-event provenance/gain/loop and processed file hashes.

Mock tests cover gesture gate, one context, persisted settings, throttling, pause/resume, in-flight cancellation, failed devices/fetch/storage and disposal. They do not replace browser listening. Runtime wiring belongs to #46. Final mix/listening, two-to-three-minute real production gameplay recording with music, autoplay/background/portrait browser checks, actual iOS/Safari/phone and family test remain pending integration and independent #37.

Verified 2026-10-17: 54/54 full Node tests, TypeScript, Vite build, diff check. Asset audit decodes 29 delivered Ogg files, verifies hashes, rejects clipping and checks ambience endpoint samples; measurements committed in asset-audit.json. Initial processing revealed a clipped interface sample: disabled limiter auto-gain and added headroom before final export.

Real Chromium 156 WebAudio smoke passed: actual Ogg decoding at the repository base path; eight scene changes, bounded looping voices, persistence, null scene stop, pause/resume and gesture gate, no page/load errors. Music pause test uses the actual water Ogg as an explicit fixture cue, not the #51 score. Both atmosphere and music restart their source at the preserved elapsed playback offset after pause; unlock cannot bypass pause. browser-smoke.json records scope/metrics. chromium-module-smoke.webm is an audio-only capture of this real WebAudio graph, **not a production gameplay video or final-mix acceptance**. Re-run `/tmp/ruby-rc-tools/bin/python tests/audio_browser.py <vite-url>` with Playwright installed.
