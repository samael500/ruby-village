# One accessory medium-brown material pilot

Source combined actor SHA b14cfb5bfd8f15922c3c736c7b827b9d1ca6c5d1143d257012443fbf140a2db7, read-only. ONE candidate, two actual Eevee128AA512×640 stills: E Walk0 and front Idle0; no repeated colour search/48 export/runtime install.

All33 `Ruta v4 padded accessory` materials are duplicated and originals retained. Insert exactly the same native MixRGB node into padded texture→DiffuseColor: factor.25, Color1 ORIGINAL padded atlas, Color2 linearRGBA[.16,.07,.028,1]. Thus75% native painted texture remains; no bitmap edits or regenerated UVs/padding. This targets boots and satchel padded surfaces only; cloth, head, hair, camera and rig unchanged. Original alpha/shader path unaffected.

Actual observation: orange cast is modestly reduced toward medium brown; original drawn mottling remains visible, including strong boot grain. This is a bounded improvement in hue/contrast, NOT proof of canonical material/art acceptance or removal of all grain. No stronger follow-up candidate is silently substituted. E changed-pixel average RGB113.65/51.95/22.22→112.09/56.43/27.39 documents weaker orange separation, not a universal colour-quality metric.

`e-before-after.jpg` and `front-before-after.jpg` show baseline left / candidate right. Complete alpha byte-identical both views; changed E bounds142,303→371,531 exclude head/hair. `cold-check.json` verifies saved source/output all mesh coordinates/topology/UV/weights,50actions, packed images and camera exact; differences are accessory material slots only. Source and output SHA in contract.json. Canonical E Walk0 blend is saved before diagnostic front rendering.

No UV-wire repair or new raw artwork is included; prior padding is preserved exactly. Native hair/card and likeness blockers remain independent.
