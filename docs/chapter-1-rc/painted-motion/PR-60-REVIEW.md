Refs #36, #62. Stacked on PR #59 (`art/36-ruta-motion`). **Needs fixes; not production-ready.**

The user rejected the previous painted cutout IK gait because knees/cuffs split and limbs stretched. Those sources remain reproducible history, not accepted finished walking.

Current E pilot uses eight complete painted poses: calm short steps, relaxed open hands, continuous trousers, one satchel/strap. Phases2/6/7 have been repainted as whole figures using pinned local pose guides. All source images, exact prompts, rejected retries, masks and scripts are retained. One shared1254→320 scale.188; whole-frame registration uses the actual waist root and supporting outsole. No per-frame height normalization or bone/limb deformation.

Measured support is now monotonic including7→0. Frame durations are derived from actual supporting-foot ΔX and sum to720ms. Source stride591px → packed111.108px →67.4584 native scene pixels at actor height136 (`nativeHeight224`). Far contact is383.756ms, not an assumed360ms. Zero residual at source boundaries follows this calibration; it is not independent approval.

**Motion still needs fixes.** Continuously moving root with a held PNG can visibly slide between source boundaries: the largest interval travels12.4416scene pixels. Source-sampled root keeps support fixed but makes the character step discretely, also not an accepted solution. The real A/B video demonstrates both. More coherent whole inbetweens are needed before other directions; no morphing/deformation or movement multiplier hides the problem.

Latest evidence:
- [Corrected eight-frame strip](https://github.com/samael500/ruby-village/blob/art/36-painted-walk/docs/chapter-1-rc/painted-motion/calm-east-stance-all8.jpg)
- [Actual Chromium A/B moving loop](https://github.com/samael500/ruby-village/blob/art/36-painted-walk/docs/chapter-1-rc/painted-motion/calm-east-stance-actual.webm)
- [Measured timing, source registration and remaining limits](https://github.com/samael500/ruby-village/blob/art/36-painted-walk/docs/chapter-1-rc/painted-motion/CALM-EAST-STANCE.md)
- Source calibration/manifests/annotations: `art/characters-walk-v1/calm-east-v5/stance-corrected/`.

Validation: eight actual RGBA frames, shared scale, positive support intervals including closure,720ms total, actual support pixels in packaged frames; real browser pause stable and zero page errors. `productionEnabled:false`. This silent resource bench is not chapter/bridge/audio QA. Other five directions and idle/start/stop/turn await a passing E pilot. Physical phone/family checks are not run. The capsule3D proof is technical geometry only, not final Ruta art. No Kling upload or paid generation was performed.

Working branch push and PR updates were explicitly authorized by Maksim. No merge/main push/deployment is performed.
