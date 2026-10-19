# Painted48 residual jitter: read-only diagnosis

User accepted the drawn appearance, but rejected residual jitter. This report diagnoses author trial `50d4074`; it changes no source images, registration, player or runtime. Native motion acceptance does not certify painted motion.

## Cadence observed in the actual browser

`cadence.py` samples the current player through rAF for nine seconds each at desktop1280×900 and emulated CDP-touch landscape844×390. Both had zero skipped phase transitions. The source clock is absolute elapsed time, 48 phases / (40/24s), shared between native and painted views; it does not accumulate rounded frame durations.

On this local approximately60Hz browser, phase holds are mostly33.3ms and periodically50ms (22 such holds in each context). 28.8fps cannot divide60Hz evenly, so this display cadence alone creates modest regular judder. Landscape rAF maximum16.8ms; desktop maximum33.3ms, with one66.6ms phase hold. This is an observation of this run, not a universal browser or physical-phone performance claim. The captured JSON retains every timestamp/phase; physical phone NOT RUN.

## Registration uncertainty can add jitter

Clasp-derived whole-cel translations have adjacent-step vector RMS2.345 native-half pixels, second-difference RMS2.835, maximum second difference11.155 at phase40. Only1.945% of translation spectral power is above6Hz; most correction is low-frequency registration and the necessary raw39→40 jump correction. Filtering the entire pivot curve indiscriminately could restore that jump and erase genuine native bob.

As an illustrative noise model ONLY, independent uniform annotation errors within ±1.5 raw pixels per axis would produce position RMS1.007 and second-difference RMS2.467 native-half pixels per axis. Actual annotation errors are not known to be independent or uniform. The stated annotation intervals therefore make noise-induced jitter plausible; these numbers do not prove that all measured jitter comes from annotations. Five hidden clasp phases remain unmeasured.

## Rigid head feature feasibility probe

`analyze.py` searches integer translations between neighbouring raw cels in two fixed RGB windows: upper head [55,25,102,49), lower head [55,50,102,72). It does not search scale, rotate, deform, fit bounding boxes, or generate raster output. Windows avoid the bag and hands; they are exploratory image patches, not certified anatomical correspondences. Both patches select the same integer shift on the median pair; maximum disagreement is sqrt(5)=2.236 raw pixels. Best upper-head RGB RMS residual is still as high as0.0674 on a0–1 channel scale: head drawings are not identical rigid copies.

After adding existing clasp pivot deltas, upper-head approximate adjacent motion is largest at31→32 (4.86px),47→0 (4.67px),10→11 (3.68px),38→39 (3.62px), all native-half comparison pixels. These are NOT native-head-subtracted errors; some motion can be genuine head movement. This cannot establish exact rigid registration. Pairwise integer head shifts sum to (0,+3) raw pixels around the loop, so blindly integrating them would introduce drift and a seam.

## Recommended next diagnostic, not an approved fix

Use a large high-information stable face/head patch with translation-only subpixel correlation against one fixed template, cross-check a second independent patch, and solve cyclic constraints rather than accumulate neighbour errors. Preserve the actual projected native head trajectory, not a static crown or image bounding box. Compare against NPC's independently measured iris/nose and actual native Head projection before selecting a candidate. Occlusion, changed hair contours and different painted/native headings must remain explicit; subpixel optimizer precision is not semantic accuracy.

If those checks justify it, publish a separate metadata-only head-registration candidate with unchanged pixels, common scale, accepted tempo, baseline toggle, phase-level residuals, and both seams. Do not claim a unique physical Root from a face feature. No such candidate or smoothing is implemented here. Bow/sole/whole-body checks and actual browser video remain necessary; head stability alone can conceal body deformation or foot sliding.

`analysis.json` contains the raw probe and pivot diagnostics; `cadence.json` contains actual browser samples. Neither proves completed smoothness or contact fidelity.

## Subpixel template and cyclic graph follow-up

`head-template.py` now evaluates a fixed phase0 upper-head template against all48 frames, plus cyclic neighbouring upper-head edges; only translation is optimized, to search resolution1/32 raw pixel. A unit-weight least-squares graph combines template and cyclic edges, fixing phase0 as gauge. The lower-face window is held out. No raster or registration metadata is changed.

The unconstrained neighbour shifts sum to(3.28125,0.4375) raw pixels around the loop. Global-template versus graph per-coordinate RMS is0.1637raw; held-out lower-face versus graph RMS is1.2655raw. Importantly, held-out disagreement reaches4.833raw at30,4.416at29,4.285at31,3.637at28: upper hair/head and lower face are not demonstrably one perfectly rigid feature. Best upper template RGB RMS can remain0.06565. The subpixel search resolution therefore must not be advertised as1/32-pixel semantic accuracy.

This supports a translation-only diagnostic experiment, but does not yet justify claiming precise head registration. NPC's independent iris/nose measurements and actual native Head projection are required before choosing the head target path or building the separate candidate. Same28.8fps native is visually accepted, so refresh quantization is insufficient to explain the extra painted jitter.

## Similarity versus internal redraw diagnostic

`head-similarity.py` fits translation-only and then translation+uniform-scale+rotation to the SAME whole-head ROI [55,25,102,72), using phase0 template. This is analysis, not exported sprite metadata. Optimized translation-only RGB RMS at30 is0.0926, versus0.0655 after head similarity (scale1.078125, rotation−3.875°);31 is0.0947→0.0627 (scale1.07,−3.3125°). At8 and40 improvement is negligible. Thus some late-cycle head appearance difference is consistent with scale/orientation change, but substantial image residual remains; this does not prove a common whole-actor transform.

`torso-crosscheck.py` applies the fitted head mapping diagnostically to independent clasp/bow points, adding the native relative torso-feature versus Head-bone displacement. The frozen actual native Head endpoints and camera are preserved in `native-head-projections.json`. This comparison assumes approximate correspondence despite the changed illustrated heading; that systematic uncertainty is unknown. At30 the clasp residual is4.07raw pixels, at31 it is5.71raw; at40 it is4.85raw despite head similarity being nearly identity. Sparse bow residuals are1.35–3.32raw and their annotation uncertainty is±3.5raw per axis. These observations do not establish one shared head-and-body similarity; uncertainty prevents declaring a universal nonrigid failure solely from those points either.

Therefore do not resize/rotate the whole actor based on head fit alone. The next justified experiment remains separate translation-only head registration, conditional on independent face measurements. Native Head-bone endpoint is a trajectory reference, not the same physical feature as painted iris, hair or chin. Native head bob should be retained. A head-stabilized candidate can be shown only as a diagnostic A/B and must report internal face/torso/sole residuals rather than imply morphing is fixed.
