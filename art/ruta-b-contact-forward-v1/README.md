# B source Walk: contact-aware forward curve candidate

Authoring contract, not independent acceptance, runtime integration, artwork approval or physical no-slip certification. Frozen input e6ab193; SHA and material vertex identities in `sample-source.json`. Source SHA unchanged before/after cold sampling. No pose/bone/shoe/image/camera/runtime edits.

One 1.666666667-second cycle: **1.277957458 m**, native forward **(0,-1,0)**. Heading/camera must remain separate. 481 samples include the repeated periodic velocity endpoint. Interpolate velocity linearly and integrate its linear segment analytically; append stride per completed cycle. This yields C1 distance, continuous velocity, nonnegative progress. Linear interpolation of distance is a different contract. Playback at another duration requires scaling velocity inversely; never reuse world speed unchanged. Turns/start/stop are outside scope.

The saved `Adventurer_Feet` mesh contributes 222 actual used material vertices (111/side); heel/toe subsets are rest sole forward extremes, not ankle points. Coordinates are evaluated from saved Walk_ProportionProposal at 480 intervals, static Root XY normalization only. Rest polygon area weights reduce tessellation bias. Each vertex's own velocity is differentiated before contact weighting; no changing-contact-centroid derivative.

Ground is an **inferred global minimum sole z**, not calibrated collision geometry. Main soft contact weight is rest area × max(0,1-height/17.5mm)². Contact confidence .01 is a reporting threshold, not a hard fit switch. Speed is a weighted least-squares common translation with cyclic adjacent-speed penalty (25ms smoothing scale). The unconstrained optimum is already positive (0.656928–0.887807 m/s); KKT residual 2.71e-14. No clipping was needed. Cyclic velocity seam is zero; largest adjacent change .006542 m/s, largest acceleration 1.8841 m/s²; at reported support switches adjacent change ≤.001723 m/s. Acceleration is piecewise constant, not C2.

| Measured contact-weighted material-vertex residual | Forward RMS m/s | Full 3D RMS m/s |
|---|---:|---:|
| Best constant, actual sole criterion (.749265 m/s) | .069287 | .099082 |
| Constant with same total stride (.766774 m/s) | .071465 | .100617 |
| Previous ankle-derived constant (.707461 m/s), evaluated on soles | .080921 | .107540 |
| Proposed common curve | .012350 | .071897 |
| Unsmoothed per-phase best common forward translation lower bound | .003445 | .070912 |

Fixed material-point inferred-contact intervals (weight/restarea >.1, ≥30ms, 222 intervals): median forward span drops 17.620→1.338mm; worst 21.181→4.875mm versus same-stride uniform. These are spans over threshold-limited intervals, not total-cycle physical stance drift.

**Limits:** 16.46% of samples have zero total soft weight and are smoothly interpolated; 36.25% have neither foot above reporting confidence. No simultaneous confidently supported feet were detected, so a two-planted-feet conflict cannot be established from these labels. Even the unconstrained per-phase forward optimum leaves nonzero within-candidate disagreement, lateral and vertical velocities: a single forward rigid translation does not exactly lock this weighted candidate set. This does not prove the same claim for true physical contact, whose labels are unavailable. Vertices above the inferred floor are deliberately fuzzy candidates; do not reinterpret the 3D residual as a measured ground-slip speed.

Height uncertainty ±7mm yields stride **1.264955–1.306171m**, zero-weight gaps 41.25%–2.29%, forward RMS .011187–.034035 m/s. Thus the curve is a transparent engineering candidate, not a uniquely recovered physical distance. Different boots, source geometry/action/scale invalidate surface-derived measurements and require resampling. 480-point finite differences are not continuous swept geometry proof. No art or gameplay verdict follows.

Reproduce in an isolated tree from e6ab193:

```
blender --background --threads 2 --python scripts/ruta-b-contact-forward-sample.py
OPENBLAS_NUM_THREADS=1 python scripts/ruta-b-contact-forward-fit.py
python scripts/ruta-b-contact-forward-diagnostic.py
```

Requires Blender numpy for sampling and numpy Python for fit. `actual-sole-samples.npz` retains all actual material-point positions; JSONs retain thresholds, hashes, solver/metric details and curve samples. `velocity-diagnostic.svg` is diagnostic only. Another reviewer must independently check this authored contract before adapter adoption.
