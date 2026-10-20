# Current export resource check

Application baseline a2c774f, layout1. The export policy and browser harness are committed together with this report. This is preliminary release preparation, not final RC acceptance.

The Vite build plugin excludes archived/source-only browser assets from generated dist. Original files remain unchanged in public/art. Current motion folder and map folder come from the runtime entry paths; final layout2 selects matching v9 instead of legacy v6/v8, with the present menu background retained. Optimized character frames and fallback references are kept. Development resource access is unchanged.

Current generated package:61.8MiB,75.6MiB of archived candidates excluded; export-assets.json records every exclusion. Sixteen actual puzzle completions across1280×720/844×390, twelve prologue frames and both completed maps loaded with zero HTTP/request/page failures. Only real UI input is used; reduced motion was explicitly enabled through settings for resource coverage. This does not approve the current rejected gait or unfinished map/art. Final resources and the new atomic layout must repeat this check. Physical phone, subjective audio and family tests remain open.

Initial build-hook implementation used the wrong API for an empty directory; it failed before verification and was corrected to rmdirSync. The final production build and complete browser runs pass. No source asset was deleted.
