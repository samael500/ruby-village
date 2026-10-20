# Chapter 1 data contract — layout 2 (#44)

Base: main `add76709d66ab6a138014886642f045e658f53bf` (PR #42 merged).
PR #41 and #42 are merged; their accepted geometry is frozen in
`docs/blender-chapter-1/layouts/engine/*.json`. Historical correction source:
`art/blender/chapter-layouts/layout-adjustments.json`.

This branch depends on #45 and #46. **Do not merge or publish it alone**:
its updated endpoints and river cells require the corresponding new artwork.
Production build currently contains legacy artwork and is not an art acceptance.

## Geometry

All 77 cells of every scene, full projected polygons, terrain, endpoints, camera,
piece shapes and accepted placements must match the frozen engine exports.
`node --experimental-strip-types scripts/blender/export-chapter.ts --check`
is read-only and checks those fields for all eight scenes. Default export writes
current production data; it no longer applies historical corrections twice.
A full Blender rebuild after such an export is required to refresh source hashes.
Existing PR #42 `.blend` sources deliberately retain their historical input hashes;
rerunning the strict audit without rebuilding reports stale inputs, not a geometry failure.
The river negative control now reverses the historical corrections explicitly,
independent of whether current production already contains layout 2.

The five starts (-1,6) are valid in the existing offset grid. Gate goal is (7,6),
with exactly eight distinct single stones. Stream water moves (5,2) to (6,2);
mill (1,4) to (2,4). The bridge middle has opposite adjoining water cells,
ends are dry and neither level admits a dry bypass. Other rules remain unchanged.
Cameras are exactly those accepted in PR #42; no new calibration is introduced.

## Persistence and integration API

The storage key and envelope `version:2` remain compatible. `layoutVersion:2`
is written by `saveSession`. Missing or `1` means legacy placement validation.
`CHAPTER_LAYOUT_VERSION` is exported from `src/session.ts`.

`recoverSession(storage, completed)` returns:

- `session`: sanitized session or null;
- `notice`: Russian recovery message or null, for a nonblocking UI notice;
- `discarded`: removed placement IDs, returned to the inventory automatically;
- `migrated`: whether a valid session came from a pre-layout-2 record.

`loadSession` is a compatibility wrapper returning only `session`. Integration #46
should use `recoverSession` and present its notice, then persist using `saveSession`.
Recovery itself is read-only and repeatable. Persisting stamps layout 2; subsequent
loads preserve the same layout. Unknown future layout versions reset only the
current road and report a notice. Unknown/invalid placements are individually
removed, checked against water, endpoints, rotations and overlap by the real engine.
Gate-8 comes from the canonical inventory, never appended to saved placements.
Completed roads remain completed even if their former solution no longer wins;
replay uses current data. Preferences, prologue/letter and unknown envelope fields
are preserved by progress writes. No storage clearing is used. Failed reads are
reported; failed writes return false for the existing storage-warning UI.
