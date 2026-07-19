# Before Measuring Context Carryover

## Exact matching, task-validity screens, and a pre-confirmatory stop in rule-bound language-model decisions

**Technical report - not peer reviewed**

**Technical report and reusable research artifact**

**Version 1.0, 19 July 2026**

> **Evidence boundary.** This note reports an authenticated design case study, not a confirmatory effect estimate. It does not establish assimilation, contrast, a null effect, a mechanism, a model-family ranking, or a causal decomposition of history channels.

## Abstract

Sequential-history experiments with language models can look deceptively simple: present the same target after positive and negative prior decisions, then compare outputs. In practice, the comparison can fail before statistical inference begins. We built a pre-confirmatory evaluation harness around two synthetic, executable institutional rule worlds. It freezes target and history cases, requires agreement between two structurally different solvers, renders each snapshot's native chat template, rejects positive-negative histories unless message-level and full-template token counts match without padding, scores an exact three-field JSON contract, preserves failed and interrupted runs, and authenticates prompts, responses, source snapshots, and local model artifacts.

The resulting artifact records a negative design decision. Five of six convenience-selected non-Qwen local four-bit snapshots failed at least one bounded representation or task screen. A 32-target Qwen calibration and an eight-target Llama 3.1 canary produced different point-estimate patterns across two worlds. The Llama targets were a subset of the Qwen targets, so this was a four-target matched diagnostic rather than an independent replication. Moreover, the executed positive-negative contrast changed facts, labels, rule identifiers, and margins together; it lacked same-target neutral histories and cannot identify a causal channel. An illustrative panel simulation showed how a pooled test can obscure a reversing cell, but it did not implement a valid simultaneous stability test and does not justify a sample-size prescription.

The contribution is therefore a reusable harness and transparent stop record. The case study demonstrates how strict preprocessing, response-validity gates, common-case comparisons, independent raw-log reanalysis, and adversarial publication review can prevent a small, underidentified calibration from becoming an overclaimed result.

**Keywords:** language-model evaluation; sequential context; exact matching; executable benchmarks; reproducibility; negative results

<!-- PAGEBREAK -->

## 1. Problem and contribution

Prior turns can alter a language model's later output. That broad fact is no longer a research gap. Work on task interference, persistent admissions conversations, legal decision order, multi-turn task sharding, context resets, and semantic distractors already documents related effects across many settings [1-7]. The narrower scientific question that motivated this project was whether prior decisions on independently complete cases change a later decision governed by the same executable rules, after generic context load and possible channels are separated.

The attractive first comparison was directional: hold a target case fixed, expose a model to five positive or five negative prior cases, and measure the paired approval difference. That comparison is not yet the scientific study. It bundles at least five changes: prior case facts, outcome labels, rule identifiers, numerical margins, and token identities. Without a same-target fresh condition, a token- and format-matched neutral history, and separated case/label/rationale arms, an observed difference cannot identify semantic competition, label carryover, rationale commitment, or generic history load.

This project therefore distinguishes three layers that are often collapsed:

1. **Scientific design:** an estimand, sampling population, controls, and an analysis that identify a bounded claim.
2. **Measurement feasibility:** a model-harness configuration can receive matched prompts, follow the output contract, and perform the target task away from unusable ceiling or floor regimes.
3. **Artifact integrity:** the exact executable inputs and outputs can be authenticated, replayed where possible, and independently reanalyzed.

Only the latter two layers were exercised here. The result is a pre-confirmatory case study with a stop decision. Its strongest defensible contribution is an inspectable reference implementation that makes several quiet failure modes visible before scale-up.

### 1.1 What this note contributes

- A dual-solver generator for two non-mathematical ordered-rule worlds.
- A native-template matching gate at both message and complete rendered-prompt levels.
- Strict separation of schema validity, decision correctness, rule correctness, and margin correctness.
- Immutable run directories, early running manifests, structured failed-run records, request/response hashes, source snapshots, retry ancestry, and model-file hashes.
- A documented chronology in which invalid canaries were retained, causal-integrity defects were repaired, portability failures were not prompt-tuned away, and a superficially tempting pooled result was not promoted.
- An independent standard-library reanalysis of 80 raw calibration responses with no numerical discrepancy.

### 1.2 What this note does not contribute

It does not show that one model family is more susceptible than another. It does not estimate a population-average carryover effect. It does not test a formal model-by-world interaction. It does not validate exact token equality as the uniquely correct control. It does not claim novelty for JSON validation, prompt hashing, executable scoring, or any other component in isolation. Closely related evaluation work already shows that prompt formatting, task operationalization, structured-output compliance, and the harness itself can materially affect measured behavior [8-11].

<!-- PAGEBREAK -->

## 2. Evaluation object and integrity contract

### 2.1 Rule worlds

The harness implements two synthetic institutional worlds. In the **benefit** world, ordered rules combine an income ceiling, residency requirement, hard sanction block, and caregiver exception. In the **permit** world, ordered rules combine safety, insurance, fee, zone, hard-block, and exception conditions. Every case is complete: no prior case supplies a fact or rule needed to solve the target.

Each frozen case contains a schema identifier, facts, a binary `APPROVE` or `DENY` label, a rule identifier, an integer margin where defined, and a structured trace. A declarative prioritized-rule solver and a separate imperative world-specific checker must agree before a case can enter a frozen set. This avoids using a language model as the answer key.

### 2.2 Paired history construction

Positive and negative history cases are constructed as counterfactual twins with equal absolute solver margins and unique facts. Target fact signatures are excluded from the history bank. A history contains five independently complete prior cases and truthful solver outputs. The target system block explicitly states that prior cases are not precedents.

For a target `i` and fixed snapshot `m`, the descriptive paired contrast is:

`d(i,m) = D(i,m,H+) - D(i,m,H-)`,

where `D` is one for an approval and zero for a denial. The reported risk difference is the mean of `d` over executed targets. Greedy outputs are deterministic conditional on the rendered prompt and backend; uncertainty would come from a declared population of cases, histories, schemas, and snapshots. That population was not frozen here, so p-values and target-only bootstrap intervals in the calibration artifacts are diagnostics, not population inference.

### 2.3 Native-template exact matching

The project chose a stringent design rule: paired histories must have equal token counts under the tested snapshot's native tokenizer for every corresponding message and after full chat-template rendering. Padding is prohibited. The governing rules and target text must be byte-identical within each pair.

This rule controls one narrow quantity: rendered token count. It does not make positive and negative histories semantically exchangeable, equalize token identities, or guarantee equivalent internal computation. It also conditions the accepted exposure bank on the tokenizer. A history accepted for one snapshot may fail for another, so cross-snapshot comparisons need a common accepted bank or an explicit model-specific-exposure estimand.

The bounded pilot banks contained 32 symmetric history fact pairs per world, organized into eight five-case history sets. Qwen's executed 16 targets per world and Llama's executed four per world passed the chosen equality checks. Phi and Mistral yielded zero admissible pairs in both worlds under literal solver-response histories. Under a separately frozen fixed-width `OUTCOME_CODE=1/0` representation, Phi matched but copied the history format instead of answering the target; Mistral still had zero matched pairs. These are representation-harness incompatibilities within this bank, not universal impossibility results.

### 2.4 Response and storage contract

Every target response must be exactly one JSON object with exactly three keys: `decision`, `rule_id`, and integer `margin`. Valid JSON is not enough. Extra keys, wrong types, text outside the object, copied history codes, refusals, and transport failures remain distinct outcomes. Completed run directories are immutable. A manifest is written before the first call and finalized atomically; failed zero-call runs are retained. Each stored record includes the abstract request, actual provider prompt, raw response, hashes, timing, model identifier, revision provenance, score, and retry linkage.

<!-- PAGEBREAK -->

## 3. Failure chronology as evidence

The audit trail is part of the contribution because the design improved only after specific failures were made inspectable.

| Stage | Observed failure | Decision and repair |
| --- | --- | --- |
| Initial local smoke | 0/4 strict-valid benefit outputs; prompt omitted complete rules and literal response contract | Preserve failed run; add a regression test; repair renderer before reuse |
| Fresh Qwen calibration | High binary accuracy but poor exact margins | Retain binary decision as plumbing endpoint; demote arithmetic margin from primary evidence |
| First history canary | Truncation selected denial-only targets | Require deterministic label-stratified selection |
| Balanced canaries | Treatment-specific padding corrupted JSON; target/history facts overlapped; permit histories had asymmetric margins | Invalidate all observed effects; prohibit padding; require full-pool fact disjointness and symmetric unique margins |
| Reproducibility review | Interrupted runs could be invisible; verifier missed prompts, retries, and causal summaries | Write an early `running` manifest; classify failed runs; authenticate provider prompts, ancestry, bounds, source, and model artifacts |
| Phi/Mistral literal preflight | 0/32 admissible pairs in each tested world | Do not relax matching; execute no literal-history responses |
| Phi coded canary | 1/16 strict-valid responses; frequent `OUTCOME_CODE` copying | Reject the snapshot-channel configuration without prompt tuning |
| Wider local screen | SmolLM3, Llama 3.2, and Granite failed bounded fresh-task screens | Stop those paths before history calls |
| Llama history canary | World point estimates differed sharply; targets overlapped Qwen | Treat only as four-target matched diagnostic; do not call it replication |
| Panel simulation review | Compound sign metric was mistaken for a simultaneous stability test | Keep only the pooling counterexample; withdraw numerical sample-size prescription |

Several general lessons follow. First, retaining invalid runs changes scientific behavior: it makes it harder to remember only the repaired, favorable path. Second, a schema-valid response can still be decision-wrong, rule-wrong, or margin-wrong. Third, prompt portability is not implied by fresh-context accuracy. Fourth, a numerical result can be perfectly reproduced and still fail identification. Artifact integrity is necessary, not sufficient.

### 3.1 Adaptive screen chronology

The snapshot search was convenience-based and adaptive. It began with Qwen as a no-cost local plumbing subject, then screened Phi and Mistral after the Qwen pilot. When their literal representations failed, a coded robustness channel was frozen before coded inference. Three tokenizers were then checked before weight download; two small snapshots proceeded to fresh baselines. Finally, Llama 3.1 and Granite 3.3 were bounded as the last local 8B candidates. Gemma was not used because the official upstream required accepting additional terms, and a public conversion was not treated as a shortcut.

This chronology rules out estimating a family-screen failure rate. The four-target baseline gate is sensitive to one response, snapshots are community four-bit conversions, and all calls used one MLX runtime. The correct unit of description is the named snapshot-runtime-prompt configuration.

<!-- PAGEBREAK -->

## 4. Bounded snapshot screen

Each non-Qwen configuration received four label-stratified fresh targets per world before any history call. “Valid” means strict three-key JSON. “Correct” means the binary decision matches both deterministic solvers. The gate was intentionally a stop screen, not a performance benchmark.

| Local four-bit snapshot | Benefit valid / correct | Permit valid / correct | Bounded outcome |
| --- | ---: | ---: | --- |
| Phi-4-mini-instruct | 4/4 / 2/4 | 4/4 / 4/4 | Fresh pass; literal unmatched; coded task-invalid |
| Mistral-7B-Instruct-v0.3 | 4/4 / 3/4 | 4/4 / 4/4 | Fresh pass; zero literal or coded matched pairs |
| SmolLM3-3B | 3/4 / 3/4 | 2/4 / 1/4 | Stop for schema/task validity |
| Llama-3.2-3B-Instruct | 4/4 / 3/4 | 4/4 / 2/4 | Stop for permit approval ceiling |
| Granite-3.3-8B-Instruct | 4/4 / 3/4 | 1/4 / 1/4 | Stop for permit schema/task validity |
| Llama-3.1-8B-Instruct | 4/4 / 3/4 | 4/4 / 4/4 | Advance to four-target history canary |

Five of the six configurations stopped at some bounded stage. That count is descriptive only. It does not imply that five-sixths of models are unsuitable, that the base families would behave the same at other sizes or precisions, or that alternative well-justified representations could not work.

### 4.1 Why strict task validity precedes effect estimation

Suppose a model copies a prior record format in one history condition but answers correctly in another. Counting the copied string as a denial can manufacture a directional effect from a channel-format failure. Similarly, a snapshot that approves every permit target can show no directional movement because it is at a ceiling, while a snapshot that cannot follow the response schema can appear to move merely because parsing success changes.

The harness therefore reports four layers separately:

1. transport completed;
2. output obeyed the exact schema;
3. binary decision matched the solver;
4. rule identifier and margin matched the solver.

For an eventual scientific experiment, invalidity must be an outcome, not an unreported exclusion. A complete-pair decision contrast should be accompanied by worst-case missing-arm bounds. The present Qwen and Llama history runs had no missing arms, so their complete-case bounds collapse to the point estimates. That fact improves accounting but does not repair the missing neutral controls or reused-history dependence.

### 4.2 Why exact matching is not a universal gate

Token equality was selected to eliminate a particular alternative explanation in a paired short-history design. It is not the only defensible approach. A future design could model token length directly, use several naturally occurring lengths, or construct a shared semantic exposure bank with predeclared tolerances. What is not defensible is treatment-specific padding that changes the response representation or retrospective prompt tuning after outcomes are visible.

<!-- PAGEBREAK -->

## 5. Calibration results: descriptive only

The Qwen calibration used 16 targets per world. The Llama canary used four targets per world. All 80 responses across these four runs were schema-valid, and every paired prompt retained byte-identical system instructions and targets with equal stored prompt-token counts.

| Snapshot and world | Targets | Valid | Correct | H+ approvals | H- approvals | Paired difference |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Qwen3.5-4B, benefit-b | 16 | 32/32 | 30/32 | 7 | 9 | -0.125 |
| Qwen3.5-4B, permit-c | 16 | 32/32 | 27/32 | 11 | 10 | +0.0625 |
| Qwen3.5-4B, combined | 32 | 64/64 | 57/64 | 18 | 19 | -0.03125 |
| Llama-3.1-8B, benefit-b | 4 | 8/8 | 5/8 | 3 | 2 | +0.25 |
| Llama-3.1-8B, permit-c | 4 | 8/8 | 4/8 | 0 | 4 | -1.00 |
| Llama-3.1-8B, combined | 8 | 16/16 | 9/16 | 3 | 6 | -0.375 |

These values are not independent cross-family estimates. The Llama target-history-condition cells are exact subsets of the Qwen pilot cells. The only honest cross-snapshot comparison uses those shared targets:

| Shared four-target subset | Qwen paired difference | Llama paired difference |
| --- | ---: | ---: |
| Benefit-b | -0.25 | +0.25 |
| Permit-c | 0.00 | -1.00 |

The shared-case table removes target-composition differences, but it does not create adequate sample size. In benefit, Qwen had one negative-only discordance while Llama had one positive-only discordance. In permit, Qwen had no discordance while Llama had four negative-only discordances. Four targets per world cannot establish an interaction, and the permit value is a degenerate diagnostic rather than a precise estimate.

### 5.1 Why the reported tests are not inferential evidence

The repository includes exact sign-test probabilities and target-level bootstrap intervals because those functions were frozen before summarization and are useful pipeline checks. They reproduce exactly. Yet each Qwen world used eight history sets across 16 targets, so histories were reused. A target-only sign test or bootstrap does not represent this crossed dependence. There is also one schema per world and no declared generator population. The current p-values and intervals therefore describe the realized calibration schedule only and are intentionally omitted from the main argument.

### 5.2 What the calibration does justify

The results justify a stop. Pooling the two worlds or two snapshots would conceal that the observed cells do not move uniformly. Because the scientific design lacks neutral and channel controls, adding more calls to the same bundled contrast would increase precision around an underidentified quantity. The rational next action is design revision, not scale.

<!-- PAGEBREAK -->

## 6. The panel simulation: illustration, not prescription

To stress-test a tempting pooled analysis, the project simulated six fixed snapshot-by-world cells under independent paired Bernoulli outcomes. Each scenario used 5,000 replications. The pooled test concatenated targets across cells. A descriptive compound metric additionally required the pooled one-sided test to reject and every observed cell point estimate to be positive.

| Scenario | Targets per cell | Total targets | Pooled rejection | Compound all-positive diagnostic | Any negative cell estimate |
| --- | ---: | ---: | ---: | ---: | ---: |
| Homogeneous null | 120 | 720 | 0.042 | 0.007 | 0.968 |
| Homogeneous +5 points | 120 | 720 | 0.997 | 0.742 | 0.140 |
| Homogeneous +5 points | 240 | 1,440 | 1.000 | 0.959 | 0.024 |
| +5-point mean, one reversing cell | 120 | 720 | 0.962 | 0.047 | 0.917 |
| +5-point mean, one reversing cell | 240 | 1,440 | 1.000 | 0.018 | 0.974 |
| +5-point mean, one reversing cell | 400 | 2,400 | 1.000 | 0.003 | 0.996 |

The valid lesson is qualitative. A pooled mean can reject almost certainly even when one cell truly reverses. More data then reveal the negative cell more reliably; they do not make the pooled directional story scientifically stable.

The invalid lesson would be to call 240 targets per cell a required sample size. The compound metric is not a simultaneous positivity test, a test of interaction, a homogeneity test, or an equivalence procedure. The simulator also omits schema clustering, reused histories, invalidity, missingness, and the hierarchical estimator proposed in the draft protocol. The 240-cell row is retained only as an illustration under its own assumptions.

### 6.1 What a confirmatory simulation would need

A later design would first define the target population, schema population, history assignment mechanism, fixed-snapshot weights, and the claim's heterogeneity margin. It would then simulate the exact planned estimator with crossed target and history effects, multiple independent schemas, invalid-output processes, missing transports, multiplicity, and predeclared cell-level or hierarchical decision criteria. Operating characteristics would include type-I error, power at a smallest effect of scientific interest, interval coverage, estimator bias, convergence, and stability under plausible misspecification.

No such confirmatory design is frozen here. The current simulator is a red-team tool that successfully blocked an overly simple pooled promotion rule.

<!-- PAGEBREAK -->

## 7. A pre-confirmatory checklist

The following checklist is the most reusable output of the case study.

### Claim and identification

- State whether the claim concerns generic load, semantic case content, prior labels, prior rationales, self-generated outputs, or a boundary operation.
- Include same-target fresh and token/format-matched neutral conditions before attributing a positive-negative difference to outcome history.
- Keep governing rules and target text byte-identical across paired arms.
- Separate facts, labels, rationales, roles, and boundary operations rather than changing them together.
- Define the expectation: target generator, schema distribution, history bank, snapshot panel, and weights.

### Measurement feasibility

- Run fresh-context task-validity screens before history inference.
- Report transport completion, schema validity, decision accuracy, rule accuracy, and numeric fidelity separately.
- Declare how invalid outputs enter the primary estimand and report worst-case missing-arm bounds.
- Preflight the actual native tokenizer and full chat template; report denominators and acceptance rules.
- Treat accepted histories as a possibly snapshot-specific exposure distribution.

### Design integrity

- Use independent executable solvers or an equivalent answer-key audit.
- Make target and history pools disjoint at the fact-signature level.
- Prevent treatment-specific padding, target truncation, or post-outcome prompt tuning.
- Randomize calls outside model conversations and keep paired conditions in separate contexts.
- Freeze control arms, analysis code, exclusions, retry rules, and stopping criteria before confirmatory outputs.

### Inference

- Use the target, not the model call, as the primary unit.
- Represent reused histories, schemas, worlds, and snapshots in the uncertainty model.
- Report cell estimates before any pooled average.
- Use a valid simultaneous, hierarchical, or equivalence procedure for stability claims; all-positive point estimates are not a test.
- Simulate the exact estimator and missingness process, not an easier surrogate.

### Artifact and audit

- Preserve abstract requests and actual provider-rendered prompts.
- Hash prompts, responses, frozen cases, executable source, and locally available model artifacts.
- Create run manifests before calls and classify completed, failed, interrupted, and retried executions.
- Retain invalid runs and protocol deviations.
- Require an independent raw-log recomputation that does not import the main analysis implementation.
- Obtain a hostile claim-level review before drafting a public abstract.

<!-- PAGEBREAK -->

## 8. Reproducibility and independent reanalysis

The repository is designed so that a reviewer can separate deterministic verification from optional local-model inference.

### 8.1 Deterministic checkpoint

With Python 3.12 and `uv`, `uv sync` followed by `make verify` runs the unit suite, Ruff, mypy, dual-solver checks, stored-artifact verification, causal summaries, retry ancestry, and prompt/response authentication. An optional Apple Silicon environment adds the MLX adapter checks. Model weights are excluded from version control; manifests record repository identifiers, revisions, operator-supplied provenance, and local file hashes. The public verifier reports excluded model folders and pre-import Git objects as unavailable instead of counting them as newly verified; `make verify-external` requires those artifacts if they are restored.

At the audited checkpoint, repository verification covered:

| Artifact class | Verified count |
| --- | ---: |
| Frozen case sets | 5 |
| Runs | 29, including 1 structured failed run |
| Executions | 292 |
| Actual provider prompts | 160 |
| Model artifact sets | 21 |
| Source snapshots | 20 |

Those model and historical-source counts describe the private audited checkpoint. The public repository is intentionally a one-commit, privacy-sanitized export: it can fully reauthenticate the included cases, prompts, responses, scores, summaries, and retry records, but it cannot independently re-hash excluded model weights or Git objects that were not published.

### 8.2 Independent standard-library reanalysis

An independent reviewer enumerated the four Qwen/Llama `executions.jsonl` files and used only Python's standard library. The script parsed every raw response directly, reconstructed pairs from cell identifiers, and recomputed approval counts, paired differences, discordance counts, and exact binomial diagnostics. A separate SHA-256 pass authenticated prompts and responses, checked exact three-key objects, compared raw decisions with stored decisions, verified unique identifiers, and checked paired target/system identity and prompt-token equality.

All six stored summaries reproduced without discrepancy. All 80 provider-prompt hashes and 80 response hashes matched. All 40 pairs preserved the intended byte and token invariants. This is strong evidence that the analysis files reflect the retained raw logs.

It is not an independent inference rerun. Three of the four run manifests recorded global Git dirtiness at start, although all four recorded clean executable-source snapshots and those snapshots verify. Existing run artifacts are a plausible source of global dirtiness, but the distinction is disclosed. Current local model files match manifest hashes; that does not independently attest the upstream repository identity at the historical run time. Backend-level deterministic replay also remains untested.

### 8.3 Release boundary

The code, generated cases, run logs, analysis, audits, and paper source are released in the public v0.1.0 repository artifact at https://github.com/shunhe-wang/ai-ml-research. Model weights are not redistributed. This repository release does not authorize a preprint upload, venue submission, external outreach, paid inference, or human-subject activity.

<!-- PAGEBREAK -->

## 9. Limitations and next scientific step

### 9.1 Empirical limitations

- The history evidence covers two community four-bit conversions on one local MLX backend.
- Qwen used 16 targets per world; Llama used four, all overlapping Qwen targets.
- There is one rule schema per calibration world and only eight reused history sets per world.
- The positive-negative contrast bundles facts, labels, rule identifiers, margins, and token identities.
- The Qwen targets lack matched fresh and neutral histories.
- No label-only, rationale, model-generated-history, assistant-deletion, soft-boundary, or fresh-replay module was executed.
- The snapshot screen was adaptive, convenience-based, and only four targets per world.
- The exact matching rule conditions accepted histories on each tokenizer and may change exposure distributions.
- No independent backend reran the model outputs.

### 9.2 Statistical limitations

The descriptive exact tests assume independent discordant target pairs, while histories are reused. The target bootstrap omits crossed history and schema uncertainty. The panel simulation uses independent Bernoulli cells and a non-inferential compound diagnostic. There is no frozen generalization population, smallest effect of scientific interest, heterogeneity margin, or simultaneous cell-level procedure. For these reasons, the note makes no effect, null, equivalence, interaction, or sample-size claim.

### 9.3 Novelty limitations

Prior work already establishes task interference, sequential decision inconsistency, legal order effects, multi-turn degradation, reset benefits, distractor effects, prompt-format sensitivity, structured-output failures, construct-validity concerns, and harness-level effects [1-11]. The present artifact does not claim priority for any individual control. Its value is the inspectable combination and the decision record showing how those controls changed an actual research program. A focused search through 2026-07-18 found this potentially useful as a technical report or resource, not ready as an archival causal paper. The search must be refreshed before any venue submission.

### 9.4 Minimum next scientific step

If the original causal question is resumed, the next step is not a larger positive-negative pilot. It is a disjoint design with multiple independent schemas and the same frozen targets crossed with fresh context, matched neutral history, case-only history, and truthful label history. At least one boundary operation should be included. A common exposure bank should be sought across predeclared snapshots, or the estimand should condition explicitly on snapshot-specific admissibility. The analysis and simulation must include crossed history effects and a formal heterogeneity criterion.

That work would require a competent broader panel or a sharply bounded fixed-snapshot claim. Paid or hosted inference, if proposed, requires a priced call manifest and explicit approval. Until those conditions are met, the correct scientific status is stopped before confirmation.

<!-- PAGEBREAK -->

## 10. Conclusion

This project did not produce a causal result about context carryover. It produced something smaller and more defensible: an authenticated evaluation harness, a complete failure trail, a reproduced calibration record, and an evidence-based decision not to scale an underidentified contrast.

The main lesson is procedural. Before interpreting a history effect, verify that paired prompts are controlled under the actual native template, that the model can perform the target task and follow the response contract, that common cases are used for cross-snapshot comparisons, that history reuse is represented in inference, and that the executed arms identify the claimed channel. Then ask an adversarial reviewer to attack the strongest sentence in the abstract. In this case, those steps changed the output from a putative directional-effect paper into a transparent methods/resource note. That narrowing is the result.

## AI-use disclosure

Generative AI tools materially assisted with literature discovery, candidate ideation, protocol drafting, implementation, testing, debugging, analysis code, adversarial review, and manuscript editing. No AI system is an author. The experimental subject models are separately identified by repository, revision, runtime, and local hashes in run manifests. AI-generated suggestions were treated as drafts rather than evidence: primary sources were checked, deterministic tests and solvers verified code paths, invalid runs were retained, and separate reanalysis and review challenged the implementation, raw logs, and claims. A human researcher remains responsible for all scientific judgments, this public release, and any future submission. No paid inference, external contact, human-subject activity, or venue submission occurred in producing v0.1.0.

## References

1. Gupta et al. “LLM Task Interference: An Initial Study on the Impact of Task-Switch in Conversational History.” *EMNLP 2024*. https://aclanthology.org/2024.emnlp-main.811/
2. Echterhoff et al. “Cognitive Bias in Decision-Making with LLMs.” *Findings of EMNLP 2024*. https://aclanthology.org/2024.findings-emnlp.739/
3. Bessis et al. “Legal Decision Biases in GPT: A Comparison with Human Judgment.” 2026. https://pmc.ncbi.nlm.nih.gov/articles/PMC13024114/
4. Laban et al. “LLMs Get Lost In Multi-Turn Conversation.” 2025. https://arxiv.org/abs/2505.06120
5. Mohammad Khalid et al. “ERGO: Entropy-guided Resetting for Generation Optimization in Multi-turn Language Models.” *UncertaiNLP 2025*. https://aclanthology.org/2025.uncertainlp-main.23/
6. Lee et al. “Lost in the Noise: How Reasoning Models Fail with Contextual Distractors.” 2026. https://arxiv.org/abs/2601.07226
7. Qin et al. “ImplicitMemBench: Measuring Unconscious Behavioral Adaptation in Large Language Models.” *ACL 2026*. https://aclanthology.org/2026.acl-long.1301/
8. Sclar et al. “Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design.” *ICLR 2024*. https://proceedings.iclr.cc/paper_files/paper/2024/hash/6c0e99d736da621403018ca7b32b1a4d-Abstract-Conference.html
9. Yao et al. “Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows.” 2026. https://arxiv.org/abs/2605.27922
10. Bean et al. “Measuring What Matters: Construct Validity in Large Language Model Benchmarks.” *NeurIPS Datasets and Benchmarks 2025*. https://papers.neurips.cc/paper_files/paper/2025/hash/1967e0fc3aa6cbbace562f5cb8e3954e-Abstract-Datasets_and_Benchmarks_Track.html
11. Geng et al. “JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models.” 2025. https://arxiv.org/abs/2501.10868

## Artifact pointers

- Complete claim-to-evidence map: `paper/appendix-artifact-index.md`.
- Repository entry points: `README.md`, `analysis/README.md`, and `runs/README.md`.
