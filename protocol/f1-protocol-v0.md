# Protocol v0 — directional cross-case carryover

**Working title:** *Do Prior Decisions Carry Over? Causal Decomposition of Sequential History Effects in Rule-Bound Language Model Decisions*
**Protocol status:** Draft before disjoint plumbing/calibration work; not yet confirmatory-frozen or preregistered.
**Date:** 2026-07-17
**Public release:** This historical protocol did not authorize release; the v0.1.0 artifact was later approved separately.

## 1. Research question and bounded contribution

When the governing rules and target case are held byte-identical and fully intact, does the same exact decision shift after positive versus negative histories of independently complete same-rule cases, beyond token-, position-, role-, and format-matched neutral history?

The primary contribution is a paired estimate of directional cross-case carryover under executable rules. The study does not claim to discover sequential interference, context pollution, legal anchoring, cognitive overload, or reset mitigation. Channel and boundary analyses are mechanism-discriminating follow-ups, not separate novelty claims.

## 2. Hypotheses and falsification

### Primary estimand

For frozen target case `i` and fixed model snapshot `m`, let `D(i,m,H+)` and `D(i,m,H-)` be binary positive decisions after matched positive- and negative-outcome histories. The primary estimand is the paired marginal risk difference:

`tau_D = E[D(i,m,H+) - D(i,m,H-)]`.

The primary alternative is directional assimilation: `tau_D > 0`. A two-sided interval and test will also expose contrast effects. The primary analysis averages over a named fixed model panel; model-specific effects and model-by-history interactions are reported without implying a random population of models.

### Key secondary estimands

- excess accuracy/error versus neutral matched history;
- incremental outcome-label effect versus label-shaped inert controls;
- incremental structured-rationale effect versus format- and token-matched inert rationale controls;
- operational boundary effects for a soft independence marker, assistant-history deletion, and literal fresh-context replay;
- horizon trend over predeclared short, medium, and long histories if design simulation shows it is estimable.

Model-generated histories are an operational exposure over a frozen transcript distribution. They do not identify private recognition of the model's own words. Any role/source analysis must cross-feed byte-identical records under assistant versus quoted-user placement.

### Scientific failure conditions

The contribution is falsified or rejected if the result is only generic extreme-length degradation, only schema-invalid output, only one model/world, selected after outcome inspection, or indistinguishable from token/position/role load. A null is interpretable only if equivalence bounds and simulation show adequate precision for a predeclared smallest effect of scientific interest (SESOI).

## 3. Task substrate

Use at least two non-mathematical synthetic institutional rule worlds and multiple independently specified rule schemas per world. The initial worlds are:

1. **Benefit eligibility:** thresholds, hard disqualifiers, and explicit exceptions.
2. **Permit approval:** safety/insurance/fee requirements, restricted zones, hard blocks, and emergency exceptions.

Each case is complete and independently decidable. A rule schema and facts produce a deterministic positive/negative label, signed threshold margin where defined, and structured rule trace. Target and history pools are disjoint.

The implementation uses two structurally different solvers: a prioritized declarative-rule evaluator and a direct world-specific imperative checker. They must agree on every frozen case and trace category before any model output is used.

## 4. Units and sampling hierarchy

- Primary unit: frozen target case.
- Independent design hierarchy: targets nested in independently specified schemas, nested in fixed rule worlds.
- Crossed nuisance unit: frozen history sequence when reused across targets.
- Repeated conditions: all primary history arms applied to the same target.
- Model snapshots: fixed panel members.
- Stochastic repetitions: nested Monte Carlo samples, never independent cases.

Confirmatory targets cannot be selected for observed history sensitivity. Pilot/calibration schemas, targets, and histories are disjoint from confirmatory material.

## 5. Staged design

Do not run a full Cartesian factorial.

### Module A — source/channel attribution

- fresh-context baseline;
- matched neutral history;
- prior case text with inert assistant records;
- prior case text plus gold outcome labels;
- prior case text plus gold labels and solver-derived structured rationales;
- frozen model-generated records as a secondary operational arm.

Positive, negative, and balanced histories are built from counterfactually paired cases. Positive/negative twins must use equal absolute solver margins and unique facts. Every target fact signature is excluded from the full history pool, not merely from the executed target subset. Labels are not falsified while the facts remain fixed in the primary natural-history contrast; an explicitly contradictory label-only manipulation, if used, is separate and exploratory.

Every incremental channel gets a role-, turn-, format-, position-, and model-token-matched comparator. Experimental arms must match naturally under both per-message and fully chat-templated model token counts. Treatment-specific padding or any padding that breaks the native case/JSON format is prohibited; unmatched twins are regenerated or excluded before outcomes are observed.

### Portability amendment — frozen before coded-history inference

The literal gold-output channel remains the representation used in the Qwen pilot. Disjoint pre-inference checks on Phi and Mistral found zero admissible positive/negative pairs in both worlds because their native tokenizers assign unequal lengths to the literal solver response fields. No history response from either family was generated, and the exact-matching rule is not relaxed.

A separately named `outcome_code` robustness channel is therefore permitted for family-portability calibration. Prior case facts remain solver-derived and unchanged. The truthful assistant record is exactly `OUTCOME_CODE=1` for an approval and `OUTCOME_CODE=0` for a denial, and the system block states that mapping while retaining the original three-key target-response contract. Twins must still match naturally under each model's per-message and fully chat-templated token counts; no padding is allowed.

This coded channel is a representation intervention, not a silent replacement for the literal channel. Its estimates cannot be pooled with literal-channel estimates without an explicit channel term and interaction analysis. It remains non-confirmatory until a disjoint multi-family pilot establishes task validity and the nested design is simulated. The amendment was written before any coded-history model call.

### Module B — boundary operations

- retained full history with no marker;
- identical history plus a soft independent-case marker;
- prior user case text retained with assistant records deleted;
- literal fresh request containing only byte-identical system/rule/target blocks;
- optional recap as exploratory only.

Module B uses one predeclared high-information history type and the neutral control. It cannot select the worst Module A condition after unblinding without a disjoint held-out confirmation set.

## 6. Outcomes and scoring

Primary outcome: exact binary/finite decision propensity, parsed from a strict small JSON schema.

Secondary outcomes:

- exact accuracy;
- solver-verifiable rule ID and threshold field where required;
- schema-invalid, refusal, extractable-nonconforming, and transport-failure indicators;
- prompt/completion tokens and latency as descriptive infrastructure variables.

A refusal or content-bearing schema failure is incorrect in the primary task-performance analysis and is also reported separately. Deterministically extractable nonconforming decisions receive only a predeclared sensitivity analysis. The decision-propensity contrast reports complete-pair estimates together with worst-case missing-arm bounds. Transport failures use a capped identical-request retry policy and remain linked to their original record.

## 7. Randomization and masking

- Build the target × condition × model schedule before calls.
- Randomize call order outside conversations and interleave conditions and models over clock time.
- Never expose alternative treatments for the same target in one conversation.
- Freeze and hash rendered prompts/transcripts before target execution.
- Keep confirmatory condition labels masked in the analysis input until deterministic scoring and integrity checks finish.

## 8. Statistical analysis

Primary analysis: paired randomization inference and/or a preregistered logistic mixed model with fixed history/streak/model/world effects, target intercepts, schema/world structure, and crossed history-sequence effects where histories are reused. Report marginal risk differences even if estimation uses log odds.

Robustness:

- paired hierarchical bootstrap at the highest defensible generalization unit, preserving within-target arms;
- model-specific estimates and sign-heterogeneity checks;
- sensitivity bounds for missing transport responses and extractable schema failures;
- equivalence analysis for the null using the frozen SESOI.

Multiplicity:

- one primary `H+` versus `H-` directional contrast;
- label/rationale channel tests gated by an overall non-neutral history effect or adjusted with Holm/max-T;
- boundary interventions treated as a second simultaneous-inference family;
- one planned horizon trend contrast rather than separate horizon fishing;
- all other slices exploratory.

## 9. Design simulation and sample size

The confirmatory item count is not yet a guessed constant. Before freeze, simulate the exact nested binary design across pilot-derived baseline rates, target/schema/history correlations, model heterogeneity, invalid-output rates, ceiling/floor regimes, missingness, and a grid of SESOI values.

For each design report type-I error under zero effect, power at the SESOI, interval coverage, estimator bias, convergence/singularity, and multiplicity-adjusted operating characteristics. Increase independent schemas and targets, not decoding repetitions, until the frozen operating targets are met. If no affordable design meets them, stop the project.

The implementation audit's 120-target, 24-cell, three-model, two-repeat layout is an upper planning example, not the frozen design. Greedy deterministic model runs should not be duplicated. The staged module design and simulation determine the final manifest and call count.

### Feasibility stop after panel simulation

The local Qwen/Llama evidence shows material model × world sign heterogeneity, while five additional family paths fail tokenizer or fresh-task gates. A six-cell simulation then shows that a pooled five-point mean can have 96.2% rejection probability at 120 targets per cell even when one cell truly reverses, while the probability of a sign-consistent rejection is only 4.7%.

Accordingly, this draft protocol is not promoted to a confirmatory freeze. In the present illustrative simulation, 240 targets per cell (1,440 targets and 2,880 H+/H− responses before neutral/channel controls) make a descriptive all-positive-point-estimate rule exceed 95% under a homogeneous +5-point scenario. This is not a validated simultaneous stability test or a sample-size recommendation. A confirmatory design would require a competent third family, a predeclared heterogeneity estimand, and operating characteristics for a valid simultaneous or hierarchical procedure. Those prerequisites are unmet. The authorized output is a methods/feasibility note under `research/publication-scope-v1.md`; no pooled causal-effect claim or confirmatory scale-up is permitted from the current evidence.

## 10. Model panel and execution tiers

### Plumbing tier

A fake provider with injected null, directional, malformed, refusal, and transport-failure responses must exercise the whole pipeline.

### No-cost local smoke/calibration tier

Use disjoint cases with one pinned native-arm64 open-weight instruct model. Validate dual solvers, generator balance, rendered transcript invariants, reset semantics, parser/scorer behavior, full provenance, runtime feasibility, and baseline task range. Smoke outputs cannot appear in confirmatory estimates.

### Confirmatory tier

At least three named model families/snapshots are required for a cross-family claim. Prefer pinned open weights and greedy decoding where capable; any hosted API model, paid call, or cloud run requires explicit user approval after a one-percent priced canary. Mutable `latest` aliases are prohibited.

## 11. Reproducibility and artifact contract

Release, if later authorized:

- rule specifications, schemas, seeded generator, all cases, both solvers, and solver-agreement proofs/tests;
- frozen history and target assignments with content hashes;
- model-specific rendered prompts and token-count manifests;
- exact request/response JSONL with model/runtime/revision/parameter metadata;
- append-only retry and error records;
- scorers, simulation code, analysis code, tables, figures, environment lock, and one-command verification;
- negative results, deviations, costs, tokens, wall time, and model/API reproducibility limitations.

No secrets or restricted data enter the artifact. Human-subject recruitment is out of scope.

## 12. Freeze and deviation policy

This v0 protocol may change only using disjoint plumbing/calibration evidence and literature checks. The confirmatory freeze will record a Git commit, protocol hash, full manifest, SESOI, simulation results, exact model panel, output grammar, exclusions, retry policy, and analysis code before confirmatory responses are inspected.

After freeze, a generator/solver defect discovered before outcome access can trigger a full rebuild and new version. After outcomes are visible, corrections require a versioned new cohort; report both analyses and every deviation. Stopping is schedule-based, never result-based.

## 13. Authorization boundary

This protocol authorized deterministic implementation, tests, simulation, and a no-cost local smoke/calibration run. It did not authorize paid inference, external annotation, cloud compute, outreach, submission, publication, or public release. The later v0.1.0 repository release was approved separately and does not expand those experimental permissions.
