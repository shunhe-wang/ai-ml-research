# Adversarial literature and novelty audit: F1 — sequential case interference in rule-bound decisions

**Audit date:** 2026-07-17
**Verdict:** **Major revision**
**Confidence:** High that the broad claim is not novel; moderate that the bounded causal-decomposition study below remains novel.

## Executive finding

The F1 proposal does **not** survive in its present form. The literature already contains all of its broad ingredients separately and several in close combinations:

- unrelated conversational task history degrading a later target task ([Gupta et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.811/));
- earlier model answers changing later decisions in a persistent, same-task admissions conversation ([Echterhoff et al., Findings of EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.739/));
- order and intermediate-self-judgment effects in non-mathematical legal decisions ([Bessis et al., 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13024114/));
- controlled non-math multi-turn degradation with executable scoring ([Laban et al., 2025](https://arxiv.org/html/2505.06120));
- random-chat, token-load, and semantically hard distractor controls ([Lee et al., NoisyBench, 2026](https://arxiv.org/html/2601.07226)); and
- a stateless context-reset intervention that nearly restores single-turn performance ([Khalid et al., ERGO, UncertaiNLP 2025](https://aclanthology.org/2025.uncertainlp-main.23/)).

The original rationale—competitive-math evidence exists, natural-chat evidence is uncontrolled, therefore an exactly scored non-math replication is open—is consequently too weak. “Sequential case interference,” “prior model reasoning can pollute a later answer,” and “resets mitigate multi-turn degradation” are not defensible novelty claims.

A smaller contribution may survive: **a paired, token- and position-controlled causal decomposition of same-task carryover in independently complete cases governed by executable rules**. The novel object would not be the existence of interference. It would be identifying whether any excess error beyond neutral context load is caused by prior case inputs, prior labels, prior rationales, or the model's own generated decisions; whether semantic congruence or conflict matters; and which boundary operation actually removes it.

That contribution is worth a design pass, but F1 should no longer be ranked first merely because the Robust Reasoning Benchmark is math-only. It should advance only if the study implements the full identification conditions stated below.

## What the search falsified

### 1. “Earlier unrelated work degrades a later target” is already a named benchmark question

[Gupta et al.](https://aclanthology.org/2024.emnlp-main.811/) formalize **LLM task interference** as sensitivity of a target response to unrelated task history. They teacher-force correct responses into histories, vary history length, and evaluate 15 switches among summarization, question answering, sentiment, human-aging knowledge, and abstract algebra on GPT-3.5, GPT-4, Llama-2-7B-Chat, and Mistral-7B-Chat. Some task histories hurt, some help, and neither response length nor a coarse task-distance measure explains the pattern. This is a direct predecessor to the broad F1 question, not merely generic long-context background.

Its remaining gaps are narrower: task *switches* rather than independently sampled cases within one rule system; gold/reference histories rather than a factorial comparison with self-generated reasoning; no token-matched neutral history; and no case-boundary reset study. These are design opportunities, not permission to claim first observation.

### 2. Same-task decision carryover from the model's prior answers has already been tested

[BiasBuster](https://aclanthology.org/2024.findings-emnlp.739/) defines sequential bias as bias induced by previous model answers. In its synthetic university-admissions study, profiles and the model's admission decisions accumulate in one conversation, while different orderings expose the same profiles to different answer histories. The authors report substantial inconsistency, especially for Llama-2 models, and test awareness, counterfactual/contrastive examples, and post-hoc review mitigations. Their released benchmark contains 13,465 prompts, including 5,449 anchoring prompts.

This paper is closer to F1 than the shortlist acknowledges: it is a persistent conversation, a repeated institutional decision task, order variation, and explicit prior model decisions. Its key limitation is that admissions labels are subjective; there is no exact rule solver or objective decision margin. It also does not separate prior inputs, labels, gold rationales, self-generated rationales, neutral tokens, or hard resets. The surviving F1 contribution must be built around those differences.

### 3. A legal, non-math self-conditioning result now exists

[Bessis et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC13024114/) use six simplified Polish criminal cases in a 2 × 2 design: incriminating-first versus exonerating-first evidence, crossed with a single final judgment versus an intermediate judgment after the first evidence block followed by a final judgment. They ran 720 trials per model/prompt combination with GPT-4o and GPT-5.2 and found order and intermediate-judgment effects, attenuated in GPT-5.2. [Code and data are released](https://github.com/tfbessis/Legal-Biases-in-GPT).

The methods and limitations matter. Trials are independent across cases, so this is within-case rather than cross-case carryover. The authors also acknowledge that evidence order is confounded with prompt position and that an intermediate judgment may self-anchor the model for reasons other than legal commitment; they explicitly propose filler/padding and an unrelated intermediate-task control. These are unusually direct motivations for F1's controls. They also mean that “first controlled non-math/legal replication” would be false.

### 4. Controlled non-math degradation and reset mitigation are already established

[Laban et al.](https://arxiv.org/html/2505.06120) shard a fully specified task across conversational turns in code, SQL, API/action, GSM8K, data-to-text, and long-context summarization, generating more than 200,000 conversations over 15 models. For code, SQL, actions, and math, scoring is exact or executable. Average performance falls sharply in the sharded condition; analyses attribute failures to premature answers, early assumptions, and overreliance on prior answers. Their [artifact is public](https://github.com/microsoft/lost_in_conversation).

[ERGO](https://aclanthology.org/2025.uncertainlp-main.23/) then uses these tasks to test entropy-guided stateless resets. A reset consolidates all user inputs into a rewritten single prompt, generates in a fresh context, and continues from the rewritten prompt and answer. It compares this with the full, sharded, recap, Snowball/repetition, random-reset, and fixed-interval-reset conditions. For GPT-4o-mini, for example, the reported aggregate moves from 44.3 in the sharded condition to 71.8 with ERGO, near the 73.8 full-prompt result.

These studies concern one task disclosed over turns rather than independent cases. ERGO's reset also rewrites and consolidates the task, so context isolation is confounded with prompt optimization and possible semantic drift. Still, F1 cannot claim novelty for either non-math controlled degradation or stateless resets. It can compare a literal fresh-context replay with softer boundaries while holding the target and rules byte-identical.

### 5. Token load versus semantic distractors has already been separated

[NoisyBench](https://arxiv.org/html/2601.07226) evaluates 11 datasets under no-distractor, random-document, random-WildChat-history, and task-specific hard-negative conditions. It also includes a fixed-total-length mixture analysis, showing that distractor composition matters beyond length. The work spans retrieval, reasoning, alignment, and tool use, reports large model-dependent drops, and analyzes semantic similarity and attention to distractors. Its workshop version is available through [OpenReview](https://openreview.net/pdf?id=RuEGeSFMo9).

NoisyBench uses exogenous chat or generated hard negatives rather than the model's own earlier decisions on matched cases, and it does not study case boundaries. But a simple 2 × 2 of “more tokens versus conflicting content” would be incremental. F1 needs the source-of-history and case-structure factors, not just neutral versus semantic distractors.

### 6. Rule retention and long-history interference are now crowded too

[ImplicitMemBench](https://aclanthology.org/2026.acl-long.1301.pdf), an ACL 2026 long-paper oral, uses learning/priming–interference–test sequences to measure procedural rules, priming, and conditioning in 17 models. Its procedural-memory condition teaches a rule with examples, inserts 15 misleading turns, and tests a novel instance with deterministic validators; its priming experiment uses matched thematic and neutral controls. This is not a later independent adjudication task—retention of the learned behavior is the target—but it occupies the intersection of explicit rules, interfering turns, and exact scoring.

[Wang and Sun's PI-LLM benchmark](https://openreview.net/forum?id=XYyMoY5nbB) streams co-referenced key–value updates and finds log-linear retrieval decay under semantically similar earlier interference, including a constant-input-length control. Earlier overwritten values are a common error source, and “ignore earlier input” prompts are insufficient. This strengthens the need to distinguish memory competition from decision-rule carryover.

Finally, [Golikov et al.'s Robust Reasoning Benchmark](https://arxiv.org/html/2604.08571) directly evaluates the final math problem after a growing sequence of earlier problems while the model's prior chains of thought remain in context. It finds degradation for several open reasoning models and observes attention to distractor regions, while proprietary models are more resilient in the limited tested conditions. The authors correctly state that generalization beyond competitive math remains open, but that open question is now bounded by the non-math work above.

### 7. Prior-behavior steering and error inheritance further narrow the claim

[HistoryAnchor-100](https://arxiv.org/abs/2605.13825) gives 17 frontier models short high-stakes trajectories in ten domains, including legal and governance scenarios, followed by a forced-choice action. Three prior unsafe actions have little effect under a neutral system prompt for the strongest aligned models, but an added instruction to stay consistent with the history flips many of them toward unsafe actions; dose and action-label controls probe the effect. These are steps in one trajectory, not provably independent cases, and the largest effect depends on an explicit consistency cue. Even so, the paper already owns a broad “prior behavior steers later high-stakes decisions” claim. F1 should use neutral prompts and make independence normatively explicit.

[Contextual Drag](https://arxiv.org/abs/2602.04288) causally inserts one or two incorrect draft solutions before the same target problem across 11 models and eight reasoning tasks. It reports error-pattern inheritance and only partial recovery from feedback, verification, denoising, or fine-tuning. Because the drafts address the same problem, it leaves cross-case independence open, but it closes another possible framing: F1 is not the first controlled study of error inheritance from prior model outputs.

### 8. “Rule-bound plus irrelevant context” is not itself enough

[RULEARENA](https://aclanthology.org/2025.acl-long.27/) already supplies executable, objectively scored reasoning over real-world airline, tax, and sports rules, including irrelevant-rule selection and application. It does not manipulate sequential history, but it is direct prior art for the task substrate. [The Paradox of Robustness](https://arxiv.org/abs/2601.21439) perturbs high-stakes rule-bound decisions in healthcare, finance, education, and immigration with affective narratives and largely finds practical invariance across eight models. [CogniLoad](https://arxiv.org/abs/2509.18458) independently varies natural-language logic-task difficulty, length, and distractor density across 22 models and releases [code](https://github.com/kaiserdan/cogniload) and [data](https://huggingface.co/datasets/cogniloadteam/cogniload).

Together these papers rule out a generic claim of “first controlled non-math cognitive-load study” or “first irrelevant-context test in institutional rules.” The remaining distinction is **self- or model-generated history from provably independent cases**, decomposed into text, verdict, and rationale channels.

## Closest-paper matrix

| Work | What it actually tests | Why it threatens F1 | Gap that remains |
| --- | --- | --- | --- |
| [LLM Task Interference, EMNLP 2024](https://aclanthology.org/2024.emnlp-main.811/) | Later target after varying amounts of teacher-forced history from a different task; five exact/generative datasets, 15 task switches, four models | Directly owns unrelated-history interference and horizon effects | Different-task rather than same-rule cases; no neutral token match, self-generated-history factor, or reset |
| [BiasBuster, Findings EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.739/) | Persistent admissions conversation; same profiles in different orders; previous profiles and model decisions remain visible | Directly owns same-task sequential decision inconsistency from prior model answers | Subjective labels; no solver, margins, clean history decomposition, or hard reset |
| [Legal Decision Biases in GPT, 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC13024114/) | Evidence order and intermediate self-judgment in six legal cases, GPT-4o/GPT-5.2 | Owns controlled legal/non-math order and prior-output effects | Within-case only; position confound; no exact labels or unrelated-case history |
| [LLMs Get Lost in Multi-Turn Conversation, 2025](https://arxiv.org/html/2505.06120) | One task sharded across turns in six domains; exact/executable scoring in four; 15 models | Owns controlled non-math multi-turn degradation and prior-answer failure analysis | Incrementally revealed task, not complete independent cases; no literal fresh reset |
| [ERGO, UncertaiNLP 2025](https://aclanthology.org/2025.uncertainlp-main.23/) | Entropy-triggered stateless prompt-consolidation reset on sharded tasks, compared with recap, repetition, random, and periodic resets | Owns the claim that explicit stateless resets can restore performance | Reset rewrites the task; no byte-identical case replay or independent-case carryover |
| [NoisyBench, 2026](https://arxiv.org/html/2601.07226) | Random documents, random chat, semantic hard negatives, and fixed-length mixtures over 11 datasets | Owns broad token-load versus semantic-noise separation | Exogenous noise; no same-task prior labels/rationales or case-boundary interventions |
| [ImplicitMemBench, ACL 2026](https://aclanthology.org/2026.acl-long.1301.pdf) | Rule learning, 15 interfering turns, novel test; matched priming controls; deterministic validators where possible | Occupies rules + interference + exact scoring | Measures desired rule retention/priming, not errors on independent rule-governed cases |
| [Robust Reasoning Benchmark, 2026](https://arxiv.org/html/2604.08571) | Final AIME problem after earlier problems and model chains of thought; eight models; attention analysis | Directly owns sequential overload and prior-reasoning exposure | Competitive math only; limited proprietary-model horizon; no reset or causal history decomposition |
| [Proactive Interference / PI-LLM, 2026](https://openreview.net/forum?id=XYyMoY5nbB) | Sequential key–value overwrites with semantic interference and constant-length control | Owns semantic proactive interference beyond raw context length | Retrieval state rather than rule application; no decisions, rationales, or resets |
| [Do LLMs Benefit from Their Own Words?, 2026](https://arxiv.org/html/2602.24287) | Full versus user-only history on 300 real 5–10-turn conversations, with pairwise/scalar LLM judging | Owns the broad prior-assistant-output/context-pollution claim | Natural conversations are confounded and open-ended; no exact labels or controlled cases |
| [B-score, ICML 2025](https://b-score.github.io/) | Repeats a question 30 times in reset versus continuous histories; measures answer-distribution bias | Demonstrates carryover may reduce, not only increase, apparent bias | Repeated identical/subjective questions, not independently solved rule cases |
| [HistoryAnchor-100, 2026](https://arxiv.org/abs/2605.13825) | Prior unsafe actions followed by a high-stakes choice; neutral and consistency-instructed prompts; dose and label controls | Owns broad prior-behavior steering in legal/governance and other high-stakes settings | One continuing trajectory; strongest effect needs an explicit consistency cue; no exact independent-case rule labels |
| [Contextual Drag, 2026](https://arxiv.org/abs/2602.04288) | Incorrect prior drafts before the same target across 11 models and eight tasks; structural error-inheritance analysis | Owns causal prior-error inheritance and mitigation attempts | Same-problem drafts, not independent cases or prior outcome streaks |
| [RCWT, 2026](https://arxiv.org/html/2607.12216) | Fixed prompt budget with increasing coordination text; intact-task ablation keeps evidence complete while total length grows | Shows apparent “interference” may simply be task-budget displacement; intact exact task can remain perfect | Narrow synthetic recall setting, but a decisive warning for F1 controls |

## A bounded contribution that survives

The search did not locate a paper that jointly provides all of the following:

1. independently complete cases sampled from the **same executable institutional rule system**;
2. paired evaluation of the exact same target case under different histories, with the target case and governing rules fully intact;
3. token-, position-, and format-matched neutral histories and semantically congruent versus conflicting prior cases;
4. separate interventions for prior case inputs, prior gold labels, prior gold rationales, and the model's own prior labels/rationales; and
5. a boundary comparison among an instruction marker, deletion of assistant-side history, and a literal fresh context with byte-identical replay of system rules and target.

This combination supports a narrower scientific claim: **causal attribution and directional transport of history effects in repeated, rule-bound decisions**. It could determine whether the effect seen in math and multi-turn task disclosure transfers to independently adjudicated cases, whether an identical target moves toward or away from a prior outcome streak, and whether the operative channel is generic load, semantic competition, label anchoring, or self-generated rationale commitment.

The institutional framing is useful but should not be confused with novelty. Synthetic legal-style cases alone are not new, and anthropomorphic terms such as “cognitive overload,” “anchoring,” or “proactive interference” should be reserved for behaviorally discriminated mechanisms. The safe vocabulary is *history-induced excess error*, *label carryover*, *rationale carryover*, and *boundary intervention*.

## Rewritten research question

> **Under a fixed evaluation budget with the governing rules and target case fully intact, does a history of independently adjudicated cases from the same executable rule system change exact decision accuracy, rule-threshold error, or directional decision propensity beyond a token-, position-, and format-matched neutral history? If so, how much is attributable to semantic case conflict, prior outcome streaks, exposure to prior labels, and the model's own prior reasoning, and which boundary operation—marker only, assistant-history deletion, or fresh-context replay—removes the excess?**

This question is materially different from the shortlist version. It does not presuppose degradation, treats improvement and null effects as possible, does not equate a fresh API call with an underspecified “reset,” and makes the intact-target control central.

## Novelty condition

F1 should be represented as novel **only if**, by the preregistration cutoff, no prior paper or released artifact is found that jointly studies:

- same-task, independently complete, solver-labeled rule cases;
- paired target instances with byte-identical, fully intact rule and target blocks;
- token/position/format-matched neutral history and semantically congruent/conflicting case history;
- gold-versus-model-generated prior label and rationale arms; and
- soft boundary, assistant-deletion, and literal fresh-context interventions,

across at least two non-mathematical rule worlds and three model families.

The claim must be phrased as the **first joint causal decomposition under these identification conditions**, not the first sequential-interference study, first non-math replication, first rule-based benchmark, first prior-answer study, or first reset mitigation.

## Minimum design needed to earn that claim

### Unit and task

Use at least two, preferably three, synthetic rule-system families with executable generators and solvers. Every case must be complete on its own. Calibrate baseline difficulty before freezing the suite so target accuracy is neither at ceiling nor floor; an approximate 60–90% band is more informative than trivially perfect rule application. Preserve adversarial threshold margins so “threshold fidelity” is a defined observable—such as distance to an eligibility cutoff or the first misapplied rule—not a rhetorical synonym for accuracy.

The statistical unit is the **target case**, not the model call. Reuse each frozen target across all history and boundary conditions, randomize condition order outside the model context, and analyze paired differences with target-, model-, and rule-world-level uncertainty. Report label errors, rule/threshold errors, refusal/format errors, and invalid outputs separately.

### Required history arms

At minimum:

1. fresh-context baseline;
2. token-, position-, and surface-format-matched neutral material;
3. prior case inputs only, with no assistant turns;
4. prior cases plus gold labels but no rationales;
5. prior cases plus gold labels and gold rationales; and
6. prior cases plus the evaluated model's own sampled labels and rationales.

Cross the substantive case histories with congruent versus conflicting rules/thresholds, all-positive versus all-negative versus balanced prior-verdict streaks, and at least three predeclared horizons. The principal directional estimand should ask whether an identical target is more likely to receive outcome Y after an outcome-Y streak, beyond any change caused by case text or token load. Keep the target case and rule text identical across arms; never obtain “matching” by truncating or rewriting the target. If prompt limits bind, shorten history rather than target evidence.

### Required boundary arms

- **Soft marker:** “New independent case; do not rely on prior cases.”
- **Assistant deletion:** retain prior user cases but remove prior assistant outputs.
- **Hard fresh context:** replay the identical system/rule block and identical target in a new context.

Do not use an LLM-generated recap as the hard-reset condition. ERGO shows that consolidation can help, but rewriting changes information, organization, and difficulty. A recap may be a separate practical intervention after the causal comparison.

### Interpretation constraints

A history effect is not evidence of an attention mechanism, working-memory limit, anchoring, or human-like cognition. Mechanism language requires discriminating predictions: for example, a label-only effect without neutral-load effect supports label carryover more than generic overload; a self-rationale effect beyond gold-rationale exposure supports self-conditioning; a conflict-specific effect under fixed length supports semantic competition. API-level outputs alone do not establish internal attention allocation.

The null result is publishable only if the study has credible paired power and passes the intact-target, task-difficulty, and implementation checks. A null on easy cases or at short horizons is not a meaningful refutation of prior interference findings.

## Direct rejection conditions

Reject F1 rather than continue iterating if any of the following occurs:

1. **Direct prior art:** before preregistration, a paper or artifact is found that already combines independently complete same-rule cases, exact labels, matched load/semantic/source controls, and literal boundary resets.
2. **No identifiable excess effect:** after holding the target and rules fully intact and matching position/format, observed degradation reduces to target truncation, missing evidence, or output-format failure.
3. **Unusable task regime:** frozen baselines are above 95% or below 50% for most models, and difficulty cannot be recalibrated without post-treatment tuning.
4. **Solver or generator ambiguity:** two independent implementations do not agree on labels/rule traces, or history manipulations inadvertently change the target's governing semantics.
5. **Confounded reset:** the “reset” benefit appears only when the target or rules are summarized, reordered, simplified, or otherwise rewritten.
6. **Pseudo-replication:** conclusions rely on aggregate calls or repeated samples as independent observations without paired target analysis and clustered/hierarchical uncertainty.
7. **Only generic extreme-length noise:** semantic, label-source, and rationale-source contrasts are null, while only very long random material hurts. That result is already covered by context-noise work and is too incremental by itself.
8. **Single-snapshot fragility:** the effect appears in one model snapshot or one rule family and fails the predeclared cross-family replication criterion.
9. **Literature-positioning failure:** the paper omits or mischaracterizes LLM Task Interference, BiasBuster, Legal Decision Biases, Laban et al., ERGO, NoisyBench, ImplicitMemBench, RRB, or RCWT.
10. **Broad novelty language:** the project continues to claim discovery of sequential interference, cognitive overload, context pollution, legal order effects, or reset mitigation rather than the bounded causal decomposition.

## Verdict and recommendation

**Major revision.** The original F1 contribution is crowded enough that proceeding unchanged would invite an immediate related-work rejection. The strongest novelty rationale in the shortlist—math-only RRB plus uncontrolled natural chat—does not survive the 2024–2026 literature, especially LLM Task Interference, BiasBuster, the legal decision-bias study, Laban et al., ERGO, NoisyBench, and ImplicitMemBench.

The revised project can still be a credible first artifact because it asks a clean identification question with an exact solver, can produce a useful null, and connects evaluation methodology to repeated institutional decisions. Its value depends on rigorously isolating *what in prior cases carries over* and on literal context isolation. If resources permit only the original four context conditions or a generic neutral-versus-conflict comparison, reject F1 and promote another finalist.

## Search scope and residual uncertainty

This audit searched current primary literature and first-party records available through 2026-07-17 across arXiv, ACL Anthology, OpenReview, conference/proceedings pages, PubMed/PMC where relevant, and linked public repositories. Queries covered sequential/task/proactive interference, context pollution, prior-answer and self-conditioning effects, order effects, long-context distractors, case/legal carryover, conversation resets, and controlled non-math replications. Methods, ablations, and stated limitations were inspected for the closest works rather than relying only on abstracts.

The search is adversarial but not a proof of absence. “Rule-bound decision,” “case carryover,” and “self-conditioning” are not standardized keywords, and a contemporaneous July 2026 preprint may be indexed late. The novelty condition should therefore be rerun immediately before preregistration and submission, with backward/forward citation checks from the direct predecessors above.
