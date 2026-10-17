# Painted motion v2 candidate

East intermediate review: separate original boots and source-pixel cutouts, driven by the original IK action. White cuffs stay on shins; boots rotate rigidly at the ankle, preserving their native painted length. Native contact knees are softened by correcting the prototype root's local Y (world-up), rather than shifting the whole rendered figure.

`character-paint-export-v2.py` reproduces six views and two camera calibrations from actual `scene-v8.json`. The original rig and accepted painted source remain unchanged. Delivery uses one common crop/scale, fixed anchor, lossless atlases, and semantic foot contacts. Walk is .72 world units per 800 ms. Start and stop are physical half steps with acceleration/deceleration; phase survives turns. `character-paint-playback.ts` is an isolated adapter, not a change to the game runtime.

The east browser screenshot is real Chromium output from `full-preview.html`. This is a labelled motion review bench on the accepted courtyard, not a claim that chapter gameplay has integrated these assets. Full six-direction rendering and video review are still in progress. Five playback tests pass, including frame-rate independence, continuous turning phase, pause/reduced motion, contact-aligned stopping and scene camera selection.

Production remains disabled pending full-set inspection and Maksim's review. Family test and physical phone: not run.
