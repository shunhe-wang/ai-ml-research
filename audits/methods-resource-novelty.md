# Focused novelty and posture audit: pre-confirmatory harness and negative design case

**Audit date:** 2026-07-18
**Search cutoff:** 2026-07-18
**Verdict:** credible as a bounded methods/resource case study; no claim of a first method, first control, causal effect, or priority

## Audit question

Does the narrowed artifact support a defensible contribution as an authenticated pre-confirmatory harness and documented stop decision, rather than as a causal finding about sequential context carryover?

## Search boundary

This was a focused, adversarial novelty check, not a systematic review. It followed the direct predecessors already collected in [`f1-literature-novelty.md`](f1-literature-novelty.md) back to their primary publication pages, then checked the adjacent literatures most likely to absorb the narrowed contribution:

- sequential-history, task-interference, and prior-answer effects;
- multi-turn degradation, contextual distractors, and reset interventions;
- prompt-format, chat-template, and evaluation-harness sensitivity;
- construct validity and structured-output evaluation; and
- the repository's own authenticated runs, independent reanalysis, and hostile methods review.

The search used publisher proceedings, arXiv records, official documentation, and first-party benchmark repositories. It supports a cautious positioning decision; it cannot prove that no contemporaneous or poorly indexed artifact uses the same combination.

## Primary-source novelty matrix

| Adjacent primary source | What the source establishes | Consequence for this artifact |
| --- | --- | --- |
| [Gupta et al., *LLM Task Interference*, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.811/) | Conversational history from a switched task can materially change later-task performance across five datasets and 15 task switches. | The broad claim that earlier conversational work can impair a later target is already occupied. |
| [Echterhoff et al., *Cognitive Bias in Decision-Making with LLMs*, Findings of EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.739/) | BiasBuster includes sequential decision conditions and a 13,465-prompt dataset for prompt-induced, sequential, and inherent bias. | Prior model decisions affecting later institutional-style decisions are not a new object of study. |
| [Bessis et al., *Legal Decision Biases in GPT*, 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13024114/) | A controlled legal-style task varies evidence order and whether the model makes an intermediate judgment; the authors report order and intermediate-evaluation sensitivity and explicitly avoid a mechanism claim. | Neither legal/non-mathematical order effects nor prior self-judgment effects can be claimed as firsts here. |
| [Laban et al., *LLMs Get Lost in Multi-Turn Conversation*, 2025](https://arxiv.org/abs/2505.06120) and [Khalid et al., *ERGO*, UncertaiNLP 2025](https://aclanthology.org/2025.uncertainlp-main.23/) | Laban et al. compare fully specified single-turn tasks with incrementally revealed multi-turn tasks at large scale; ERGO tests an entropy-triggered prompt-consolidation reset on that setting. | Controlled non-mathematical multi-turn degradation and reset mitigation are prior art, even though those studies do not use independently complete cases with byte-identical fresh replay. |
| [Lee et al., *NoisyBench*, 2026](https://arxiv.org/abs/2601.07226) and [Qin et al., *ImplicitMemBench*, ACL 2026](https://aclanthology.org/2026.acl-long.1301/) | NoisyBench evaluates random documents, irrelevant chat histories, and hard negative distractors across 11 datasets; ImplicitMemBench uses learning/priming-interference-test protocols for procedural memory, priming, and conditioning. | Context load, semantic distractors, interfering turns, and rule-like behavioral carryover already have dedicated benchmarks. |
| [Yao et al., *Harness-Bench*, 2026](https://arxiv.org/abs/2605.27922) | Across 106 sandboxed tasks and 5,194 trajectories, the benchmark reports substantial variation across model-harness pairings and recommends configuration-level attribution rather than base-model-only attribution. | Treating the harness as part of the evaluated object is not novel; this repository is a much smaller sequential-history case study. |
| [Sclar et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/6c0e99d736da621403018ca7b32b1a4d-Abstract-Conference.html) and [Razavi et al., 2025](https://arxiv.org/abs/2502.06065) | Sclar et al. report large few-shot performance variation under meaning-preserving prompt formats and weak cross-model correlation in format performance; Razavi et al. introduce prompt-sensitivity prediction and PromptSET for slight prompt variations. | Prompt-format sensitivity and the danger of one arbitrary cross-model format are established concerns. |
| [Hugging Face Transformers chat-template documentation](https://huggingface.co/docs/transformers/v4.43.0/en/chat_templating) | The official documentation states that chat models can require different input formats and that the inference template should match the format used in training. | Rendering each snapshot's native chat template is sound implementation discipline, not a novel control. |
| [Bean et al., *Measuring What Matters*, NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/hash/1967e0fc3aa6cbbace562f5cb8e3954e-Abstract-Datasets_and_Benchmarks_Track.html) | A systematic review of 445 LLM benchmarks identifies construct-validity problems in measured phenomena, task operationalizations, and scoring metrics and provides eight recommendations. | The task substrate, item selection, exposure construction, and scoring contract must be treated as part of the claim's operationalization. |
| [Geng et al., *Generating Structured Outputs from Language Models*, 2025](https://arxiv.org/abs/2501.10868) and the [EleutherAI JSONSchemaBench task](https://github.com/EleutherAI/lm-evaluation-harness/blob/main/lm_eval/tasks/jsonschema_bench/README.md) | JSONSchemaBench evaluates structured generation; the lm-evaluation-harness implementation reports JSON validity separately from schema compliance and warns that sequence length varies with the tokenizer. | Strict JSON, schema compliance, and tokenizer-aware length accounting are established evaluation components, not contributions in isolation. |

## Repository evidence for the narrowed contribution

The potentially useful contribution is the inspectable combination and decision record, not any individual control and not an empirical carryover result.

| Repository artifact | What it authenticates | Limitation preserved by this audit |
| --- | --- | --- |
| [`publication-scope-v1.md`](../research/publication-scope-v1.md) | The frozen writing scope: a pre-confirmatory pipeline and negative design case, with causal, interaction, null, equivalence, family-level, and sample-size claims expressly excluded. | The scope is a writing boundary, not proof that the resource is novel or publishable. |
| [`independent-reproduction.md`](independent-reproduction.md) | An independent standard-library reanalysis reproduced all stored counts and diagnostics; 80 prompt and response hashes, 40 matched prompt-token pairs, and strict response shape were rechecked. | This is independent analysis of stored outputs, not a new inference run, backend replay, or upstream attestation of model weights. |
| [`methods-note-red-team.md`](methods-note-red-team.md) | The hostile review identifies the target overlap, invalid simultaneous-stability interpretation, missing causal controls, and crossed-history reuse that prevent promotion. | The executed positive-negative contrast cannot identify a history channel or support formal interaction or population inference. |
| [`family-canary-v1.md`](../analysis/family-canary-v1.md) | Named local snapshot/runtime/prompt configurations encountered bounded schema, task, or representation failures; the surviving Qwen and Llama diagnostics differ by world. | The screen was adaptive and tiny, and the Llama targets overlap Qwen; it does not estimate a family failure rate or constitute independent replication. |
| [`runs/README.md`](../runs/README.md) and immutable run directories | Failed canaries, prompt repairs, representation incompatibilities, exact prompts, raw responses, manifests, hashes, and retry ancestry are retained rather than silently discarded. | Retention and authentication improve auditability but cannot repair an underidentified design. |

## Surviving contribution and safe language

None of the following is novel by itself: executable answer keys, strict JSON, schema checks, native chat templates, token counting, prompt hashing, immutable logs, validity gates, independent reanalysis, or stopping rules. The search also does not establish priority for their combination.

The defensible contribution is therefore:

> A case study and reference implementation of a pre-confirmatory sequential-history evaluation workflow. It documents how native-template matching, strict response and task-validity gates, authenticated local runs, independent raw-log reanalysis, and adversarial methods review led to stopping an underidentified design before confirmatory scale-up.

Safe descriptors are **case study**, **technical report**, **reference implementation**, **reusable harness**, **negative design case**, and **pre-confirmatory stop record**. Avoid **first**, **novel method**, **causal carryover effect**, **mechanism**, **model-family comparison**, **replication**, **formal interaction**, **null result**, **equivalence**, and **validated sample-size requirement**.

The modest resource claim is strongest when tied to what a reader can inspect and reuse: exact task generators and solvers, native-template matching checks, failure-preserving run storage, response/task validity separation, artifact verification, and the explicit decision boundary between reproducible numbers and identified scientific conclusions.

## Decision

The artifact clears a narrow credibility threshold for a working technical report or repository release after final verification. It does **not** clear the threshold for an archival empirical paper about context carryover, and this audit does not establish that the resource itself is first or publication-worthy.

Before any public release:

1. rerun the focused primary-source search and check all links and bibliographic metadata;
2. keep every empirical statement subordinate to the authenticated local artifacts;
3. preserve the no-effect, no-mechanism, no-interaction, no-family-rate, and no-sample-size-claim boundary; and
4. label the Qwen/Llama outputs as overlapping calibration diagnostics, not independent replication.
