# One ready MPFB hair asset pilot — likeness unresolved

Candidate: **Adrienne Hair by Elvaerwyn**, from the official MakeHuman/MPFB hair02 pack. The source description explicitly names a long side-part style. Official asset table, author/header, download URL, rights evidence and byte hashes are preserved in `source-provenance.json`, `source/`, and `ATTRIBUTION.md`. Attribution and modification/game use are governed by CC-BY; this contributed asset is not CC0. Version is not asserted from the unversioned original header; official community guidance links4.0.

Exactly one ready asset was fitted and rendered, not a catalog of alternatives. Existing `_tools` files/processes were only read; own copies match corresponding entries in the existing official pack byte-for-byte. Browser access verified the official listing/thumbnail and attribution FAQ. A direct urllib evidence-thumbnail download returned403; no bypass or fresh download is claimed. The original pack thumbnail and full original asset files are retained.

## Actual result

Three actual Eevee128sample stills: `e-walk00.png`, `front-diagnostic.png`, `threequarter-diagnostic.png`. `source-adrienne-threeview-comparison.jpg` compares complete unchanged512×640 renders (no fit/crop); it includes the author credit. The new asset opens the forehead and provides genuine curved layers with flowing/curled ends. **Current fit is strongly asymmetric and shows a heavy side curl, with short-looking opposite E silhouette. The approved broad long loose waves are not established.** It is one reviewable ready-asset pilot, not accepted final Ruta hair or a completed likeness solution.

## Geometry/material contract

Original OBJ6266 vertices,9381 faces,3075 boundary edges. This is actual layered curved3D alpha geometry, not closed solid volumes and not a complete hairstyle billboard that follows the camera. Standard hair cards/sheets are allowed for this experiment; the earlier assumption that every surface must be closed was explicitly corrected. No primitive hair rebuild or whole-body image bone warping occurs.

One documented fixed REST-fit matrix converts MakeHuman Y-up/+Z-front to Ruta Z-up/−Y-front and accommodates the broad stylized head. No per-frame fit or actor/body scale change occurs. Hair is attached to existing Head with weight1; no source rig/actions/bones/body/face/eyes/neck geometry is changed. Old19 hair objects are retained but hidden only in the derivative.

Native face UV topology is reconstructed exactly and both original diffuse/alpha and normal images are packed unchanged. New hair material only: fixed warm multiplier[1.32,.92,.70], diffuse roughness.8, source normal strength2; explicit alpha>.5 binary coverage under Blender `BLENDED`, not DITHERED/HASHED alpha.128offline render samples cover edges; this is a deterministic material policy, not proof that all future rendered motion is shimmer-free. Native image texture detail, alpha sorting and intersections can still require review.

The original base camera,512×640 full canvas, actor scale, E headingπ/2 and footRoot are unchanged. Front0 and three-quarterπ/4 views are explicitly diagnostic. Source face/gaze and rear-three-quarter E view remain, not a hidden camera correction to mimic the accepted painted profile.

## Technical checks and limits

`make-pilot.py` creates exactly one derivative and three stills. `cold-check.py` reopens the saved blend and verifies all original mesh coordinates/topology/UV/weights/materials, all action curves and bone rests; new native UV numeric readback, fixed Head binding and original packed image bytes. Source and output hashes remain unchanged after readback. This does not certify likeness, future alpha sorting,48phase motion, shoulder collisions, game integration or physical-phone behaviour. No48 export, runtime/common-script edits, imagegen, external paid service or publication occurs.
