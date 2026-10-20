# Native contact start/stop plan — future integration, no new clips

Read existing native transition inventory and PR71 analysis first; no duplicate50-action inventory or new animation was created. Frozen source is bae05a2f29298aa1848130267bba802dab731951451af04a7e93f2f0e92f2706, `Walk_ProportionProposal`0..40 at24fps (1666.667ms), `Idle_Neutral_ProportionProposal`0..50. No authored Start/Stop clips exist. Motion acceptance does not certify contact; image-quality gate remains open. No runtime/source/rig/actions/bitmap changes.

## Evidence reused, not resampled or inferred from pixels

`analyze.py` reads the existing final-shoe480-interval/481-endpoint actual material-vertex archive, exact SHA verified against its curve metadata, plus existing measured Idle/Walk poses. All input hashes are in numeric-contract.json. `sole-trajectories.csv` records fixed heel/toe vertex means under the explicitly experimental forward-distance curve (native forward0,−1,0). It is a native world trajectory, not an alpha bbox or moving contact-centroid track. Mesh/material vertex identities are in the original sample-source.json. Original source Root remains exactly0 throughout the samples; global travel is applied externally once.

Candidate low-height windows: L phase.045833–.3625, R.545833–.860417 (sourceframes1.833–14.5 /21.833–34.417). These are17.5mm-band inferred minZ soft-weight confidence>.01 labels, not physical collision truth. Confidence peaks at sourceframes5.5/25.4167. Sourceframes**5 and25** therefore give convenient nearby joins exactly represented by native48 phases**6 and30**, phase.125/.625. Retain actual continuous source clock; joining must not reset it to0.

| Join/support | Confidence | Heel mean Z Walk / Idle | Min sole Z | Other foot min Z | Fitted native forward speed |
|---|---:|---:|---:|---:|---:|
| frame5 / L | .588890 | 2.674 /2.948mm | −.708mm | 38.838mm | .666827m/s |
| frame25 / R | .589785 | 2.679 /2.948mm | −.682mm | 38.664mm | .731843m/s |

Nonzero heel proxy residual velocities after the curve remain: L(14.64,7.15,5.04)mm/s, R(−20.38,8.15,4.79)mm/s in XYZ. This is not zero-slip or proof of a locked sole; contact/floor uncertainty and lateral/vertical motion remain.

## Start: genuine first step required

Direct Idle0→Walk5 with the SAME initial left heel held would require Root forward displacement **−140.20mm**, lateral+21.20mm; frame25/right requires−137.32mm, lateral−20.88mm. Those are backward movements, so a naive blended pose plus preserved initial heel cannot be presented as a natural forward start.

A future native Start must begin with the opposite idle foot supporting, release the lead foot, author its forward swing/landing, transfer support, and end at the *exact* measured Walk5/25 pose and one-sided local joint velocities. For a nonnegative Root advance, lead landing lies at least140.20/137.32mm ahead of its original Idle heel (plus whatever Root advance the new first step authors). Initial idle support target remains fixed until release; the new landing target is distinct. No frozen sprite translation, pose warp, jump to sourcephase0, arbitrary time compression or old painted-body clips.

The native Start duration/travel are unresolved;400ms remains only the prior bounded engineering trial, not an existing clip. Full-body FK/foot constraints and contact transfer must be solved on an isolated native copy before rendering. This document does not create that animation.

## Stop: endpoint geometry fixes travel, not an arbitrary phase snap

At a continuous Walk5/25 capture define `q = RootWorld + HeadingRotation * heelMeanNative(join)`. Preserve this selected support target through stopping. Idle endpoint then requires `RootFinal = q − HeadingRotation * heelMeanNative(Idle0)`.

Consequently Root advances140.20mm(L) /137.32mm(R) after capture, with lateral offset−21.20mm(L)/+20.88mm(R) and vertical−.274/−.270mm if that same fixed heel-mean proxy is held exactly. The lateral offset cannot be silently dropped or hidden by a pivot; it is a real compatibility constraint between source poses. If route-centre/Root endpoint must stay fixed, a future native pose/contact solve must adapt the idle foot placement or choose a different verified target. Both constraints cannot simply be asserted simultaneously.

A constant-deceleration area calculation `duration=2*advance/joinSpeed` gives **420.5ms L /375.3ms R**. These are test hypotheses only: they match Root travel/speed endpoints but do not validate local joint C1 continuity, jerk, full-sole orientation or swing-foot landing. Complete the other foot's real movement into idle, retain supporting sole geometry, end at true Idle pose/velocity. No transition assets exist yet.

## Continuous adapter contract and remaining gates

A stop request keeps current Walk phase and Root travel until the next selected capture; maximum wait approaches833.333ms. Reserve the exact upcoming curve distance plus the measured stop advance when planning an endpoint; never stop the clock and translate a frozen pose. `numeric-contract.json` gives the two half-cycle distances and their maximum. On entering steady Walk at phasep, distance must use `D(p+elapsed)−D(p)` plus the accumulated Start endpoint, not `D(elapsed)` or an origin reset. Integrate piecewise-linear velocity analytically (C1 distance), add stride1.277750296m per completed cycle, rotate native travel once for heading. Camera projection is separate. Stable semantic Root anchor staysworld0 within source; start/stop RootWorld remains continuous externally. Source timing is unchanged.

Reuse PR71 principles—phase queue, measured support, complete swing, root consumed once, actual skinned soles and cold-open clips—rather than MPFB rig/actions/stride or360/180ms constants. Before any integration: author ONE bounded native start+matching stop on a copy, demonstrate exact pose and one-sided velocity joins, measure every used sole point/floor sensitivity and new-contact transfer, verify Root/Hips/Head accelerations and bag/hand/boot clearance, retain actions through cold open, then inspect a small actual E sequence independently. Heading turns/mid-stop cancellation/restart remain unspecified and require separate contracts. No physical no-slip, art/game acceptance or transition readiness is claimed.
