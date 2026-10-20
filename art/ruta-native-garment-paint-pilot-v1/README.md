# Garment painted-material preparation checkpoint

One clothing/accessory RGB atlas, skin/head/hair excluded. `body-uv-flat-target.png` is deterministic technical color guide; `body-uv-wire-guide.png` shows actual chart boundaries. `texture-request.txt` is the proposed one-target built-in imagegen edit request. Canonical style reference: public/assets/characters-v1/ruta-idle-pilot.png. Root owns generation and saved output.

`ruta-garment-uv-derivative.blend` derives from frozen hair material pilot, not an overwrite. Only garment `RutaPaint` UV coordinates changed. Original palette UV retained active for unpainted materials. Future painted materials must explicitly bind `RutaPaint`; native head/hair materials and original palette maps must not change. Hair geometry remains separate owner's scope.

Temporary staging meshes use world/rest scaled geometry, weld at1e-7, SmartUV66°, average chart density and global packing. Transfer uses original face ID and world-rest corner position, with float-roundoff tolerance1e-4; original positions/topology/weights hash equality asserted. Skin faces explicitly skipped, no skin chart is supplied. Icosphere diagnostic object excluded. Original staging meshes are deleted. New action/mesh/rig/weights are not authored.

The old atlas incorrectly gave large bag islands due object-local scale and preexisting UV layer selection; this fresh atlas avoids both. There remain many small hardware charts and real low-poly clothing boundaries: painting cannot invent a new garment silhouette. This is preparation only; texture coverage and actual E0/30/40/front/threequarter stills follow after root's immutable generated texture handoff. No48, runtime or finished-whole-Ruta claim.
