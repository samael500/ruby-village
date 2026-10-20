# Independent atlas retry reproduction — #37 / #62

Reviewed source: integration commit `5a7672a`, `src/ruta-motion-view.ts:12–15`.

P2 reproduced in real Chromium: the cache retains an `Image.decode()` rejection. Two concurrent initial callers share one aborted request. After restoring network, two retry callers both reject without sending a new request. A fresh control image from the same endpoint decodes successfully as 2×2 pixels.

`before.json` records the actual browser outcome. `source-5a7672a.ts` preserves the reviewed source. `review.py` obtains the selected Git source, removes imports unused by the exercised function and compiles TypeScript with esbuild; cache/decode/prepare logic is unchanged. It runs real browser Image requests and decoding, not a mocked Image class.

Run from this checkout with `/tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/atlas-retry/review.py --ref <commit> --output <result.json>`; default repository supplies installed esbuild. This scoped function check does **not** certify full-game reentry, all scenes, a physical phone, or art acceptance. No runtime files were edited.

## Fix verification: `41f8c8c`

**PASS, scoped Chromium module test.** The harness includes the exact extracted `image-decoder.ts` dependency at the requested Git commit (hash recorded separately); no replacement decoder is injected. Two concurrent failures share the first aborted atlas request. Two simultaneous retry callers both succeed after network restoration, sharing exactly one fresh request. Two further callers reuse the successful decoded image without another request. The endpoint control also decodes. Raw outcome: `after-41f8c8c.json`; exact dependency: `decoder-41f8c8c.ts`.

Full-game reentry remains to be verified against the forthcoming frozen ordinary production build; this result alone makes no full-game claim.

## Actual game reentry verification

**PASS** on an isolated clean production build of `41f8c8c`, layout version 1, served bundle `index-BC1WQ_hQ.js` (port 5298). Real mouse UI enters gate with image requests deliberately aborted, observes `data-motion=load-failed`, restores network, opens settings, returns to the map, and enters the same level. Without a page reload, motion reaches `ready` and the six real atlas requests succeed. `game-reentry.py`, before/after screenshots and `game-reentry-41f8c8c.json` preserve evidence. A progress-only `introSeen=['gate']` fixture skips the unrelated prologue; no layout/win state is injected. This is a targeted retry test, not the forthcoming layout-2 full-chapter acceptance.
