# Independent saved-file retarget B audit — `a6250cb`

**BLOCKED: saved B .blend lacks its contracted retargeted Walk action.** A fresh Blender 4.5.3 LTS process opened the actual file, not an author's still-running scene. `rest-transform-contract.json` names `Walk_ProportionProposal`; `bpy.data.actions` contains the original `Walk` and `Idle_Neutral_ProportionProposal`, but **no `Walk_ProportionProposal`**. Saved active action is the retargeted Idle.

Actual B source SHA256: `32a86cd5e047708e30c0b21c589b85a2753e2c793ebe3e69ec5148d00c926987`. Contract SHA256: `e7d65d8f3d5f8b2c51378122b32e51d04b369af4212cac710df88014058934f4`. `saved-action-inventory-a6250cb.json` records every saved action, users, fake-user flag, curve count and frame range. `inventory.py` reproduces the independent cold open; `failed-walk-open-a6250cb.log` preserves the audit's concrete missing-action failure.

The writer copies Walk and Idle but leaves the unused Walk copy without a fake user when saving an Idle proof; this explains a plausible orphan-action loss. The **missing saved action** is directly proven; the writer diagnosis is separate source-code evidence. No author source was changed by QA.

`audit.py` is the prepared fuller saved-file comparison, currently stopped at the missing retargeted action. No PASS for the retargeted Walk's rotation curves/key times, location scaling, full-mesh 0/40 seam, 24-phase projection, stance velocities or stride is claimed on this source. No temporary reconstruction is substituted for the absent saved action.

Root is preparing an author fix that preserves both retargeted actions. The corrected file must be cold-opened and audited separately. Rest/body marker numbers alone are not artistic acceptance; stock appearance and the internally rejected style prototype remain separate. No runtime, game-route, physical phone or final-art certification belongs to this source-level check.
