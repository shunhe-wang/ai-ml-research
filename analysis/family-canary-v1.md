# Multi-family feasibility canaries v1

**Date:** 2026-07-17
**Status:** local calibration; not confirmatory evidence
**Decision:** do not scale the current design

## Fresh-context gate

Each cell used four deterministic, label-stratified targets. Values are strict-schema-valid / decision-correct.

| Family snapshot | Benefit-b | Permit-c | Gate result |
| --- | ---: | ---: | --- |
| Phi-4-mini 4-bit | 4/4 / 2/4 | 4/4 / 4/4 | Fresh pass; literal histories unmatched; coded histories task-invalid |
| Mistral-7B-v0.3 4-bit | 4/4 / 3/4 | 4/4 / 4/4 | Fresh pass; zero matched history pairs in either representation |
| SmolLM3-3B 4-bit | 3/4 / 3/4 | 2/4 / 1/4 | Reject for schema/task validity |
| Llama-3.2-3B 4-bit | 4/4 / 3/4 | 4/4 / 2/4 | Reject: permit approval ceiling |
| Granite-3.3-8B 4-bit | 4/4 / 3/4 | 1/4 / 1/4 | Reject for permit schema/task validity |
| Llama-3.1-8B 4-bit | 4/4 / 3/4 | 4/4 / 4/4 | Pass; literal-history canary eligible |

The gate is deliberately based on fresh contexts and tokenizer checks, not observed history effects. Failed models were not prompt-tuned after outcomes.

## Llama 3.1 literal-history canary

| World | Targets | Valid | Correct | H+ approvals | H− approvals | Paired difference | Positive-only | Negative-only | One-sided p | Two-sided p | Paired bootstrap interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Benefit-b | 4 | 8/8 | 5/8 | 3 | 2 | +0.25 | 1 | 0 | 0.5 | 1.0 | [0.0, 0.75] |
| Permit-c | 4 | 8/8 | 4/8 | 0 | 4 | −1.00 | 0 | 4 | 1.0 | 0.125 | [−1.0, −1.0] |
| Combined | 8 | 16/16 | 9/16 | 3 | 6 | −0.375 | 1 | 4 | 0.96875 | 0.375 | [−0.875, 0.125] |

The degenerate permit bootstrap interval reflects four identical observed pair differences, not population precision. Four targets and one model cannot support a claim.

## Cross-family implication

The larger Qwen pilot was near zero overall (`−0.03125`) with opposite small signs by world. The Llama canary reused four target/history assignments from each Qwen world and therefore is not a disjoint replication. On those matched four-target subsets, Qwen's paired differences were `−0.25` for benefit-b and `0.0` for permit-c, compared with Llama's `+0.25` and `−1.0`. The comparison is diagnostic of model-by-world instability, but its sample is much too small for a formal interaction claim. Phi's coded history format is invalid, and the other local families fail tokenizer or fresh-task gates.

The current evidence rejects a stable pooled directional-assimilation assumption. It does not establish a general contrast effect: model, world, response-format, and baseline-competence interactions are unresolved, and the Llama sample is only four targets per world. A confirmatory design must model these interactions explicitly and requires at least one additional competent family. Local scale-up is blocked until nested operating characteristics and a credible panel are available.
