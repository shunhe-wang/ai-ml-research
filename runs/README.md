# Run registry

All runs here are local and non-confirmatory. Valid within-run target/history pools enforce the stated fact-disjointness rules, but targets can overlap across separate calibration runs: the Llama canaries deliberately reuse four Qwen targets per world and are matched diagnostics, not independent replications. Execution logs are append-only and preserve exact rendered prompts, raw responses, hashes, scores, and token counts. Completed manifests are not rewritten.

## Preserved failure and repair chain

- `smoke-qwen35-4b-benefit-20260717`: 0/4 schema-valid. The renderer omitted the full ordered rules and literal output contract. Preserved as a negative implementation result.
- `smoke-qwen35-4b-benefit-promptfix-20260717`: 4/4 schema-valid, 3/4 decision-correct.
- `smoke-qwen35-4b-permit-promptfix-20260717`: 4/4 schema-valid, 4/4 decision-correct.

## Fresh-context calibration

- `calibration-qwen35-4b-benefit-a-20260717`: 48/48 schema-valid; 44/48 decision-correct; 20/48 margin-correct; 19/48 exact.
- `calibration-qwen35-4b-permit-a-20260717`: 48/48 schema-valid; 45/48 decision-correct; 14/48 margin-correct; 14/48 exact.

These two manifests record the base Git commit while the prompt repair was still uncommitted. Their execution records retain the exact prompts and request hashes. Later manifests add an executable-source content hash and dirty-tree flag.

## Paired-history canaries

- `history-canary-qwen35-4b-benefit-a-20260717`: rejected because `limit=4` selected four denial targets.
- `history-canary-qwen35-4b-benefit-a-balanced-20260717`: rejected after independent review found that token matching added a treatment-specific `x` suffix and corrupted assistant-record JSON; target/history fact disjointness was not enforced.
- `history-canary-qwen35-4b-permit-a-balanced-20260717`: rejected for the same padding and disjointness defects, plus asymmetric positive/negative margins and repeated negative history facts.

The observed `0.0` differences in the balanced canaries have no scientific interpretation. The failed artifacts are retained to disclose the defect chain. The remediated runner forbids asymmetric padding, requires natural equality under both per-message and fully rendered model token counts, uses symmetric twin margins, excludes all frozen target fact signatures from history generation, and reports worst-case bounds when either arm is invalid or missing.

## Remediated paired-history canaries

- `history-canary-v2-qwen35-4b-benefit-a-20260717`: four label-balanced targets; 8/8 schema-valid, 7/8 decision-correct, no missing/retry attempts; three approvals after positive histories versus two after negative histories; paired risk difference `+0.25`.
- `history-canary-v2-qwen35-4b-permit-b-20260717`: four label-balanced targets under the threshold-500 calibration schema; 8/8 schema-valid and decision-correct; two approvals in each arm; paired risk difference `0.0`.

Both v2 runs use symmetric margins, full-pool fact disjointness, naturally token-identical per-message and fully rendered prompts, no padding, strict three-key scoring, atomic running/completed manifests, full model-artifact hashes, actual provider-prompt bytes and hashes, retry ancestry, and per-call timing. They remain four-target, single-model, calibration-only diagnostics. Neither value is an effect estimate suitable for a paper, model comparison, or null claim.

## Disjoint Qwen pilot

- `history-pilot-qwen35-4b-benefit-b-20260717`: 16 paired-valid targets; 32/32 schema-valid; 30/32 decision-correct; 7 versus 9 approvals; paired difference `−0.125`; two negative-only discordances; exact one-sided assimilation `p=1.0`.
- `history-pilot-qwen35-4b-permit-c-20260717`: 16 paired-valid targets; 32/32 schema-valid; 27/32 decision-correct; 11 versus 10 approvals; paired difference `+0.0625`; one positive-only discordance; exact one-sided `p=0.5`.

Combined: 32 targets, three discordances, difference `−0.03125`, one-sided `p=0.875`, two-sided `p=1.0`, paired-bootstrap interval `[−0.125, 0.0625]`. This pilot is for nuisance calibration and sign-heterogeneity detection. It does not support promotion, rejection, or a null claim.

## Additional-family baseline and tokenizer gate

- Phi-4-mini-instruct 4-bit: 8/8 strict-schema-valid and 6/8 decision-correct across four label-balanced benefit-b and four permit-c fresh targets.
- Mistral-7B-Instruct-v0.3 4-bit: 8/8 strict-schema-valid and 7/8 decision-correct across the same gate. `family-baseline-mistral7b-v03-4bit-benefit-b-20260717` preserves a zero-execution native-template failure; the new alternating-role fallback was tested and the successful replacement uses a distinct `v2` run ID.

Before any family-history inference, the literal `gold_label` matcher yielded zero admissible pairs for each Phi/Mistral × benefit/permit combination. No run directory was reserved and no response was generated during those tokenizer preflights. The exact-match requirement was retained. A separately frozen `outcome_code` robustness channel uses truthful fixed-width `OUTCOME_CODE=1/0` records and must pass the same native per-message and full-template checks before calls.

Phi's coded two-world schedule passed exact matching but failed task validity: benefit-b had 1/8 strict-valid outputs and permit-c had 0/8, leaving no paired-valid target in either run. Raw outputs show frequent copying of the archived `OUTCOME_CODE` record format instead of target JSON. These runs reject Phi for effect estimation; they do not estimate carryover.

## Bounded replacement-family screen

- SmolLM3 3B: 5/8 strict-valid and 4/8 decision-correct; rejected before history.
- Llama 3.2 3B: 8/8 strict-valid and 5/8 correct, but all four permit responses approved; rejected for a world-specific ceiling.
- Granite 3.3 8B: benefit 4/4 valid and 3/4 correct; permit 1/4 valid and correct; rejected before coded history.
- Llama 3.1 8B: 8/8 strict-valid and 7/8 correct; advanced to literal `gold_label` history canaries.

Llama 3.1 benefit-b: 8/8 valid, 5/8 correct, three versus two approvals, paired difference `+0.25`. Permit-c: 8/8 valid, 4/8 correct, zero versus four approvals, paired difference `−1.0`. Combined exact analysis is eight targets, difference `−0.375`, one-sided `p=0.96875`, two-sided `p=0.375`, bootstrap interval `[−0.875, 0.125]`. These are four-target diagnostics and do not support assimilation, contrast, or generalization claims.
