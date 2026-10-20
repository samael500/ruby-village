# Independent UI follow-up review — #48 / #79

Reviewer did not author the runtime changes. Read AGENTS.md and reviewed current diff plus `src/ui-miniatures.ts` at working tree `/home/mskorokhod/life/ruby-village-ui-followup`. Tested dev server http://localhost:5392/ruby-village/.

## Result

No blocking findings in the reviewed UI scope.

- Chromium desktop 1440×900: actual mouse clicks.
- Chromium emulated landscape 844×390 and 740×360: actual Playwright touch taps, not physical devices.
- Opened all eight level scenes at each viewport (24 entries). Asserted exact “Уровень N из 8”, progress within viewport, no horizontal text overflow, corresponding distinct painted miniature visible. Captured each actual scene.
- Examined actual stream screenshot, short-screen Adventure dialog and contact sheet of eight actual miniature captures. Progress foreground rgb(80,57,35), background rgb(255,242,217); legible and stable in reviewed screenshots.
- Opened Adventure, confirmed no sandbox action, ending and invitation visible after progress completion. Actual click/tap opened both narrative dialogs, invitation title identifies the letter. Both entries show artwork and type subtitles.
- Reload retained 8/8 progress in all three contexts. No page errors in these runs.
- Separate genuinely fresh browser profile: ending and invitation hidden; restart disabled; sandbox absent.

## Scope limits

Completed progress was seeded into localStorage solely to access all existing scenes and unlocked Adventure entries. This is not a full chapter solve, a migration test, physical-phone test, or audio review. No runtime or git changes were made by reviewer. The checked author changes were uncommitted during this review; parent must associate resulting commit with this snapshot.

## Evidence

`results.json`: per-scene viewport/progress bounds/colors and dialog/reload results.
`{1440,844,740}-{gate,garden,well,bakery,stream,mill,post,forest}.png`: actual scene screenshots.
`{1440,844,740}-adventure.png`: actual completed Adventure dialogs.
`740-fresh-adventure.png`: genuinely fresh profile dialog.
`miniatures-contact.jpg`: enlarged crops from the actual 844-wide scene screenshots, for comparing all eight landmarks.
`check.py`, `extra.py`, `contact.py`: review scripts.
