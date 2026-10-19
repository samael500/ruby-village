# Ready native character walk pilot — #36

New approach requested by Maksim: use a complete freely licensed rigged character with existing real walk animation, then render actual whole-body frames. Prior bespoke MPFB wardrobe branch is preserved read-only at8e9619f; none of its source or runtime is reused here.

Selected Quaternius Ultimate Modular Women Adventurer: official author pack/release state CC0,10 characters,24 animations. The public author Drive returned quota HTML; those responses were rejected. Downloaded glTF through a fixed GitHub mirror revision; exact source, license discrepancy, URLs and hashes are in art/ready-character-walk-v1/provenance.json. Bundled License.txt says Males although it is in the Women directory; author Women page/release independently verifies CC0. No purchase, login, upload or generated animation.

Imported source has62 bones, four skinned character parts and24 actions, including real Walk [0,40]. Helper Icosphere is excluded from character geometry checks. Pilot selects Walk, mutes other NLA tracks, uses source bone animation without authoring replacement joint motion. Orthographic elevation asin(.65), six projected direction yaws defined, only E rendered first. Native Blender source preserves reusable actions.

Stock adult low-poly explorer is not approved Ruta likeness: short hair, shorts, boots/backpack, no approved shirt/vest/scarf/satchel. This pilot proves complete geometry and source motion, not final character art or game acceptance. No production/runtime/common-manifest edits. Next:24-phase whole frames, large loop/contact strip, geometry/alpha/anchor/loop evidence, then independent art/motion review before root game integration.

## Completed E source pilot

24 distinct whole-frame RGBA renders, fixed512×640 canvas and camera, all any-alpha within canvas (minimum margin70px). No per-frame crop/translation/scale. Fixed world origin projects to footAnchor[256,516.859312]; exact numbers in contract. Atlas, all24 sheet, eight large keyposes, lossless animated WebP, GIF and MP4 are included. Source62-bone rest skeleton, all four mesh geometry/weights and Walk action hashes match imported source.

Native Walk spans40 frames at24fps (1.6667s), sampled at24 evenly spaced phases without repeating endpoint. Root travel0m. Foot-sole floor−0.004907m; inferred contact threshold floor+25mm. Median backward ankle velocity in contact1.04952m/s → estimated root travel1.74921m/cycle. Contact velocity residual RMS0.19232m/s (range−0.65279..+0.20768), so constant-speed runtime is not promised slide-free. Contact inference uses sole height, not source-authored contact labels. Endpoint bone-position error0m is a seam check only.

Current status: source/motion pilot ready for independent review, stock likeness explicitly unapproved, game integration not performed. No six-direction batch before E review.
