# Adversarial experimental-design and statistical audit of F1-F3

**Audit date:** 2026-07-17
**Inputs:** `selection-synthesis-v0.md` and the full F1, F2, and F3 literature/novelty audits
**Role:** Attempt to show that each surviving claim is unidentified, underpowered, or pseudoreplicated before any model calls are authorized
**Overall verdict:** **F1 can be made identifiable with a sharply staged paired design. F2 is identifiable only after adding an outer sampling/reference-population design that is not yet in the proposal. F3 as originally stated remains rejected; its pivot is high-risk and its proposed selection/application decomposition is not causal unless it becomes an explicit two-stage intervention.**

No numerical power claim is made below. Any final item count must come from a frozen design simulation using a predeclared smallest effect of scientific interest (SESOI), realistic baseline accuracy, cluster variance, invalid-output rates, and the actual planned estimator.

## Cross-candidate rules

### What is and is not an independent observation

| Candidate | Primary independent unit | Nested observations that must not be counted as independent |
| --- | --- | --- |
| F1 | A frozen target case or independently generated case sequence, clustered within a rule schema/world | Repeated decoding samples, prompt-format variants, history arms applied to the same target, and multiple targets generated from one near-identical template |
| F2 | A source/seed problem for task-population inference; an independently sampled benchmark realization for coverage inference | Surface variants from one seed, repeated model samples on one variant, and repeated generator calls on the same fixed seeds |
| F3 pivot | An independently substantive rule change/migration; target cases are nested within it | Paraphrases, fact variants, presentation permutations, model calls, and 30-50 cases produced from the same few amendments |

The evaluated model snapshots are normally a **fixed panel**, not a random sample from a population of models. Three or five models do not justify a random-model population claim. Report panel-average and model-specific results, and restrict conclusions to the named snapshots unless models were sampled under a defensible design.

### Repeated calls

If decoding is deterministic, repetitions add no information except platform nondeterminism. If decoding is stochastic, repetitions estimate the response distribution of one model snapshot on one prompt. They may reduce Monte Carlo error for that prompt, but they do not increase the number of target cases, seed families, or rule migrations. Any analysis that places repeated calls in the denominator as if they were new cases is pseudoreplication.

### Common freeze rule

Before confirmatory outcomes are inspected, freeze:

- task/generator code and commit hashes;
- rule texts, solvers, target items, family/migration identifiers, and all prompt bytes;
- model IDs/snapshots, inference stack, decoding settings, and retry policy;
- exclusions, output grammar, scorers, primary estimand, SESOI, model formula, multiplicity procedure, and simulation code;
- the exact scheduled number of independent units and calls.

Stopping must be schedule-based, not result-based. A pilot may estimate nuisance parameters only on disjoint pilot items and must never be folded into confirmatory results unless an adaptive design and combination rule were preregistered. A discovered generator/solver defect may trigger a full pre-outcome rebuild; after outcomes are visible, corrections require a versioned new cohort and transparent reporting of both analyses.

## F1 - causal decomposition of cross-case carryover

### Audit verdict

**Conditional advance, major statistical narrowing.** The paired target design can identify history effects, but the current phrase “how much is attributable to prior case text, labels, gold rationales, or the model's own rationales” overstates what a simple arm comparison can establish. In particular, gold and model-generated rationales differ simultaneously in content, correctness, length, style, role metadata, and generation process. A gold-versus-own comparison does not identify “self-commitment.” Either cross-feed frozen identical records under manipulated role/source attribution, or rename the estimand to the effect of exposure to a frozen model-generated history distribution.

The full Cartesian product suggested by the novelty audit is also too large for a first paper. The confirmatory experiment should be split into an attribution stage and a boundary-intervention stage with a small set of planned contrasts.

### Experimental units and sampling frame

- **Primary unit:** frozen target case (i), sampled from a declared population of executable cases.
- **Clustering:** targets are nested in independently designed rule schemas (s), themselves nested in rule worlds (w). Cases that differ only by a threshold value or paraphrase are variants, not independent targets.
- **Repeated measures:** every target is evaluated under the planned history conditions. This pairing is the major source of efficiency and must be preserved in randomization, storage, and analysis.
- **History unit:** a frozen history sequence (q). If the same history sequence is paired with many targets, it is a crossed cluster and requires a history-sequence random effect or sequence-level resampling.
- **Model:** fixed effect. Model-by-treatment interactions are reported; a pooled “LLMs” conclusion is not licensed.
- **Stochastic repetitions:** nested within target × history × boundary × model. They estimate decoding probability only.

The target-case sampling frame must be frozen before histories are run. Difficulty calibration uses disjoint pilot cases. Selecting confirmatory cases because a model is history-sensitive is outcome-conditioned sampling and invalidates prevalence or average-effect claims.

### Outcomes

**Primary outcome for directional carryover:** exact binary/finite decision (D_{im}(h,b)), not accuracy. If prior positive and negative streaks shift an identical target in opposite directions, averaging accuracy across positive- and negative-label targets can cancel the effect.

**Co-primary only if the budget supports multiplicity correction:** exact accuracy

\[
A_{im}(h,b)=\mathbf 1\{D_{im}(h,b)=y_i^*\}.
\]

Prefer one primary and make the other key secondary.

**Secondary outcomes:**

- structured rule/threshold error, only where the model emits a deterministically scorable rule ID or numeric intermediate value;
- refusal, schema-invalid response, and extractable-but-nonconforming response rates;
- latency and tokens, descriptive only;
- model-specific treatment heterogeneity;
- persistence over predeclared horizons.

Free-form chain-of-thought labels cannot serve as ground-truth mechanism outcomes. “First misapplied rule” is valid only if obtained from a constrained trace that an independent executor can verify.

### Explicit estimands

Let $H^+$, $H^-$, and $H^0$ be token/position/format-matched histories containing positive, negative, and balanced/neutral outcome information. Let $N$ be matched neutral material. Let $B_0$ denote no boundary marker/full retained history.

1. **Directional streak effect:**

\[
\tau_D=E_{i,m}\left[D_{im}(H^+,B_0)-D_{im}(H^-,B_0)\right].
\]

This is the cleanest serial-dependence estimand. It requires the positive and negative histories to be exchangeable except for the manipulated outcome channel. Naturally sampled positive and negative cases will not satisfy that condition without counterfactual pairing and balancing.

2. **History-induced excess error for channel $k$:**

\[
\tau_{E,k}=E_{i,m}\left[A_{im}(H^k,B_0)-A_{im}(N,B_0)\right].
\]

The neutral history must match target position, total token budget, turn structure, surface format, and assistant/user-role pattern. Otherwise this estimand combines semantic carryover with generic load and role-position effects.

3. **Incremental label effect:**

\[
\tau_L=E\left[D(H_{case+label})-D(H_{case+neutral\ label})\right].
\]

The control needs label-shaped, role-matched inert tokens. Comparing case-plus-labels with case-only histories is not enough because it also changes length and assistant-turn structure.

4. **Incremental rationale effect:**

\[
\tau_R=E\left[D(H_{label+rationale})-D(H_{label+matched\ inert\ rationale})\right].
\]

Gold-rationale versus no-rationale is a practical contrast but not a pure semantic-rationale effect unless token and format load are matched.

5. **Operational boundary effect for boundary $b$:**

\[
\tau_{B,b}=E\left[A(H^{*},b)-A(H^{*},B_0)\right],
\]

where $H^{*}$ is one predeclared history condition, chosen before confirmatory outcomes. A hard fresh context necessarily removes history, whereas assistant deletion retains user-side case text. These are different interventions, not levels of a latent psychological “reset.” The estimand is comparative operational mitigation, not a pure boundary mechanism.

6. **Model-generated-history effect:**

\[
\tau_M=E_{Q\sim G_m}\left[D(Q)-D(Q^{gold/matched})\right].
\]

This averages over a frozen distribution $G_m$ of records generated by model $m$. It does **not** identify an effect of the model recognizing its own words. To claim self-conditioning, cross the identical frozen text with assistant versus quoted-user placement and, if used, truthful source attribution. Even then, the conclusion concerns role/source cues, not private memory of authorship.

### Factorial structure that remains feasible

Do not run one enormous partially empty factorial. Use two confirmatory modules.

**Module A: source attribution**

- history content: neutral; case text only; case + gold label; case + gold label/rationale; frozen model-generated record;
- streak: positive; negative; balanced where logically applicable;
- horizon: three frozen lengths;
- target label/difficulty margin: balanced blocks, not treatments;
- model and rule world: fixed blocking factors.

Every incremental channel needs a token/format-matched comparator. Counterfactual prior-case twins should alter only the rule-relevant fact needed to flip the gold outcome, and the assignment of twins to history direction should use a Latin-square or equivalent balancing schedule. If outcome labels are simply falsified while case facts remain fixed, the experiment measures reaction to contradictions, not natural serial carryover; report that as a separate label-only manipulation.

**Module B: boundary operations**

- retained full history/no marker;
- identical retained history plus soft independence marker;
- prior user cases retained, assistant history deleted;
- literal fresh context containing byte-identical system/rule/target blocks;
- optional recap only as an exploratory practical intervention.

Apply Module B to one predeclared high-information history type and the neutral control. Choosing the “worst” history after seeing Module A requires a held-out confirmation set or renders Module B exploratory.

### Randomization and paired/hierarchical analysis

- Construct the full target × condition schedule first.
- Randomize call order outside conversations and interleave conditions/models over clock time to prevent provider drift from aligning with treatment.
- Never place two alternative treatments for the same target in one conversation.
- Use deterministic prompt construction and hash every prompt.

Primary analysis should be a paired generalized linear mixed model or a target-level randomization analysis. A suitable logistic model includes fixed history/streak/boundary/model terms and predeclared interactions, a target intercept, rule-schema/world effects, a crossed history-sequence intercept where histories are reused, and—if estimable—target or schema random slopes for the primary treatment. With only two or three rule worlds, treat world as fixed and do not rely on asymptotic random-world inference.

Report marginal risk differences as the main effect scale even if estimation uses log odds. Verify the mixed-model result with a paired cluster bootstrap that resamples the highest generalization unit: rule schema/world first, then targets, while preserving all within-target arms. A call-level bootstrap is invalid.

### Multiplicity

- Freeze one primary contrast: preferably $H^+$ versus $H^-$ on decision propensity, averaged over a named fixed model panel.
- Gate incremental label/rationale tests behind evidence of an overall non-neutral history effect, or control their family-wise error with Holm/max-$T$.
- Boundary comparisons form a second family and require simultaneous intervals against full-history control.
- Horizon trend should be one planned contrast, not three independent pairwise tests.
- Model-, world-, threshold-margin-, and error-type decompositions are secondary/exploratory unless separately powered.

The paper must not select whichever model/history/horizon produces significance and then describe it as the primary effect.

### Invalid outputs and missingness

- Use a strict, published output schema and deterministic parser.
- A refusal or content-bearing response that fails to produce a valid decision counts as incorrect for the primary task-performance analysis and is also reported separately.
- If a valid decision can be deterministically extracted from a schema-invalid response, report a prespecified sensitivity analysis; do not manually rescue responses.
- Transport/API failures are not model errors. Retry only under a fixed capped policy using the same prompt and decoding seed. Remaining failures are missing, tabulated by condition/model, and handled with complete-case plus worst/best-case sensitivity bounds.
- Do not condition target analysis on prior model turns being correct or schema-valid. That selects histories post-treatment. Either include the generated history as produced under an intention-to-treat pipeline estimand, or generate and quality-freeze the history bank before target assignment and explicitly redefine the target population.

### Power and design simulations required

Before freezing $N$, simulate the exact mixed/paired analysis under:

- pilot-derived baseline decision probabilities by model, world, and target-label margin;
- a grid of target/schema/history-sequence intraclass correlations;
- the predeclared SESOI on both risk-difference and log-odds scales;
- treatment heterogeneity across models and worlds, including sign reversals;
- realistic invalid-output and API-missingness patterns;
- all planned multiplicity corrections;
- ceiling/floor scenarios and sparse separation.

For each candidate design, report rejection probability under the SESOI, type-I error under zero effect, interval coverage, convergence/singularity rate, and bias of the marginal risk-difference estimator. Choose the smallest design meeting predeclared operating targets. If no affordable design does, reject F1 rather than replace independent targets with repeated calls.

### Strongest unresolved confounds

1. Positive versus negative case histories change case semantics as well as outcomes.
2. Gold versus model rationales confound provenance with quality, correctness, style, length, and role.
3. Reused history sequences create crossed dependence across targets.
4. Soft marker, assistant deletion, and hard reset remove different information; their differences are not a single reset mechanism.
5. A target later in a long prompt differs in position even if its bytes are intact; only a length/format-matched neutral history addresses this.
6. Synthetic cases from one template may give hundreds of apparent items but only a handful of independent rule structures.
7. Provider updates or load-dependent nondeterminism can align with condition if calls are not interleaved.
8. An accuracy null can hide equal-and-opposite directional shifts.

### Minimum publishable sample structure

This is a structural minimum, not a power claim:

- at least two non-mathematical executable rule worlds and preferably the three-world novelty condition;
- multiple independently designed rule schemas per world, with target count determined by the frozen simulation at the schema/target level;
- every confirmatory target observed in every primary history arm for pairing;
- three named model families/snapshots if retaining the cross-family novelty claim, analyzed as fixed panel members;
- three frozen horizons only if the simulation shows the treatment-by-horizon trend is estimable;
- an independent frozen history bank or independently randomized histories, with sequence identifiers exposed;
- disjoint pilot, confirmatory, and—if selecting an intervention after Module A—held-out confirmation cases.

If budget permits only one rule world, one model, four loosely matched context arms, or many repeated calls on few targets, the minimum claim is not earned.

### F1 verdict

**Advance only after rewriting the claim and preregistering the staged design.** The causal history and boundary contrasts are identifiable. “Attribution to the model's own rationale” is not identified as currently phrased, and a full factorial is likely unaffordable. F1 is the strongest of the three candidates if it prioritizes one directional estimand, uses independent schemas/targets, and treats rationale/source and boundaries as carefully controlled secondary modules.

## F2 - joint validity-bias and coverage audit of generated benchmark families

### Audit verdict

**Not yet identified.** The proposal correctly defines seed-family dependence, but repeated generator draws on the same fixed source seeds do not reveal coverage for new problem concepts. More seriously, empirical interval coverage is not observable unless the study defines a truth against which intervals are checked. A single generated benchmark—or ten repeated generations—can show score/rank variability but cannot establish that an interval procedure has 95% or any other nominal coverage.

F2 requires both an explicit sampling population and either a finite reference population with known model scores or a simulation with known truth. Without that outer design, its central “miscoverage” claim is rhetoric.

### Experimental units and hierarchy

For generator $g$, task/corpus $t$, realization $r$, source seed $s$, variant $x$, and evaluated model $m$:

- **task-population unit:** source seed $s$;
- **generator-realization unit:** $r$, only if generator version, prompt, decoding distribution, and source-seed sampling protocol are frozen;
- **nested variant:** $x\sim G_g(\cdot\mid s)$;
- **paired model observation:** all models answer the same $x$;
- **stochastic response repetition:** nested below $x,m$, not an additional benchmark item.

If each generator is applied to a different benchmark/domain, generator is perfectly confounded with task and seed population. Generator-level comparisons then are descriptive case studies, not estimates of generator-regime effects. To compare generators, cross each generator with the same seed corpora or apply every generator to at least two common task domains.

### Target populations and estimands

F2 must choose among:

1. a finite frozen seed set;
2. future variants of those seeds under one pinned generator;
3. new seeds from a declared task population.

The novelty claim needs target population 3, while many feasible experiments identify only target population 2.

Let $V_{gsx}$ indicate independently adjudicated validity and $Y_{mgsx}$ exact correctness. For equal seed weighting, the valid-variant capability estimand is

\[
\theta^{valid}_{m,g}
=E_S\left[
\frac{E_X\{Y_m(X)V(X,S)\mid S\}}
{E_X\{V(X,S)\mid S\}}
\right],
\]

defined only on seeds with positive probability of a valid generation. This estimand differs from the pooled mean among all valid variants, which overweights large/easy/high-validity families. The paper must choose one and not switch according to convenience.

For a predeclared model pair $a,b$:

\[
\Delta^{valid}_{ab,g}=\theta^{valid}_{a,g}-\theta^{valid}_{b,g}.
\]

Define an equal-seed raw estimand using all emitted scorable variants, then

\[
B_{ab,g}=\Delta^{raw}_{ab,g}-\Delta^{valid}_{ab,g}.
\]

This is **validity bias only if raw and valid estimands use the same seed weighting**. Otherwise $B$ mixes invalidity with informative family-size weighting.

For interval procedure $j$, coverage is

\[
C_j=P_R\{\Delta^{truth}_{ab,g}\in I_j(R)\}.
\]

The probability is over a fully defined repeated benchmark-sampling process. “Truth” must be known or approximated with uncertainty. Repeated draws from fixed seeds identify conditional-generator coverage, not new-seed task-population coverage.

Rank-decision distortion should be defined against a simultaneous rank confidence set, not point ranks:

\[
R_j=P_R\{\mathcal C^{naive}_R\neq\mathcal C^{family}_R\},
\]

with a stricter secondary measure for whether substantive dominance conclusions differ. Mere set inequality can be driven by trivial boundary changes and should not be oversold.

### Required two-part design

**Part A: empirical generator audit**

- at least two pinned open generator systems with different construction regimes;
- each crossed with common seed corpora/tasks;
- multiple independently seeded complete realizations;
- identical evaluated-model panel on every variant;
- deterministic/formal validity checks where available and blinded independent adjudication for residual semantic validity;
- raw outputs, family sizes, generation failures, validity reasons, and all model responses retained.

This part estimates validity rate, invalidity-model-performance association, variance components, paired gaps, and how conclusions change after correction. It does not by itself prove nominal coverage.

**Part B: coverage calibration with known truth**

Use one of two designs:

- **Finite reference bank:** construct and fully score/audit a large two-stage population of seeds and variants. Define its equal-seed model gap as finite-population truth, repeatedly sample benchmark realizations from the bank, and measure interval/rank-set coverage. The claim is limited to this bank and sampling protocol.
- **Calibrated simulation:** fit nuisance ranges from Part A, then simulate seeds, family sizes, validity, paired model outcomes, and generator runs under known parameters. Vary invalidity-difficulty correlation, informative family size, ICC, and model-specific invalidity effects. Coverage claims are simulation claims, not direct facts about future generator output.

A nested Monte Carlo approximation to the live generator population is possible, but its reference truth has Monte Carlo uncertainty and may be prohibitively expensive. That uncertainty must propagate into reported coverage.

### Factorial/sampling structure

- generator regime $g$: at least two;
- common task/domain $t$: at least two if claiming cross-generator regularity;
- generator realization $r$: repeated complete draws;
- source seed $s$: sampled as the primary unit;
- variant $x$: nested in $s,r,g,t$;
- validity $V$: measured property, not randomized treatment;
- evaluated model $m$: paired fixed-panel factor.

Invalidity and dependence cannot be said to “interact” merely because both exist. A joint result should predefine, for example, a generator × validity-status difference in paired model performance and show that filtering invalid variants changes seed-level variance/coverage or the substantive confidence set. Because validity is not randomized, such an interaction is associational and may reflect difficulty or construct drift.

### Outcomes

**Primary empirical outcomes:** validity rate with seed-weighted uncertainty and validity bias $B_{ab,g}$ for one predeclared model pair.

**Primary calibration outcome:** empirical coverage error of the naive item-wise interval versus the family-aware interval under the known-truth sampling/simulation design.

**Secondary:** interval width, variance components/ICC, family-size informativeness, rank-confidence-set coverage/size, dominance-decision disagreement, generator failure rate, and model-specific effects. Point-rank reversals are descriptive and not an inferential endpoint.

### Paired/hierarchical analysis

Compare at least:

1. naive item-wise analysis, preserved as the deliberately misspecified baseline;
2. two-stage seed-cluster bootstrap, resampling seeds and retaining all within-seed variants and paired model responses;
3. a predeclared multilevel paired model with seed, realization, and variant levels as the generator hierarchy requires;
4. simultaneous rank-set inference whose coverage is validated in Part B.

Analyze paired correctness differences or a joint/bivariate Bernoulli model rather than separate independent proportions for each model. Unequal and informative family sizes require equal-seed weights or an explicit target that weights variants. A random-intercept logistic model alone does not automatically recover the desired marginal equal-seed gap; compute and report marginal standardization.

The cluster bootstrap must match the inferential population. Resampling variants within fixed seeds cannot generalize to new seeds. Resampling seeds from a convenience set cannot generalize beyond that set without a sampling argument. If generator realizations are also a target of inference, resample or model that level too.

### Multiplicity

- Predeclare one primary model pair, generator contrast, task aggregate, and confidence level.
- Treat all other model pairs with max-$T$, closed testing, or a simultaneous rank-confidence-set procedure.
- Validity bias, coverage error, interval width, and rank disagreement are different endpoints; designate primary/co-primary endpoints and adjust or gate them.
- Generator × domain × model interactions are exploratory unless the design simulation powers them.
- Do not search across generators, tasks, model pairs, filtering rules, and interval methods for the largest rank change.

### Invalidity, generator failure, and missingness

- Invalid variants remain in the raw estimand and generator-validity denominator; they are excluded only from the explicitly conditional valid estimand.
- Report construct drift, wrong label, unsatisfiable/ambiguous item, parser failure, and duplicate as separate validity categories.
- A seed with zero valid variants creates a positivity failure for the per-seed conditional-valid estimand. Do not silently drop it. Report its frequency and either restrict the estimand to support-positive seeds or fit a predeclared model that acknowledges partial identification.
- Generator failure/no output is not a valid variant and not ordinary missingness. Report availability separately and include it in an end-to-end generator utility outcome if desired.
- Evaluated-model refusal/schema failure counts as incorrect for task performance and separately as invalid output. Transport failures follow a capped retry policy and then receive missingness bounds.
- Human/adjudicator disagreement is measurement error, not proof of ambiguity. Use blinded independent reviews, adjudication rules, and a sensitivity analysis for plausible validity-label misclassification. An LLM judge from the generating model family cannot be the sole ground truth.

### Power, coverage, and design simulations required

No item count is defensible without nested simulation. Simulate:

- seed-level difficulty and paired model advantage;
- unequal/informative family sizes;
- generator-run variation;
- within-seed correlation varying by generator/model/task;
- invalidity correlated with seed difficulty, model advantage, and surface form;
- adjudication error and zero-valid-variant seeds;
- API missingness and model refusals;
- ties and near-ties relevant to rank sets.

For effect estimation, choose a SESOI for validity bias/model-gap change and solve for the required number of independent seeds and realizations under the exact estimator. For coverage calibration, choose an acceptable Monte Carlo standard error ε and determine the number of independent replications (R) from

\[
MCSE(\hat C)=\sqrt{C(1-C)/R},
\]

using a conservative value of $C(1-C)$ when $C$ is unknown. The reference-truth bank or outer simulation must be large enough that truth-estimation error is negligible relative to the chosen MCSE or explicitly propagated. Report coverage, interval width, type-I error, rank-set coverage, convergence, and estimator bias across the nuisance grid.

### Strongest unresolved confounds

1. Generator is confounded with domain/seed corpus unless generators are crossed on common tasks.
2. Validity is associated with difficulty and model-specific strengths; filtering invalid variants changes the target population, not merely label noise.
3. Family size may be informative, so a pooled valid-variant mean changes seed weights.
4. Repeated generation on fixed seeds does not sample new problem concepts.
5. A finite empirical dataset has no observable frequentist coverage without reference truth.
6. Adjudicator errors can create or erase estimated validity bias.
7. Generator/evaluator model kinship can create a family-specific advantage.
8. Generator version drift destroys the repeated-draw distribution.
9. Benchmark contamination and seed memorization can masquerade as variant robustness.
10. Rank sets can change because of altered weighting even when no generator defect exists.

### Minimum publishable sample structure

This is a structural requirement; simulations determine counts:

- at least two established open generators with pinned reproducible implementations;
- each generator crossed with at least two common seed corpora/task domains if making comparative generator claims;
- enough independently sampled seed families and complete generator realizations to meet frozen bias and coverage operating targets; variants per seed cannot substitute for seeds;
- at least three evaluated model snapshots if simultaneous rank confidence sets remain a headline outcome, while one model pair is primary;
- an independent validity reference process, including deterministic execution and at least two blinded human/expert judgments where execution cannot settle semantic preservation;
- a finite truth bank or known-truth simulation for coverage;
- a disjoint pilot for nuisance estimation and a frozen confirmatory generation schedule.

If only one generator/domain, one fixed set of seeds, one generated dataset, or no independent validity ground truth is feasible, reject the joint coverage claim.

### F2 verdict

**Conditional hold, bordering on rejection for a first project.** F2 can become a rigorous measurement paper, but it is substantially larger than “cluster-aware error bars.” Its centerpiece—coverage—requires an outer truth/sampling design, and a causal comparison of generator regimes requires common tasks. Independent semantic adjudication may also require collaborators. Advance only if those resource requirements pass implementation review; otherwise the project is statistically underidentified even if its code runs perfectly.

## F3 - temporal-applicability pivot

### Audit verdict

**Original F3: reject. Pivot: high-risk conditional hold.** The pivot's selection accuracy and salience contrasts are identifiable, but the proposed quantities $p_S$, $p_A$, and $p_E$ do not by themselves answer “how much end-to-end error comes from selection versus execution.” They are results from different prompts/treatments and do not form an additive causal decomposition. A wrong selected version followed by the label that version would imply is suggestive of substitution, not proof that version selection caused the answer.

To make the causal language defensible, add an explicit two-stage pipeline: first elicit a version ID; then, in a fresh standardized application prompt, supply either that selected version or the oracle version. Keep the integrated all-versions answer as an external-validity outcome, not the source of decomposition.

### Experimental units and hierarchy

- **Primary independent unit:** substantive rule migration/change $c$.
- **Nested units:** rule family/world $w$, case facts $i$ within migration, version-order/label permutations, tasks, model calls, and stochastic repetitions.
- **Real-rule validation:** six rule changes remain six primary clusters even if they generate 50 cases. The validation can demonstrate replication within those fixed changes but cannot estimate a broad population of legal amendments with six clusters.
- **Model:** fixed panel member.

Synthetic migrations produced from one template share logic and are not independent merely because names, dates, or thresholds vary. Independence requires separately specified rule structures/transition logic, not lexical variation.

### Observable outcomes

For item $i$ with correct version $v_i^*$ and correct outcome $y_i^*$:

- exact version selection $S_i=\mathbf 1\{\hat v_i=v_i^*\}$;
- oracle application $A_i(v)=\mathbf 1\{\hat y_i(v)=y_i(v)\}$ for each candidate version, not only $v_i^*$;
- integrated end-to-end joint correctness $E_i=\mathbf 1\{\hat v_i=v_i^*,\hat y_i=y_i^*\}$;
- two-stage pipeline correctness when applying the selected version;
- version-consistent substitution: wrong selected version and output equal to the deterministic label under that version;
- refusal/schema-invalid/API-missing indicators.

Every primary case must be counterfactually discriminating across versions. Publish the full deterministic version-by-item label matrix. A case where all versions yield the same label supplies no evidence about version fidelity even if the model emits a version ID.

### Explicit estimands

Let $Z$ be a randomized salience/order treatment and $T\in\{temporal,control\}$ distinguish event-date applicability from a token/position-matched non-temporal conflict task.

1. **Selection effect of salience/order:**

\[
\tau_S(z,z')=E\left[\mathbf 1\{\hat V_i(z)=v_i^*\}-\mathbf 1\{\hat V_i(z')=v_i^*\}\right].
\]

2. **Temporal-specific salience interaction:**

\[
\tau_{TS}=
\{E[S\mid Z=z,T=temporal]-E[S\mid Z=z',T=temporal]\}
-\{E[S\mid Z=z,T=control]-E[S\mid Z=z',T=control]\}.
\]

This difference-in-differences, not a latest-position main effect, is the defensible primary novelty estimand. The matched control must use an equally structured non-temporal rule-selection criterion.

3. **Oracle execution error:**

\[
L_A=1-E\left[A_i(v_i^*)\right].
\]

4. **Interventional loss from model selection:** let $\tilde Y_i(v)$ be the decision from the standardized fresh application prompt when supplied version $v$. Then

\[
L_S=E\left[
\mathbf 1\{\tilde Y_i(v_i^*)=y_i^*\}
-\mathbf 1\{\tilde Y_i(\hat V_i(Z))=y_i^*\}
\right].
\]

Because the application prompt is held fixed and only supplied version changes, $L_S$ estimates the consequence of the selection stage under this two-stage pipeline. It is not the natural indirect effect inside an unconstrained end-to-end generation.

5. **Integrated-prompt gap:**

\[
G_E=E[E_i^{integrated}]-E[\mathbf 1\{\tilde Y_i(\hat V_i)=y_i^*\}],
\]

reported descriptively as the effect of integrating selection and execution into one prompt versus a staged pipeline. It may reflect prompt structure, context load, or self-consistency, not only execution.

The marginal $p_S,p_A,p_E$ remain useful descriptive rates. Subtracting them is not a causal error attribution.

### Factorial structure and aliasing

Use three modules rather than one oversized factorial.

**Module A: selection mechanism**

- task frame: event-date-derived applicability; explicit requested version; matched non-temporal priority/conflict;
- presentation: all six permutations of three versions or a balanced incomplete schedule justified by simulation;
- version identifiers: neutral IDs versus truthful temporal labels;
- applicable version identity: old/middle/new, balanced across items;
- migration type: threshold, exception, precedence, scope, deadline as blocked strata.

Chronological presentation and applicable-version position are not freely crossable factors. In ascending order, an old applicable version must appear before a new one. Coding “ascending/descending/random” and “first/middle/last” as a full independent factorial produces aliased coefficients. Use the six actual permutations and derive position/chronological-order contrasts from an estimable design matrix. Verify full rank before calls.

Likewise, “old/current/latest” labels carry truthful information as well as salience. Neutral-ID versus temporal-label differences do not isolate a pure lexical bias. The matched non-temporal control and explicit-version frame are necessary, and the interpretation should remain “temporal-label/order interaction,” not an internal recency mechanism.

**Module B: application and causal staging**

- oracle application under each candidate version separately, using identical application prompt format;
- application under the version selected in Module A;
- oracle-correct version intervention;
- exact deterministic scoring under every version.

**Module C: integrated prompt**

- all versions + event date, forced version ID and decision;
- same counterbalanced order/label schedule as Module A;
- compared with the staged pipeline as a secondary external-validity result.

Drop repair from the confirmatory first paper. Effective-date metadata, forced version, execution counterexample, and documentation repair add another post-error factorial whose novelty is already weak. If retained, use a held-out exploratory set and make no confirmatory repair claim.

### Randomization and paired/hierarchical analysis

- Pair every underlying item across permutations, task frames, label conditions, and oracle/staged conditions.
- Randomize and interleave calls across conditions/models/time.
- Balance applicable-version identity, target outcome, rule-text length/complexity, and transition-clause difficulty.
- Use a preregistered design matrix and prove it is full rank before data collection.

Primary analysis should model exact selection with fixed salience/order, task-frame, and model effects; the primary term is the temporal-specific interaction. Include migration random intercepts and, if supported, salience slopes; cases are nested in migrations. With few migrations, use migration fixed effects and migration-level paired/randomization inference rather than trusting cluster-robust asymptotics.

Report marginal risk differences and simultaneous intervals. Verify with a hierarchical bootstrap that resamples rule families/migrations first, then cases while preserving all within-case permutations. Never bootstrap presentation rows independently.

For the two-stage pipeline, estimate $L_S$ by paired item differences under selected-versus-oracle supplied versions. Because selected version is a post-randomization mediator, causal claims should be limited to the explicit interventional pipeline. Do not regress outcome on observed selection correctness and call the coefficient a causal selection effect.

### Multiplicity

- One primary estimand: τ_TS for a single predeclared salience contrast.
- Selection main effects, oracle application, $L_S$, integrated-prompt results, and version-consistent substitution are key secondary outcomes with a gatekeeping order.
- Migration-type and model-specific interactions are exploratory unless independently powered.
- Six permutations should be summarized through planned contrasts, not 15 pairwise comparisons.
- Real-rule validation tests replication of direction/magnitude under one predeclared contrast; it is not a new discovery family.

### Invalid outputs and missingness

- Force exact version IDs and decisions through a strict schema.
- Wrong/invalid version ID is a selection failure. A valid decision paired with invalid version ID fails joint end-to-end correctness.
- Refusal/schema failure counts as task failure and is separately reported.
- If the selected-version pipeline receives an invalid version ID, do not silently replace it with the oracle. Score pipeline failure; an oracle-rescued sensitivity analysis is secondary.
- Transport failures follow a fixed capped retry policy; remaining missingness is reported with worst/best-case bounds.
- Transition-clause or official-version ambiguity discovered during blinded legal verification invalidates the item before model outcomes. Post-outcome legal relabeling requires versioned disclosure and sensitivity analysis.

### Power and design simulations required

Simulate the exact nested binary design under:

- baseline selection and application accuracy by model and migration type;
- migration- and rule-family-level heterogeneity;
- within-item correlation across permutations and task frames;
- a grid of temporal-specific salience interactions centered on the SESOI;
- generic position effects that are as large as or larger than the temporal interaction;
- label/order aliasing and unbalanced missing cells;
- invalid output and transport missingness;
- only a small number of real-rule migrations.

Evaluate type-I error for τ_TS under generic position effects but zero temporal-specific interaction, power at the SESOI, interval coverage, bias, model convergence, and robustness of the migration-level bootstrap/randomization test. Increase the number of independent migrations—not merely cases per migration—until operating targets are met. If the required migration count is infeasible, the mechanism claim is underpowered.

For the real-rule arm, simulate what six independent migrations can and cannot establish. If it cannot support an inferential replication test, preregister it as a fixed-domain descriptive validation and report migration-level paired effects without population-wide legal claims.

### Strongest unresolved confounds

1. Presentation order and applicable-version position are structurally aliased unless permutations are designed correctly.
2. Temporal labels add information as well as salience.
3. Event-date parsing, interval mapping, transition-clause interpretation, and rule execution are distinct failure stages.
4. Version texts differ in length and substantive complexity.
5. Cases nested in one amendment create severe pseudoreplication.
6. A version-consistent wrong label may be coincidence, not proof of causal substitution.
7. Oracle and integrated prompts change context and task structure, so marginal rate differences are not an additive decomposition.
8. Parametric knowledge conflicts and contamination may differ between synthetic and real rules.
9. A simple threshold migration can reduce the task to date lookup plus arithmetic and may not generalize to exceptions or precedence.
10. Official legal applicability may require expert interpretation of transition provisions; a solo annotation is not independent ground truth.

### Minimum publishable sample structure

This is a structural minimum; simulation determines item counts:

- several independently specified synthetic rule families/worlds, with multiple independent migrations rather than many surface cases from one migration;
- all five claimed migration types represented by independently substantive changes if the paper generalizes across them;
- enough migration clusters to estimate the primary interaction under the frozen simulation; cases per migration cannot repair too few migrations;
- at least three fixed model families if claiming cross-model regularity;
- all three candidate versions executed on every primary case and a published cross-version matrix;
- a full-rank counterbalanced permutation schedule and matched non-temporal conflict control;
- for real-rule validation, the novelty audit's floor of at least six substantive changes across three regimes and 30-50 discriminating cases, with two-person verification, while treating six changes—not 30-50 cases—as the independent replication count;
- disjoint pilot and confirmatory migrations.

If the real validation has only one easy threshold table, if fewer migrations are available than the design simulation requires, or if no second qualified verifier can check effective intervals and transitions, reject the pivot.

### F3 verdict

**Reject original F3. Hold the pivot behind a design-simulation and verification gate.** Its primary temporal-specific selection interaction is identifiable with full permutation counterbalancing and matched controls. Its selection-versus-execution causal claim is unidentified under the proposed $p_S,p_A,p_E$ comparison and requires the explicit selected-versus-oracle two-stage intervention above. Even repaired, F3 is a risky first project because the effective sample size is the number of substantive migrations and the real-rule ground truth requires independent legal verification.

## Comparative recommendation

| Candidate | Identification after repair | Main statistical bottleneck | Resource risk | Statistical disposition |
| --- | --- | --- | --- | --- |
| F1 | Strong for paired directional and excess-error contrasts; weak for “own rationale” unless cross-fed | Independent schemas/targets and crossed history sequences | Moderate | **Advance first** with staged scope |
| F2 | Strong only with a reference truth/outer simulation and common generator-task crossing | Seeds and independent benchmark realizations, not variants | High | **Hold; reject if outer design or independent adjudication is infeasible** |
| F3 pivot | Strong for selection interaction; causal decomposition needs two-stage intervention | Independent migrations and legal verification | High | **Hold as a new candidate; original remains rejected** |

The best first-project design is therefore F1 after removing or demoting the self-rationale mechanism claim. It offers the clearest paired randomization, objective outcomes, and interpretable null without requiring external semantic adjudication or a large population of independently verified historical rule changes. F2 is the strongest measurement-methods concept but may exceed a solo first project's annotation and simulation budget. F3's pivot should proceed only if a bottom-up migration inventory and power simulation show that the independent-cluster requirement is affordable.
