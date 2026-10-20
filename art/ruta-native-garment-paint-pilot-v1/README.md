# Garment painted-material preparation checkpoint

One clothing/accessory RGB atlas, skin/head/hair excluded. `body-uv-flat-target.png` is deterministic technical color guide; `body-uv-wire-guide.png` shows actual chart boundaries. `texture-request.txt` is the proposed one-target built-in imagegen edit request. Canonical style reference: public/assets/characters-v1/ruta-idle-pilot.png. Root owns generation and saved output.

`ruta-garment-uv-derivative.blend` derives from frozen hair material pilot, not an overwrite. Only garment `RutaPaint` UV coordinates changed. Original palette UV retained active for unpainted materials. Future painted materials must explicitly bind `RutaPaint`; native head/hair materials and original palette maps must not change. Hair geometry remains separate owner's scope.

Temporary staging meshes use world/rest scaled geometry, weld at1e-7, SmartUV66°, average chart density and global packing. Transfer uses original face ID and world-rest corner position, with float-roundoff tolerance1e-4; original positions/topology/weights hash equality asserted. Skin faces explicitly skipped, no skin chart is supplied. Icosphere diagnostic object excluded. Original staging meshes are deleted. New action/mesh/rig/weights are not authored.

The old atlas incorrectly gave large bag islands due object-local scale and preexisting UV layer selection; this fresh atlas avoids both. There remain many small hardware charts and real low-poly clothing boundaries: painting cannot invent a new garment silhouette. This is preparation only; texture coverage and actual E0/30/40/front/threequarter stills follow after root's immutable generated texture handoff. No48, runtime or finished-whole-Ruta claim.

## Bounded actual five-still material pilot

`trousers-only/generated-v1/painted-trousers-uv-v1.png` is root's immutable f45ea50 output (1254²). Actual cargo interior192035texels after3px erosion: cream0%, olive0%, background-like0%; whole UV beige-like .0765% at edges. No image/UV correction performed. This interior diagnostic alone cannot establish seamless filtering.

`partial-reuse-contract.json` explicitly selects only validated non-pants mixed-map groups (shirt/vest/brown boots/leather/pockets). Original bow, tiny brass, laces and socks retain original materials. Trousers exclusively bind the new trousers map. Mixed map remains rejected as a whole atlas: its12.227% olive contamination must never be bound to trousers. Corrected root mixed-generation provenance is retained. All new painted materials use explicit `RutaPaint`→frozen RGB→matte Diffuse(.8); Eevee source lighting retained. Native skin/head/hair shaders and UVs remain unchanged.

Actual `renders/e-00.png`, `e-30.png`, `e-40.png`, `front-neutral.png`, `threequarter-neutral.png` and packed `ruta-painted-garment-pilot.blend` are the bounded output. **Author visual defect: light UV seam lines on trousers and boots; high painted fold contrast can look shiny even with no specular shader.** No assertion of seamless texture fit or finished canonical likeness. The real render reveals limitations not exposed by eroded-interior color tests. Hair silhouette remains the separately reported mismatch. No48 batch, runtime, source geometry or gait modifications.

Cold-open checks compare all mesh rest coordinates/topology/weights, rig rest bones, all50 actions, and protected head/hair UV/material assignments against source: exact equality. Twelve explicit painted bindings checked. Source SHA remains a60a9601d6a8daa3dfc271b5152d41a361f9397847e111d80c08b3ae05e6d754. `cold-open-check.json` is an invariant check, not artistic acceptance.
