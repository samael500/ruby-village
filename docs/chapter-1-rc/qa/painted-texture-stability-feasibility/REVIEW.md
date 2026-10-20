# #36/#62 — stable painted-texture fallback feasibility

Read-only audit at root 5394414. **No fix or new artwork produced.** The accepted appearance and head-registered pilot movement remain the target; image flicker remains open. This fallback must not replace the concurrent higher-resolution full48 trial without its temporal review.

## What exists, verified by cold-open

`inventory.json` comes from Blender 4.5.3 cold-opening frozen SHA `bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706`; no autoexec, render, save, action or geometry edit. Source hash unchanged.

- Body 5742 vertices, feet 336, tailored trousers 1426, single strap 296: each has UVMap. Bag/flap/pockets also have UVMap. UV existence does **not** establish nonoverlap, paint-ready density or correct seams.
- Ellie head 25239 vertices has six existing UV layers, including Full and Baking. Real separate eyes, brows, lashes, face lines and hair geometry survive. Six packed images include 1024² ellie.head, 2048² dirt and 512² donor hair images; these are existing source textures, **not accepted Ruta painted textures**.
- Cap 5617 vertices plus 18 complete native layered locks, 231–339 vertices each, retain UVMap/Alignment and ellie.hair_mesh. Repeated locks inherit donor UVs: deliberately distinct painted lock patterns would need new UV islands or immutable per-object UV offsets.
- Bow loop/tail patches, shirt V and sock cuffs lack UVs. This is a small explicit unwrap task; projected screen-space decoration would not solve it.

Source evidence: `scripts/ruta-native-style.py` materials are mostly flat colour/roughness; its optional fixed front-face texture belongs to the alternate procedural-head branch. Frozen source uses native Ellie head instead. Do not accidentally switch head modes or revive the unaccepted primitive face to obtain a texture slot.

## Why this would differ from the rejected shader study

`art/ruta-native-painted-render-study-v1/README.md` explicitly records failed appearance: native back-three-quarter face, smooth hair and sparse garment/bag detail remain. Its script preserves native face/hair materials, adds rest-bound grain and Fresnel ink to other materials and a one-pixel compositor outline. More grain/outline tuning is not a materially different fallback.

A genuine alternative is **one authored surface texture set**, fixed to rest-space UVs, reused through the unchanged 3D rig. It must encode actual painted locks, brows/eyelids/cheeks, vest edges, cloth folds, bag seams, brass and boot details. Stable geometric occlusion and deformation then come from the whole actor. This is not a flat character picture warped by 2D bones, and does not redraw details independently on every frame. Broad fixed lighting plus low-specular diffuse shading should avoid sliding highlights; no screen-space noise, temporal dithering or per-frame texture switching. Persistent texture alone does not guarantee alias-free output: render supersampling and one final downsample still need checking.

## Concrete next pilot, if full48 still fails

1. Create a derivative Blend, preserve rig/rest/weights/actions/camera and source hash. Audit UV overlap/density; retain face/eye alpha masks and make explicit new atlas islands only where needed. Pack a single versioned 2048² body/accessory and 2048² head/hair texture set (resolution is a starting budget, not a quality claim).
2. Author those textures once from the approved canonical Ruta and accepted painted pilot. Use multi-view UV-aware painting/baking, not a one-view whole-person image pasted over the mesh. A single E image has no information for hidden face/body surfaces. Preserve original shaders separately; explicitly change derived head/hair base-colour inputs rather than globally overwriting protected alpha/normals/iris masks.
3. Before a 48-frame batch, render three actual E poses 0/30/40 and one front/three-quarter view, at identical camera/scale. Check accepted youthful face, copper hair volume, one right satchel and one strap. If native silhouette/gaze is wrong, **texture cannot correct it**; stop and report the geometry/view discrepancy rather than cover it by screen projection or per-frame scaling.
4. Only if those actual stills match style: render unchanged 48 E poses; direct final-resolution/DPR playback, same 40/24 s clock. Inspect hair/face/bag landmarks and 39/40, 47/0; require stable texture detail without new contour shimmer. Then six-direction/transition/game checks separately. No runtime install before those gates.

## Honest blockers and scope

There is no ready authored Ruta UV texture set in the audited pipeline. Designing and painting it is substantial artwork, not a shader toggle. The native pose guide and accepted repaint have different heading/face and some silhouette details; matching one does not prove the other. Texture cannot change silhouette, silhouette hair mass, face geometry or eye direction. Therefore this is technically viable for temporal consistency, **unproven for accepted likeness** and not a quick guaranteed replacement. Do not expand to a full six-direction repaint/render batch before the bounded style pilot passes.

Licenses/provenance: unchanged Quaternius source/gait CC0 provenance stays under `art/ready-character-adapted-v1/`; Ellie by Blender Studio / Blender Foundation is CC BY 4.0, with original Blend, native packed textures, attribution and changes retained under `art/ruta-ellie-head-v1/`. Retain donor hair notices and hidden rejects; do not turn hidden Cortu/old hair back on. Record new texture author/tool, exact references, hashes and derivative shader/UV changes. This audit relied on the repository's saved provenance and did not newly verify external websites or assert new licensing facts.
