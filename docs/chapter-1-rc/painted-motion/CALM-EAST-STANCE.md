# Corrected E stance source and measured timing — review candidate

After f438a36, phases2,6,7 were repainted as complete figures. Nonfinal local color-block guides pin the actual boot and sketch the connecting shin; the final images are builtin imagegen whole-pose paintings. Supplying only the new guide, without the old second pose reference, retained the new contact placement. Earlier attempts that restored the old boot remain preserved. No PNG is a runtime cutout deformation; no per-frame character scale is used.

Selected outputs: phase-{2,6,7}-guide-only-painted.png under art/characters-walk-v1/calm-east-v5. Packaging and calibration: scripts/character-paint-stance-package.py; generated resources/annotated measurements: calm-east-v5/stance-corrected/.

The visible gold waist-buckle is detected consistently in a constrained ROI. Only whole-frame X translation registers that visible root. The shared1254→320 scale remains.188. Y translation now registers the actual **supporting** outsole, never the swinging foot or global bbox; visible root Y varies144.798..149.216native pixels. This is a modest measured body bob, with no independent limb distortion.

Support X is now strictly monotonic including far7→next0. The landmark method is explicit: observed toe-front alpha silhouette, corresponding forefoot pad70source pixels behind it; partially occluded far pads0/7 are manually inspected. The former audit used approximate manually chosen pad points, so its4.28/11.13spread is historical and not a directly comparable calibrated score. Both definitions/raw source annotations remain available. New source frames were physically repainted before timing was calculated; measurement uncertainty is±8source pixels.

| Measured contract | Value |
|---|---:|
| Source full-cycle root travel |591source px |
| One source→packed scale |.188 |
| Packed/native full stride |111.108px |
| Native sprite height / native scene actor height |224 /136px |
| Resulting stride in native scene coordinates |67.45843px |
| Cycle duration |720ms |
| Frame durations |77.3604,113.2995,132.7919,60.3046,77.9695,74.3147,92.5888,91.3706ms |
| Near contact |0ms |
| Far contact |383.7563ms (not360ms) |

Each duration is720×measured supporting-foot ΔX /total measured stride. All eight intervals are positive. This is constant-speed source timing; no arbitrary movement multiplier or large X correction hides pose errors. Swing feet are not required to remain fixed. Semantic contact timing is asymmetric and must not be silently replaced with half-cycle360ms.

## What this proves, and what remains

World support coordinates match **at source-frame boundaries** by the measured calibration. That zero residual follows the fit; it is not an independent motion approval. Annotated original soles and registered source roots allow review, with partly occluded landmarks explicitly identified.

A whole PNG is held between those boundaries. With a continuously moving root, support can still drift during that hold; the largest interval represents12.4416scene pixels. Holding root advance at the measured source samples keeps the foot fixed but makes body movement visibly discrete. The actual A/B recording shows both modes, plainly labelled; no overall continuous-footplant PASS is claimed. A smoother result may require additional whole inbetweens (especially the largest phase2→3 gap) or an appearance-matched continuous3D model. The capsule proof is not an acceptable substitute.

## Actual evidence

- calm-east-stance-all8.jpg — corrected native strip and measured per-frame durations.
- calm-east-stance.html — actual browser bench; both root modes, real sole markers and pause.
- calm-east-stance-actual.webm — real Chromium recording: continuous root first, source-sampled root second.
- calm-east-stance-{continuous,sampled}.png and browser JSON.

Browser recording: no page errors, real pause stable. Source is E-loop only and remains productionEnabled:false. Other five directions, idle/start/stop/turn and integration await review. This is a silent resource bench on the courtyard, not chapter/bridge/audio gameplay QA. Family/physical phone are not run. No Kling upload/paid generation, merge or deployment.

Coordinator review explicitly rejects source-sampled stair-step root as a final solution. The next allowed direction is more complete painted inbetweens, with no morphing/deformation; first review this corrected A/B loop.
