# Deterministic native NPR fallback study (#36)

Two source-frame0 Walk studies only, E and front; not accepted painted Ruta or runtime assets. This intentionally stops before a new fitting cycle.

Source: existing CC0 ready-part adapted assembly from65bacb7, with unchanged native bones/actions/mesh positions/weights. Parent `ready-character-adapted-v1/assembly.json` and ready-character source provenance retain licenses. No new assets, generation, retopo, cutout deformation, garment fitting or skeletal pose adjustment.

Changes: custom smooth normals averaged across coincident stock vertices without welding; warm three-stop Eevee lighting ramp multiplying original material colors/texture and retaining original alpha; subtle native compositor Sobel gradient contour with source render alpha restored. Global root-rest origin normalization is Rz(yaw) @ T(-RootRestGround), matching the final gait contract. Both768×960 images have root384,775.2889680862. Source render camera and ground projection unchanged. Save source retains all original actions, with Walk active; no loop batch produced.

`checks.json` verifies all action curves and mesh coordinates/weights unchanged by this script. `ruta-stock-npr.blend` is complete native source; `rejects/material-only-first-pass.blend` retains first shader study before shared-position normals/compositor contour. Reproduce with Blender4.5.3: `blender -b -t3 --python scripts/ready-character-npr-pilot.py`.

Observed limitation: toon treatment softens shading but does not create the approved storybook likeness. Adult stock proportions, faceted/simple head and boot shape, hair geometry and box bag remain apparent. No claim that silhouette/color style is accepted. No bow added; adding a bow would not solve the dominant shape gap. Real native gait/contact geometry is preserved, unlike unconstrained painted pose drift, but actual runtime installation is outside this study.
