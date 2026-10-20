# #44 validation

Validated on Node 22.18.0, 2026-10-17.

- `npm test`: 58 pass, 0 fail. Eight real-engine reference solutions; minimum
  gate path requires every one of eight stones; bridges mandatory with dry ends;
  six directions and water/overlap/invalid-turn rejection; negative axial starts.
- Legacy fixtures from `add76709`: all eight former layouts, preserved completion
  and settings, selectively discarded new-water placements, replay inventory,
  corrupted/unavailable/quota-limited storage, repeated recovery and persisted
  migration, future layout rejection, unknown letter/prologue fields preserved.
- `npm run build`: TypeScript + Vite passed. JavaScript 81.36 kB (gzip 27.04 kB),
  CSS 16.01 kB (gzip 4.42 kB). These are bundle sizes, not all asset download sizes.
- `node --experimental-strip-types scripts/blender/export-chapter.ts --check`:
  all eight exact accepted geometry snapshots match; no files rewritten.
- `python3 -m py_compile scripts/blender/audit_chapter.py`: passed. Historical
  Blender audit not rerun against changed production hashes; see data-contract.
- `git diff --check`: passed.

Not run / acceptance dependency: browser with matching final #45 artwork,
physical phone, family test. Integration #46 and independent #37 own those
checks. The old-art build is not evidence of visual alignment. User-facing
recovery notices require the coordinator's main.ts integration of recoverSession.
