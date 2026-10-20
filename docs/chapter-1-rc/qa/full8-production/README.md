# Independent ordinary-build chapter acceptance — #37/#62

**Executed on ordinary source `6108ec2`; see RESULTS.md.** No activation waiver or runtime patch belongs to this QA branch.

`review.py` starts two genuinely empty browser contexts (1280×720 mouse and 844×390 native CDP touch), plays the prologue, then all eight places in story order using real controls. Accepted solution JSON is a guide for inputs; placements are not injected. The test explicitly chooses select mode through settings and its native select control when needed; reduced motion remains off. It captures intro/replayed/arrival pages, reloads before placement, after the first piece and after the whole layout, checks saved layouts/progress, walks the actual route, captures distinct results, then the ending and completed map. It retains actual silent videos and browser/network errors. This is browser phone emulation, not a physical phone or family test.

`migration.py` is a separate legacy-session fixture in separate browser contexts. Its old stream solution and one now-illegal placement exercise visible migration, progress preservation, return-to-tray, version persistence and repeat reload. It never seeds the clean sequential run.

Run with `/tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/full8-production/review.py` and `migration.py` after building/serving the frozen ordinary snapshot on port 5298. Raw reports will record source HEAD, served scripts, viewport, saved state, screenshots and recording scope. Harness preparation is not a passing runtime result.
