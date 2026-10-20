# Native sprite integration contract — proposed, not runtime-enabled

Owner: root (#46). Art/action authors supply immutable sources, clips, manifests and checks.
The integration game remains e32cad4. This contract records current agreements; it does
not claim implementation, accepted appearance, physical no-slip, or final #37/#49.

## Coordinate and image contract

- Source rig/body: frozen native layered v2; existing Walk/Idle curves are preserved.
  Native rest-ground reference is `[0,-0.050602056086063385,0]`.
- Canonical camera/full frame:512×640, fixed ortho matrix, full Root projection
  `[256,516.8593120574951]`. Production direction yaws come from the frozen heading
  contract. Front-proof yaw0 is a diagnostic, **not** the production E direction.
- Whole poses are rendered in3D. No per-frame image fit, head registration, scaling,
  warping, mirrored asymmetric props, or synthetic old-set transition substitutes.
- Delivery may use ONE fixed crop across a clip/set. `footAnchor` shifts by that same
  crop origin; retained RGBA bytes remain exact. GlobalROI E diagnostic is
  `[123,110,260,434]`, Root anchor in crop `[133,406.8593120574951]`.
- Runtime scale must be calibrated once against the accepted actor/world reference,
  independently of cropped PNG height or per-direction alpha bounds. The legacy
  `height/frameSize[1]` assumption cannot silently redefine native actor height.
  Idle, Walk, transitions and story poses must share calibrated scale/ground origin.

## Motion and clock contract

- Initial native Idle delivery is one actual Idle0 pose per heading (standing), with
  zero pose velocity at Start entry/Stop completion. The original native Idle action
  remains intact; its animated forward derivative is not the static delivery target.
- Preserve the accepted Walk cycle40/24seconds. Native48 loop samples use source
  frame40*i/48, with phase5/40 at48-index6 and phase25/40 at48-index30.
- Actor/root travel is external metadata: monotonic forward distance plus explicitly
  declared lateral offset in native ground coordinates. In-place action poses are
  solved relative to that trajectory. Never bake the same root displacement into
  both PNG motion and the route controller.
- Native root-motion authoring may produce an extracted in-place action and paired
  distance curve; record the extraction, transforms and checks. Root/foot anchors
  are geometric source references, not the current silhouette bottom.
- Clip metadata supplies source action/hash/range/FPS, duration, frame times, loop
  flag, endpoint pose hashes, root curve, contact events and join phase. Walk5 itself has a source one-sided derivative kink: Start exit matches outgoing
  Walk-right velocity, while Stop entry matches incoming Walk-left velocity. Do not
  use a central derivative there. Non-loop authoring endpoints need C0/C1 verification against next Idle/Walk state; avoid an
  extra held endpoint interval while the route continues moving.
- Pause/dialog/hidden-tab stops both phase and travel clocks. Resume must discard
  suspended elapsed time, matching current CharacterPlayer semantics.
- Route length, corners, short journeys, endpoint reserve and lateral offsets are
  unresolved integration constraints. A contact-phase queue must not overshoot the
  destination, leave a bridge, freeze a moving image, or reset gait phase silently.

## Contact and audio contract

The current runtime has `CharacterFrame` fields `sourceRect`, `frameSize`,
`footAnchor`, positive `durationMs` and optional `contact:'left'|'right'`.
`CharacterPlayer` emits `FootContact {type:'foot-contact',foot,surface}`; main routes
that through the existing audio module as `gameAudio.play(foot-${surface})`.
Retain that single audio owner rather than adding per-actor audio players.

Native contact data must describe actual source feet/sole geometry and timing.
Heel proxies alone are insufficient. Current full-sole measurements identify Walk5/25
as near-flat candidates, but residual sole movement means physical no-slip is not
certified. The first-step prototype and Stop must inherit/damp endpoint motion
explicitly, verify dense between-key poses, and preserve original source actions.
If skin weights/rig inheritance cause planted-foot deformation, diagnose complete
world matrices and skinning contributions before changing an isolated derivative.
Any weight/rig delta requires a new source pin and Walk/lace/contact regression checks.

Contacts at transition boundaries must fire once, including loop entry/wrap, pause
and replay. Derive earth/stone/wood from scene geometry at the contact point where
available; do not queue stale footsteps after scene/pause changes. No new audio
acceptance is inferred from silent sprite-study videos.

## Activation gate

Need coherent art matching accepted Ruta, real temporal review with visible face,
all six production headings and compatible Idle/transitions, uniform scale/anchors,
lazy resource budgets, real short/long/bridge/turn/start/stop game checks and independent
#37. Source renders/atlas presence/build success do not replace those checks.
Physical phone and family tests remain NOT RUN. No main merge or publication.
