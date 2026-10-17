# #49 static-character delivery variants

Deterministic delivery encoding only. No new art, no runtime path changes, no approval changes; original source/export PNGs remain unchanged. This update can be integrated independently of final walking/rig work.

20 runtime images are provided in `public/assets/characters-v1/optimized`: accepted Ruta idle/bust, six resident idle/bust pairs, four Ruta acting poses, rabbit baking group and basket prop. The unused back-view design study is deliberately excluded from runtime delivery.

- WebP q92, method6; alpha encoded losslessly and decoded alpha compared **bit for bit** with the resized source alpha for every image.
- Sprites/poses max height512; real dialogue busts384; standalone basket108. Resampling is Lanczos with aspect retained to nearest integer output dimensions.
- Original total18,429,921 bytes → optimized1,059,906 bytes (94.25% lower transfer size).
- This is a transfer saving **after runtime selects these files**. PNGs intentionally remain in the repository/public tree, so total repository/build size does not shrink from this additive delivery commit.

`delivery-manifest.json` is version1 with `deliveries[originalRelativePath]`. Both original and optimized/image paths are relative to assets/characters-v1. Each entry records delivered frameSize/sourceRect/footAnchor, preserved sceneHeightPx, bytes, sourcehash, optimized SHA256, original sizes/anchors, and resizeScale[sx,sy]. Anchors are scaled separately per X/Y using actual integer dimensions; normalized anchor error is below1e-12. No source coordinate is rounded prematurely.

For Ruta acting poses, source scaling136/768 remains authoritative. Each delivered frame preserves its original sceneHeightPx (standing136, crouch93.146 etc.), with delivered nativeStandingHeightPx adjusted by the export's Y ratio. **Do not stretch the crouch to136px.** Source poses/manifests and the approved appearance decision are untouched. The coordinator's renderer can replace only image/frameSize/footAnchor while retaining its scene height.

`checks.json` records all20 exact-alpha/source-unchanged/anchor checks and actual source-vs-WebP comparisons at **2× game display size** on light/dark/green backdrops. These composites compare full-resolution PNG rendered at target size against decoded WebP at the same size. Minimum PSNR36.32dB (tiny basket), mean41.05dB across60 comparisons; worst mean absolute channel error2.34/255. No clipping/fringe or significant blur seen in the viewed 2× panels, including crouch hair/hands/basket, rabbit ears/whiskers/table and Ruta dialogue face. Focused excerpts and full three-background plates are retained. This is a visual delivery check, not actual-phone validation.

Reproduce with Pillow/libwebp:

```
python3 art/characters-v1/build-delivery.py
```

Active production integration and browser/device QA belong to #46/#37/#49. The coordinator has relayed Maksim's authorization to include the character set in game review; this delivery does not reinterpret it as final animation approval.
