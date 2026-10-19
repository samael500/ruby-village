# Native appearance development study — NOT final Ruta

Maksim rejected the painted pilot: adult proportions and visible jerks. This branch preserves a deterministic whole-3D appearance experiment over measured body-proportion proposal B. The rendered studies are not artistically accepted and are not in the game.

The attempted custom round head, fixed painted face texture and native wave meshes improve frame consistency but remain a weak likeness: helmet-like hair, doll-like facial appearance and an insufficiently tailored outfit. They must not be sold as finished sprites. Independent feedback is being retained. A ready authored Blender Studio head is being investigated separately.

Reproduce internal study:

```
/tmp/blender-4.5.3-linux-x64/blender --background --threads 2 --python scripts/ruta-native-style.py
```

Default input is the committed `art/ruta-native-proportions-study-v2/b-neutral/ruta-proportion-proposal.blend`, with its rest transform contract. `RUTA_STYLE_INPUT`, `RUTA_REST_MAP`, `RUTA_STYLE_ACTION` override these. `RUTA_HEAD_MODE=source` preserves the head already in a supplied source file; `procedural-study` is the rejected internal head experiment. Body tailoring, boots, bow and bag remain independently reusable. Source Walk curves are not modified by this appearance script; the body owner's retarget copies already have changed translations documented separately.

One head UV texture was generated with builtin image_gen using the accepted Ruta appearance reference; its prompt and original raster are kept under `textures/`. It is applied once to real 3D head geometry and remains fixed in every pose. It does not count as accepted facial likeness. No per-frame generative repaint, raster warp, individual resize, camera fitting or anchor shift is used. PNGs here are native render outputs, not gameplay evidence.

The script replaces/tailors whole 3D parts, including topology changes to boots. It does not claim all original source mesh vertices/weights are unchanged. New details have explicit native bone bindings. Inputs remain read-only. Native meshes/materials are packed in the output blend.

Licensing: stock body/rig source and accepted gait are from the Quaternius CC0 sources already documented in `art/ready-character-walk-v1/`; this local appearance study is separately authored. The proposed Blender Studio head is not yet included here; its CC BY attribution must accompany any eventual import.
