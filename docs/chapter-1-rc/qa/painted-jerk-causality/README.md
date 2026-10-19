# Why the rejected painted E pilot jerks — independent diagnostic / #36

**The rejected pilot remains blocked. This analysis provides no replacement art, registration fix or runtime activation.** It separates deterministic common translation from changes already present in the whole painted source frames, using the earlier actual browser capture (`d894a82`), the unchanged origin proposal and existing native reference. All author source hashes remain unchanged.

## Exact decomposition

For an image landmark `p_i`, proposed art origin `a_i`, constant diagnostic origin `A`, display origin `O=(180,320)` and the same global display scale `k=1.2182050753643954`:

```
shown_i = O + k * (p_i - a_i)
fixed_i = O + k * (p_i - A)
Δshown = k * Δp - k * Δa
```

`A` is the component-wise median of all 24 proposed origins. It is only a constant coordinate gauge; its choice does not affect transition deltas. No anatomical correctness is claimed for it. The fixed-origin pictures are diagnostic, not corrected animation. Every image keeps the same global scale and whole actor; no per-frame resizing, body fit, warping or rig edits occur.

The **raw-source term `kΔp` includes both source/packing placement drift and source pose/drawing changes**. Fixed origin alone does not isolate those. Translation-invariant relative landmarks below distinguish changes that no common origin shift removes.

## Two observed transitions

Vertical deltas in 360×360 preview pixels, positive downward. The preview is 2× intended game size. Iris is a manually marked visible painted iris center (2 art-pixel uncertainty); clasp is the earlier visible satchel-clasp landmark (3 pixels), **not a belt buckle, hip or bone**.

| Transition / image feature | Raw source at common scale | Added common metadata shift | Shown proposal |
|---|---:|---:|---:|
| 17→18 iris | −12.18 | +31.51 | **+19.33** |
| 17→18 satchel clasp | −15.84 | +31.51 | **+15.67** |
| 17→18 right heel profile | −30.46 | +31.51 | +1.05 |
| 23→0 iris | +21.93 | −30.29 | **−8.36** |
| 23→0 satchel clasp | +24.36 | −30.29 | **−5.92** |
| 23→0 left heel profile | +31.67 | −30.29 | +1.39 |

Thus the proposal's large common shifts reverse the visible head/body image-feature movement at these transitions while largely compensating the chosen heel-profile movement. This contribution is exactly determined by the saved metadata. It is not a timing, slider, CSS-scale or random browser failure: re-rendering all 24 proposal canvases through the same browser draw formula reproduced the earlier actual canvas PNG bytes **exactly**, and the original desktop/landscape captures matched each other.

The existing actual silhouette observation is consistent: 17→18 painted top drops 18 preview pixels, native top rises 3; painted silhouette extent loses 13 pixels, native gains 3. At 23→0 painted top rises 11, native falls 1. Silhouette bounds are image diagnostics, not head bone or physical height measurements. The additional iris trajectory avoids relying only on a hair/bbox extremum; its manual uncertainty remains explicit.

## What originates inside the source frames

At 17→18 the painted `iris.y − heelR.y` changes by **15 art pixels = 18.27 preview pixels**, independent of any origin translation. The sum of the declared per-point coordinate allowances for that four-point difference is 10 art pixels = 12.18 preview pixels (a conservative manual allowance, **not** a statistical confidence interval). The satchel-clasp/right-heel relative change is 12 art pixels = 14.62 preview pixels, with a 12-art-pixel allowance; that second value alone does not exceed its manual allowance.

This establishes some change of relative **2D image geometry** beyond a common placement shift. It does not prove incorrect skeletal lengths: walking changes relative geometry, boots/hair/bag have their own shapes, and the painted iris/clasp/profile are not calibrated equivalents of native Hips or vertex-region markers. The native Hips-minus-right-heel reference changes about −2.52 preview pixels at 17→18; that is a different feature pair, retained only as context, not subtracted as a calibrated registration residual.

Conditionally, if the chosen right-heel image trajectory is retained near its current position, shifting the whole next actor upward to cancel the iris dip necessarily shifts that heel upward by the same amount. One common translation cannot independently preserve both conflicting image trajectories. This explains why simply changing origin metadata or selecting one fixed origin is insufficient evidence of a valid correction. It does not prescribe a per-frame resize, a particular redraw, or a unique correct anchor.

## What is and is not proved

Proved: the exact common metadata contribution; the actual rendered dip; a translation-invariant source-image geometry change; stable deterministic browser rendering; source byte preservation. Fixed-origin diagnostics show raw drift instead of the proposal's compensated-foot/body-dip tradeoff.

Not proved: how much raw placement drift came from the original generated sheet versus packing; a unique correct artist origin; anatomical proportions or bone lengths; native/painted semantic landmark equality; physical contact/no-slip; a valid production correction. User rejection of adult-looking proportions is an artistic decision respected separately, not inferred from these silhouette numbers. The raw source and metadata are causally linked because the latter was fitted to the former; this decomposition does not blame an independent "bad shift" for every source inconsistency.

Artifacts: `analysis.json` contains all 24 source/fixed/proposal landmark trajectories, all cyclic transition decompositions, uncertainty and source hashes. `fixed/` and `proposal/` contain diagnostic browser renders; `fixed-versus-proposal-key-transitions.png` compares the two key transitions. `image-landmark-trajectories.svg` plots the iris and satchel-clasp trajectories; missing/occluded clasps stay missing. `manual-iris-landmarks24-diagnostic.png` shows the additional visible image cues. Native physical-gait acceptance and the prior real loop recordings remain separate evidence.
