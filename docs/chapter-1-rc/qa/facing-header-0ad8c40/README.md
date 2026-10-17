# Independent scoped review — checkpoint 0ad8c40

**Result: needs correction (F1).** Header and event-driven facing checks pass; actual mill arrival exposes a character overlap. This is not whole-RC acceptance.

Separate worktree `/tmp/ruby-qa-facing-0ad8c40`, branch `qa/37-facing-0ad8c40`, immutable baseline `0ad8c40`. Read repository AGENTS.md and coordination handoff. No source, runtime, art or coordinator worktree edits. `tsc --noEmit` and real Vite production build passed (70.4 MiB exports). Own server 5298 used because strict-port 5297 was occupied; 5180/5286 untouched.

## F1 — squirrel obscured at mill arrival

Reproduce with normal motion: reach mill with preceding five scenes completed, close intro, place the supplied production solution through tray/rotate/cell/Place, press Check, allow actual walk, advance arrival to Miller speaking. Screenshot `mill-arrival-5.jpg` and actual input video `mill-normal-motion-silent.webm` show Ruta partly covering the squirrel. Viewport 1280×720. Source `independent-edges.py` reproduces via real coordinate mouse clicks, without forced actions, layout injection, motion changes or skipped walking.

Scene-native coordinates: Ruta facing ne, feet (1356.9623,466.5), sprite viewport box (1298.6766,311.0714,116.5714,174.8571). Squirrel conversation-front feet (1330,405), image box (1284.4071,313.4071,90.8805,92). Miller conversation-left feet (1430,398), image box (1386.198,217.724,78.373,181). `mill-overlap.py` decodes actual sprite alpha at recorded runtime coordinates: 1,345 overlapping native pixels above combined alpha threshold 32; mask/JSON retained. Breathing subpixel scale is excluded from this rounded-native computation. Existing full-cell clearance only checks puzzle cells and does not detect this actor/actor overlap. Runtime owner has been notified; no attempted QA-side runtime fix.

## Passing scoped checks

- `resident-facing-runtime.py`: all 12 author state cases independently rerun (six resident scenes × desktop1280×720/landscape844×390). Intro, activity, replay, persisted reload, actual UI solutions, arrival dialogue and result resident presence. Stable native anchor transforms, expected authored view transitions, no page/resource errors. Author harness uses reduced-motion for arrivals and forced cell locator clicks; this does not certify motion quality.
- `resident-facing-clearance.py`: all 10 authored-view/scene alpha clearances pass against current legacy ground/water polygons. Limited to layout1; final layout2 needs repeat.
- `headers.py`: all 24 actual game cases pass (eight scenes × desktop1280×720 DPR1, landscape844×390 DPR2,740×360 DPR2). Painted plaque remains raster, title is live DOM text; titles/targets remain inside viewport, text does not overflow, no header-control overlap or resource errors. `header-contact-sheet.jpg` visually reviewed with full-frame samples; all eight names readable, medallion intact.
- `independent-edges.py`: deliberately holds authored resident image requests. Approved idle remains present while new PNG is pending, then authored view appears at the same anchor. Before/after screenshots retained. Moving the native mouse over the scene does not change facing; desktop→landscape→desktop preserves native anchors.
- Actual normal-motion mill solution completes, more than 20 distinct route-time samples recorded, arrival/result retain both residents. Script verifies reduced-motion is disabled. Silent video records actual browser input and walking; it is not a gait approval or audio capture.
- `geometry-audit.py`: independently compares all 12 observed arrival directions with vector from **actual rendered Ruta feet** to resident feet, selecting the nearest authored direction by dot product. All pass. Eight authored views declare no mirroring; measured runtime ancestor transforms have positive determinants. Normal walking has at most two resident view states (activity and arrival), without continuous facing tracking.

## Visual review and interpretation

Actual desktop/landscape meeting/activity/arrival frames were inspected for rabbit, teacher, baker, squirrel, miller and hedgehog. Rabbit remains by the garden table; teacher remains by the well; correct authored left/front views appear without CSS reflection. Enlarged screenshot crops of the small landscape rabbit and well arrival are retained; these confirmed visibility rather than relying only on DOM presence. Ruta turns toward the counterpart on meeting/arrival; stationary authored feet remain fixed through view changes. F1 remains a real visible composition failure despite the passing automated state/clearance assertions.

An initial independent direction estimate using scene metadata goal-center predicted post=e while runtime=ne. This was a QA measurement error: actual walking settles within the goal polygon, not necessarily at its center. Replaced the estimate with measured rendered feet; all twelve pass. No game fix is claimed for this diagnostic.

Physical phone, Safari/iOS and family playtest: **NOT RUN**. No audio listening or recording claim; WebM is silent. Art/layout2/road/gait remain pending outside this scoped review. Old gait is explicitly not artistically approved. No main merge or deploy performed.

## Reproduce

Build this immutable checkout and serve its dist at5298. Run copied `resident-facing-runtime.py` and `headers.py` with `RUBY_QA_URL=http://127.0.0.1:5298/ruby-village/`; clearance and geometry audit use local sources/evidence. `independent-edges.py` uses own5298 explicitly. All scripts and JSON evidence are alongside this report.
