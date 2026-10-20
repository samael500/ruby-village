# Independent targeted credits/source review

**PASS for the tested credits access, package and start-game scope**, frozen source `8bb08fbcb747ccc43cf8e24c8b627acb8d65b099`, actual production preview `http://127.0.0.1:5390/ruby-village/`. No source/runtime/asset edits, full8 or rebuild. Reproduce `review.py` with `/tmp/ruby-rc-tools/bin/python`.

Two fresh Chromium contexts (1280×720 and844×390) click the actual menu `#game-credits` anchor. It resolves under `/ruby-village/credits.html`, opens a separate tab with `_blank` and `noopener`; closing it preserves the original menu. Actual `#continue-game` starts the six-frame prologue, then real Skip enters gate dialogue. Screenshot proof retained; landscape credits text wraps without horizontal overflow and remains readable by scrolling. This tests clean-profile Start through the existing shared Start/Continue control, **not a separate saved-session continuation/migration run**.

Five local credits/license/source URLs return HTTP200 and byte-equal the built dist: credits page, full GPL text, music notices, sourceZIP and sound notices. Archive has exactly11 files: composer script, music notice, five MIDI, TimGM6mb.sf2 and three license/copyright texts. Every uncompressed entry is byte-identical to its repository path; per-fileSHA in `report.json`. No lossless masters, model or audio recording is included in the sourceZIP. Menu/start requests do not autoload the ZIP; explicit HTTP verification downloads it only for this audit. No observed page errors.

The page states declared music authorship/GPL2/TimGM copyright, KenneyCC0 and generated-effectsCC0, and links editable source plus project repository. This closes the previously reported absence of deployed accessible notices/source for the inspected snapshot. It is a source/package verification, not independent legal advice or a fresh artistic/audio acceptance.

Harness correction: first assertion expected menu to disappear immediately on Start; the actual modal prologue correctly leaves menu underneath. Corrected assertion requires the visible prologue, clicks Skip and then checks menu hidden. No game defect inferred from that first harness failure.

Limits: physical phone/Safari/family NOT RUN, no subjective listening, no gameplay beyond start/gate, no published-host/deploy verification. Temporary walking quality remains explicitly deferred by user, not silently marked accepted.
