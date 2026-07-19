# Hostile methods and publication audit

**Date:** 2026-07-17
**Scope:** current methods/feasibility-note claim
**Verdict:** reject as an archival empirical paper; major revision as a technical report or resource release

## P0 findings adopted

1. **The Llama canary is not disjoint.** Its four targets and eight target-by-history-by-condition cells per world are subsets of the Qwen pilot. It is usable only as a matched four-target descriptive comparison. On the shared targets, Qwen's risk differences are `-0.25` in benefit-b and `0.0` in permit-c; Llama's are `+0.25` and `-1.0`.
2. **The panel simulation does not validate a 240-target-per-cell minimum.** Its “sign-consistent rejection” metric combines a pooled `p <= 0.05` with all six point estimates above zero. This is neither a simultaneous positivity test nor a homogeneity, interaction, or equivalence test. The simulation illustrates how pooling can hide a reversing cell, but the numerical threshold is not an inferential sample-size recommendation.
3. **The executed evidence does not earn the causal-decomposition novelty claim.** Neutral histories, separated case/label/rationale channels, model-generated histories, and boundary interventions were not executed. Positive and negative histories change facts, labels, rule IDs, margins, and token identities together.
4. **The calibration uncertainty calculations ignore crossed history reuse.** Each Qwen world reuses eight history sequences across 16 targets. Exact binomial probabilities and target-only bootstrap intervals are descriptive diagnostics, not population uncertainty.

## Further constraints

- Describe observed point-estimate variation, not an estimated model-by-world interaction.
- Exact token matching failed only within the bounded generator bank and chosen representations. Call this representation/harness incompatibility, not a universal family limitation.
- The four-target validity screens cover convenience-selected quantized snapshots, not model families or a population of models.
- The expectation in the proposed estimand lacks a defined target/history/schema population and weighting scheme.
- The Qwen pilot lacks same-target fresh and neutral controls, so it cannot estimate excess error relative to generic history load.
- All empirical outputs come from community four-bit conversions on one MLX backend without an independent backend rerun.

## Required publication posture

The defensible contribution is an authenticated, reusable pre-confirmatory evaluation harness and transparent negative design case study showing how exact chat-template token matching, strict response/task screening, and cell-level diagnostics can stop an underidentified sequential-history experiment before confirmatory scale-up in named local quantized snapshots.

The note must not claim a carryover effect, causal decomposition, mechanism, formal interaction, family-level failure rate, or validated confirmatory sample size. An archival empirical paper would additionally require multiple independent schemas, same-target fresh and neutral controls, at least one identifying channel contrast, a boundary intervention, a broader competent panel or sharply fixed-snapshot claim, and an analysis/simulation that represents the crossed design.
