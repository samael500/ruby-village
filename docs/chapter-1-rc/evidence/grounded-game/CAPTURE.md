# Actual grounded gameplay capture

Runtime: integration `6637b8c`, clean Vite build at localhost:5180. Layout1 and its matching legacy scenes remain active; final v9 scenes and residents are not certified by this capture.

All eight puzzles were played with real tray/rotation/cell/place/check inputs; six prologue frames were advanced normally. No layout injection. The script wrote `browser-report.json` with eight levels and no page errors. `gate-walking.jpg` is an actual frame at 18 seconds, not a mockup.

`chapter-playthrough-with-audio.mp4`: 182.464 seconds, H.264 + AAC, 27,779,036 bytes. Audio is the actual browser master graph captured during this playthrough, not a soundtrack added from separate files. `game-audio.webm` is preserved. The raw Playwright video remains locally under ignored `video/`; curated screenshots and the mixed MP4 are versioned.

The original wrapper exited 143 after gameplay assertions/report had completed, during audiovisual encoding. Encoding was rerun from the preserved raw video and browser audio with `ffmpeg -preset ultrafast -threads 2 -crf 30 -c:a aac -shortest`, exit 0; ffprobe verified both streams and duration. This is not recorded as a clean exit of the original combined command. Independent QA also completed its own exact-build run and audiovisual capture; see `qa/GROUNDED-RUNTIME-REPORT.md`.

This precedes the small result-background fix `5dc2036`, which independent QA separately retested on all eight landscape results. Physical phone, Safari, family playtest and subjective listening remain NOT RUN.
