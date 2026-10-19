# Whole actor E24 extraction: supersedes fixed-grid clipping diagnosis

Source contains24 separate4-connected alpha≥16 actor components (minimum500pixels); they do not touch across rows. The earlier analysis24 fixed-grid export cut actors at imaginary grid boundaries. **That did not prove source artwork was clipped.** This whole-actor extraction supersedes that conclusion. Original fixed-grid analysis remains preserved as a diagnostic of that rejected extraction method.

Each full actor alpha≥16 bounding rectangle is copied with its original RGBA, byte-equality checked. No per-frame body scaling, deformation, pose shift correction or foot correction. Very low-alpha source pixels inside each rectangle remain unchanged; the rectangle is defined by alpha≥16, not by bright-red alpha1…3 noise outside it. Original full source remains preserved in analysis24.

Common frame384×416 sourcepixels; common padding64,48 beyond each original rounded nominal cell origin. This padding applies uniformly; actor bbox is placed using original source offset, not centered by its own bounds. Thus artist placement differences remain. `packing.json` records actor bounds, original exact and rounded cell origin, bbox offsets, translation to packed canvas and unverified grid-root reference. `footAnchor:null`: nominal grid root is not a verified painted support point.

Open `index.html` for unclipped whole-actor loop,24frames/1666.667ms, large and native-reference136px game scale. `whole24-sheet.png` is a contact sheet. Style/pose/scale/anchor acceptance remains separate. No native guide/source/render changes; runtime untouched.

Reproduce: `python3 scripts/painted-ruta-extract24.py`.
