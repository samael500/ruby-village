# Independent source/export audit — temporary-walk RC

Frozen input `/tmp/ruby-final-rc`, commit **fbd4d19ad4778a1a334d1f225bf94d771b3cb46b**. Only this new docs directory changed. This is source/existing-package inspection, not a new build, browser test, legal opinion or final release acceptance. Parent already ran npm ci/TS/Vite successfully; those expensive/network steps were deliberately not repeated.

## Actual commands and reproducibility

- `git rev-parse HEAD` → frozen commit above.
- `/home/mskorokhod/.ya/tools/v3/14019382748/bin/node --version` → **v24.15.0**.
- `PATH=/home/mskorokhod/.ya/tools/v3/14019382748/bin:$PATH npm --version` → command not found in this shell. This is a local tool PATH limitation, not a project build failure; coordinator's existing npm/build result is not replaced by an invented independent run.
- `python3 docs/chapter-1-rc/release/temporary-walk-rc/source-audit/audit.py` → `report.json`: complete dist file hashes, source reference hashes and existing export report. Script reads only source/dist; it does not call the pruning function, which mutates its output.
- Read `README.md`, `package.json`, `package-lock.json`, `vite.config.ts`, `.github/workflows/pages.yml`, `scripts/release-export.mjs`, audio notices/manifests and actual generated `dist/index.html`.

## Findings

| Check | Result | Evidence / limit |
|---|---|---|
| Documented Node floor and commands | PASS source consistency | package engines `>=22.18.0`; README22.18+, CI setup-node24; scripts dev/test/build/preview exist. `build` explicitly runs `tsc --noEmit && vite build`; tests use native strip-types. No dependency install/new build run here. |
| Vite base / production entry | PASS static | config `/ruby-village/`; generated HTML script/CSS links both have that prefix and actual files exist. Published-host HTTP behavior remains separate. |
| Chapter2 absence | PASS documentation | README explicitly says chapter2 unimplemented; no claim a second chapter was added. Functional ending verified elsewhere, not re-executed here. |
| README current behavior | NEEDS FIX, coordinator already editing | Frozen README incorrectly says no audio, static Ruta/wheel, and invalid drag returns; v6/v8/Blender sections read as current. Root explicitly owns current prepend/historical labels/invalid-preview correction. This audit does not edit README or verify a not-yet-frozen replacement. |
| Active resource selection | PASS inspected export | layout2; motion `characters-walk-v1/animated-v3`; map `chapter-map-v2`; explicit v9 manifest selects current scene layers/wheel, floor-v4 and road retained. Native/MPFB/painted experiments are not implicitly active. Existing exporter keeps bounded directory prefixes, not a full transitive dependency proof. |
| Existing dist source exclusion / byte identity | PASS measured | **143 files,108,746,595 bytes**. No `.blend/.fbx/.obj/.gltf/.glb/.sf2/.flac/.mid/.midi/.psd/.kra`, no LFS pointer files, no detected localhost/tmp/generated-image temporary URLs. Every dist asset having a public counterpart is byte-identical. Full hashes in report. Source masters remain repository-side. |
| Release exporter robustness | LIMIT, not observed leak | Unknown extensions are retained by the current permissive branch; adding a future source model to public could leak it. Current dist scan finds none. No speculative exporter redesign is required for this frozen RC. |
| SFX provenance | PASS repository evidence | `art/audio/sfx/THIRD_PARTY_NOTICES.md` plus `src/sound-manifest.json`: Kenney official sources, CC0, event author/license metadata; original license texts/source recordings retained. No paid/native-head source assets active in this dist. |
| Music attribution/source access in shipped package | **OPEN release documentation gap** | Five active Ogg cues; repository `THIRD_PARTY_MUSIC.md` declares GPL-2.0-only, TimGM attribution and editable source/license locations, and explicitly asks accessible game credits. Current143-file dist has no credits/license/source-offer page; main has no credits link. Repository provenance exists, but source-only notices are not a deployed credits surface. No independent legal-compliance certification claimed. |
| Temporal appearance | DEFERRED by explicit user | Temporary walking permitted to finish game. This does not label disputed native/painted identity or jitter as accepted, nor trigger another model/render stage. |
| Physical phone/family/Safari/listening | NOT RUN | Source audit cannot close human/device/audio-quality gates. |

## Minimal root fixes / freeze follow-up

1. Finish coordinator-owned README corrections, explicitly temporary gait and current layout2/v9/audio/wheel, historical sections labelled. No app feature rework.
2. Add a **static deployed credits/license document**, with Kenney CC0 attribution, music authors/TimGM notices, full declared music license text and stable repository links to the exact corresponding editable music source/license revision; make its URL accessible from README and an existing suitable game/help surface. Review distribution requirements against the project's declared licensing before publication. This is a recorded source/package documentation gap, not a recommendation to recompose/relicense audio.
3. After these small root edits, pin final RC, rebuild through existing process and recheck output credits/base/path hashes. This audit does not certify the future modified package. No main merge/deployment performed.
