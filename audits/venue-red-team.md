# Hostile venue-fit review of the surviving formulations

**Review date:** 2026-07-17
**Role:** hostile Reviewer 2 plus venue-fit auditor
**Inputs:** `selection-synthesis-v0.md` and the F1, F2, and F3 novelty audits
**Scope boundary:** no submission, contact, or venue action was taken.

## Executive decision

None of the three formulations is submission-ready. The forced ranking is:

1. **F2 — joint bias/coverage audit:** **Major revision; advance to a costed feasibility and statistical-design gate.** It has the clearest venue-native contribution, especially for an evaluation-methodology audience, but the paper exists only if it performs repeated full generator draws, independent validity adjudication, and decision-changing coverage analysis. A cluster bootstrap applied to one generated dataset is not a paper.
2. **F1 — causal carryover decomposition:** **Major revision; retain as the runner-up.** It has the cleanest behavioral question and a plausible ACL/TMLR audience, but it looks like a factorial bundle of controls around phenomena already demonstrated in adjacent settings. It must produce a mechanism-specific dissociation, not merely another degradation curve.
3. **F3 — temporal applicability pivot:** **Reject from the first-project slate.** Its identity is strongest, but its novelty position is weakest: *Asking For An Old Friend* already studies historically applicable statutory versions, and the pivot mainly adds forced version IDs, exact execution, and counterbalancing. Those are excellent controls for a replication, not yet a new central finding.

**Selection recommendation:** select **F2 conditionally**, with F1 as the predeclared fallback. Before any model-scale experiment, require F2 to pass a small feasibility pilot showing that two established open generators can be pinned, regenerated independently, mapped to defensible seed families, and adjudicated without relying on the generating model. If that fails, stop F2 and promote F1. Do not spend a first-project budget on F3 unless a new theory or cross-domain phenomenon appears that is not a direct extension of the ICAIL predecessor.

The rank is about publication probability after a successful experiment, not ease. F2 is the most expensive and operationally fragile of the three.

## Venue reality check

The strongest general venue match is the [NeurIPS 2026 Evaluations & Datasets Track](https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets), which explicitly treats evaluation as an object of scientific study and welcomes comparisons of evaluation assumptions, auditing, stress-testing, refined protocols, and negative results. Its reviewer rubric is also a warning: evaluation methodology should change scientific conclusions, benchmark analysis should change how progress is measured, and auditing findings must be rigorous rather than superficial ([reviewing guidelines](https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines)). That is a natural home for F2, a possible stretch home for F1, and a poor rescue route for a narrow F3 benchmark.

[TMLR](https://www.jmlr.org/tmlr/editorial-policies.html) is the most realistic general archival fallback. Its scope includes experimental studies yielding insight into model behavior, applications that expose strengths and weaknesses, new assessment methods, and reproducibility studies. It emphasizes evidential correctness over subjective significance, but explicitly excludes work that merely re-implements an already reproduced idea. This helps a careful F1 or F2 paper; it does not erase an obviousness problem.

[ACL 2026](https://2026.aclweb.org/calls/main_conference_papers/) explicitly accepts substantial original work including negative findings, resources, and reproductions, with relevant areas including model analysis, language models, logical reasoning, resources and evaluation, and RAG. That makes ACL-family review legitimate for all three, but the realistic target for a narrow diagnostic study is often **Findings**, not a main-conference long paper. Recent track records support that distinction: broad executable reasoning benchmarks such as [RULEARENA](https://aclanthology.org/2025.acl-long.27/) reached ACL main, while narrower legal/evaluation resources such as [OpenExempt](https://aclanthology.org/2026.findings-acl.1328/) and temporal-conflict studies such as [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) appeared in Findings.

For a genuinely legal F3, [ICAIL](https://iaail.org/icail-2026-first-call-for-papers/) and [JURIX](https://jurix.nl/) are scope-correct. ICAIL invites AI-and-law foundations, methods, systems, applications, computable legal rules, legal reasoning, and empirical work. JURIX invites work on legal and normative systems but explicitly expects added value, novelty, significance, and proper evaluation. Scope fit therefore does not solve F3's direct-prior-art problem.

## F1 — narrow causal carryover in repeated rule-bound decisions

### Reviewer 2 rejection case

> The paper repackages known task interference, sequential decision bias, prior-output anchoring, semantic distractors, and context reset into one synthetic factorial. Each control is sensible, but their conjunction is engineering completeness rather than a scientific contribution. The claimed mechanism is inferred from surface ablations, not identified: removing labels or rationales changes both semantics and token structure, and self-generated histories select on model errors. The executable rules make scoring clean but reduce ecological validity. With many arms, horizons, rule worlds, model families, and outcome-streak directions, the study will either be underpowered or become a large fishing expedition. A null result is unsurprising for strong current models; a positive result can be dismissed as another long-context interference effect.

This attack is supported by unusually close predecessors. [LLM Task Interference](https://aclanthology.org/2024.emnlp-main.811/) already studies later targets after unrelated histories; [BiasBuster](https://aclanthology.org/2024.findings-emnlp.739/) already studies prior model decisions in a persistent same-task conversation; [ERGO](https://aclanthology.org/2025.uncertainlp-main.23/) already tests stateless reset mitigation; and [NoisyBench](https://arxiv.org/abs/2601.07226) already separates random-chat and semantically hard distractors. F1's novelty is therefore only the joint causal decomposition in independently complete same-rule cases.

### Obviousness and incrementality attack

Once the predecessors are known, a competent follow-up author would naturally add an exact rule solver, token-matched neutral histories, gold-versus-self outputs, and a fresh-context reset. The remaining claim risks being “we ran all the controls prior work omitted.” That can be publishable only if the controls reveal a non-obvious causal pattern, such as label carryover without rationale carryover, directional transport tied to rule margins, or a boundary intervention that distinguishes semantic contamination from generic context load.

### Benchmark-without-insight attack

The failure mode is a new synthetic rule suite followed by a heat map of accuracy versus history length. Such an artifact would be cleaner than prior work but would not explain why the same target changes, predict when it changes, or alter evaluation/deployment practice. Calling the arms “anchoring,” “commitment,” or “memory” without discriminating those mechanisms would make the paper weaker, not stronger.

### Likely audience

LLM behavioral evaluation; multi-turn and long-context robustness; instruction following and logical reasoning; researchers studying model self-conditioning; practitioners operating repeated decision workflows in one conversation.

### Realistic venue categories

1. **ACL/EMNLP via ARR, probably Findings:** best topical audience for language-model behavior, reasoning, and resources/evaluation. Main-conference placement would require a stronger cross-model mechanism or broadly reusable evaluation result than a single synthetic setting.
2. **TMLR:** realistic for a rigorous, narrowly claimed empirical model-behavior study, including a well-powered negative result with tight bounds.
3. **NeurIPS E&D, stretch:** viable only if framed as a reusable protocol showing that conversational evaluation practices change conclusions about model reliability. A degradation benchmark alone would fail the track's significance test.

### Result threshold above a blog post

At minimum, the paper needs all of the following:

- a predeclared primary interaction showing history-induced excess error beyond token-, position-, and format-matched neutral load;
- replication in at least two genuinely different executable rule worlds and across at least three materially different model families;
- a mechanism-specific dissociation: for example, prior labels or self-rationales shift the same target while matched case text or gold rationales do not, with the shift following a predeclared directional prediction;
- paired uncertainty intervals and multiplicity control tight enough to rule out a trivial effect. As a go/no-go guide, an absolute target shift around five percentage points or an odds ratio around 1.5, replicated rather than isolated, would be clearly paper-scale; a smaller effect needs a credible high-stakes consequence or a much stronger mechanistic explanation;
- a literal fresh-context replay that cleanly removes the effect, or a comparably decisive boundary result; and
- if the primary result is null, equivalence bounds narrow enough to rule out practically meaningful carryover rather than merely failing to reject zero.

**Verdict: Major revision.** Keep it alive, but do not call it a benchmark contribution. The paper must earn its place through a non-obvious dissociation.

## F2 — joint invalidity bias and seed-family coverage distortion

### Reviewer 2 rejection case

> The paper applies textbook clustered-data inference and label cleaning to dynamic benchmarks. We already know that variants from one source problem are dependent, that invalid paraphrases bias scores, and that naive intervals under-cover when the analysis pretends clusters are independent. FormInv already combines semantic-validity auditing, family-level analysis, uncertainty, and rank changes; PTEB and DyCodeEval already repeat stochastic generation and validate variants; recent work already supplies hierarchical prompt inference and rank confidence sets. The cross-generator comparison adds breadth, not a new method. Worse, heterogeneous generators do not share a clean sampling hierarchy, so the proposed “common” estimand may be artificial. Any rank reversal can be manufactured by choosing nearly tied models, while any undercoverage result can be demonstrated in simulation without this expensive audit.

The closest collision is [FormInv](https://arxiv.org/abs/2605.29001), which already audits semantic invariance by equivalence family and reports a rank change after removing invalid variants. [The Emperor's New Clothes in Benchmarking?](https://arxiv.org/abs/2503.16402) already audits 20 benchmark-update strategies across five benchmarks; [PTEB](https://aclanthology.org/2026.eacl-long.130/) repeats stochastic paraphrase generation and checks semantic validity; and [DyCodeEval](https://arxiv.org/abs/2503.04149) repeats complete generated benchmarks. The surviving novelty is only empirical calibration of the *joint* bias-and-coverage distortion across materially different established generators.

### Obviousness and incrementality attack

“Use the seed as the cluster” is ordinary experimental design. So are cluster bootstrap, random effects, paired comparisons, and simultaneous rank inference. The paper cannot list these as contributions. Even the joint analysis is obvious unless invalidity changes the dependence structure, evaluation-efficiency conclusion, or rank decision in a way that separate audits would miss.

### Benchmark-without-insight attack

The failure mode is an audit dashboard reporting validity rate, intraclass correlation, effective sample size, and corrected leaderboard order for two repositories. That is useful internal QA and perhaps a technical report, but it teaches no general lesson unless the repeated-generation study establishes when current evaluation conclusions are unreliable and supplies a transferable design rule.

### Likely audience

Benchmark-methodology and measurement researchers; dynamic benchmark designers; statistical ML and uncertainty researchers; leaderboard maintainers; reproducibility and evaluation-infrastructure practitioners.

### Realistic venue categories

1. **NeurIPS Evaluations & Datasets:** strongest fit. F2 directly matches evaluation methodology, statistical evaluation, auditing, and comparisons of assumptions. The work must show that the corrected design changes conclusions and must release reproducible artifacts.
2. **TMLR:** strong fit for a technically rigorous calibration paper whose contribution is modest but well supported. Rolling review also accommodates a complete, careful empirical package better than forcing a conference deadline.
3. **ACL/EMNLP via ARR, likely Findings unless the protocol is broadly adopted:** suitable if the generators and models are predominantly NLP/LLM benchmarks and the paper makes a clear resources-and-evaluation contribution.

### Result threshold above a blog post

The minimum credible package is:

- at least two established open generator systems with materially different construction regimes and defensible, explicitly mapped sampling hierarchies;
- enough independent source families to estimate family-level variation credibly—roughly 100 per generator is a reasonable planning floor, subject to a pre-study power analysis rather than a magic acceptance number;
- repeated *complete* independent generator draws, or a large held-out generator population, so coverage is measured empirically rather than asserted from one bootstrap;
- independent validity ground truth using execution/formal checks where possible and blinded human adjudication for residual cases, with reasons and agreement reported;
- a predeclared comparison of naive item-wise inference, seed-cluster bootstrap, and a paired multilevel model, with simultaneous rank confidence sets rather than point-order drama;
- a joint result: validity filtering materially changes variance components, coverage, efficiency, or rank conclusions. Separate “some items are bad” and “ICC is positive” tables are insufficient;
- decision-scale consequences in at least two generator/task settings. A compelling positive result would show severe naive miscoverage—e.g. nominal 95% intervals covering far below 90%, with the corrected method returning near-nominal coverage—and a changed dominance/rank set or evaluation-budget recommendation. These numbers are go/no-go guides, not venue rules;
- if distortion is small, a powered negative result with tight bounds plus a reusable protocol that tells generator authors when simpler inference is safe.

**Verdict: Major revision, first-ranked.** Advance only to a pilot and costed design. This is the best venue fit but the easiest project to ruin through inadequate repeated draws or weak adjudication.

## F3 — causal temporal-applicability selection versus execution

### Reviewer 2 rejection case

> This is a direct replication-and-controls paper built around omissions in *Asking For An Old Friend*. That paper already asks whether models apply the historically correct statutory version, creates version-discriminating questions, tests retrieval and grounding, and separately scores version application. The new work forces a version ID, adds an oracle-version arm, counterbalances order and “current/latest” labels, and swaps free-form legal answers for an executable DSL. Those changes improve internal validity but do not establish a new phenomenon. Adjacent work on version-conditioned code, API drift, context-memory conflict, instruction hierarchy, and executable legal rules already supplies the rest of the benchmark skeleton. The synthetic task is ecologically thin; the small tax extension is legally narrow; and the claimed selection/application decomposition is an expected diagnostic, not a theory.

The collision is decisive: [Asking For An Old Friend](https://arxiv.org/abs/2605.23497) is an ICAIL 2026 historical-law study with expert-validated, version-sensitive questions. [DeonticBench](https://arxiv.org/abs/2604.04443) supplies executable legal/policy rules, [GitChameleon 2.0](https://openreview.net/pdf?id=b854ec44410bd665f638826904b650347f56d150) supplies executable historical-version tasks, and [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) supplies temporal context-memory conflict. The pivot combines these ingredients more cleanly; it does not yet outrun them.

### Obviousness and incrementality attack

Once a paper infers historical-version use from open-ended answers, the obvious follow-up is to force the version choice and condition application on the oracle version. Once recency is suspected, the obvious controls are order, position, neutral IDs, and a non-temporal conflict. Reviewer 2 can therefore characterize the entire design as reviewer-proofing a predecessor rather than discovering a new mechanism.

### Benchmark-without-insight attack

The failure mode is a polished temporal-rule DSL, several migration templates, and a leaderboard decomposed into selection and execution scores. That is a good artifact but not a new scientific insight. A “latest wins” main effect is predictable and confounded unless a temporal-specific interaction remains after all generic conflict and position controls.

### Likely audience

Temporal reasoning and context-memory conflict; rule-following and RAG reliability; legal NLP and computational law; policy and compliance system evaluation; version-sensitive software/code evaluation.

### Realistic venue categories

1. **ICAIL or JURIX:** best audience only if the real-law component is substantial, legally verified, and connected to legal applicability rather than used as decorative validation. The direct ICAIL predecessor makes novelty scrutiny especially severe.
2. **ACL/EMNLP via ARR, likely Findings:** plausible for a cross-domain temporal-conflict mechanism with executable scoring. A law-only replication with better controls is unlikely to clear the main-conference bar.
3. **TMLR:** possible only if the paper becomes a general model-behavior result across legal/policy and non-legal rule worlds, with claims tightly limited to the identified mechanism.
4. **NeurIPS E&D, stretch:** possible only if the protocol changes how version-sensitive evaluations are designed across multiple domains. Another temporal benchmark is not enough.

### Result threshold above a blog post

To reopen F3, require:

- a predeclared temporal-applicability interaction that survives matched non-temporal conflict, order, position, neutral-ID versus “old/current/latest” labels, and oracle-application controls;
- forced version-ID selection, deterministic execution, and a full cross-version label matrix for every primary item;
- a version-consistent substitution signal: when the wrong version is selected, the model produces that version's exact outcome more often than can be explained by generic answer error;
- replication across at least two synthetic rule worlds and one official real-rule family with verified effective intervals and transition provisions;
- direct comparison with a meaningful subset or protocol from *Asking For An Old Friend*, not merely a citation;
- a nontrivial effect after controls—again, roughly a replicated five-point absolute error shift is a useful go/no-go guide—or a stronger theoretical prediction that the data uniquely support; and
- a conclusion that changes mitigation: for example, effective-date metadata repairs selection while oracle version text exposes a distinct residual execution failure. Generic RAG improvement is already occupied.

**Verdict: Reject.** The current pivot is too close to its direct predecessor for a first project. Better controls and deterministic scoring are not enough by themselves.

## Forced comparison

| Criterion | F1 | F2 | F3 |
| --- | --- | --- | --- |
| Remaining novelty | Narrow joint causal decomposition | Narrow cross-generator joint calibration | Very narrow control-heavy extension |
| Cleanest audience | ACL/TMLR model behavior | NeurIPS E&D/TMLR measurement | ICAIL/JURIX, then ACL Findings |
| Reviewer 2 attack strength | High | High | Decisive |
| Main empirical risk | Factorial explosion; no mechanism-specific effect | Cost, adjudication, and insufficient repeated draws | Null temporal-specific interaction after controls |
| “Just a benchmark” risk | High | Medium-high | Very high |
| Solo-project feasibility | Medium | Low | Medium-low |
| Recommendation | Runner-up | Conditional selection | Retire |

## Final recommendation

Advance **F2**, but only as a staged measurement study. The first irreversible expense should come after a pilot proves that the repeated-generator coverage estimand is executable with two real systems. Preregister the F1 fallback trigger now: if F2 cannot obtain independent validity labels, reproducible generator draws, or a defensible common estimand, terminate it and move to F1 rather than shrinking F2 into a one-generator cluster-bootstrap note.

F1 remains scientifically respectable if it can simplify its design around one sharp directional interaction and one decisive boundary intervention. F3 should be removed from the slate; preserving it would reward a recognizable theme over a defensible contribution.

## Source note

Venue statements above use current official calls, scope pages, and reviewer guidance as of 2026-07-17. Prior-art claims are drawn from the primary papers and official proceedings linked inline and from the three dedicated novelty audits. Venue fit is an informed judgment, not an acceptance prediction.
