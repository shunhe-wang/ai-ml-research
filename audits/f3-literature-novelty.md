# F3 adversarial literature and novelty audit

**Candidate:** Temporal rule-version fidelity beyond code
**Audit date:** 2026-07-17
**Verdict:** **Reject as stated**

## Bottom line

F3 fails the literature-gap hard gate. Its central question is no longer merely adjacent to prior work; it is directly occupied.

[*Asking For An Old Friend: Diagnosing and Mitigating Temporal Failure Modes in LLM-based Statutory Question Answering*](https://arxiv.org/abs/2605.23497) (Prior, Schultz, and Grabmair, ICAIL 2026) already studies both failure modes named by F3: models applying superseded rules after amendments and models preferring newer provisions when a historical version governs. It releases 312 expert-validated German statutory QA pairs, including 113 pre-amendment and 84 multi-provision pre-amendment questions, evaluates five frontier models, separately scores **version application correctness**, and compares closed-book, web, and two temporally filtered RAG conditions. Its public repository includes the QA set and prompts ([artifact](https://github.com/TUMLegalTech/temporal_bias)).

That paper is more directly on point than the shortlist's cited quantum API benchmark. It explicitly asks whether models “recognize the need to apply historical versions of the law, even when the most recent paragraph versions are available,” which is substantively the same as F3's working question. The paper also reports a multi-provision ceiling when historical provisions change asynchronously and calls for extension beyond German civil law. “Domain-general rules beyond code” is therefore an extension axis, not a new problem.

Other close work occupies nearly every remaining component:

- [CLAW](https://aclanthology.org/2025.findings-emnlp.646/) includes all available historical versions of 306 Chinese national statutes—424 statute versions and 64,849 subparagraph-level entries with revision timestamps—and separately studies statutory recall and case reasoning.
- [DeonticBench](https://arxiv.org/abs/2604.04443) supplies 6,232 context-grounded legal/policy tasks across tax, airline, housing, and immigration, with executable Prolog and exact labels; its SARA examples already involve historically anchored tax years ([artifact](https://github.com/guangyaodou/DeonticBench)).
- [OpenExempt](https://aclanthology.org/2026.findings-acl.1328/) dynamically generates legal-rule tasks and machine-computable solutions from expert symbolic representations.
- [GitChameleon 2.0](https://openreview.net/pdf?id=b854ec44410bd665f638826904b650347f56d150) already frames version-conditioned generation as control and disambiguation among historical versions encountered in training; it has 328 executable version-sensitive tasks, RAG documentation, and self-debugging.
- [Quantum API Drift](https://arxiv.org/abs/2607.04072) evaluates requested-version fidelity across three SDK versions, a cross-version execution matrix, failure modes, and documentation-guided repair; it releases prompts, environments, execution, repair, and analysis code ([artifact](https://github.com/arasyi/quantum-api-drift)).
- [When LLMs Lag Behind](https://arxiv.org/abs/2604.09515) studies context-memory conflict over 270 real API updates from eight libraries and measures adoption and execution under update descriptions, structured documentation, and self-reflection.
- [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) directly studies temporal context-memory conflict using changed versus stable Wikidata facts.
- [Task Matters](https://aclanthology.org/2026.findings-acl.202/) already injects controlled context-memory conflicts while holding knowledge constant and varies which knowledge source the task requires.
- [Where Instruction Hierarchy Breaks](https://arxiv.org/abs/2606.07808) decomposes rule-following failure into instruction identification, conflict resolution, and response realization. Thus, F3's proposed separation of version selection, application, and repair is not itself a novel diagnostic pattern.

The proposed benchmark—100 synthetic scenarios, three migrations, controlled placement/recency, exact labels, and one real rule family—would read as a factorialized synthetic replication combining Prior et al.'s legal task with DeonticBench's executor and the code-version papers' controls. That can be useful engineering, but it does not support the current contribution claim.

## Closest-paper matrix

| Work | What it already contributes | Collision with F3 | What it leaves open |
| --- | --- | --- | --- |
| [Asking For An Old Friend](https://arxiv.org/abs/2605.23497) (ICAIL 2026) | 312 expert-validated time-sensitive statutory QA pairs; post-cutoff staleness; pre-amendment and multi-provision historical-law questions; five models; closed-book, web, and two temporally filtered RAG systems; explicit version-application score; released prompts/data. | **Extremely high / decisive.** Same historical-version, newer-rule, stale-knowledge, and repair/grounding question. | German statutory law only; questions and answers are LLM-generated then expert-filtered; open-ended LLM-judge scoring; no executable oracle; no randomized placement/order factorial; recency evidence is mixed outside web search. |
| [CLAW](https://aclanthology.org/2025.findings-emnlp.646/) (EMNLP Findings 2025) | Historically versioned corpus of every Chinese national statute, exact revision timestamps, fine-grained statutory recall, and a separate case-reasoning task. | **Very high on historical rule versions and stale/repealed provisions.** | Does not appear to factorially present conflicting versions or provide executable counterfactual labels for version selection versus application. |
| [DeonticBench](https://arxiv.org/abs/2604.04443) (2026) | 6,232 real legal/policy tasks; context-grounded reasoning; exact answers; reference executable Prolog; direct and solver-assisted modes; tax-year facts plus airline, housing, and immigration. | **Very high on F3's explicit-rule, exact-execution, and real-rule claims.** | Does not compare multiple versions of the same rule family as the manipulated variable. |
| [OpenExempt](https://aclanthology.org/2026.findings-acl.1328/) (ACL Findings 2026) | Expert symbolic representation of bankruptcy/exemption law, dynamic natural-language cases, machine-computable solutions, controlled complexity, public framework. | **High on contamination-resistant executable legal rules.** | Single legal regime rather than controlled historical migrations; no version-selection factorial. |
| [GitChameleon 2.0](https://openreview.net/pdf?id=b854ec44410bd665f638826904b650347f56d150) (NeurIPS 2025 workshop) | 328 manually authored historical version-conditioned Python tasks with executable hidden tests, documentation references for RAG, visible tests for repair, and multiple system types. | **Very high on requested historical-version fidelity and executable evaluation.** | Code only; does not study effective-date applicability or institutional rules. |
| [Quantum API Drift](https://arxiv.org/abs/2607.04072) (2026) | 50 tasks × three Qiskit versions, version-anchored prompts, cross-version execution, error taxonomy, and documentation-guided repair across 17 models. | **Very high on the proposed benchmark skeleton and repair claim.** | One SDK; API execution is not temporal legal/policy applicability; benchmark limitation notes semantic correctness is not measured. |
| [When LLMs Lag Behind](https://arxiv.org/abs/2604.09515) (2026) | 270 real API updates, 11 models, controlled external update specifications, structured documentation, adoption/execution metrics, and self-reflection. | **High on stale parametric knowledge versus authoritative update text and documentation assistance.** | Forward API updates, not selection of a governing historical rule from multiple valid versions. |
| [When Facts Change](https://aclanthology.org/2026.findings-acl.103/) (ACL Findings 2026) | WIKIRECENTCHANGES; stable versus changed facts; temporal context-memory conflict; conflict detection and mutability reasoning. | **High on temporal stale-knowledge mechanism.** | Facts rather than executable rules; current-fact trust rather than historical applicability. |
| [TRACK](https://aclanthology.org/2026.eacl-long.273/) (EACL 2026) | Updated facts that conflict with parametric knowledge; multi-step propagation in WIKI, CODE, and MATH; separates knowledge integration failure from downstream reasoning failure. | **High on the proposed selection/application separation.** | No rule-version or effective-date variable. |
| [Task Matters](https://aclanthology.org/2026.findings-acl.202/) (ACL Findings 2026) | Holds underlying knowledge fixed, injects conflicts, and varies whether tasks require contextual or parametric knowledge; tests rationale/reiteration interventions. | **High on controlled source-conflict design.** | No temporal applicability or executable institutional rule system. |
| [IHEval](https://aclanthology.org/2025.naacl-long.425/) (NAACL 2025) and [Where Instruction Hierarchy Breaks](https://arxiv.org/abs/2606.07808) (2026) | Conflicting rule priorities; identification/conflict-resolution/realization decomposition; monitor-and-repair methods. | **Medium-high on positional salience, precedence, stage diagnosis, and repair.** | Authority hierarchy is specified by message privilege, not by effective dates or rule versions. |
| [PolicyBank](https://arxiv.org/abs/2604.15505) (2026) | Evolving organizational-policy interpretation, structured policy memory, controlled policy gaps, and separation of alignment from execution. | **Medium.** Occupies “evolving policy understanding” and staged failure diagnosis. | Policies evolve through corrective feedback, not historical version selection by event date. |
| [tBen](https://openreview.net/forum?id=q3MYZQ3es8) (2024/2025) | Synthetic DatalogMTL benchmark for rule-based temporal-logic reasoning with configurable rule complexity. | **Medium on temporal-rule DSL and scalable exact labels.** | Time is inside the object-level logic; the governing rule set itself is not versioned. |
| [Do LLMs Truly Understand When a Precedent Is Overruled?](https://arxiv.org/abs/2510.20941) (JURIX 2025) and [CaseFacts](https://aclanthology.org/2026.acl-long.785/) (ACL 2026) | Temporal validity of precedent, overruled authorities, era sensitivity, and evolving legal truth. | **Medium-high on legal temporal validity beyond statutes.** | Precedent status and retrieval rather than explicit versioned rule execution. |

## Why the direct predecessor is fatal

Prior et al. did not merely note that law becomes stale. Their design deliberately pairs statute versions around substantive changes, generates fact patterns whose legal consequence changes depending on the version, and includes pre-amendment questions where a current rule is available but historically inapplicable. Experts rejected cases where the amendment was editorial, where the answer did not change across versions, or where the generated answer was legally wrong. Their rubric separately scores outcome, reasoning, legal basis, and version application.

The released artifact is thinner than the paper's full experimental stack—the repository currently exposes an Excel QA set and prompt directory, but not a turnkey reproduction harness. That is an artifact limitation, not an unoccupied scientific question. Releasing a cleaner DSL and runner would improve reproducibility, but artifact quality alone cannot rescue novelty.

The paper's important weaknesses do identify a possible follow-up:

1. Its ground truth is open-ended text and its outcome/version metrics are assigned by an LLM judge rather than a deterministic executor.
2. It does not force a version-ID choice before application, so wrong selection and wrong rule execution are inferred from answers rather than separately observed.
3. It does not randomize the order, position, labels, duplication, or salience of competing versions.
4. Its recency-bias result is strongest in web retrieval and is not consistently significant in other conditions.
5. Its questions are all German statutory law; it does not establish that any failure is a domain-general temporal-control phenomenon.

These are good extension points. They are not enough to retain F3's present “first domain-general version fidelity benchmark” framing.

## The only plausible pivot: a causal mechanism study

A narrower general technical contribution may survive, but it should not be sold as discovering temporal rule-version fidelity. The sharp question is:

> **When all competing rule versions and a decisive event date are present in context, how much end-to-end error is caused by failure to map the event date to the governing version, versus failure to execute a correctly selected rule, and is the selection error causally amplified by version order or “current/latest” salience beyond matched non-temporal conflict controls?**

This is a mechanism-and-identification paper, not a broad benchmark paper. It must make each stage observable:

- **Selection task:** output only the applicable version ID from the event date, effective intervals, and transition clauses.
- **Oracle-application task:** receive only the correct selected rule text and output the exact decision.
- **End-to-end task:** receive all versions and the case, then output version ID plus exact decision.
- **Repair task:** after a wrong answer, receive either effective-date metadata, the governing version, or an execution counterexample. Documentation-assisted repair in general is occupied; the contribution must be the *differential causal value* of these repair signals.

Cases must be counterfactually discriminating: executing at least two candidate versions on the same facts must yield different labels. Otherwise, end-to-end correctness cannot identify version fidelity because a model can choose the wrong version and still obtain the same answer.

A useful decomposition is to report:

\[
p_S=P(\hat v=v^*), \qquad
p_A=P(\hat y=y^*\mid \text{oracle }v^*), \qquad
p_E=P(\hat v=v^*,\hat y=y^*),
\]

plus the probability of a **version-consistent wrong answer**: the model selects version \(v\neq v^*\) and outputs exactly the label produced by executing \(v\). That quantity distinguishes systematic rule substitution from generic reasoning error.

The core factorial should cross:

- applicable version (old, middle, new);
- chronological presentation (ascending, descending, randomized);
- positional placement of the applicable version (first, middle, last);
- neutral IDs versus “old/current/latest” labels;
- explicit requested version versus event-date-derived applicability;
- all versions versus oracle-only text;
- substantive migration type (threshold, exception, precedence, scope, deadline);
- matched non-temporal rule conflicts with identical token/order structure.

The publishable result would be an interaction showing that models exhibit a temporal-applicability error beyond ordinary position, label, context-memory conflict, and rule-execution difficulty. A main effect of “latest text wins” without those controls is already anticipated by the literature.

## Minimal real-rule validation

Do **not** create another broad legal QA dataset. Reuse one public executable rule family and validate only the synthetic causal finding.

The least risky choice is a small, versioned extension of DeonticBench/SARA using official archived U.S. federal income-tax rules across three regimes surrounding a substantive change (for example, pre- and post-2018 standard-deduction/exemption rules plus one adjacent annual regime). Build version-specific Prolog modules from official archived IRC/IRS materials, and generate paired facts for which at least two regimes yield different exact tax or entitlement labels.

Minimum credible validation:

- at least six independently substantive rule changes across three effective-date regimes;
- 30–50 counterfactually discriminating paired cases;
- exact execution under every version, with a published cross-version label matrix;
- two-person manual verification of effective intervals, transition rules, and a sample of executions;
- the same counterbalanced version-order and neutral/current-label interventions used in the synthetic DSL;
- direct comparison with at least one subset or protocol from Prior et al., rather than implying their benchmark does not exist.

This validation is sufficient only if the synthetic temporal-salience interaction replicates. A single easy threshold table is not enough; it would confound date selection with arithmetic and could be dismissed as a toy transfer.

## Novelty condition for the pivot

The pivot survives only if all of the following are true:

1. The paper leads with **causal decomposition of temporal applicability**, explicitly positioning Prior et al. as the direct predecessor.
2. Version selection is observed through a forced exact version ID, not inferred from a chain-of-thought rationale or an LLM judge.
3. Rule application has an oracle-version condition and deterministic labels, permitting selection and execution errors to be estimated separately.
4. Every primary item is counterfactually version-discriminating, and the benchmark publishes the full version-by-item execution matrix.
5. Placement, order, semantic labels, and general context conflict are counterbalanced so “recency bias” is not just a last-item or “latest” lexical shortcut.
6. The primary claim is an interaction or decomposition not reported in Asking For An Old Friend, GitChameleon 2.0, Task Matters, or the instruction-hierarchy diagnostics.
7. The real-rule study uses official version provenance and exact execution, but remains a validation domain rather than the claimed novelty.
8. The artifact releases the DSL, generators, version graphs/effective intervals, all prompts, model outputs, deterministic scorers, and analysis code.

## Rejection conditions

Reject the project if any of the following remains true after redesign:

- The title or abstract claims to introduce temporal historical-rule fidelity, stale-law diagnosis, or recency bias as a new problem.
- The contribution is still “version fidelity beyond code.” Prior et al., CLAW, and historical-precedent benchmarks already take the problem beyond code.
- The study merely replaces German law with synthetic institutional policies and one other legal rule family.
- Documentation-assisted repair is a headline contribution. Quantum API Drift, When LLMs Lag Behind, GitChameleon 2.0, and Prior et al. already evaluate documentation/RAG/repair.
- Selection and application are separated only by inspecting free-form rationales or asking another LLM to label error types.
- The version DSL is the main novelty. tBen, DeonticBench, and OpenExempt already establish synthetic/executable rule frameworks.
- Cases do not change answer across candidate versions, making “correct answer” an invalid proxy for correct version selection.
- The only controls are ascending versus descending order; generic position, lexical “latest,” context-memory conflict, and instruction-priority effects remain unseparated.
- The real-rule source lacks official historical text, effective intervals, or transition provisions that can be verified without expert legal interpretation.
- The study cannot compare against or reproduce a meaningful subset of Asking For An Old Friend, DeonticBench, or GitChameleon-style baselines.
- The planned result is just another model leaderboard. The surviving value is a mechanism, not a score table.

## Recommended disposition

**Reject F3 from the finalist slate in its present form.** Its working question and most of its claimed novelty were independently published at ICAIL 2026, while adjacent 2025–2026 work supplies the historically versioned corpora, executable legal rules, version-conditioned code benchmarks, context-memory controls, and stage-wise diagnostics.

If the program wants to preserve the institutional-rule theme, open a **new candidate** rather than lightly editing F3:

**Working title:** *Which Rule Was in Force? Causal Decomposition of Temporal Applicability Errors in Language Models*

**Contribution statement:** A counterbalanced, executable experiment that directly observes event-date-to-version selection, oracle-conditioned rule execution, and end-to-end decisions; estimates version-consistent substitution errors; and tests whether temporal applicability creates failures beyond matched positional and context-memory conflicts, with a small official real-rule replication.

That pivot is narrower and plausibly general. It remains high risk because it is assembled from well-established components, and its novelty depends on a clean interaction result rather than on releasing another benchmark.

## Search scope and evidence status

This audit searched primary literature and released artifacts through 2026-07-17 across: historical/versioned rule following, statutory temporal applicability, recency and stale-knowledge bias, overruled precedent, time-sensitive QA, temporal logic, context-memory conflict, instruction hierarchy, evolving policies, API/SDK drift, version-conditioned code, documentation/RAG repair, and executable legal reasoning. It inspected the full text or official paper/artifact pages for the load-bearing works, including the data/prompt repository for Prior et al., the DeonticBench repository, and the Quantum API Drift repository.

The search found an exact direct predecessor, so absence-of-evidence uncertainty is not the deciding issue here. A final search before any pivot should nevertheless check citations to Prior et al. and new ACL/ICML/NeurIPS 2026 releases for a factorial temporal-applicability diagnostic matching the proposed mechanism study.
