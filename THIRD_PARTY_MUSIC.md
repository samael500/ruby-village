# Music sources and redistribution

The five Ruby Village cues are newly composed for this repository by the Codex agent on 2026-10-17, not library music or another game's soundtrack. Score source: `scripts/music-compose.py`; editable MIDI, lossless FLAC masters and exact instrument source are in `art/audio/music`. All new score, MIDI and rendered music files in this change are offered under **GPL-2.0-only**, with the complete preferred editable form included. This is an explicit license choice for this distribution; it is not a claim that every recording made using GPL software or a GPL SoundFont automatically inherits GPL.

Instrument samples: **TimGM6mb.sf2**, Copyright 2004 Tim Brechbill; 2010 David Bolton; GPL version 2. The unmodified SoundFont and complete GPL-2 text are included. Keep attribution and license with redistribution; if distributing modified versions under GPL, include corresponding editable source and identify modifications. No NC/ND, subscriptions, purchases or ripped soundtrack material used.

Primary source URLs verified on 2026-10-17:

- https://packages.debian.org/sid/timgm6mb-soundfont — Debian package/source description and official copyright link.
- https://metadata.ftp-master.debian.org/changelogs/main/t/timgm6mb-soundfont/timgm6mb-soundfont_1.3-5_copyright — exact copyright retrieved successfully with curl; saved as `art/audio/music/licenses/debian-online-copyright.txt`.
- https://github.com/musescore/musescore-old/commit/90c33ef9d87b3f5ff92efd3b07d89eb455fb1fef — upstream source recorded by Debian.
- https://www.gnu.org/licenses/old-licenses/gpl-2.0.html — GPL-2 text (local complete copy included).

Rendering uses the installed FluidSynth shared library, not bundled with the game; encoding uses FFmpeg/libvorbis. Browser fetches only the Ogg cues, never MIDI/FLAC/SF2. SHA256SUMS records exact distributed files. This attribution should remain accessible from the game's credits alongside sound-effect attribution.
