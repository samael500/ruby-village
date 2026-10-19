# Independent atlas retry reproduction — #37 / #62

Reviewed source: integration commit `5a7672a`, `src/ruta-motion-view.ts:12–15`.

P2 reproduced in real Chromium: the cache retains an `Image.decode()` rejection. Two concurrent initial callers share one aborted request. After restoring network, two retry callers both reject without sending a new request. A fresh control image from the same endpoint decodes successfully as 2×2 pixels.

`before.json` records the actual browser outcome. `source-5a7672a.ts` preserves the reviewed source. `review.py` obtains the selected Git source, removes imports unused by the exercised function and compiles TypeScript with esbuild; cache/decode/prepare logic is unchanged. It runs real browser Image requests and decoding, not a mocked Image class.

Run from this checkout with `/tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/atlas-retry/review.py --ref <commit> --output <result.json>`; default repository supplies installed esbuild. This scoped function check does **not** certify full-game reentry, all scenes, a physical phone, or art acceptance. No runtime files were edited.
