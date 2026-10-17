# Installed road pilot (#45/#46/#62)

Latest user instruction makes joined painted paving required. It supersedes the earlier optional-only scope. This file is an implementation contract, not finished art approval.

Coordinator owns src/connected-road.ts, src/bridge-art.ts, main/style, runtime selection and release export. art_scenes owns art/road-v1 and public/assets/road-v1. Initial pilot is stream only; do not roll out all scenes before viewing the finished earth→road→bank→bridge→bank fragment in actual gameplay.

Resource: assets/road-v1/charoite.webp, square512 or1024 seamless painted angular flagstones, natural fine seams, no hex frame or raised internal rim, no baked route, no independent perspective. Original generation/source, prompt and manifest stay in art/road-v1. Material has a fixed world registration (3.2hex radii per pattern repeat), receives the same ground camera as all cells. A union of confirmed land polygons clips the surface; no preview, terrain vacancy or suggested solution enters this clip. Both endpoints are existing fixed scene stones. External boundary comes from the actual union including adjacent bridge ends; shared instance edges are absent from installed material.

Input polygons/owner identities remain unchanged. Selecting a placed figure outlines all and only its cells. Inventory and preview keep exact figure silhouettes. Bridge timber stays inside the exact three-hex figure; in joined rendering internal hex rims and cap edges adjacent to real paving are omitted. Undo/move/rotation/return/reload rebuild all material/adjacency from confirmed layout. Invalid preview must not change art or save. No generative service is called at runtime.

Pilot acceptance: desktop and landscape native touch; before/after each placement; repeated selection; whole-instance move/rotate/return/undo; remove a neighboring piece and inspect the opened external edge. Save/reload retains identical road cells. Stream and mill water overlay + clean art checks use actual water polygons/accepted layout in the same camera, not CSS offsets. Video combines real input and eventual sound mix. Physical phone remains NOT RUN until a person performs it.
