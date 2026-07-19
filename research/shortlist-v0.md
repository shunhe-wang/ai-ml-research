# Preliminary shortlist and research niches

Last updated: 2026-07-17

This ranking follows `protocol/promotion-standard.md`. Scores are provisional literature-screen scores, not final promotion decisions. A candidate can still be rejected after a direct-artifact audit.

## Updated rejection log

| Candidate | Status | Reason |
| --- | --- | --- |
| C01 decision-relevant judge reliability | Rejected as framed | [*When LLM Judge Scores Look Good but Best-of-N Decisions Fail*](https://arxiv.org/abs/2603.12520) already introduces decision-centric judge metrics. |
| C05 generic budget-optimal panels | Rejected as framed | Recent work on correlated panel errors, effective panel size, and calibrated aggregation makes a small cost/Pareto study too incremental. |
| C09 broad burden-of-proof calibration | Rejected as framed | [A February 2026 technical report](https://hermes-labs.ai/papers/asymmetric-burden-of-proof.pdf) directly studies asymmetric burden of proof, and [ICLR 2026 work](https://openreview.net/forum?id=EO6WtJ0q6G) studies confidence-threshold adherence and rationality. A narrower institutional-threshold task may survive only as part of a different mechanism. |
| C13 missing evidence: guess/abstain/ask | Rejected as framed | [*Value of Information: A Framework for Human-Agent Communication*](https://arxiv.org/abs/2601.06407) and related 2026 work directly formalize when agents should ask. |
| C17 generic multi-turn tool recovery | Rejected as framed | Tool-recovery benchmarks and methods are arriving rapidly, including [ReIn](https://openreview.net/forum?id=4J3kkHI6m5) and within-episode recovery work. |
| C19 policy compliance during recovery | Rejected as framed | [Solver-aided compliance](https://arxiv.org/abs/2603.20449), [near-miss detection](https://arxiv.org/abs/2603.29665), [policy-invisible violations](https://arxiv.org/abs/2604.12177), SafeClawBench, and τ-Knowledge substantially occupy policy-aware tool behavior. |
| C20 outcome success versus process validity | Rejected as framed | [Procedure-Aware Evaluation](https://arxiv.org/abs/2603.03116), [ProcBench](https://arxiv.org/abs/2605.20251), and Near-Miss directly study corrupt success and latent procedural failures. |
| C21 causal value of deliberation | Hold, below finalist line | Important but increasingly crowded, and a convincing matched-budget study would cost more than the current first-project alternatives. |
| C24 cross-provider reproducibility envelope | Hold, below finalist line | Judge-replacement work published in July 2026 is very close; longitudinal API dependence also weakens reproducibility. |
| C25 semantic-preservation audit alone | Merge into finalist F2 | FormInv already audits bad paraphrases and ranking changes. A viable contribution must jointly analyze variant validity *and* dependence/uncertainty across multiple dynamic benchmark generators. |

## Ranked surviving candidates

| Rank | Candidate | Score / 60 | Hard-gate status | Main reason |
| ---: | --- | ---: | --- | --- |
| 1 | F1: Sequential case interference in rule-bound decisions (evolved C28) | 55 preliminary | **Major revision after audit** | Broad interference and reset claims are occupied; only a paired causal decomposition of directional cross-case carryover under exact rules may survive. |
| 2 | F2: Are dynamic benchmark variants independent evidence? (C03 + C25) | 54 preliminary | **Major revision after audit** | FormInv and prompt-dependence work defeat the broad claim; only a cross-generator joint validity-bias and inferential-miscoverage estimand may survive. |
| 3 | F3: Temporal rule-version fidelity beyond code (C16) | 54 preliminary | **Rejected as stated after audit** | ICAIL 2026 directly studies historical-version statutory QA, stale rules, recency bias, and temporally filtered retrieval; only a new high-risk causal applicability pivot remains. |
| 4 | C06 audit-trail ablation for multi-agent judging | 49 | Provisional pass | Explicit gap and bounded replication, but artifact availability and narrowness are concerns. |
| 5 | C04 rubric portability audit | 47 | Provisional pass | Important distribution-shift question, but comparable human/model response data may be hard to obtain cleanly. |
| 6 | C10 evidence-order invariance | 46 | Novelty uncertain | Very feasible and falsifiable, but a direct order-effects predecessor likely exists. |
| 7 | C03 dependent-case uncertainty alone | 45 | Borderline | Correct problem, but may look like standard clustered inference unless it changes scientific conclusions. |
| 8 | C27 human-disagreement-aware judge reanalysis | 44 | Borderline | Low-cost and credible, but likely incremental relative to existing uncertainty-stratified evaluation. |

## Finalist F1 — Sequential case interference in rule-bound decisions

- **Revised working question:** With governing rules and target case held byte-identical and fully intact, does a history of independently adjudicated same-rule cases change exact decisions beyond token-, position-, and format-matched neutral history? Which part of the history—case text, outcome label, gold rationale, or the model’s own rationale—carries any directional effect, and which boundary operation removes it?
- **Revised contribution:** A paired causal decomposition of directional cross-case carryover in independently complete, solver-labelled rule decisions, distinguishing generic load, semantic conflict, label carryover, rationale carryover, and literal context isolation.
- **Why only the revision survives:** LLM Task Interference, BiasBuster, controlled legal order effects, Laban et al., ERGO, NoisyBench, ImplicitMemBench, RRB, HistoryAnchor-100, and Contextual Drag collectively defeat claims to discovering sequential interference, non-math degradation, prior-output pollution, or reset mitigation. The search did not find their joint identification design in exact same-rule cases.
- **Smallest credible study:** At least 2 non-math executable rule worlds and preferably 3, paired frozen targets, neutral/case-text/gold-label/gold-rationale/self-rationale history arms, positive/negative/balanced verdict streaks, multiple horizons, and soft-marker/assistant-deletion/literal-fresh-context boundaries across at least 3 model families.
- **Likely useful result:** Causal attribution of an effect beyond load, or a well-powered null that sharply bounds when independently complete cases do not contaminate one another.
- **Primary risk:** The necessary factorial design may exceed a “small” first project, while any cheaper subset becomes an incremental context-noise replication.

## Finalist F2 — Are dynamic benchmark variants independent evidence?

- **Revised working question:** Across established dynamic-benchmark generators, how much do semantic-invalidity bias and within-seed dependence separately and jointly distort paired model gaps, interval coverage, and simultaneous rank confidence sets over repeated independent generator draws?
- **Revised contribution:** A common repeated-generation protocol and generator-level bias–coverage profile that estimates valid-variant performance over seed populations, calibrates naive versus family-aware interval coverage, and measures scientific-decision disagreement.
- **Why only the revision survives:** FormInv already combines validity checks, equivalence families, bootstrap uncertainty, and rank reversals; prompt-dependence and rank-interval work already provide hierarchical inference; PTEB and DyCodeEval already repeat dynamic generation. No audited work was found that measures validity bias and inferential miscoverage jointly across materially different open generators.
- **Smallest credible study:** At least 2 established open generators with different sampling hierarchies, independent deterministic or blinded expert validity adjudication, repeated complete generator draws, seed-cluster bootstrap plus a paired multilevel model, and simultaneous rank confidence sets across multiple models and task settings.
- **Likely useful result:** A reusable bias–coverage audit that shows when generator validity and family dependence change rank sets or evaluation-budget decisions—or a powered negative result showing current generators are robust under this stricter analysis.
- **Primary risk:** Independent validity ground truth and repeated generator runs may make the credible study too large; any one-generator or one-dataset reduction collapses to already-published work or standard clustered inference.

## Rejected finalist F3 — Temporal rule-version fidelity beyond code

- **Disposition:** Reject the finalist as stated. [*Asking For An Old Friend*](https://arxiv.org/abs/2605.23497) (ICAIL 2026) already tests post-cutoff staleness, historical-version recency bias, version application, and temporally filtered retrieval on expert-validated statutory questions. CLAW, DeonticBench, GitChameleon 2.0, Quantum API Drift, and temporal context-memory work occupy the remaining benchmark components.
- **Only plausible new candidate:** Directly observe event-date-to-version selection, oracle-conditioned rule execution, and end-to-end decisions; estimate version-consistent substitution errors; and test whether temporal applicability creates an interaction beyond matched position, “latest” labels, and generic context-memory conflict.
- **Why this is not a light revision:** The contribution changes from introducing a benchmark/problem to a causal mechanism study, and it requires counterfactually discriminating cases plus a version-by-item execution matrix.
- **Primary risk:** Even the pivot may be an overassembled bundle of known components; novelty depends on a clean temporal-applicability interaction and a credible small real-rule validation.

## Recommended research niches

### Niche A — Behavioral reliability of AI decision systems under institutional constraints

- **Central questions:** Do models follow explicit thresholds, precedence rules, temporal versions, and procedural boundaries? Which invariances should a reliable decision system satisfy?
- **Why it matters / comparative advantage:** These are general reliability questions that benefit from rigorous institutional thinking. The advantage is the ability to formalize rules, evidence burdens, remedies, and procedures—not merely supply legal text.
- **Skills to build:** Experimental design, probabilistic modeling, domain-specific languages, property-based testing, mixed-effects models, and benchmark validation.
- **Leading work/groups to follow:** Stanford CRFM evaluation work; Princeton/Sierra agent evaluation (τ-bench/τ-Knowledge); OpenAI instruction-hierarchy research; researchers around AI-agent infrastructure such as Gillian Hadfield, Seth Lazar, and Alan Chan.
- **Important recent anchors:** [Infrastructure for AI Agents](https://openreview.net/forum?id=Ckh17xN2R2), [Instruction Hierarchy](https://arxiv.org/abs/2404.13208), [τ-Knowledge](https://openreview.net/forum?id=XHZK5abtw2), [ToolBench-X](https://arxiv.org/abs/2606.25819).
- **Venues:** TMLR; ACL/EMNLP Findings; AAMAS; ICML/NeurIPS workshops on agents, evaluation, safety, or mechanism design.
- **Three-paper sequence:** (1) sequential case interference; (2) temporal/authority rule fidelity; (3) policy-compliant agent recovery with formal enforcement baselines.
- **Avoiding the lawyer pigeonhole:** Use executable abstract rule worlds, make claims about model behavior, compare against ML baselines, and treat law as one validation domain rather than the contribution.

### Niche B — Measurement validity for model-based evaluation

- **Central questions:** When do LLM judges or dynamic benchmarks produce valid rankings, calibrated uncertainty, and reproducible conclusions?
- **Why it matters / comparative advantage:** AI research increasingly delegates evaluation to models. Legal training in evidence and standards of proof helps frame validity questions, but the work must be statistical and empirical.
- **Skills to build:** Measurement theory, calibration, hierarchical models, bootstrap/conformal methods, causal inference, and reproducible evaluation harnesses.
- **Leading work/groups to follow:** LMSYS/Chatbot Arena; Stanford HELM/CRFM; Salesforce AI Research judge benchmarks; Apple ML judge-panel work; TMLR/MLRC reproducibility community.
- **Important recent anchors:** [Fiedler 2026](https://arxiv.org/abs/2605.06939), [JETTS](https://openreview.net/forum?id=CgJEHynkJt), [CARE](https://openreview.net/forum?id=XdcofpTCyq), [FormInv](https://openreview.net/forum?id=X8Fdpx4GX9), [Beyond correlation](https://openreview.net/forum?id=E8gYIrbP00).
- **Venues:** TMLR; NeurIPS Evaluations & Datasets; MLRC; ACL/EMNLP evaluation workshops.
- **Three-paper sequence:** (1) dynamic-variant dependence audit; (2) rubric portability across response distributions; (3) decision-valid calibration for judge panels.
- **Avoiding the lawyer pigeonhole:** Lead with estimands, uncertainty, baselines, and reusable tooling. Do not analogize judges to courts unless it clarifies a formal property.

### Niche C — Reproducible science for long-horizon and tool-using agents

- **Central questions:** Which agent improvements survive matched budgets, clean baselines, implementation changes, and independent reproduction? What trace evidence is necessary to support causal claims?
- **Why it matters / comparative advantage:** Agent papers are vulnerable to harness artifacts and protocol ambiguity. Litigation-style attention to records and audit trails becomes valuable when converted into schemas, validators, and experiments.
- **Skills to build:** Agent harness engineering, fault injection, event schemas, containerized reproduction, statistical power analysis, and systems measurement.
- **Leading work/groups to follow:** Princeton/Sierra τ-bench; Microsoft AgentRx; MLRC; SWE-bench ecosystem; groups working on ToolBench-X and ToolFailBench.
- **Important recent anchors:** [AgentRx](https://openreview.net/forum?id=VDQkzHwidO), [ToolRL-DR](https://arxiv.org/abs/2605.11928), [ToolFailBench](https://arxiv.org/abs/2607.04686), [Treat LLM Agents as Programmable Subjects](https://openreview.net/forum?id=8W6hjNj4Kf).
- **Venues:** MLRC; TMLR; AAMAS/ICML/NeurIPS agent workshops; systems-oriented workshops where evaluation artifacts are central.
- **Three-paper sequence:** (1) audit-complete reproduction of a claimed agent gain; (2) controlled multi-turn recovery study; (3) cross-harness reproducibility standard and reference implementation.
- **Avoiding the lawyer pigeonhole:** Ship runnable infrastructure, deterministic validators, and causal ablations; never rely on “audit” as rhetoric alone.

## Current recommendation

F1 remains the leading candidate only provisionally and only in its narrower causal-decomposition form. F2 is a more domain-neutral alternative but now requires a demanding repeated-generator coverage study. F3 is rejected as stated; its temporal-applicability pivot will be assessed as a new, high-risk candidate so the audit record is not lost.

No finalist is selected yet. Each now needs independent adversarial literature, design, statistics, implementation, reproducibility, venue, and red-team review as required by the goal.
