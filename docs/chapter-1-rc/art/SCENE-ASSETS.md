# Accepted-style seven-scene production

Maksim explicitly accepted the courtyard style on 17 October 2026. Seven scene production is authorized; no second style approval is required. Existing gate core/clean layers remain unchanged.

Contract: `public/assets/chapter-1/v9/manifest.json`; per-scene `background.png`, `foreground.png`, `wide.png`, optional `water.png`, `wheel.png`. Shared original canvas 1672×941, origin (0,0), camera/start/goal read unchanged from exact geometry packages. Wide canvas 3200×1600, originalRect [764,329,1672,941]. The renderer must use the same scale for core art, wide surrounding, geometry and character feet; wide surrounding is behind the original core. Exact original center is joined through native SVG registration, never replaced by a newly inferred outpainting.

All produced images remain candidates until full-mask visual audits; manifest readiness is per scene. The accepted style does not imply that an unchecked individual generation is production-ready. Original prompts, tool outputs, failed attempts, source hashes, exact clip masks and checks remain in `art/chapter-1-v9`.
