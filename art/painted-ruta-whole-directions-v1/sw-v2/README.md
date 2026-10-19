# SW v2 whole-actor candidate

Status: candidate, independent review pending. Source painted-base-sw24-v2.png preserved as source.png. SW v1 is direction-rejected and remains untouched in ../sw; this is a separate replacement candidate, not accepted runtime art.

Same strict extraction:24 separate8-connected alpha>=16 actors (minimum500pixels), no other actor visible pixels inside any bbox, raw crop RGBA exact equality. Common512x512 source1x with padding128,96 and original source-cell offset preserved. No per-frame resize, warp, foot correction or physical anchor. Source/crop/frame hashes and offsets in manifest.json; index.html24-phase1666.667ms unregistered whole-character loop.

Reproduce: PAINTED_DIRECTIONS=sw PAINTED_SOURCE_VERSION=v2 python3 scripts/painted-ruta-extract-directions.py.
