# Read-only painted48 layout diagnosis

Baseline: pack/player1a16d10, immutable raw b06b455. **No pixels, source rects, pivots, scales, player or runtime were changed.** analysis.json binds raw/manifest/HTML hashes; analyze.py reproduces the numeric analysis. This is a planning note, not animation acceptance.

The baseline is one grid(0,30),162×200,8×6. Opaque row bands (alpha>128, half-open maxY) are[40,207),[243,410),[443,611),[642,816),[846,1022),[1039,1204). Empty gutters have heights36,33,31,30,17pixels. The final gutter midpoint1030.5 is near current source-row start1030. The gutter supplies an interval of valid non-clipping cuts, not an authored boundary marker or physical Root. A different row sourceRect might be legitimate, but its correctness cannot be recovered from empty space alone.

One fixed diagnostic paint→native-half calibration remainsS1.1631563024644236,T(29.60245861921824,53.313741280992616). Inverse native-full→paint isS.4298648418450994,T(−25.450112385152693,−45.835405927848875). These are alpha shape calibration, not exact anatomical registration.

For matched half-cycle groups40..47 versus16..23, after subtracting actual native descriptor displacement, mean residual vertical shifts in painted pixels are: crown-band−3.104(sd.253), whole centroid−6.874(sd.894), lower-band−8.367(sd1.153). Those descriptors do not agree on one rigid−8translation. **They are not semantic landmarks:** changed band membership, silhouette, clothing and heading also affect them. This neither proves a pure gutter error nor rules out a useful shared artist-origin correction combined with remaining drawing error.

A numerical counterfactual—not an image correction—adds8paintedpixels to all last-row positions. Residual step means painted-minus-native displacement, Ypositive down; units below are native256×320comparison pixels:

| Shape proxy | Baseline39→40 Y | Baseline47→0 Y | +8row39→40 Y | +8row47→0 Y |
|---|---:|---:|---:|---:|
| Crown band | −8.994 | 1.204 | .312 | −8.102 |
| Whole centroid | −8.895 | .771 | .410 | −8.534 |
| Lower band | −18.262 | .968 | −8.957 | −8.338 |

Thus blindly fixing one boundary can move the pop to the cycle seam, while a lower-body mismatch remains. No image/pivot was generated from this counterfactual.

A legitimate shared-row decoding or artist-pivot change is still possible. Required next evidence is semantic matching with explicit uncertainty: visible bow-knot centre(Chest) and satchel-clasp centre(Hips) against actual evaluated native mesh centres; preferably all eight last-row poses and their corresponding native positions. Agreement of two independent landmarks can support a rigid metadata candidate without any image deformation. It must still disclose remaining head/foot/shape residuals and pass independent actual browser checks at39→40,47→0and all row boundaries. No per-frame scale or warp follows from such evidence. Root/NPC semantic results and stream browser findings are being collected separately; current shape/gutter measurements alone do not select a final correction.
