# C06 contingency audit: audit-trail ablation for multi-agent judging

**Candidate:** Which logged artifacts are necessary to distinguish genuine deliberation gains from parser/fallback artifacts in multi-agent judging?
**Audit date:** 2026-07-17
**Verdict:** **PROMOTE — contingency only, after narrowing the claim**
**Constraint:** Literature and public-artifact audit only. No model calls, implementation, artifact modification, or spending was performed.

## Bottom line

The broad C06 claim is nearly killed. [Yang et al. (2026)](https://arxiv.org/abs/2607.08535) already state the exact attribution problem, describe a debate evaluator whose parse failures can default to option A or preserve the previous verdict, and prescribe the missing minimum trace: raw outputs, parse status, round verdicts, and fallback behavior. General audit-trail work also means that proposing an event schema is not by itself a scientific contribution. Multi-agent-debate papers already own round-count, ensemble-size, stability, and cost/accuracy ablations.

A narrower, conclusion-changing contingency does survive. A read-only integrity check of JudgeBench's released ChatEval output found that the artifact used to reproduce its published **34.00%** ChatEval score is not consistently associated with the enclosing benchmark rows and does not consistently contain the stated two-role debate. The released file is therefore sufficient to invalidate a clean interpretation of that number, but insufficient to reconstruct a corrected score or identify the root cause. This is the exact kind of case where an audit-complete rerun could change a scientific interpretation rather than merely improve engineering hygiene.

The surviving paper is not “logs are important.” It is:

> **A trace-complete forensic reproduction of one multi-agent judging pipeline that quantifies how data association, role construction, parsing, retries, and fallback policy alter measured accuracy, coverage, and the apparent benefit of debate.**

Promote this only as a fallback artifact paper. If an instrumented clean rerun does not change an accuracy, coverage, rank, or debate-versus-single-agent conclusion, C06 collapses to a useful engineering report and should not displace the main candidate.

## What is actually open and reproducible

The candidate does not name a specific implementation. The closest implied open pipeline is ChatEval because it is a canonical multi-agent LLM judge and JudgeBench explicitly evaluates it.

| Component | Publicly available | What can be reproduced | Missing or unstable |
| --- | --- | --- | --- |
| [Yang et al. debate experiment](https://arxiv.org/html/2607.08535) | Paper and aggregate results | The stated protocol and failure semantics can be inspected. | No code, raw response corpus, parser logs, parse-success flags, or public run manifest was found. The exact reported run cannot be re-audited. |
| [ChatEval](https://github.com/thunlp/ChatEval) | Apache-2.0 source, inspected at commit `56b320c04f311705e24922817172a6a4c4749325` | The multi-agent orchestration can be read and modernized. | Only two repository commits; mostly unpinned dependencies, a Git-head dependency, placeholder/hard-coded API configuration, and no released paper-result traces. The runner serializes only tail messages, while parser failures are retried without an exported attempt/status trail. |
| [JudgeBench](https://github.com/ScalerLab/JudgeBench) | Benchmark, scoring code, and raw outputs, inspected at commit `e2c52c284e735e139b3daa61c206ee208f36c461` | The published ChatEval metric can be recomputed from the released JSONL. | The current judge factory has no ChatEval implementation, and repository history did not reveal one. Thus the output exists but its generation path is absent. No license file was visible, so redistribution/reuse terms need clarification. |
| [LLMBar](https://github.com/princeton-nlp/LLMBar) | MIT-licensed data and evaluation code; 419 labeled pairs | A small clean benchmark alternative is available. | It does not supply the missing Yang or JudgeBench debate traces. |
| Original judge snapshot | JudgeBench names `gpt-4o-2024-05-13` in its raw file | The exact string and outputs are preserved. | Current official model listings do not expose that snapshot, and OpenAI's [backward-compatibility guidance](https://platform.openai.com/docs/api-reference/backward-compatibility) warns that behavior changes across model versions. A new run can be a reproduction, not an exact replication. |

There is therefore **no single turnkey public chain** from benchmark row to debate prompt to every attempt to parsed/fallback decision to published metric. Upstream ChatEval has source without full historical outputs; JudgeBench has outputs without the ChatEval generator. That split is itself the practical motivation for the minimum artifact below.

## Read-only forensic result on the released JudgeBench ChatEval file

The inspected file was:

`outputs/dataset=judgebench,response_model=gpt-4o-2024-05-13,judge_name=chat_eval,judge_model=gpt-4o-2024-05-13.jsonl`

Method: parse every released row; for each orientation and agent record, test exact inclusion of the enclosing question and both candidate responses in the stored prompt; count role pairs; and recompute the repository's official metric. This is a conservative association check—it does not require semantic similarity or subjective labeling.

| Integrity check | Result |
| --- | ---: |
| Benchmark rows | 350 |
| Swapped-order debate runs | 700 |
| Agent records | 1,400 |
| Agent records containing the enclosing row's exact question | **72 / 1,400** |
| Agent records containing both enclosing candidate responses | **70 / 1,400** |
| Orientations in which both agent records align to the enclosing row | **35 / 700** |
| Rows in which both orientations fully align | **6 / 350** |
| Expected one-`General Public`/one-`Critic` role pair | **400 / 700** |
| Duplicate `General Public` pairs | **175 / 700** |
| Duplicate `Critic` pairs | **125 / 700** |
| Published metric reproduced with the repository scorer | **34.00%** |

The failures are plainly substantive, not just punctuation differences. For example, one enclosing item concerns malicious-prosecution law while its stored debate prompt asks why a flock of birds would be called a society; the reverse orientation contains a marine-ecosystem question. This establishes that the released 34.00% file is not interpretable as a clean item-by-item measurement of ChatEval on JudgeBench.

As a diagnostic only, the tiny exact-alignment subsets score 53.3% for the 15 aligned original-order orientations and 60.0% after correcting orientation for the 20 aligned reverse-order orientations. These are **not corrected ChatEval estimates**: the subsets are tiny, selected post hoc, and nonrandom. They show only that filtering on an objective trace-integrity property materially changes the observed number and that a clean rerun is warranted.

This audit does **not** establish the corruption's root cause. The missing generator, request IDs, attempt logs, and full event history prevent distinguishing write-order bugs, stale-memory reuse, concurrency errors, row-index misalignment, serialization mistakes, or another mechanism.

## Direct predecessors and collision test

| Work | What it already owns | Collision with C06 | Remaining opening |
| --- | --- | --- | --- |
| [When the Judge Changes, So Does the Measurement](https://arxiv.org/abs/2607.08535) (Yang et al., 2026) | Exact warning that debate attribution is impossible without raw outputs and parser/fallback logs; a concrete default-A/carry-forward failure policy; minimum audit-trail fields. | **Very high.** C06 cannot claim discovery of the problem or the basic field list. | Yang cannot estimate deliberation because its own raw/parser traces were not retained. A trace-complete rerun that changes its interpretation remains open. |
| [ChatEval](https://arxiv.org/abs/2308.07201) (ICLR 2024) | Multi-agent judge roles, communication, and debate-based scoring. | **Very high on pipeline novelty.** | Does not release audit-complete event traces or a replay analysis of parser/fallback policies. |
| [Should We Be Going MAD?](https://proceedings.mlr.press/v235/smit24a.html) (ICML 2024) | Open benchmarking of multi-agent debate strategies; debate often fails to beat self-consistency/ensembling and is hyperparameter-sensitive. | **High on generic debate ablations.** | Does not center judgment-parser failures, data association, or replayable fallback policy. |
| [Multi-Agent Debate for LLM Judges with Adaptive Stability Detection](https://arxiv.org/abs/2510.12697) (2025) | JudgeBench/LLMBar evaluation; judgment distributions across rounds, ensemble sizes, and adaptive stopping. | **High on round dynamics and ensemble-size claims.** | Does not supply the proposed attempt-level parser/fallback audit. |
| [An Empirical Study of LLM-as-a-Judge](https://arxiv.org/abs/2506.13639) (2025) | Controlled prompt, decoding, and chain-of-thought design ablations for judge reliability. | **High on generic “design choices matter.”** | Not an event-provenance or silent-fallback study. |
| [Audit Trails for Accountability in Large Language Models](https://arxiv.org/abs/2601.20727) (2026) | General event schemas and audit-trail architecture for LLM systems. | **High on schema novelty.** | Does not quantify conclusion changes in a concrete multi-agent judge benchmark. |

### Kill test results

- **“Define the minimum logs.” — Failed.** Yang et al. already do this directly; general audit-trail literature supplies broader schemas.
- **“Ablate number of debate rounds or agents.” — Failed.** Prior multi-agent debate studies already own this space.
- **“Release a more reproducible ChatEval implementation.” — Insufficient.** Valuable engineering, but not a scientific contribution without a conclusion change.
- **“Show parser/fallback policies alter judge metrics.” — Survives conditionally.** It must be measured on a trace-complete clean run, with all attempts and failures counted.
- **“Show the released JudgeBench ChatEval result is not a clean measurement, then recover an interpretable estimate.” — Survives strongly.** The public raw artifact provides a concrete, falsifiable target; only the first half is currently established.

## Exact surviving contribution

The paper can claim only the following if the clean rerun supports it:

1. **Artifact finding:** the released JudgeBench ChatEval output that reproduces the published 34.00% metric contains systematic item/prompt association failures and duplicated role construction.
2. **Measurement finding:** after a clean, trace-complete rerun, quantify how much the apparent ChatEval accuracy and debate-versus-single-agent comparison change under strict trace-integrity validation.
3. **Mechanism finding:** use replay—not speculation—to decompose changes attributable to parser failure, retry selection, fallback policy, role construction, data association, and genuine round-to-round judgment movement.
4. **Reusable artifact:** publish an append-only event schema, validator, and policy-replay scorer that can recompute every reported number from immutable raw events.

The contribution fails if it stops at the first item. A corrupted release can support a reproducibility note, but the candidate's stated science question requires the second and third items. It also fails if it claims that the exact historical JudgeBench number has been “corrected” using a different model snapshot; that would be a new reproduction under a declared current model.

## Minimum publishable artifact

### A. Zero-call forensic package

1. A content-addressed manifest for the pinned JudgeBench file and repository commit.
2. A deterministic validator for row/question/response association, orientation pairing, role cardinality, score parseability, and metric recomputation.
3. A machine-readable exceptions table with row ID, orientation, agent role, failed invariant, and hashes of the enclosing/stored content.
4. Tests containing synthetic correct, swapped, duplicated-role, malformed-score, and missing-attempt records.
5. A report that reproduces 34.00% before showing the integrity failures; no silent row exclusion.

This package is enough for the artifact finding, not enough for a corrected capability estimate.

### B. Clean instrumented reproduction

Run one fixed public benchmark—preferably all 350 JudgeBench pairs, or LLMBar if JudgeBench licensing cannot be clarified—with both response orders and one pinned current open 4B–8B instruct model. Fourteen billion parameters are unnecessary and tight on the available 16 GB machine. Preserve the original two-role/four-turn structure where possible, plus a matched single-agent baseline.

Every append-only event needs:

- `run_id`, benchmark item ID, orientation ID, agent ID, role ID, round ID, and attempt ID;
- exact model/revision, tokenizer, runtime/container, chat template, decoding parameters, seed, and request hash;
- complete prompt, raw response, finish/error status, latency, token counts, and parent event IDs;
- parser version, parse success/failure, extracted fields, retry reason, and whether the retry changed prompt/state;
- explicit fallback action (`abstain`, retry, default-A, carry-forward, or other), intermediate verdict, and final verdict;
- environment lock, source commit, input/output hashes, and one-command metric reproduction.

### C. Offline replay and ablation

From the same immutable raw attempts, compare at minimum:

1. final verdict only;
2. round verdicts without raw/parse status;
3. raw outputs plus parser result;
4. complete attempts, retries, and fallback events;
5. strict abstention, bounded retry, default-A, carry-forward, and constrained-output policies;
6. clean trace-only versus all-run accuracy, coverage, order sensitivity, and failure rate;
7. debate versus matched single-agent/self-consistency under equal or explicitly reported inference budgets.

Do not condition the primary result on parseable outputs. Report an accuracy–coverage pair and count every assigned item. Policy replay is valid only where the same raw attempt supports the alternative; if a policy would alter subsequent prompts or state, rerun that preregistered branch instead of pretending it is offline-replayable.

## Feasibility

| Phase | Estimate | Feasibility |
| --- | --- | --- |
| JudgeBench forensic validator and report | 1–3 focused days; $0 | **High.** The released raw file and scorer are sufficient. |
| ChatEval modernization and event instrumentation | 4–8 focused days | **Moderate.** The code is small, but dependencies, provider assumptions, parser retries, and serialization need replacement rather than cosmetic logging. |
| Local smoke run | 20–40 items, both orders, two roles, four turns, plus baseline; roughly 200–500 calls | **High** with a quantized 4B model; hours rather than days. It validates plumbing only. |
| Full JudgeBench reproduction | 350 items × 2 orders × 4 debate turns = about **2,800 debate calls per model**, plus matched baselines and any non-replayable policy branches | **Moderate.** A 4B–8B quantized local run is plausible but may take days; a bounded cloud run should fit the candidate's $0–100 range after a priced pilot. |
| Exact historical replication | N/A | **Not feasible.** The original generator path is absent and the named 2024-05-13 proprietary snapshot is not currently exposed. |

The data volume is small. The main cost is provenance-correct orchestration, not storage. The strongest low-cost sequence is: release the zero-call integrity report; build the clean trace path; run a local plumbing subset; then seek approval for a frozen full run only if the instrumentation exposes nontrivial failure rates and the selected model is neither at floor nor ceiling.

Licensing is a real gate. ChatEval is Apache-2.0 and LLMBar is MIT. JudgeBench's repository did not expose a license in this inspection. Before redistributing its rows or derived bundled artifacts, obtain/locate explicit permission or switch the clean reproduction to LLMBar while publishing only hashes, row IDs, and a validator that users run against their own JudgeBench checkout.

## Promote / hold / reject decision

**PROMOTE — contingency only.** The original generic logging-ablation concept is rejected, but the released JudgeBench artifact creates a much sharper, evidence-backed study whose result is already capable of changing how a published metric is interpreted.

Promotion is conditional on four gates before any paid/full run:

1. independently reproduce the integrity counts from a fresh pinned checkout and archive hashes;
2. clarify JudgeBench reuse terms or move the clean run to MIT-licensed LLMBar;
3. freeze the event schema, parser, fallback policies, and matched baseline before seeing the full clean-run results;
4. require a conclusion-changing endpoint: accuracy/coverage, ordering, or debate-versus-baseline interpretation—not merely “more logs were collected.”

If the fresh-checkout counts fail to reproduce, **reject**. If they reproduce but a clean rerun cannot be built without a proprietary unavailable model or ambiguous data rights, **hold** as an artifact note. If the rerun is trace-complete and the attribution or debate conclusion changes, C06 earns the contingency publication slot.

## Search and evidence status

This bounded screen inspected primary papers and official repositories through 2026-07-17 for ChatEval, JudgeBench, LLMBar, multi-agent-debate reliability, adaptive debate judging, judge design ablations, parser/fallback behavior, and LLM audit trails. Repository claims above are pinned to the inspected commits, not inferred from READMEs alone. The negative claim is deliberately narrow: no public Yang implementation or complete ChatEval-to-JudgeBench generation chain was found in the paper, official repositories, or exact-title/author searches. Absence from this bounded search is not proof that no private or unindexed artifact exists.
