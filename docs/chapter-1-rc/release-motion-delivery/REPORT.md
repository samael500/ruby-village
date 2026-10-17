# Issue 49 — motion RGB delivery experiment

Recommended optional delivery: `animated-v3`, WebP RGB quality94, alpha quality100, method6. Runtime paths are unchanged in this branch; the coordinator must explicitly connect the delivery.

The source v2 atlases already use an8×8 layout,1152×1728 pixels. There was no tall-texture defect to repair. V3 retains that exact layout and all source rectangles. Geometry, anchors, native height, stride, durations, foot-contact events, camera variants, source files and production-enable flag remain exact JSON equivalents, except delivery paths/compression metadata/status. Original v2 and source frames remain untouched.

| Encoding | Total atlas bytes | Change from source |
|---|---:|---:|
| Source v2 lossless RGB |9,339,468|—|
| Experiment WebP92 |4,918,458|−47.3%|
| Recommended WebP94 |5,422,838|−41.9%|

Decoded memory remains95,551,488 bytes for all12 atlases; max texture side remains1728. This saves download/storage bytes, not decoded GPU memory. Loading fewer camera variants is a separate runtime concern.

`encoding-audit.json` records12sourceSHA256s, both encoding experiments, exact whole-atlas alpha checks and1062manifest frame references (708unique frame rectangles). Every frame alpha is byte-identical, so foot silhouette/coverage is unchanged. Source/encoded manifest equality passes after normalizing only allowed delivery metadata. Conservative unweighted visible-pixel RGB measurement: worst atlas mean absolute channel error3.44/255, minimum PSNR30.29dB; pixels with tiny alpha count equally in this metric.

Actual Chromium compared all12view pairs at2× game display height and exercised an800ms walk cycle for900ms. `chromium-source-q94.png` shows two alpha backgrounds; `chromium-source-q94-same-background.png` compares identical backgrounds. Visual inspection found no new fringe or significant blur at that scale; existing source motion cutout shapes remain source properties. Browser console errors:0. This preview does not claim a physical-phone check or new artistic approval.

Reproduce: `python3 scripts/release-pack-motion.py`; serve repository root with `python3 -m http.server 5199 --bind 127.0.0.1`; run `/tmp/ruby-rc-tools/bin/python scripts/release-pack-motion-browser.py`. Runtime code, main.ts and source art were not edited. No remote push, merge or publication performed.
