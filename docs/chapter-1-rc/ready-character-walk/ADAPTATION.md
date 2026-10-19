# Minimal ready-part adaptation

Source-only checkpoint. Native Adventurer Walk/actions and62-bone rest skeleton unchanged. Whole disconnected backpack/bedroll/straps removed without cutting shirt/arm faces; one simple native 3D satchel rigidly bound to Hips and one torso/hip-blended diagonal strap added. Stock Casual trousers swap directly: all rest bones match0m difference, existing skin weights retained. CC0 Cortu hair copied from read-only existing native source, head-bound and proportion-fitted; official CC0 evidence preserved despite stale generic OBJheader.

One initial hair fit is retained as rejected high-cap screenshots; one targeted lower/wider fit is being inspected. No new vest, no sewing/retopology, no six-direction batch. Adult stock proportions/short sleeve shirt still differ from approved Ruta. Three views and full E loop/intersection checks pending before any acceptance.

## Delivered pilot

The single lower/wider hair correction is retained; current front/three-quarter/E renders and24 actual E frames are complete. One explicit bag offset moved the same rigid satchel60mm outward,20mm backward and40mm down, with strap endpoint following. Earlier wrist/bag examples retained. No further bag variants or sewing.

Source62-bone rest skeleton and all24 original actions hash-identical. Ready Casual trouser vertices/weights unchanged. One satchel body and one diagonal strap verified. All24 whole-frame alpha bounds checked, atlas/large8poses/all24/loop exported. Final bag/trousers contacts0 across9 sampled poses; bag/body contacts0..111 (mostly swing-hand grazing/occlusion). Pants/boots174..182 and hair/shoulder/head overlaps are disclosed as expected layered-garment/root contacts, not automatically called visual defects. Visual E phase09 now shows wrist outside the satchel top and fingers alongside its rear edge; independent review must judge residual contact. No no-clipping/accepted-Ruta claim.

Core gait remains original in-place Walk; original measured root/stride contract carries forward because native boots, skeleton and motion are unchanged. Adult low-poly proportions/face and green stock shirt remain likeness limitations; no custom vest constructed. Root handles actual-game review/integration. Six-camera export remains held until heading contract/review is settled.

## Source-origin calibration erratum

Native Root rest head ground point is(0,−0.0723,0), not object origin. Earlier E pilot has constant22.0308native-pixel forward origin offset (corrected from17.6 after true portrait-camera PPM measurement). Rotating that object without normalization would orbit the semantic root; this was discovered before runtime integration, not called an observed game bug. Pre-normalization six-view draft renders are retained under ready-character-six-v1/rejects.

New render-only world matrix is Rz(yaw) @ T(−RootRestGround), using actual native rest Root, never posed hips. Source bone rest, local geometry/weights/actions remain unchanged. Camera/viewport fixed, world anchor0 shared. Static proof of all12 headings precedes any full rerender; no per-frame crop/translation.

Static12-headings proof completed: actual posed Root projects to common anchor with maximum error0.0pixels across Walk/Idle0/half/end, heading reprojection below1e−6rad; all24 proof alpha bounds inside canvas. REST world bodyZ bbox[−0.000507894,1.810024023]m → height1.810531917m. Actual camera pixel projection gives horizontal304.761902px/m and vertical Z231.599035px/m. Thus body reference419.317445nativepx,209.658723deliverypx at uniform.5. Canvas640/320 is not body height. Earlier portrait-camera metadata incorrectly used512/2.1; corrected to measured304.761902, no image/camera change.
