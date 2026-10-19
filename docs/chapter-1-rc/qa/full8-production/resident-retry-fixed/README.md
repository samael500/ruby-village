# Targeted verification of resident recovery fix `7244fb2`

**PASS: actual game reentry changes Rabbit from `idle` fallback to `conversation-left` after restoring network, without page reload.** The failed facing URL is requested again and decoded; the same endpoint control is 604×981. See screenshots and `report.json`. Real mouse UI and the genuinely earned garden save match the prior `6108ec2` reproduction.

Built the author's unmodified fix on the isolated QA tree after the full frozen playthrough. Runtime/scripts/assets diff against `7244fb2` is empty. Served JS `index-Booi3P-Q.js`, SHA256 `d6f9e80949b87752e1eee897a8ca2d49d08e591aa9c92f22c961ba0e2b7aca28`. The source difference from the full-playthrough snapshot `6108ec2` is only the `loadingViews` failure catch in `src/resident-scene.ts`: it removes the matching rejected Promise, preserving the successful path and idle fallback. No authored runtime edits by QA.

The final probe explicitly awaits the visible authored `data-view` after reentry. An initial immediate read could still see `idle` while the new decode/render was in flight; receiving a new network request alone was not called success. The final screenshot and recorded view establish completion. This targeted run does not claim a second full-chapter playthrough on `7244fb2`; the full two-input gameplay evidence belongs to `6108ec2`.
