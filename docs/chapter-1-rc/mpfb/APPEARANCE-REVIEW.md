# Actual MPFB appearance studies — all need fixes

See actual rendered source PNGs and `appearance-v1-v4-vs-approved.jpg`; the comparison resizes only review panels by visible height. Original native renders/cameras and packed model files are preserved. No screenshot is presented as gameplay. No walk exported.

- v1: genuine weighted MPFB body/clothes, one bag strap; generic realistic doll, small eyes/neutral expression, straight quiet hair, incorrect arm relaxation, coarse garment edges. Rejected.
- v2: correct arm relaxation via localZ, larger head and eye targets, sewn waistcoat surface. Hair locks misregistered above scalp; waistcoat inside white shirt; generic face. Rejected.
- v3: actual modeled eye/lid/mouth surfaces on head rig, copper sculpted hair curves, lacing/pockets. Oversized overlays read as googly eyes; tubular locks and garment intersections remain. Rejected. Earlier transform-bake error render is preserved in rejects/unupdated-transform-bake.png; fixed script forces evaluated transform update and deselects other objects before converting curves, final v3 source is reproducible.
- v4: continuous native MPFB face/eye mesh sculpt instead of eye overlays; real fitted hair mesh length/wave edit retaining original UV/alpha. Eye expansion / smile field introduces cheek creases and distorted expression; still straight-looking hair, weak likeness, wardrobe unpolished. Rejected.

Technical success is independent of artistic failure: these are real 3D meshes, original fitted garment skin weights, packed source .blend files, and actual Cycles renders. All share approved palette/accessory intent and one diagonal sling, but do not match approved face/volume/clothing quality. MPFB implementation alone does not make them final Ruta.

Remaining concrete work: authored face/head sculpt or retopology with integrated expressive eyes/lids/smile and correct cheeks/nose; broad volumetric copper waves with coherent scalp roots; tailored shirt/vest/cargo pockets and boot eyelets/laces/sole; softer sewn satchel; controlled warm painted/cel shading. Need another actual full-body E appearance comparison before authoring the real IK-contact walk. No six-view/animation rollout of rejected studies.
