# Semantic39→40 diagnosis — annotations only

Frozen native source SHA `bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706` and raw painted sheet remain unchanged. No renders, PNG edits, pivots, image scaling, fitted metadata or native saves were made. Probe opens Blender with autoexec disabled, recreates the actual exporter camera matrix/ortho viewport and E actor yaw/root normalization, and samples the original Walk_ProportionProposal at40*i/48. Raw painted source hashes remain in full48-inputs-and-proof.json.

## Definitions and coordinates

`full48-native-semantic-projections.json` contains all48 actual native projected knot/clasp coordinates at FULL512×640, world points and fixed packer calibration. The exact named authored objects are `Burgundy bow knot` (Chest) and `Satchel warm brass clasp` (Hips). Their centroid is computed over evaluated used mesh vertices. It is a geometric model feature, **not** actor bbox, crown or sole boundary. Source hashes before/after are identical; probe never saves.

`full48-semantic-landmarks.json` has manual painted annotations in LOCAL162×200 shared cells (origin0,30; pitch162×200), absolute sheet positions and native calibrated counterparts. `full48-semantic-packer-view.json` provides the packer's requested compact schema with nativeFULL points. Packer and stream reviewer were informed of the same definitions. No competing grid/calibration is introduced.

Painted clasp means the centre of the **entire visible front brass clasp/ring including its dark aperture**, not the top highlight, strap fastener or belt. At this size the ring is only several pixels across.43 phases receive visible/partial manual coordinates;14/15/16/17/32 are occluded and remain null. Conservative approximate per-axis uncertainty is±1.5rawpx for visible,±2.5 for partial13/31/33. These are annotation intervals, not statistical confidence. No null is guessed or interpolated here.

Bow is an independent **estimated knotted junction** between upper loops and lower tails, not centre of the whole red silhouette. Hair/profile partly hide it, so12 boundary/check phases have±3.5rawpx uncertainty per axis. Other phases are unannotated null. It is weaker than the clasp and not an exact physical joint correspondence. Face/eye matching is not provided: native eye/head visibility and repainted profile differ too much for defensible same-feature identity.

Nearest-neighbour magnified ruler crops are saved as full48-clasp-rulers-row0..5.png and full48-bow-rulers-boundaries.png. They are diagnostic displays of original RGBA over beige, not edited assets. Coordinates were manually reviewed against these5px rulers. Earlier quick-chat coordinates were provisional highlight-centred approximations; this saved whole-ring dataset supersedes them.

## Corrected temporal deltas

NativeFULL coordinates map to painted-cell diagnostics with fixed `p=.4298648418450994*n+(-25.450112385152693,-45.835405927848875)`. This calibration is the packer's global shape-proxy estimate, **not a physical bone fit**. For a temporal check, subtract actual projected native delta from painted manual delta; a constant feature-definition/style bias cancels, but pose-dependent occlusion/view bias may remain.

| Transition | Feature | PaintedΔ(x,y) rawpx | NativeexpectedΔ | CorrectedΔ | Annotation difference interval per axis |
|---|---|---|---|---|---|
|39→40|clasp|(+2,−10)|(0,+.0605)|(+2,−10.0605)|±3|
|39→40|estimated knot|(+3,−10)|(−.0735,−.2825)|(+3.0735,−9.7175)|±7|
|47→0|clasp|(0,+1.5)|(0,+.1488)|(0,+1.3512)|±3|
|47→0|estimated knot|(+1,+1)|(≈0,+.1488)|(+1,.8512)|±7|

**39→40: these two semantic features agree with a common upper-body translation within annotation uncertainty. They do not establish an internal deform at this boundary.** Crown/soles were deliberately not used in this fit-free conclusion. At47→0 both semantic features are nearly continuous within uncertainty. Therefore adding+10px to the whole last row would create a semantic seam that was not previously present; a single last-row translation is not supported.

Other row-boundaries' available corrected clasp changes are7→8(+2,+2.55) and23→24(0,+1.70), within±3;15→16 and31→32 clasp are occluded. Bow checks at those boundaries are also within their broad±7 difference bounds. These are weak static checks, not proof of smooth motion.

## Whole-frame pivot proposal vs internal residual

The all48 dataset can support a **separate explicitly experimental whole-frame resource-pivot trial** using fixed global scale and the native Hips-bound clasp path, with baseline rawRGBA unchanged. It must not be described as an exact physical Root or accepted repair. This author implements no pivots.

One clasp provides only two translation constraints; it does not prove the rest of the drawing is rigid. Painted front-vs-native back-three-quarter viewpoint and hidden knot introduce definition bias. Independent bow residuals and rendered head/legs must be reviewed after a trial; bow must not be reused as another fitting target. Halfcycle16..23 vs40..47 corrected clasp shifts vary (approximately−7..−11rawpx where visible), while bow tendency differs by several pixels; this does not support one rigid last-row offset and warns that a per-frame pivot can leave real internal pose/shape differences. Broad knot uncertainty prevents certifying a precise torso-growth measurement.

Any future null interpolation must be explicitly labelled estimated with unknown added uncertainty; do not invent confidence or measured clasp coordinates for occluded frames. A global mean feature bias is a trial placement choice, not anatomy. Compare39→40 AND47→0 after trial and retain native body bob; do not normalize heights, warp limbs or silently align crown/sole contours. No no-slip, exact knee pose, game or final-art acceptance follows.
