# Sound effects provenance / rights

Selected original recordings © Kenney, CC0 1.0 Universal. Official sources verified 2026-10-17:
- https://kenney.nl/assets/impact-sounds
- https://kenney.nl/assets/interface-sounds
- https://kenney.nl/support confirms commercial use and no required attribution.
- https://creativecommons.org/publicdomain/zero/1.0/

Included untouched selected `.ogg` originals and original license texts reside in `originals/`. Processed files are resampled, filtered and faded derivatives; event-level source URLs/authors/license and processed SHA256 hashes are in `src/sound-manifest.json`. No ripped/game/movie source material or paid purchases.

The `original-*.wav` masters and synthesis in `scripts/audio-effects-build.py` are original Ruby Village contributions, dedicated under CC0 1.0 Universal (https://creativecommons.org/publicdomain/zero/1.0/). They contain deterministic generated noise, periodic oscillator textures, sparse synthesized birdlike chirps and soft harmonic chimes, not field recordings or third-party samples. All rights to these contributions are waived to the extent permitted by law; provided without warranty. This dedication applies only to these audio contributions, not unrelated repository code/assets.

Reproduction: the build script uses committed selected originals if already present; first acquisition only requires the two official Kenney ZIPs extracted at `/tmp/ruby-audio-download/{impact,interface}`. No complete unselected download is committed.
