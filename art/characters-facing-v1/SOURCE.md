# Facing pilot provenance

Tool: built-in `image_gen.imagegen` via imagegen skill; no CLI/API fallback, upload or external generation service.
Approved identity reference: `public/assets/characters-v1/residents/rabbit-idle.png` from integration43e64bd; original unchanged.

Prompt history:
- `rabbit-left-prompt.txt`: first attempt, source retained in rejects due ear swap and clipped edge.
- `rabbit-left-correction-prompt.txt`: two-reference correction failed output moderation; no output.
- `rabbit-left-short-prompt.txt`: single approved reference retry.

`export-pilot.py` does technical packing only: alpha-based crop, one uniform resize, alpha composite onto transparent canvas. It never draws character features, flips, deforms or replaces generated art. Source PNG is preserved whole. Native frame height981 and foot anchor302,977 retain the existing Rabbit runtime scale/sole contract; scene height108.

Pilot status is deliberately pending coordinator's actual-scene comparison. Do not generate the remaining five residents before reviewing this in the garden alongside Ruta. The intended runtime policy is choose an authored facing on encounter/dialogue entry and preserve it during the conversation; idle returns toward activity, without per-frame tracking. Runtime code and existing resident presence belong to coordinator.

- `rabbit-ear-correction-prompt.txt`: targeted ears-only correction of second returned output.

Teacher: `teacher-left-prompt.txt`, original approved idle reference, returned whole `teacher-left-source-v1.png`; new physical left-facing view, book/can ownership preserved. Packed by `export-residents.py`. This generalized exporter may extend frame and pixel footAnchor together when a new silhouette needs more room; this preserves caller's world foot position and scale and never crops an arm/prop to force old pixel width. Height and foot baseline remain canonical.

Hedgehog: builtin imagegen from approved idle, prompt/source `hedgehog-left-*`; no flip, preserved satchel/letter ownership and one strap. Cap tilt varies naturally. Source whole RGBA retained, technical packing only.

Squirrel: builtin original-reference left view followed by accessories-only correction. Prompt/source `squirrel-left-*`, targeted prompt `squirrel-correction-prompt.txt`; rejected wrong-side-bag source retained. Final bag/strap/scarf ownership preserved; one acorn in both paws. Original idle unchanged.
