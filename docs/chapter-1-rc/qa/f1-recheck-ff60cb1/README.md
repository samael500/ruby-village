# Independent F1 correction recheck — ff60cb1

**PASS: F1 corrected in this immutable checkpoint.** This is scoped character-composition QA, not whole-RC acceptance.

New separate checkout `/tmp/ruby-qa-f1-ff60cb1`, branch `qa/37-f1-ff60cb1`, created directly from `ff60cb1`. Read repository AGENTS.md and current coordination. Production TypeScript check and real Vite build pass; own production HTTP server5298, no changes to user5180 or coordinator5286. Only QA scripts/evidence/report added.

`recheck.py` independently completes the actual mill solution through visible tray/rotate/coordinate-cell/Place/Check input at **1280×720 and 844×390**, with reduced-motion disabled. It does not inject a solution/layout, force clicks or skip the normal route. Each case captures both intro pages, activity, both story-replay pages, persisted reload, **all three arrival dialogue pages** (Ruta, Miller, After victory) and result. Two silent videos record real input and normal walking. The existing gait remains unapproved; no motion-quality acceptance is implied.

At every captured state the Miller remains at native(1430,398), squirrel at native(1530,450); images remain opacity1 and anchors do not change with dialogue pages. Arrival shows authored squirrel conversation-left; Miller remains visible. Ruta's measured feet-to-Miller direction selects ne, matching observed ne on every arrival page. Actual desktop and landscape arrival and result frames were visually inspected: the squirrel is now clearly separated from Ruta, and Miller is still present. Result preview retains both residents.

The pairwise measurement uses **nested Ruta SVG viewport x/y/width/height with its parent screen CTM**, and actor image x/y/width/height with its own screen CTM. It does not use the parent SVG bounding box, which includes atlas children. The full clipped viewport rectangles are strictly disjoint on every arrival page and on the board behind result: intersection0. This stronger rectangle separation guarantees zero visible alpha intersection. At Miller's arrival page horizontal gaps are approximately53.10 desktop and28.49 landscape screen pixels (exact boxes in report.json). Result-clone separation is additionally visible in the result screenshots; the cloned scene retains the same actor/viewport transforms and positive common fit.

`clearance.py` independently repeats all10 full-alpha authored-view clearances against accepted current legacy ground/water polygons; all pass, including both squirrel authored views at the new mill anchor. No logical level data or camera was changed by this work. These clearances certify legacy layout1 only; repeat after final layout2/art switch.

Artifacts: report.json includes every measured page, source scripts alongside; full screenshots show each state; `mill-normal-1280-silent.webm` and `mill-normal-844-silent.webm` are actual input/walk captures. No page errors. Original failing F1 evidence remains preserved in the prior checkpoint report.

Final art, connected road, MPFB gait and atomic layout2 integration remain pending. Physical phone, Safari/iOS, family playtest and audio listening: NOT RUN. Videos are silent. No main merge/deployment.

Reproduce: build this checkout, serve dist at5298, run `/tmp/ruby-rc-tools/bin/python docs/chapter-1-rc/qa/f1-recheck-ff60cb1/recheck.py` and `clearance.py` from repository root.
