# Single-pass DPR-aware renderer A/B

Working review: http://127.0.0.1:5364/render-sampling-study/review.html . Serve the parent packing directory. Branch art/36-render-sampling-study from f3f69db; only this render-sampling-study directory is changed.

Frozen head-pivot manifest is an exact byte copy in frozen-manifest.json. Original HTML is retained under inputs/ for provenance. Raw/packed PNGs, frame rectangles,48poses, head pivots, fixed actor scale and1.666667s clock/28.8fps are unchanged. Both canvases have exactly320×400 CSS pixels and logical256×320 coordinates. No changed actor CSS size or nearest-neighbour display.

- Baseline exact: original256×320 backing, Canvas2D smoothing low, then browser CSS enlargement. Same drawImage source/destination as frozen head trial.
- Direct: backing rounded(CSSsize×DPR), fixed logical256×320 transform, smoothing high; source atlas goes directly to final physical pixels. No intermediate256×320 raster enlargement.
- Optional direct-only device-pixel snap rounds the **whole frame destination origin** in physical pixels. Destination size remains unchanged; manifest/pivots are not rewritten. This is explicitly a sampling diagnostic and can itself quantize motion, not an accepted correction.

The page reports phase, DPR, CSS/backing sizes, mode, logical/physical origin and fixed draw size. ResizeObserver only changes backing when physical dimensions change and does not change CSS, preventing layout feedback. One shared animation clock drives both panels; pause/scrub and dark background operate on both.

## Author actual smoke

browser-smoke.py used headless Chromium contexts DPR1 and2 at1000×1000. Actual controls pause/scrub to40, optional snap and no-paused-ResizeObserver-loop checks passed. Baseline canvas PNG data matched the original frozen head-trial page **exactly** at the same phase in both DPR contexts. Both direct modes preserve identical logical actor size. Direct backing is320×400 atDPR1 and640×800 atDPR2; baseline stays256×320. Snapped direct physical origin is integer. No page errors. Results/states and two actual screenshots are retained.

DPR2 still frame author observation: direct is visibly a little clearer, but this is a renderer-quality comparison, **not evidence that temporal artwork shimmer/internal redraw is solved**. Filtering cannot recover original missing raster detail or enforce identical drawn contours. Root/independent reviewer must compare actual playback; no new pose/pivot/FPS or full animation acceptance follows.

Reproduce smoke with `/tmp/ruby-rc-tools/bin/python browser-smoke.py` while serving the parent directory on127.0.0.1:5364. This is local review only, no publication or runtime changes.
