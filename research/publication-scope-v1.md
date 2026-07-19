# Publication scope v1 — methods and feasibility note

**Status:** frozen writing scope after local calibration runs; released as the v0.1.0 working technical report
**Date:** 2026-07-17

## Working title

*Before Measuring Context Carryover: Exact Matching, Task-Validity Screens, and a Pre-Confirmatory Stop in Rule-Bound Language-Model Decisions*

## Claim that the evidence supports

A reproducible pre-confirmatory pipeline and negative design case show how native-template token matching, strict target-response screening, and cell-level diagnostics can stop an underidentified positive-versus-negative history experiment before scale-up. Five of six convenience-selected local quantized snapshots failed at least one bounded representation or task screen; the two snapshots with history outputs produced different point-estimate patterns across two worlds, making pooled promotion unjustified.

This is a methods/resource contribution about evaluation design and stopping discipline. It is not a causal decomposition, a formal interaction analysis, or evidence that language models generally assimilate to or contrast against prior decisions.

## Retained evidence

- dual-solver synthetic institutional tasks with frozen disjoint cases;
- exact native per-message and fully chat-templated token matching with no treatment padding;
- immutable, crash-auditable local runs with exact prompts, responses, hashes, source snapshots, and failed-run records;
- a 32-target Qwen pilot across two worlds;
- a Llama 3.1 four-target-per-world family canary that reused a subset of the Qwen target cases and therefore is not an independent replication;
- rejected Phi, Mistral, SmolLM3, Llama 3.2, and Granite paths with explicit gate reasons;
- descriptive paired analyses, missingness bounds, and an illustrative panel simulation showing that pooled significance can coexist with a reversing cell.

## Claims explicitly excluded

- a population-average carryover effect;
- a stable assimilation or contrast direction;
- a null or equivalence conclusion;
- frontier-model or hosted-model generalization;
- legal, policy, or human decision-maker generalization;
- any mechanism identification or formal interaction claim;
- a validated simultaneous stability test or confirmatory sample-size prescription;
- independent target replication across Qwen and Llama;
- superiority of any model family.

## Note structure

1. Why sequential-history effects require causal and tokenizer controls.
2. Paired executable-rule substrate and audit harness.
3. Failure chain and predeclared gates.
4. Qwen pilot, family screen, and Llama canary.
5. Fixed-panel simulation showing pooled-power/sign-stability divergence.
6. Recommended evaluation checklist and stopping rules.
7. Limitations, negative results, AI-use disclosure, and replication instructions.

The main text should remain 6–12 pages excluding appendices. Tables must distinguish scientific results from calibration and failed feasibility runs. Every quantitative claim must point to an authenticated repository artifact.
