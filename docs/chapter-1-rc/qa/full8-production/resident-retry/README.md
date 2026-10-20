# P2: failed resident-facing decode never retries

Actual ordinary production source `6108ec2`, bundle `index-swBMIpGK.js`. `src/resident-scene.ts:26–29` retains the rejected decode Promise in `loadingViews`. The author-facing view then remains unavailable across level reentry.

Independent real mouse reproduction: resume an **actually earned** garden save from this clean sequential playthrough; abort the resident-facing PNG request; Rabbit renders the legacy `idle` fallback. Restore network, use settings → map → garden. Rabbit still renders `idle`, while the correct normal activity view is `conversation-left`. There is no new request for the failed resource. A separate real `Image.decode()` of the same asset with a control query succeeds at 604×981. The Rabbit is present: this is permanent loss of the authored facing after a transient network error, not a disappearance claim.

`report.json` preserves both views and actual requests, two screenshots preserve the actual game. `actually-earned-save.json` is a captured real playthrough state, not fabricated completion. `../resident-retry.py` is the reproducible harness. Its first preliminary glob matched only direct-child PNGs and intercepted nothing; that preliminary run did not establish a bug. The saved final run correctly intercepts nested resident assets and confirms the failure.

No runtime changes. This separate failure-injection context does not affect the clean full-chapter run.
