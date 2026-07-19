# Literature leads for a first independent project

Last updated: 2026-07-17

This is a lead register, not a novelty memo. A limitation stated by an author is evidence that the paper did not answer a question; it is not evidence that nobody else has answered it.

## High-signal leads

### 1. LLM judges are a measurement system, not a neutral oracle

Yang, Hou, and Yang study evaluator replacement, bias, correlated jury errors, and debate auditability. Their validity discussion explicitly leaves calibration, long-form rationale quality, domain-specific consistency, additional languages, and broader instruction distributions open. Their main result also suggests that adding jurors may contribute little when errors are correlated. [Paper](https://arxiv.org/abs/2607.08535)

Fiedler shows that naive LLM-judge estimates are biased and that shared calibration can even reverse the apparent direction of model comparisons. The paper is limited to binary outputs and does not address ordinal or continuous scores, dependent inputs, adaptive collection, or nonlinear metrics. [Paper](https://arxiv.org/abs/2605.06939)

Gupta and Kumar find substantial per-document transitivity failures and use conformal prediction-set width as an instance-level reliability diagnostic, but study SummEval and four evaluation criteria. This makes cross-task and decision-relevant validation a plausible extension, not a proven gap. [Paper](https://openreview.net/forum?id=FbDuesI6tD)

Zhao et al. propose confounder-aware aggregation of multiple LLM judges. This substantially raises the novelty bar for any generic claim that majority vote is inadequate. [Paper](https://openreview.net/forum?id=XdcofpTCyq)

**Research leads:** decision-relevant rather than aggregate judge reliability; ordinal-score calibration; reliability under dependent case families; rubric portability; correlation-aware panel selection under a fixed budget; audit-trail completeness as an experimental factor.

### 2. Tool-agent benchmarks are moving from clean calls to recovery behavior

ToolRL-DR reports a systematic sim-to-real tool-use gap and explicitly leaves multi-turn recovery, larger model scale, and transition robustness open. Its single-turn setting cannot measure error accumulation or clarification behavior. [Paper](https://arxiv.org/abs/2605.11928)

ToolBench-X introduces recoverable specification drift, invocation errors, execution failure, output drift, and cross-source conflict. It sharply narrows the room for a generic “tools can be unreliable” benchmark; a useful extension needs a distinct mechanism, such as policy-constrained recovery or the value of diagnostic information. [Paper](https://arxiv.org/abs/2606.25819)

ToolFailBench distinguishes tool skipping, result ignoring, output fabrication, and unnecessary tool use. Its limitations identify multi-turn state updates, recovery from earlier mistakes, shared judge blind spots, domain coverage, and future contamination as unresolved. [Paper](https://arxiv.org/abs/2607.04686)

**Research leads:** controlled multi-turn recovery; whether agents request the right missing information; policy compliance during recovery; diagnostic hints versus generic extra tokens; outcome-equivalent but process-invalid trajectories; held-out task generation for post-release contamination.

### 3. Long reasoning chains may create controlled cognitive interference

Golikov et al. report reasoning degradation from preceding problems and explicitly restrict their study primarily to competitive mathematics. They identify legal, medical, and coding generalization and optimal subtask granularity as open questions. [Paper](https://arxiv.org/abs/2604.08571)

**Research leads:** replicate the interference effect on low-compute, programmatically verifiable rule systems; distinguish mere context length from semantic conflict; test reset granularity without claiming architectural causality.

### 4. Prompt sensitivity is documented; predicting or controlling it remains difficult

PromptSET frames prompt-sensitivity prediction as a task and reports that self-evaluation, classifiers, and query-performance predictors struggle. The work focuses on QA-derived prompt variants. [Paper](https://arxiv.org/abs/2502.06065)

**Research leads:** sensitivity prediction for structured decisions; whether disagreement features predict instability; sensitivity under semantically equivalent rule presentations rather than generic wording variants.

### 5. Conflicting evidence now has direct benchmarks

ConflictScore and ConflictBench directly measure whether responses acknowledge coexisting support and contradiction. This makes a broad “LLMs fail on conflicting evidence” paper insufficiently novel. [Paper](https://openreview.net/forum?id=JRqzDZ6EiD)

FactConf studies conflict between parametric knowledge and external evidence. [Paper](https://openreview.net/forum?id=VgEEl1UDlg)

**Research leads:** decision thresholds under controlled evidentiary conflict; source-reliability and burden-allocation mechanisms; order and advocacy effects after holding the evidence graph fixed.

### 6. Legal benchmarks are broad, but mostly measure competence rather than controlled behavior

LEXam includes multilingual, long-form law examinations with reference guidance and validated LLM judging. Its authors leave broader common-law/civil-law and cross-cultural evaluation open, and note possible temporal staleness in legal materials. [Paper](https://arxiv.org/abs/2505.12864)

Juvekar et al. evaluate Indian legal examinations and explicitly list exam representativeness, limited model selection, endpoint variance, and assessor sample size as limitations. [Paper](https://arxiv.org/abs/2510.17900)

Shen et al. create a structured legal-reasoning benchmark organized around facts to prove, evidence, and experience. [Paper](https://arxiv.org/abs/2503.00841)

**Research leads:** controlled behavioral tests using synthetic, executable rules rather than another exam benchmark; time-indexed rule fidelity; procedure/relief invariance; reproducible meta-evaluation of legal-answer judges.

### 7. Rule-bound emotional-framing robustness has already been studied

The TMLR submission *The Paradox of Robustness* tests affective framing in rule-bound institutional tasks and reports small effects. It was rejected and remains useful as a warning: a generic “does emotional framing bias institutional LLM decisions?” study is no longer novel. [Paper](https://openreview.net/forum?id=2XPD66IiQI)

**Research consequence:** reject generic emotional-framing studies unless the contribution is a materially different mechanism, stronger identification strategy, or independent high-value replication.

### 8. Multi-agent systems need baselines that test whether interaction adds value

Garcia et al. reproduce an LLM stakeholder-negotiation study and show that single-agent or communication-free approaches can match multi-agent negotiation in many settings. [Paper](https://openreview.net/forum?id=MTrhFmkC45)

Zhang et al. identify “lazy agents,” where one agent dominates and the system collapses toward a single-agent process. [Paper](https://openreview.net/forum?id=5J6u03ObRZ)

**Research leads:** causal contribution of deliberation in judgment panels; communication-free and shuffled-message baselines; whether diversity helps only on identifiable task slices.

### 9. Contamination work makes ordinary benchmark refreshes a weak contribution

CoDeC, DyVal, DyCodeEval, and recent surveys already cover contamination detection and dynamic evaluation. A new benchmark needs a sharper property than simply generating variants. [CoDeC](https://openreview.net/forum?id=YlpaaYxx4t) · [DyVal](https://openreview.net/forum?id=SRB8ricWVr) · [DyCodeEval](https://openreview.net/forum?id=3BZyQqbytZ) · [TMLR survey](https://openreview.net/forum?id=SxNMjbtdFm)

**Research leads:** contamination-resistant controlled rule worlds whose labels are generated by executable specifications; empirical comparison of variant generators on semantic-preservation error.

### 10. Human uncertainty must be modeled rather than erased

The ICLR 2025 paper *Beyond correlation* argues that a single aggregate correlation can hide important differences between human labels and automatic evaluators, and recommends stratifying by human-label uncertainty. [Paper](https://openreview.net/forum?id=E8gYIrbP00)

**Research leads:** distinguish clear cases from genuinely contestable cases; evaluate judge reliability against adjudicative consequences and human disagreement strata rather than one pooled agreement number.

## Immediate rejections or high novelty barriers

- Generic LLM-judge position/verbosity bias benchmark — heavily occupied.
- Generic majority-vote panel study — correlated-error and aggregation papers already exist.
- Generic tool unreliability benchmark — ToolBench-X, ToolRL-DR, and ToolFailBench already occupy it.
- Generic prompt-sensitivity benchmark — numerous existing benchmarks; needs a new estimand or domain mechanism.
- Generic conflicting-evidence benchmark — ConflictBench and FactConf are direct predecessors.
- Another law-exam benchmark — LEXam and jurisdiction-specific exam studies already provide strong baselines.
- Generic affective-bias-in-institutions paper — *Paradox of Robustness* is too close.
- Multi-agent negotiation without a communication-free baseline — known validity failure.
- Static benchmark whose sole novelty is new questions — weak and contamination-prone.
