# Gate and bakery: matching the approved chapter map

Scope #45 / #62 / #48, resource work for existing PR #56. Branch art/45-map-match, base integration 1c806f1. Only these two scene resources and isolated scripts/docs are changed; common manifests, runtime, six other scenes and water remain with the coordinator/art_scenes.

The approved map is the architectural reference. Gate now has cream stucco, a two-storey red-gabled home, light chimney and flowering climbers; bakery has the corresponding cream/red building, red-and-cream striped cloth awning and visible bread counter/baskets. All output remains a candidate for visual/game review, not an accepted final illustration.

Raw built-in imagegen outputs are preserved as generated-core-01.png. Gate registration uniformly scales the facade edit by .92 around (400,220) to fit the existing blocker footprint. The approved source is restored outside a feathered editable region; all full free polygons plus a 3px guard retain their original pixels. The source camera, start/goal, blockers and geometry files are unchanged. This is deterministic source registration/masking, not procedural replacement of the painted art.

Core exports are opaque lossless WebP, 1672×941. See core-contracts.json for native anchors, camera, geometry/source hashes and exact registration. Review overlays show every full cell polygon; map-before-after-comparison.jpg compares the actual approved map object, previous scene and candidate.

Gate foreground/closed/open resources keep the existing geometry. Their native masks are below y692, while this facade edit ends above y435; no new foreground fence or gate is painted. Coordinator integration must preserve those layers without duplicating the house. Existing runtime asset URLs use the assets/chapter-1/v9 prefix: an isolated resource can be referenced relatively as ../../chapter-1-map-match/gate/background.webp (and bakery likewise), or passed through the coordinator’s asset adapter.

Wide surroundings are being generated independently. Required contract: wide.file, canvas 4096×1600, originalRect{x:1212,y:329,width:1672,height:941}. The approved candidate center remains a separate exact asset. No SVG embedding external images will substitute for the opaque wide raster.

Checks so far: both native core dimensions/opacity, complete free-polygon pixel preservation, geometry/layout-adjustments hash pinning and visual full-polygon overlays. Actual game/phone screenshots, wide seam/coverage and artistic acceptance remain pending. Family test and physical phone are not run. Remote push/PR update is deliberately not attempted while explicit authorization remains pending after automatic-review rejection; local commits are handed to the coordinator.
