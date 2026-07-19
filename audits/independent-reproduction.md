# Independent reproduction of calibration analyses

**Date:** 2026-07-17
**Scope:** read-only recomputation from raw execution logs
**Verdict:** reproduced without numerical discrepancy

## Independence boundary

The reviewer used a standalone standard-library script and did not import the project analysis module. It parsed each stored `raw_response` directly, reconstructed positive/negative pairs from cell identifiers, and recomputed approval counts, paired risk differences, discordance counts, and exact sign-test probabilities. A separate SHA-256 pass authenticated stored provider prompts and raw responses and checked strict response shape, stored decisions, unique identifiers, pairwise target/system identity, and prompt-token equality.

This is an independent reanalysis and integrity check, not an independent inference rerun. It does not establish backend-level deterministic replay or independently attest the upstream identity of model files at execution time.

## Reproduced results

| Snapshot and world | Pairs | Valid | Correct | H+ approvals | H- approvals | Risk difference | Positive-only | Negative-only | One-sided p | Two-sided p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen, benefit-b | 16 | 32/32 | 30/32 | 7 | 9 | -0.125 | 0 | 2 | 1.0 | 0.5 |
| Qwen, permit-c | 16 | 32/32 | 27/32 | 11 | 10 | +0.0625 | 1 | 0 | 0.5 | 1.0 |
| Qwen, combined | 32 | 64/64 | 57/64 | 18 | 19 | -0.03125 | 1 | 2 | 0.875 | 1.0 |
| Llama 3.1, benefit-b | 4 | 8/8 | 5/8 | 3 | 2 | +0.25 | 1 | 0 | 0.5 | 1.0 |
| Llama 3.1, permit-c | 4 | 8/8 | 4/8 | 0 | 4 | -1.0 | 0 | 4 | 1.0 | 0.125 |
| Llama 3.1, combined | 8 | 16/16 | 9/16 | 3 | 6 | -0.375 | 1 | 4 | 0.96875 | 0.375 |

Every count, effect, and exact probability matched the six generated analysis JSON files.

## Integrity checks

- all 80 provider-prompt hashes and all 80 raw-response hashes recomputed correctly;
- all 80 raw responses were exact three-key JSON objects and agreed with the stored parsed decision;
- all paired targets and system instructions were byte-identical;
- all 40 positive/negative pairs had equal stored prompt-token counts;
- repository verification completed with 5 case sets, 29 runs including 1 failed run, 292 executions, 160 provider prompts, 21 model-artifact sets, and 20 source snapshots.

## Limitations and disclosure items

- The Qwen benefit manifest recorded a clean Git tree at start. The Qwen permit and both Llama manifests recorded global Git dirtiness but clean executable-source snapshots. Existing run artifacts are a plausible source of global dirtiness, but the distinction should be disclosed.
- Local model files currently match the operator-supplied hashes in the manifests. That is artifact consistency, not independent upstream attestation.
- Qwen has 16 targets per world and Llama only four. The Llama targets overlap a subset of the Qwen target cases, so the Llama canary is neither confirmatory nor an independent target replication.
- The Llama permit value is four identical observed pair differences and conflicts in direction with its benefit result. It is a diagnostic, not a population estimate.
