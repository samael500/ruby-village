# Independent saved-file retarget B audit — corrected source `e6ab193`

**PASS for the stated native retarget contract, with changed motion scale disclosed. Not art, gameplay, physical no-slip or final-Ruta acceptance.** The previous saved-file blocker in `a6250cb` remains documented separately: its Walk copy was absent. This review cold-opens the corrected actual file and exercises the saved `Walk_ProportionProposal`; no missing action was reconstructed by QA.

Exact inputs: B `.blend` SHA256 `a4215f55a1bad78ae2e0e35b9ce572515e398053e64db5d483ee518e8b1923b5`; contract `a863fa63e3cd0925561af8e545cbdb84210e902ac9fd6494e00cdf4c556e0d14`; original adapted source `e643c4e4067585a9c7fbbe5d4fa0269019ea04e2d79764a8b3568732c7209d9c`. Hashes were verified unchanged after independent reads/evaluation. Local integration of the author's fix is `b9212a8`; no author-source edits or source `.blend` saves by QA.

## Contract readback

- All **48 original actions** retain their full curve/key/handle data. Retargeted Walk has 408 curves and Idle 380. Rotation curves, handles, key times, handle x positions, interpolation/handle types and other unchanged channels match exactly. Location keys and handle y values follow the stated **parent-bone scale**; maximum scaling discrepancy is 1.49×10⁻⁸ (float storage). Location channel/factor lists match the contract.
- Independently recomputing every rest bone from original heads/parents/scales and every rest vertex from unchanged normalized source weights yields **zero observed error**. All 10,407 rest vertices, weights, polygon vertex orders and object-local matrices are accounted for.
- The actual evaluated **nine-mesh / 10,407-vertex** Walk endpoints at 0 and 40 have maximum and RMS distance **zero**. This measures loop closure, not support/no-slip or every intermediate collision.
- One saved orthographic camera (scale 2.0999999046) remains unchanged across 24 phases. Normalized Root projects to **[256, 516.859312]** on 512×640 with zero observed spread. This is the Root marker, not a measured physical sole anchor. No per-phase camera fitting or crop is used.
- Rest whole-actor used-vertex height is **1.61315087974 m**, versus original **1.81053191755 m**. Rest `Adventurer_Head` mesh height is **0.36626482010 m** (22.71% of whole rest height). These are explicitly named mesh extents, not inferred visible head/garment proportions. Independently read neutral joint markers match the earlier author table to float precision: Head head z 1.25101602077, Neck 1.12825775146, Hips 0.69595593214, left Wrist 0.73034232855 m. Marker positions are not artistic likeness acceptance.

## What changed in the motion

Both files were sampled at **401 phases** over frame 0…40, cycle 40/24 = 1.6667 s, with the same E yaw and normalized Root. Retargeted ankle trajectories match **0.7 × original** to at most **1.051×10⁻⁷ m**; Root is in-place in both. The rotation/timing preservation therefore does not mean unchanged world movement or unchanged stride.

For explicitly diagnostic contact intervals, use each model's evaluated boot-side minimum relative to its global boot floor, tolerance **25 mm original / 17.5 mm B**. The uniformly scaled tolerance yields the same sampled contact windows (173 left / 171 right consecutive intervals). This is not authored contact labeling or a calibrated physical stance test.

| Diagnostic metric | Original | B |
|---|---:|---:|
| Median backward ankle speed during inferred contact, m/s | 1.010656 | 0.707461 |
| Cycle stride inferred from that median, m | 1.684427 | 1.179102 |
| Constant-speed residual RMS, m/s | 0.275774 | 0.193042 |
| Inferred stride / whole rest height | 0.93035 | 0.73093 |

The nonzero residual is retained, scaled from the original gait, rather than certified away. Foot roll/vertical motion and this source contact heuristic prevent calling these values pure planted-sole sliding measurements. The displayed/runtime travel contract must eventually use the accepted new body reference and source stride; this report installs no adapter. New appearance/boot geometry is outside these exact input hashes and has not inherited a whole-mesh/contact certification from this run.

`audit.json` preserves the actual rest/curve checks, 401×2 model sample sets, all 24 camera/Root readbacks and neutral markers. `summary.json` is a compact independently checked aggregation; `audit.log` records the cold-open process. Reproduction uses `../retarget-b-a6250cb/audit.py --source-commit e6ab193 --output-dir <own-output>` after Blender's `--`; it never saves source files. Optional technical E24 render evidence is being captured separately and is not a final-art claim.

**Not checked/accepted:** stock likeness/style, the internally rejected 3D style prototype, final boots/face/clothes, mesh collisions through all poses, physical foot no-slip, route/gameplay, physical phone, final game animation. Numerical retarget success does not approve the appearance.
