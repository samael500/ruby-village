# Resident facing runtime checkpoint

Sources: PR67 / 200b1c0; integrated as4f97ea6. Runtime source and these captures belong to this checkpoint commit.

Twelve actual Chromium desktop1280×720 / landscape844×390 runs: all six scenes, six residents, intro, activity, replay, persisted reload, actual UI solution placement, arrival dialogue, result resident presence. All anchors remain equal across states; resource/page errors zero. See report.json and screenshots. Ten full-alpha ground/water clearances in ../runtime-clearance.json apply to current legacy layout only.

Reduced motion enabled through settings before solution checks: this validates view/state behavior, NOT gait quality. Physical phone/family NOT RUN. New authored views retain original idle fallback until image decoding succeeds; appropriate front views exist only for Teacher/Squirrel. No CSS mirror or anchor mutation. Independent review and accepted-layout2 repeats pending.

## F1 follow-up

Independent source10c5291 (integrated25fcc96) found1345 alpha pixels where Ruta hid the mill Squirrel. The mill Squirrel now waits at1530,450 on dry outer ground beside the cart, rather than1330,405 directly behind the arrival goal. Activity and meeting use a genuine left view toward the actors. The root checkpoint repeats all12 state runs and10 alpha clearances; both mill viewport captures now show separated figures and strict Ruta viewport/Squirrel image boxes have zero overlap at first arrival speaker. These two zero-box checks use the actual clipped frame viewport attributes transformed via the parent CTM: SVG getBoundingClientRect can include the uncut atlas children and is not a valid viewport measurement. Independent correction review still pending, all later speaker pages and normal motion to repeat. Final layout2 anchor audit is separate.
