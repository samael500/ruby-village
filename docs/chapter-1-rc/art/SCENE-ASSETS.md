# Accepted-style seven-scene production

Maksim explicitly accepted the courtyard style on 17 October 2026. Seven scene production is authorized; no second style approval is required. Existing gate core/clean layers remain unchanged.

Contract: `public/assets/chapter-1/v9/manifest.json`; per-scene `background.png`, `foreground.png`, `wide.png`, optional `water.png`, `wheel.png`. Shared original canvas 1672×941, origin (0,0), camera/start/goal read unchanged from exact geometry packages. Wide canvas 3200×1600, originalRect [764,329,1672,941]. The renderer must use the same scale for core art, wide surrounding, geometry and character feet; wide surrounding is behind the original core. Exact original center is joined through native SVG registration, never replaced by a newly inferred outpainting.

All produced images remain candidates until full-mask visual audits; manifest readiness is per scene. The accepted style does not imply that an unchecked individual generation is production-ready. Original prompts, tool outputs, failed attempts, source hashes, exact clip masks and checks remain in `art/chapter-1-v9`.

## Failed attempts saved for coordination

Water corrections v5/v6 copied the old river and failed exact target geometry, despite contrasting cyan stencil input. They are rejected and not activated. Dry base plates successfully remove old rivers and are usable compositing ingredients.

Gate/garden wide-v1 was requested at4096×1600, but the tool returned2006×784 and reframed interior content. Native exact-core rejoining reveals a rectangular seam and doubled outer fence. These files are **failed wide attempts**, not final ready surroundings. Current runtime must not reference them. Gate/bakery map-match work is delegated to a separate owner; common scene manifest stays owned by this branch.
