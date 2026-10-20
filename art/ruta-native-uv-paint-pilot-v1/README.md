# Bounded native UV-paint pilot — source preparation checkpoint

Separate derivative of frozen source SHA bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706, branch from8bd422c. No source/runtime changes. Existing Walk/rig/weights/positions/topology remain; only new derivative body UV layer is authored.

Cold constraints.json reveals an important blocker hidden by mere UV-layer existence: body2854/2854faces, feet610/610 and trousers706/706 have ZEROarea palette-point UVs. They cannot carry real painted details as-is. Temporary welded STAGING copies are SmartUVunwrapped and UVs transferred back via original face IDs and exact rest-coordinate corners; source mesh topology/weights/positions are preserved. Temporary objects removed, new layer RutaPaint saved in ruta-native-uv-derivative.blend. uv-derivative-contract.json records exact geometry/weight hashes and staging counts. Native Ellie head/hair UVs remain unchanged.

UVflat/wire PNGs are technical actual-geometry guides, **not painted artwork** or a generator substitute. Body guide has actual material-ID fills; head/hair maps reproduce actual original UV polygons. Native packed-images/ are exact embedded bytes, preserved with inherited Blender Studio CC-BY4.0/Quaternius and documented donor provenance. They are not newly accepted Ruta textures.

**Selected minimal generation target:** hair-uv-flat-target.png2048², supporting hair-uv-wire-guide.png; exact prompt in hair-texture-request.txt. Active hair is native solid Ellie cap+6authoredlockUVcharts reused over18locks; its ellie.hair_mesh uses procedural Alignment Height/Fac into SH-Hair, not a bitmap. New texture will explicitly use the native UVMap and drive only the derivative hair base colour. Packed strawberry_cloud_diff is for the HIDDEN REJECTED Cortu479v donor and MUST NOT be guessed onto Ellie hair.

Root owns the one built-in imagegen texture call. No generation by this agent. Root's separate native HEAD SKIN UV edit failed moderation (reported request297c5a4a-d977-4b0a-b042-bccd8cca8ecc, output category sexual); no asset produced, no retry/rephrasing to bypass. Native head texture/geometry/eyes/alpha are retained for this pilot. Unaffected hair/material work continues.

Next: consume one immutable generated hair/material map, create actual derivative native surface shader, render only E0/30/40 and front/three-quarter proofs. Native back-three-quarter heading/hair silhouette differs from accepted painted profile. Texture cannot fix silhouette, face geometry or gaze; this is explicitly not a guaranteed accepted replacement, no48batch. Actual painted surface details must be judged; more grain/outline tuning is not the goal.

## Bounded actual hair material pilot

Generated immutable input: `inputs/painted-hair-uv-v1.png` (1254²), from root e769a7b; provenance and exact prompt preserved. Actual native UVMap, no chart/image warp, no pixel cleanup. Technical coverage diagnostic finds 0 background-like eroded-interior texels for RGB-distance thresholds 15–50; whole UV background-like fraction .085–.255%, at edges. This color test is not proof of exact boundary correspondence; bright painted highlights can also bias classification.

`renders/` contains actual E0/30/40 and neutral front/three-quarter only. Source camera unchanged, one Root-rest normalization and constant yaw per view. Hair shader output is **Diffuse BSDF roughness .8**, frozen UV texture→Color, no active SH-Hair specular/Height/Fac output. `rejected-native-hair-shader-renders/` retains preliminary native shader comparison, not the chosen pilot. All original skin/eye materials remain native. Skin generation moderation failure was not retried.

Author visual check: broad copper strand painting materially changes the real surface, with no obvious beige interior holes in inspected E30/three-quarter. Hair remains composed of large cap/lock volumes, front fringe is unlike the approved drawn fringe, and native E side/back-three-quarter visibility differs from accepted profile. Clothing/bag still use flat native materials. **Not finished whole-character painted style, not appearance acceptance, not temporal/no-slip/game validation.** No 48 expansion performed. Texture cannot fix silhouette mismatch.

Reproduce: Blender 4.5.3 `--disable-autoexec -b -t 3 --python-exit-code 1 --python art/ruta-native-uv-paint-pilot-v1/apply-hair-pilot.py`; then `cold-open-check.py`. Contract records unchanged action hashes; cold open verifies frozen mesh positions/topology/weights and rest rig. Raw input and original frozen source remain immutable.
