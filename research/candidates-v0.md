# Candidate projects — broad screen

Status: `lead` for every candidate. These are not novelty claims. Costs exclude the researcher's time and assume either local open-weight inference or tightly capped API experiments; current provider prices must be rechecked before an approved run.

Difficulty uses a 1–5 scale. “Collab: helpful” means expert review would materially improve the work but is not required for a defensible first release.

## Evaluation and LLM-as-judge

### C01 — Decision-relevant judge reliability

- **Question / smallest contribution:** When two systems are compared by an LLM judge, how often do judge errors change the downstream select/deploy decision, rather than merely reduce label agreement? Release a decision-weighted meta-evaluation on two public human-rated datasets.
- **Why care / closest work / exact gap:** Existing work studies bias, agreement, calibration, transitivity, and uncertainty, but usually pools errors rather than weighting the decisions they alter. Closest: [Fiedler 2026](https://arxiv.org/abs/2605.06939), [Gupta & Kumar 2026](https://openreview.net/forum?id=FbDuesI6tD), and [Beyond correlation](https://openreview.net/forum?id=E8gYIrbP00). Novel only if decision-weighted conclusions differ materially from aggregate metrics and no direct predecessor is found.
- **Data / models / compute / cost:** SummEval plus one pairwise-preference dataset; 3–5 open judges and optionally 2 APIs; 3 repetitions. Rough cost $0–$250.
- **Difficulty / timeline / skills / collaborator:** 3/5; 4–6 weeks; Python, bootstrap inference, decision analysis; statistician helpful.
- **Format / venues:** Short empirical paper + evaluation code; TMLR or an ML evaluation/reproducibility workshop.
- **Useful null / strongest risk:** A null would show aggregate reliability is an adequate proxy in these settings. Main risk: “downstream decision” choices may look arbitrary.

### C02 — Ordinal LLM-judge calibration under model comparison

- **Question / smallest contribution:** Do calibration corrections for 1–5 judge scores remain valid when comparing response generators with different output distributions? Extend binary bias diagnostics to ordinal scores on one public dataset.
- **Why care / closest work / exact gap:** [Fiedler 2026](https://arxiv.org/abs/2605.06939) explicitly limits its framework to binary outputs; ordinal/continuous settings are open. Novelty requires a statistically sound ordinal estimand and evidence not covered by existing ordinal judge-calibration work.
- **Data / models / compute / cost:** SummEval or TopicalChat human ratings; 3 open judges; simulations plus cached or local outputs; $0–$100.
- **Difficulty / timeline / skills / collaborator:** 4/5; 6–8 weeks; ordinal regression, bootstrap/calibration, Python; statistical collaborator strongly helpful.
- **Format / venues:** Measurement paper; TMLR, AISTATS workshop, or evaluation workshop.
- **Useful null / strongest risk:** Null maps where binary lessons transfer. Risk: technical novelty may be too incremental for the required statistical effort.

### C03 — Dependent-case uncertainty for LLM judges

- **Question / smallest contribution:** How badly do ordinary confidence intervals understate uncertainty when benchmark items are related variants of the same base case? Provide cluster-aware estimates on generated case families.
- **Why care / closest work / exact gap:** [Fiedler 2026](https://arxiv.org/abs/2605.06939) excludes dependent test inputs; dynamic benchmarks create exactly this dependence. The contribution is novel only if it quantifies practical ranking/coverage changes, not merely restates clustered standard errors.
- **Data / models / compute / cost:** Public benchmark seeds with 5–10 controlled variants each; cached candidate responses or 2–4 open models; $0–$150.
- **Difficulty / timeline / skills / collaborator:** 3/5; 4–6 weeks; hierarchical bootstrap, mixed models; statistician helpful.
- **Format / venues:** Technical note + reusable analysis package; MLRC, TMLR, evaluation workshop.
- **Useful null / strongest risk:** Null justifies simpler analyses for tested variant families. Risk: reviewers may see it as textbook statistics applied to LLMs.

### C04 — Rubric portability audit

- **Question / smallest contribution:** Does a rubric calibrated on model-written answers retain validity on concise human answers, cross-domain answers, or a second generator family? Audit one published judge prompt across controlled distribution shifts.
- **Why care / closest work / exact gap:** [LEXam](https://arxiv.org/abs/2505.12864) notes distribution shift between human and model answers; judge-reliability work emphasizes dataset slices. The gap is systematic cross-distribution rubric portability with human anchors.
- **Data / models / compute / cost:** One dataset with human and model responses or two public response corpora; 3 judges; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; sampling, reliability statistics, rubric analysis; domain annotator helpful.
- **Format / venues:** Robustness audit; ACL Findings or evaluation workshop.
- **Useful null / strongest risk:** Stability would validate reuse boundaries. Risk: obtaining comparable human answers and labels may be difficult.

### C05 — Budget-optimal judge panels under correlated error

- **Question / smallest contribution:** Given a fixed inference budget, when is one strong judge better than a diverse panel of weaker judges? Publish Pareto curves using measured error correlations and costs.
- **Why care / closest work / exact gap:** [Yang et al. 2026](https://arxiv.org/abs/2607.08535) shows correlated jury errors; [CARE](https://openreview.net/forum?id=XdcofpTCyq) proposes principled aggregation. The gap must be a transparent cost-constrained selection rule validated out of sample, not another majority-vote comparison.
- **Data / models / compute / cost:** Two public judge benchmarks; 6–10 mostly open judges; current serving costs; $50–$300.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; optimization, resampling, API accounting; no collaborator necessary.
- **Format / venues:** Empirical study + selection tool; evaluation workshop or TMLR.
- **Useful null / strongest risk:** A null tells users to buy the strongest single judge. Risk: prices and models drift quickly.

### C06 — Audit-trail ablation for multi-agent judging

- **Question / smallest contribution:** Which logged artifacts are necessary to distinguish genuine deliberation gains from parser/fallback artifacts in multi-agent judging? Re-run one open debate pipeline with complete event logging and ablations.
- **Why care / closest work / exact gap:** [Yang et al. 2026](https://arxiv.org/abs/2607.08535) explicitly finds debate attribution limited by missing raw outputs and parser logs. Novelty requires demonstrating that conclusions change under audit-complete analysis.
- **Data / models / compute / cost:** LLMBar or JudgeBench; open 4B–14B models; $0–$100 local/cloud compute.
- **Difficulty / timeline / skills / collaborator:** 3/5; 4–6 weeks; pipeline instrumentation, parsers, paired tests; no collaborator necessary.
- **Format / venues:** Reproducibility/negative-result paper; MLRC, workshop, technical report.
- **Useful null / strongest risk:** Null validates the original qualitative pattern while providing a reusable logging schema. Risk: too implementation-focused unless it changes scientific interpretation.

### C07 — Can judge disagreement predict its own unreliability?

- **Question / smallest contribution:** Do cross-judge disagreement, self-consistency, and rationale divergence predict per-item human disagreement or judge error well enough to trigger abstention?
- **Why care / closest work / exact gap:** [Sage](https://openreview.net/forum?id=JFTSZa2stt) studies consistency; [Gupta & Kumar](https://openreview.net/forum?id=FbDuesI6tD) use conformal sets. The new claim would be an out-of-distribution abstention rule evaluated on held-out tasks.
- **Data / models / compute / cost:** Two human-labeled judge datasets; 4 open judges; $0–$150.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; calibration, selective prediction, feature analysis; statistician helpful.
- **Format / venues:** Empirical reliability paper; TMLR or evaluation workshop.
- **Useful null / strongest risk:** Negative result warns against “disagreement means uncertainty.” Risk: feature space may duplicate existing uncertainty work.

### C08 — Criterion decomposition versus holistic judging

- **Question / smallest contribution:** Does decomposing a judgment into verifiable criteria improve ranking validity, or merely create more correlated opportunities for error? Compare holistic, checklist, and deterministic-plus-LLM judging.
- **Why care / closest work / exact gap:** [RocketEval](https://openreview.net/forum?id=zJjzNj6QUe) supports checklist judging; [JETTS](https://openreview.net/forum?id=CgJEHynkJt) studies judges in test-time scaling. The gap is a controlled error-budget decomposition with matched tokens.
- **Data / models / compute / cost:** One verifiable generation task and one open-ended task; 3 judges; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; evaluation design and matched-cost analysis; no collaborator necessary.
- **Format / venues:** Short empirical paper + evaluator; workshop or ACL Findings.
- **Useful null / strongest risk:** Null shows decomposition is not universally beneficial. Risk: checklist quality is a confound.

## Rule following, evidence, and institutional decisions

### C09 — Burden-of-proof calibration in executable rule worlds

- **Question / smallest contribution:** Can LLMs implement different decision thresholds consistently when the underlying evidence likelihoods are held fixed? Release a synthetic, executable benchmark varying only the prescribed proof threshold.
- **Why care / closest work / exact gap:** Risk-aware deferral varies utilities ([Wu et al.](https://openreview.net/forum?id=Xpf7AUOcnT)); legal benchmarks test broad competence ([LEXam](https://arxiv.org/abs/2505.12864)). The proposed gap is controlled threshold-following with exact labels, not legal knowledge.
- **Data / models / compute / cost:** Programmatically generated Bayesian evidence tasks; 4–8 open/API models; $50–$300.
- **Difficulty / timeline / skills / collaborator:** 3/5; 6–8 weeks; probability, synthetic-data validation, mixed-effects analysis; statistician helpful.
- **Format / venues:** Benchmark + empirical paper; evaluation workshop, TMLR, or NeurIPS Datasets & Benchmarks if expanded.
- **Useful null / strongest risk:** A null showing threshold consistency would establish a positive capability boundary. Risk: synthetic tasks may lack ecological validity or collapse into arithmetic.

### C10 — Evidence-order invariance with a fixed evidence graph

- **Question / smallest contribution:** Holding every proposition and source constant, do permutations of supportive and adverse evidence change decisions or calibrated confidence? Provide a factorial order-sensitivity study.
- **Why care / closest work / exact gap:** ConflictBench measures acknowledgment of conflict ([paper](https://openreview.net/forum?id=JRqzDZ6EiD)); prompt-sensitivity work studies wording. The exact gap is decision invariance to evidence sequence under a fixed graph and threshold.
- **Data / models / compute / cost:** 100–300 generated cases with deterministic labels and balanced permutations; 5 models; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 2/5; 4–6 weeks; factorial design, Python; no collaborator necessary.
- **Format / venues:** Short empirical paper + dataset; workshop or Findings.
- **Useful null / strongest risk:** Null is useful evidence of order robustness. Risk: nearby order-effect papers may already exist; novelty search is critical.

### C11 — Source-reliability discounting under conflicting evidence

- **Question / smallest contribution:** Do models correctly discount a numerically weaker or demonstrably unreliable source when evidence conflicts, and do explanations track the actual weight used?
- **Why care / closest work / exact gap:** ConflictScore tests conflict acknowledgment and FactConf tests parametric/external conflict. Neither lead, from the current screen, isolates known source reliability and decision thresholds.
- **Data / models / compute / cost:** Executable evidence generator with reliability parameters; 4–6 models; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; probabilistic modeling, causal perturbations; no collaborator necessary.
- **Format / venues:** Measurement/behavior paper; TMLR or trustworthiness workshop.
- **Useful null / strongest risk:** Null maps a precise failure boundary. Risk: model may solve it as explicit arithmetic unless naturalistic variants are carefully designed.

### C12 — Procedural remedy invariance

- **Question / smallest contribution:** When facts and liability are fixed but the authorized remedies change, do models keep merits reasoning stable while changing only the permissible output?
- **Why care / closest work / exact gap:** Legal benchmarks emphasize substantive answers and procedure but do not isolate this invariance. The contribution would be a controlled, domain-general “decision versus remedy” task, not a legal QA set.
- **Data / models / compute / cost:** Synthetic policies with executable remedy sets; 4–6 models; $25–$200.
- **Difficulty / timeline / skills / collaborator:** 2/5; 4–6 weeks; rule engine, test generation, analysis; domain reviewer helpful.
- **Format / venues:** Benchmark note; AI governance/evaluation workshop.
- **Useful null / strongest risk:** Strong invariance is a useful positive result. Risk: may appear too domain-specific or obvious.

### C13 — Missing-evidence behavior: guess, abstain, or ask

- **Question / smallest contribution:** Under controlled missingness, when do agents guess, abstain, or request the uniquely decision-relevant fact? Score not just correctness but value of the requested information.
- **Why care / closest work / exact gap:** [Answer, Refuse, or Guess?](https://openreview.net/forum?id=Xpf7AUOcnT) studies risk-aware deferral; tool-agent benchmarks study recovery. The gap is targeted information acquisition under explicit decision rules.
- **Data / models / compute / cost:** Synthetic decision problems with known value of information; 4–6 models; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; decision theory, agent harness; no collaborator necessary.
- **Format / venues:** Agent-behavior study + environment; AAMAS/agent workshop or TMLR.
- **Useful null / strongest risk:** Negative result shows that calibrated abstention does not imply useful questioning. Risk: overlap with active-questioning literature.

### C14 — Conflicting authority hierarchy

- **Question / smallest contribution:** Can models resolve conflicts between rules from different authority levels while resisting recency, length, and placement confounds?
- **Why care / closest work / exact gap:** Instruction hierarchy research tests system/user priority ([paper](https://arxiv.org/abs/2404.13208)); evidence-conflict work tests content conflict. The gap is generalization to explicit institutional rule hierarchies with executable outcomes.
- **Data / models / compute / cost:** Generated rule systems with precedence graphs; 4–8 models; $50–$300.
- **Difficulty / timeline / skills / collaborator:** 3/5; 6–8 weeks; logic/program synthesis, factorial experiments; no collaborator necessary.
- **Format / venues:** Benchmark + empirical study; trustworthiness/evaluation workshop.
- **Useful null / strongest risk:** Positive robustness is publishable as a bounded capability result. Risk: instruction-priority benchmarks may subsume it.

### C15 — Symmetry and party-label invariance

- **Question / smallest contribution:** If party identities and narrative order are swapped while the formal case remains isomorphic, do LLM decisions transform symmetrically?
- **Why care / closest work / exact gap:** Judge-bias work tests position and style; institutional-bias papers test framing. The exact contribution is an automatically verified metamorphic test for relational decisions.
- **Data / models / compute / cost:** 200 paired synthetic cases; 4–6 models; $25–$150.
- **Difficulty / timeline / skills / collaborator:** 2/5; 3–5 weeks; metamorphic testing and paired statistics; no collaborator necessary.
- **Format / venues:** Robustness audit + test generator; workshop/technical report.
- **Useful null / strongest risk:** Null validates a basic invariance. Risk: too small alone unless combined with a richer invariance suite.

### C16 — Temporal rule-version fidelity

- **Question / smallest contribution:** Given explicit versioned rules, can models apply the requested historical version rather than the newest or memorized version? Build executable rule migrations and test documentation-assisted repair.
- **Why care / closest work / exact gap:** [Quantum API drift](https://arxiv.org/abs/2607.04072) studies SDK versions; legal studies note stale answers and endpoint variance. The gap is domain-general rule-version fidelity outside code, with formal labels.
- **Data / models / compute / cost:** Synthetic policy versions plus one public real rule set; 4–6 models; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–8 weeks; versioned data design, parsers; domain reviewer helpful.
- **Format / venues:** Benchmark/evaluation paper; TMLR or evaluation workshop.
- **Useful null / strongest risk:** Null gives a positive boundary for explicit-context rule following. Risk: quantum API study may make the conceptual contribution look derivative.

## Agents, tools, and process reliability

### C17 — Multi-turn recovery after a wrong tool result

- **Question / smallest contribution:** Which agents detect and recover from one earlier, recoverable tool error across a multi-turn stateful task, and which merely rationalize the corrupted state?
- **Why care / closest work / exact gap:** ToolRL-DR and ToolFailBench explicitly leave multi-turn recovery open; ToolBench-X covers recoverable hazards. The new contribution must isolate state correction over time rather than add more hazard categories.
- **Data / models / compute / cost:** Extend a small open tool environment with 100 deterministic tasks and injected errors; 3–5 models; $100–$400.
- **Difficulty / timeline / skills / collaborator:** 4/5; 7–10 weeks; stateful harness, trace scoring, fault injection; engineering collaborator helpful.
- **Format / venues:** Benchmark + agent reliability paper; agent/evaluation workshop or TMLR.
- **Useful null / strongest risk:** Uniform failure would establish a clean negative result. Risk: ToolBench-X follow-ups may close the gap quickly.

### C18 — Recovery hints versus extra inference budget

- **Question / smallest contribution:** Are targeted diagnostic hints more valuable than an equal-token generic reasoning budget when recovering from tool hazards?
- **Why care / closest work / exact gap:** ToolBench-X reports that targeted hints recover failures while test-time scaling helps less. A controlled token-matched causal test across hazard classes would sharpen that observation.
- **Data / models / compute / cost:** Reuse ToolBench-X or ToolRL-DR; 3–5 open models; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 2/5; 3–5 weeks; benchmark integration and paired tests; no collaborator necessary.
- **Format / venues:** Short replication/extension; workshop or research note.
- **Useful null / strongest risk:** Null bounds the claimed value of diagnosis. Risk: contribution may be too small or already derivable from released results.

### C19 — Policy compliance during tool-error recovery

- **Question / smallest contribution:** When the easiest recovery path violates an explicit policy, do agents choose a slower valid path or specification-game the task? Create tasks with outcome-equivalent valid and prohibited recoveries.
- **Why care / closest work / exact gap:** Tool reliability benchmarks optimize task recovery; instruction hierarchy tests authority. The gap is the interaction between recovery pressure and procedural constraints.
- **Data / models / compute / cost:** 100–200 executable tasks with paired legal/illegal recovery paths; 4 models; $100–$400.
- **Difficulty / timeline / skills / collaborator:** 4/5; 7–10 weeks; environment engineering, trace validators, security thinking; collaborator helpful.
- **Format / venues:** Agent safety benchmark + paper; safety/agent workshop or TMLR.
- **Useful null / strongest risk:** Strong compliance is informative; failures expose a mechanism rather than random errors. Risk: scenario validity and prohibited-path realism are hard.

### C20 — Outcome success versus process validity

- **Question / smallest contribution:** How often do agents reach the correct final answer through a trace that violates explicit constraints, and how much do standard outcome metrics overestimate reliability?
- **Why care / closest work / exact gap:** [AgentRx](https://openreview.net/forum?id=VDQkzHwidO) diagnoses critical failure steps; [programmable subjects](https://openreview.net/forum?id=8W6hjNj4Kf) calls for trace standards. The gap is a deterministic benchmark where process invalidity can coexist with outcome success.
- **Data / models / compute / cost:** Small executable environment with trace validators; 3–5 models; $75–$300.
- **Difficulty / timeline / skills / collaborator:** 3/5; 6–8 weeks; event schemas, property-based tests; no collaborator necessary.
- **Format / venues:** Measurement paper + validator; agent/evaluation workshop.
- **Useful null / strongest risk:** Low divergence validates outcome scoring for the tested class. Risk: process rules may appear artificially strict.

### C21 — Causal value of deliberation in agent panels

- **Question / smallest contribution:** Does inter-agent communication improve decisions after controlling for extra samples and tokens? Compare real deliberation with communication-free, shuffled-message, and same-budget self-consistency baselines.
- **Why care / closest work / exact gap:** Negotiation reproduction shows communication-free baselines can match multi-agent systems ([Garcia et al.](https://openreview.net/forum?id=MTrhFmkC45)); lazy-agent work shows interaction can collapse ([Zhang et al.](https://openreview.net/forum?id=5J6u03ObRZ)). The gap is causal attribution on verifiable judgment tasks.
- **Data / models / compute / cost:** Two programmatically scored tasks; 2–3 open model families; $100–$500.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–8 weeks; matched-budget experiments, mediation/influence measures; statistician helpful.
- **Format / venues:** Multi-agent negative-result/empirical paper; AAMAS workshop, TMLR.
- **Useful null / strongest risk:** No benefit is a valuable correction to multi-agent claims. Risk: many concurrent studies may already use these baselines.

### C22 — Independence contamination in sequential panels

- **Question / smallest contribution:** How much does showing earlier votes or rationales reduce effective panel diversity, and can blinded-then-deliberate protocols preserve accuracy at equal cost?
- **Why care / closest work / exact gap:** Judge-panel work models correlated errors; multi-agent work studies communication. The proposed gap is a controlled protocol comparison of independent first votes versus sequential exposure.
- **Data / models / compute / cost:** Public judge benchmark; 4–6 open judges; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 2/5; 4–6 weeks; panel protocols, correlation analysis; no collaborator necessary.
- **Format / venues:** Agent/judge behavior study; evaluation workshop.
- **Useful null / strongest risk:** Null shows exposure does not materially erode diversity. Risk: obvious result or prior jury-protocol literature.

### C23 — Tool-result trust calibration

- **Question / smallest contribution:** Can an agent distinguish reliable, stale, conflicting, and malformed tool results and choose verification effort proportionate to expected harm?
- **Why care / closest work / exact gap:** ToolBench-X covers output drift and cross-source conflict; ToolFailBench covers ignoring results. The gap would be a risk-sensitive verification policy with controlled costs, not raw recovery accuracy.
- **Data / models / compute / cost:** Deterministic tool world with varying error probability and consequence; 4 models; $75–$300.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–8 weeks; decision theory, fault injection; no collaborator necessary.
- **Format / venues:** Agent reliability paper; TMLR or workshop.
- **Useful null / strongest risk:** Null shows agents do not adapt verification rationally. Risk: overlap with adaptive tool-use and uncertainty papers.

## Reproducibility, contamination, and human–AI systems

### C24 — Cross-provider reproducibility envelope

- **Question / smallest contribution:** For a frozen evaluation protocol, what fraction of conclusions survive model-provider/version substitution, repeated calls, and prompt-preserving rewrites?
- **Why care / closest work / exact gap:** Judge replacement has direct recent study ([Yang et al.](https://arxiv.org/abs/2607.08535)); Indian legal evaluation notes endpoint variance ([Juvekar et al.](https://arxiv.org/abs/2510.17900)). A publishable gap must be a general “reproducibility envelope” with predeclared conclusion levels, not another drift snapshot.
- **Data / models / compute / cost:** One public evaluation with archived outputs; 4 providers/versions if accessible; $200–$800.
- **Difficulty / timeline / skills / collaborator:** 3/5; 6–10 weeks plus time; experiment logging, equivalence testing; no collaborator necessary.
- **Format / venues:** Reproducibility audit; MLRC/TMLR.
- **Useful null / strongest risk:** Stability is useful evidence. Risk: expensive, time-dependent, and the July 2026 judge-replacement paper may make it redundant.

### C25 — Semantic-preservation audit of dynamic benchmark generators

- **Question / smallest contribution:** How often do automatic benchmark-variant generators silently change the correct answer or difficulty, and which validation strategies catch the errors?
- **Why care / closest work / exact gap:** DyVal and DyCodeEval generate dynamic variants; contamination work increasingly relies on them. The gap is independent measurement of label-preservation error with deterministic or expert-verifiable seeds.
- **Data / models / compute / cost:** Public generators plus 100–300 executable seed problems; mostly local models; $0–$150.
- **Difficulty / timeline / skills / collaborator:** 3/5; 5–7 weeks; property-based testing, sampling, annotation protocol; no collaborator necessary.
- **Format / venues:** Reproducibility/measurement paper + test harness; MLRC or evaluation workshop.
- **Useful null / strongest risk:** Low error validates current generators. Risk: only a software QA result unless tied to ranking distortion.

### C26 — Fresh executable rule benchmark for contamination-resistant evaluation

- **Question / smallest contribution:** Can freshly generated executable rule worlds discriminate current models while resisting memorization and providing exact counterfactual variants?
- **Why care / closest work / exact gap:** Dynamic evaluation and contamination-resilient datasets already exist ([DyVal](https://openreview.net/forum?id=SRB8ricWVr), [CoreEval](https://openreview.net/forum?id=YPiM4OpdRH)). Novelty requires a distinctive institutional-rule structure and diagnostic counterfactuals, not freshness alone.
- **Data / models / compute / cost:** Generator and verifier; 5–8 open/API models; $100–$500.
- **Difficulty / timeline / skills / collaborator:** 4/5; 8–12 weeks; DSL design, property testing, benchmark validation; engineering collaborator helpful.
- **Format / venues:** Dataset/benchmark paper + package; NeurIPS D&B workshop/track or TMLR.
- **Useful null / strongest risk:** If models saturate it, the generator still supports harder follow-up tasks. Risk: benchmark construction without a scientific insight.

### C27 — Human-disagreement-aware judge evaluation without new human subjects

- **Question / smallest contribution:** Do judge rankings change when evaluation is stratified by existing human disagreement, and can models identify genuinely contestable rather than merely difficult cases?
- **Why care / closest work / exact gap:** [Beyond correlation](https://openreview.net/forum?id=E8gYIrbP00) motivates uncertainty stratification. The extension must add a new selective-prediction or ranking result across multiple archival datasets.
- **Data / models / compute / cost:** Public multi-annotator datasets only; 3–5 open judges; $0–$150. No new human-subject study.
- **Difficulty / timeline / skills / collaborator:** 2/5; 4–6 weeks; reliability statistics, archival-data ethics; no collaborator necessary.
- **Format / venues:** Reanalysis/measurement paper; TMLR or evaluation workshop.
- **Useful null / strongest risk:** Stable rankings justify pooled evaluation. Risk: too close to the source paper or limited by heterogeneous annotations.

### C28 — Replication of context-interference outside mathematics

- **Question / smallest contribution:** Does solving prior, structurally unrelated rule tasks degrade performance on a later target task, and do explicit context resets remove the effect?
- **Why care / closest work / exact gap:** [Robust Reasoning Benchmark](https://arxiv.org/abs/2604.08571) explicitly leaves legal, medical, and coding generalization open and asks about reset granularity. A clean replication on executable rule systems could establish whether the effect is domain-general.
- **Data / models / compute / cost:** Generated logic/rule tasks with exact solvers; 4–6 open models; $50–$250.
- **Difficulty / timeline / skills / collaborator:** 2/5; 4–6 weeks; replication design, paired inference, task generation; no collaborator necessary.
- **Format / venues:** Replication/extension paper; MLRC, workshop, or research note.
- **Useful null / strongest risk:** No degradation would sharply limit the original generalization claim. Risk: the original effect may depend on long reasoning traces or unavailable model internals.

## Preliminary screen observations

- The highest-upside cluster is controlled evaluation of decision systems: C01, C03, C09, C13, C19, C20, C21, C25, and C28.
- The lowest engineering-risk studies are C10, C15, C18, C22, C27, and C28.
- Candidates most likely to be overtaken quickly are C05, C17, C18, C23, and C24 because their literatures are moving very fast.
- Candidates with the clearest comparative advantage without becoming “legal AI” are C09, C13, C14, C19, and C20: they use institutional-design reasoning to construct general technical evaluations.
- No candidate should be ranked until a broader search tests direct predecessors and available artifacts.
