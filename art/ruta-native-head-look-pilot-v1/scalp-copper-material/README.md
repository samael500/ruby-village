# One copper scalp material study

Material-only derivative of the chosen up20 model. `ellie.head_hair` is preserved with fake-user retention; its copy `Ellie copper scalp root material diagnostic` replaces ONLY Head slot3. No polygons are reassigned. Only Principled Base Color changes from the original dark value to linearRGBA[.32,.095,.035,1], one warm chestnut/copper root colour matching the Daisy painting's range. Native roughness.82131147, alpha1 and specular0 remain unchanged. No image is generated or altered.

Actual front/threequarter stills use the same Eevee128AA512×640 camera and diagnostic yaws as the before images. The black stripe is visibly replaced by a continuous warm copper root; this does not add painted strand detail to the scalp or change worried brows/likeness. Before-after JPGs are evidence composites only, not model textures.

`pixel-comparison.json`: front678 changed pixels, bounding227,152→306,199; threequarter419, bounding242,148→285,175. Alpha changes ZERO in both complete frames. Front dark sample(250,162)24,24,24→176,94,54; skin samples(250,174)255,198,163 and(250,190)255,196,162 remain byte-identical. Eye sample(240,210)also identical. Cold-open `cold-check.json` proves all mesh coordinates/topology/UV/weights,50actions,10packedimages,camera and original scalp material unchanged; the sole mesh record difference is Head material slot3. Non-scalp skin/eye/brow/mouth materials are untouched.

`ruta-copper-scalp.blend` retains canonical E/Walk0 state. `apply.py` saves that state before rendering front/¾ Idle0. Source hashes are pinned in contract.json. Source input remains unchanged. First saved copy did not retain unused original material; a save-only follow-up enabled original fake-user and cold-open verification passed. Actual render material/geometry is identical across that save-only correction.

No runtime, no48, no art acceptance or all-phase intersection certificate. This is a single recommended material study, not a list of colour variants.
