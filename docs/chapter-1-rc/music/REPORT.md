# #51 recommended music suite

Branch feat/51-music, base add7670. One original score family, no external soundtrack. See THIRD_PARTY_MUSIC.md for exact source/rights and complete license files. New compositions/rendered assets are explicitly GPL-2.0-only with editable source, independent of questions about GPL sample output.

## Cue sheet

| Cue | Duration | Scene | Arrangement |
|---|---:|---|---|
| village | 106.667 s | menu/map/early prologue | flute, nylon guitar arpeggios, acoustic bass, harp, soft strings |
| day | 106.667 s | gate/garden/well/bakery/post | quieter lead with breathing space, sparse vibraphone |
| water | 106.667 s | stream/mill | pan flute, harp and celesta, alternate phrase order |
| evening | 106.667 s | forest/final anticipation | lower clarinet register, related harmony, restrained music-box accents |
| ending | 17.333 s | chapter ending only | shared opening motif, tonic cadence and natural release |

Tempo 108 BPM, 3/4, D-major/B-minor harmonic family. Main cues have 64 bars: A, supported A, lower-register B, returning A; lead phrases have rests and two-bar answers. Distinct sampled instruments, dynamic variation and layering are used; this is not a loop of a few synthetic sine tones. The suite is recommended as one set, pending actual listening review in the game.

Main loops render three complete cycles through the same synth state and export the third, retaining preceding instrument/reverb tails. A 4 ms boundary fade protects against sample discontinuities without changing loop duration; no silence padding is inserted. Ending is not looped. Masters: stereo FLAC 32 kHz/16-bit; game: stereo Ogg Vorbis quality 3. Manifest API agreed with #50; gain .65 is multiplied by the common music preferences/master bus. No independent AudioContext/settings introduced.

## Reproduction

```
python3 scripts/music-compose.py
python3 scripts/music-normalize.py
python3 scripts/music-verify.py
```

Requires Python3 standard library, libfluidsynth.so.3, ffmpeg with libvorbis/libmp3lame. SoundFont source is included. Optional MUSIC_CUES=evening,ending selects a subset. Rendering is deterministic at score/event level; FluidSynth version may affect exact audio/reverb, so SHA values describe this rendered delivery rather than guaranteeing cross-version bit identity.

`analysis.json` decodes actual game Ogg files, records duration/peak/RMS, checks finite samples and compares the repeated boundary step against ordinary sample steps. The same boundary occurs on both repeats of a three-copy concatenation. `*-seam-preview.mp3` contains the seven seconds before/after each seam for direct listening. These signal checks are not represented as human listening.

## Remaining validation

**Not yet done:** perceptual listening through two cycles, listening approval of instruments/composition, final mix in the actual game, full menu→prologue→day→water→evening→ending recording, mobile speaker/headphone checks. The available agent environment provides file synthesis/analysis but no reliable auditory perception; do not mark this acceptance checkbox passed from FFmpeg metrics. Integration #46/#50 must check autoplay/mute/ducking/pause/background and cue persistence. No real phone or family test claimed.

Technical checks in this branch: 51/51 existing tests pass, TypeScript noEmit and Vite production build pass. Manifest validates all five existing files and ending loop=false. Game exports total approximately 4.9 MiB; lossless/source bundle approximately 31 MiB. Browser does not fetch that source bundle.

Final decoded RMS levels are approximately -24.44 to -24.53 dBFS; maximum peak is -3.69 dBFS (ending). Main-loop boundary steps are 0.00021–0.00104 full scale after the 4 ms protection, below normal musical sample differences. This confirms signal integrity, not perceived musical quality.
