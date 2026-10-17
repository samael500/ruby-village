# Painted motion v2 review status

The complete six-view candidate is driven by one IK action, with separate actual painted legs and boots. White cuffs stay on shins; boots rotate rigidly at the ankle. Source knee caps have rounded alpha ends, preserving the original painted pixels. Uniform registration around the same source hip makes all six body head-tops 32px, preventing the source-scale jump at turns. Both actual scene camera calibrations have individually retargeted limb exports.

The source action corrects the prototype root’s local Y (world-up), keeping contact knees soft and body rises small. Walk remains .72 world units per 800ms; physical half-step start and stop join its speed continuously. One clock keeps phase through every directional turn, freezes on pause, and emits semantic foot contacts. No mirrored satchel, phase-by-phase generation, crossfade or whole-body-only bob is used.

See V2-INTEGRATION.md for the exact manifest, physical timing, source and integration contract. Actual source/render/browser audits and the six-direction route video sit beside this file. This is an isolated motion review on the accepted courtyard, not production chapter gameplay. Production integration and independent #37 review belong to the coordinator.

Production remains disabled pending complete visual acceptance. Six-view turns are discrete authored views with continuous step phase, not a continuous painted rotation. Family test, physical phone and iOS: not run. Rejected generation attempts, unnormalized cutout samples and pre-correction video are retained with their actual defects.
