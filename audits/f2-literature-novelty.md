# F2 adversarial literature and novelty audit

**Candidate:** Are dynamic benchmark variants independent evidence?
**Audit date:** 2026-07-17
**Verdict:** **Major revision**

## Bottom line

F2 does **not** survive with its current contribution claim: “jointly measure semantic-preservation failures and family dependence, then recompute rankings with cluster-aware uncertainty.” Almost every component is already occupied, and several close papers combine more of them than the shortlist acknowledges:

- **FormInv** already audits generated paraphrases for semantic errors, organizes responses by equivalence family, connects within-family variation to generalizability theory, bootstraps at the theorem level, and shows that removing four bad MathCheck paraphrases changes a model from rank 2 to rank 4. It also reports that 47% of one automatically generated paraphrase family was invalid ([Thomas & Thomas, 2026](https://arxiv.org/abs/2605.29001)).
- **Correcting Prompt Dependence in LLM Benchmarks** already argues that test prompts are dependent and fits a Bayesian hierarchical model with embedding-space prompt clustering to correct uncertainty ([Llewellyn et al., 2026 revision](https://arxiv.org/abs/2510.05709)).
- **The Emperor's New Clothes in Benchmarking?** is a multi-method audit of 20 benchmark-update strategies on five benchmarks and defines question-level fidelity and contamination-resistance metrics; it finds no method that reliably balances both ([Sun et al., ICML 2025](https://arxiv.org/abs/2503.16402)).
- **PTEB** generates stochastic paraphrases at evaluation time, validates semantic preservation with gold ratings and humans, repeats evaluation across six paraphrasing seeds, and reports run-to-run variation across 20 datasets and 25 languages ([Frank & Afli, EACL 2026](https://aclanthology.org/2026.eacl-long.130/)).
- **DyCodeEval** generates variants from seed code problems, uses a validator, manually checks generator consistency, and repeats the complete dynamic benchmark ten times to assess score stability ([Chen et al., ICML 2025](https://arxiv.org/abs/2503.04149)).

The statistical observation—variants sharing a seed are clustered, so item-wise intervals can be too narrow—is textbook survey/experimental-design statistics. A July 2026 technical report even applies Kish's design effect and cluster bootstrap directly to “multiple prompts per template” in LLM evaluation ([TMLS AI Research, 2026](https://www.tmls.nyc/research/eval-sample-complexity)), while recent primary work already provides prompt-cluster hierarchical inference and rank intervals.

One narrower empirical contribution was not found in this search: **a cross-generator calibration study that jointly estimates (i) bias from invalid variants and (ii) inferential miscoverage from treating seed-family variants as independent, using repeated independent generator draws and family-aware rank inference.** That is the only plausible surviving F2. It is a materially different and more demanding study than “apply clustered standard errors.”

## The conceptual answer: independent with respect to what?

Automatically generated variants may be independent draws from a generator's random seed **conditional on a fixed source item**. They are not thereby independent evidence about performance on a population of underlying problems. Variants from one seed share latent logic, answer, difficulty, topic, canonical solution, generator prompt, and often wording templates. If the target of inference is performance on new problem concepts, the seed—not each surface variant—is the primary sampling unit.

There are at least three distinct estimands, and they cannot be mixed:

1. **Finite generated-set score.** If the benchmark file is the complete target, its mean is descriptive; no item-sampling confidence interval is needed. Only model-generation randomness remains.
2. **Conditional generator score.** If seeds are fixed and only generator randomness is in scope, variants can be independent conditional draws, but inference generalizes only to future variants of those same seeds under that generator version.
3. **Task-population score.** If the claim concerns new underlying problems, evidence must generalize over seed families. Resampling individual variants is pseudoreplication; resampling seed families or fitting a multilevel model is required.

F2 is interesting only under the third estimand. The paper must say this explicitly.

## Closest-paper matrix

| Work | What it already contributes | Collision with F2 | What it leaves open |
| --- | --- | --- | --- |
| [FormInv: A Measurement Protocol for Semantic Invariance](https://arxiv.org/abs/2605.29001) (2026) | Audits paraphrase validity; formal/CAS/expert verification tiers; theorem equivalence classes; SCR and Cochran's Q; generalizability-theory interpretation of paraphrase variance; theorem-level bootstrap; family-conditional rank reversals; external MathCheck audit where four invalid paraphrases alter rankings. | **Very high.** It already combines variant validity, family structure, uncertainty, and ranking consequences. | Does not benchmark multiple dynamic-generator systems under a common repeated-generation protocol; does not directly estimate naive item-wise CI coverage versus seed-cluster coverage across generators. |
| [Correcting Prompt Dependence in LLM Benchmarks](https://arxiv.org/abs/2510.05709) (2025; revised/accepted 2026) | Explicitly rejects prompt independence; uses embedding-space clustering and Bayesian hierarchical inference for more reliable uncertainty in limited-data LLM evaluation. | **High on dependence/statistics.** “Use a hierarchical model for related prompts” is not novel. | Security/adversarial-prompt setting; no semantic-equivalence or label-validity audit of generated variants. |
| [The Emperor's New Clothes in Benchmarking?](https://arxiv.org/abs/2503.16402) (ICML 2025) | Controlled audit of 20 contamination-mitigation/update strategies, 10 models, five benchmarks, and two contamination regimes; question-level fidelity and resistance metrics. | **High on multi-generator audit/validity.** A cross-method generator audit is already a major-paper contribution. | Does not center seed-family dependence or calibrate rank-interval coverage. |
| [PTEB](https://aclanthology.org/2026.eacl-long.130/) (EACL 2026) | Dynamic stochastic paraphrasing at evaluation time; gold-score and human validity checks; six random seeds; score means/standard deviations; 20 datasets and 25 languages. | **High.** It already combines generated-variant validity and repeated-run uncertainty in a dynamic benchmark. | Does not decompose uncertainty into seed-family and variant components or compare naive and cluster-aware rank coverage. |
| [DyCodeEval](https://arxiv.org/abs/2503.04149) (ICML 2025) | Multi-agent variants from seed HumanEval/MBPP problems; LLM validator; manual consistency check (reported 95% with Claude 3.5 Sonnet versus 83% with Haiku); ten full generated benchmark runs and score stability analysis; DyPass over variants. | **High.** It partially performs the proposed combined audit inside one generator. | Validation is probabilistic and lightly sampled; stability is score-level, not a coverage study; family dependence is not modeled explicitly. |
| [MathCheck](https://arxiv.org/abs/2407.08733) (ICLR 2025) | Checklist-style mathematical robustness benchmark with original problems and rewritten variants, evaluated on 26+ LLMs. | **Medium.** Establishes the seed/variant design and robustness question. | FormInv later demonstrates that its paraphrase verification was insufficient and that bad paraphrases changed ranks. |
| [DyVal](https://arxiv.org/abs/2309.17167) (ICLR 2024) | Procedurally generates reasoning tasks from randomized DAGs with controlled complexity and exact algorithmic structure. | **Low-to-medium.** It is a major dynamic-benchmark anchor, but many samples are new DAG instances, not merely variants of one seed. | F2 should not force a seed-family dependence correction onto DyVal without first showing the actual sampling hierarchy. |
| [Is Your Benchmark (Still) Useful?](https://arxiv.org/abs/2503.06643) (2025) | Semantic-preserving code mutations; reports performance drops and model-ranking shifts under dynamic variants. | **Medium-high.** Ranking instability under semantic-preserving dynamic changes is already demonstrated. | Does not perform independent semantic-validity auditing or family-aware uncertainty calibration. |
| [CLEAN-EVAL](https://arxiv.org/abs/2311.09154) (2023) | Generates paraphrase/back-translation candidates, filters with a semantic detector and BLEURT, and uses human assessment to support meaning preservation. | **Medium.** Generator validity/filtering is established work. | No seed-family inferential analysis. |
| [QuickScope: Certifying Hard Questions in Dynamic LLM Benchmarks](https://arxiv.org/abs/2604.17842) (2026) | Treats dynamic benchmark templates/configurations as a potentially unbounded evaluation space and uses uncertainty-aware sampling to identify hard configurations. | **Medium.** Shows that dynamic-benchmark uncertainty and template structure are already active topics. | Targets hard-question discovery, not validity or average/rank coverage. |
| [Prompt-Dependent Ranking of LLMs with Uncertainty Quantification](https://arxiv.org/abs/2603.03336) (2026) | Contextual Bradley-Terry-Luce model with prompt-specific marginal and simultaneous rank confidence sets; shows many apparent rank differences are not distinguishable. | **High on ranking uncertainty.** Point-rank recomputation is insufficient; valid rank sets are available. | Human pairwise preferences rather than exact-answer seed families. |
| [Rank Intervals for Leaderboards](https://arxiv.org/abs/2606.08679) (2026) | Hierarchical task- and leaderboard-level rank confidence/prediction intervals with coverage guarantees; evaluates correlated-task simulations and MMLU/PromptEval. | **High on hierarchical ranks.** F2 cannot claim rank-aware hierarchical inference as new. | Does not audit generator validity or seed/variant clusters. |
| [Pervasive Label Errors in Test Sets](https://arxiv.org/abs/2103.14749) (NeurIPS 2021) | Estimates at least 3.3% test-label errors across ten major datasets and demonstrates benchmark-ranking instability. | **High on label-error consequences.** “Bad labels can alter rankings” is mature. | Not specific to dynamic generation or within-seed variants. |
| [Are LLMs Better than Reported?](https://arxiv.org/abs/2410.18889) (EMNLP 2025) | Uses LLM ensembles to flag label errors and compares expert, crowd, and LLM annotations across TRUE datasets. | **Medium-high on scalable validity auditing.** Ensemble disagreement as an audit mechanism predates F2. | No dynamic-generator dependence analysis. |
| [Auditing LLM Benchmarks with Item Response Theory](https://arxiv.org/abs/2605.30504) (2026) | Uses responses from 114 models to surface likely mislabels across seven benchmarks and traces label-error mechanisms. | **Medium-high.** Benchmark audits that connect model response structure to label quality are current. | No generated equivalence families or cluster-aware coverage study. |

## What is already textbook rather than publishably novel

For equal-sized clusters with exchangeable intra-family correlation \(\rho\) and \(m\) variants per seed, Kish's approximate design effect is

\[
DEFF = 1 + (m-1)\rho, \qquad n_{eff} = n/DEFF.
\]

Applying this formula, a cluster bootstrap, cluster-robust standard errors, GEE, or a random-intercept logistic model to benchmark families is good practice, not by itself a research contribution. The same applies to saying that paired model comparisons are preferable because all models answer the same items. Recent LLM-evaluation work already addresses variance sources ([Bouthillier et al., MLSys 2021](https://arxiv.org/abs/2103.03098)), small-sample error bars ([Miller, 2024](https://arxiv.org/abs/2411.00640)), prompt dependence ([Llewellyn et al.](https://arxiv.org/abs/2510.05709)), and valid rank uncertainty ([Neuhof & Benjamini](https://arxiv.org/abs/2606.08679)).

The Kish formula is also too weak as the primary method here: family sizes are unequal; correlations can vary by generator, task, model, and difficulty; model comparison is paired; invalid variants create bias rather than merely extra variance; and there may be generator-run and model-sampling levels above and below the seed family. A serious study needs a predeclared multilevel data-generating model plus family-level resampling and repeated generator realizations.

## Exact surviving estimand

Let \(S\) be a source/seed problem sampled from a declared seed population, \(X \sim G(\cdot\mid S)\) a variant produced by generator \(G\), \(V(X,S)\in\{0,1\}\) an independently adjudicated indicator that the variant preserves the seed's target construct and label, and \(Y_m(X)\in\{0,1\}\) model \(m\)'s correctness.

The capability estimand should be:

\[
\theta_{m,G}^{valid}
=
\mathbb{E}_{S}
\left[
  \mathbb{E}_{X\sim G(\cdot\mid S)}
  \{Y_m(X)\mid V(X,S)=1\}
\right].
\]

The primary comparison for models \(a,b\) is the paired gap

\[
\Delta_{ab,G}^{valid}=\theta_{a,G}^{valid}-\theta_{b,G}^{valid},
\]

with seeds as primary sampling units. F2's genuinely useful target is not merely \(\rho\). It is the **joint distortion** induced by the common naive analysis:

1. **Validity bias:** \(B_{ab,G}=\Delta_{ab,G}^{raw}-\Delta_{ab,G}^{valid}\), where raw includes invalid variants and any family-size weighting.
2. **Dependence miscoverage:** the empirical coverage and width difference between naive item-wise intervals/rank sets and seed-family-aware intervals/rank sets over repeated independent realizations of \(G\).
3. **Decision distortion:** the probability that naive and corrected analyses disagree on sign, dominance, or the simultaneous rank confidence set.

This yields an interpretable generator-level output: a **bias–coverage profile** \((q_G,B_G,C_G,R_G)\), where \(q_G=P[V=1]\), \(C_G\) is interval miscoverage, and \(R_G\) is rank-decision disagreement. That profile, compared under one protocol across materially different generators, is the plausible new artifact.

## Novelty condition

The revised project survives only if all of the following are true:

1. It audits **at least two established, open generator systems with different construction regimes**, not two prompt variants written for this paper. A sensible contrast is a seed-rewrite generator such as DyCodeEval/MathCheck and a programmatic generator such as DyVal, but only after mapping each system's actual sampling hierarchy.
2. It uses **independent validity adjudication**: deterministic execution/formal checks where possible, plus blinded expert review for the residual cases. An LLM judge sharing the generator's model family is not adequate ground truth.
3. It repeats complete generator draws enough times to estimate **frequentist coverage**, or constructs a large held-out generator population against which interval coverage can be checked. A single generated dataset cannot establish undercoverage.
4. It compares naive item-wise analysis with at least two appropriate corrections: seed-cluster bootstrap and a predeclared multilevel paired model; rank claims use simultaneous rank confidence sets, not point-order changes alone.
5. It shows an **interaction** between validity and dependence. For example, filtering invalid variants changes the estimated ICC/variance components or reverses which generator appears statistically efficient. Merely reporting two unrelated audit tables is not a joint contribution.
6. The correction changes a scientific conclusion, a rank confidence set, or an evaluation-budget recommendation in at least two generator/task settings. If all differences are negligible, the result can still be a useful negative result only if the coverage study was adequately powered and the artifacts are reusable.
7. It releases family identifiers, generator versions/prompts, validity decisions with reasons, raw model responses, and analysis code so other dynamic benchmark authors can reproduce the correction.

## Rejection conditions

Reject F2 before implementation if any of these obtain:

- A further search before preregistration finds a paper that already estimates validity bias and seed-cluster coverage across multiple dynamic generators.
- The target population remains “benchmark variants” without specifying whether inference is over fixed seeds, generator randomness, or new task concepts.
- The contribution is described as “using clustered standard errors,” “measuring ICC,” or “computing effective sample size.”
- Only one generator, one task domain, or one underlying seed benchmark is feasible.
- Variant validity is judged only by embeddings, the generating LLM, or an uncalibrated LLM ensemble.
- There are too few independent seed families to estimate family-level variance and rank uncertainty credibly, and no simulation/coverage study justifies the design.
- Rank conclusions use overlapping per-model confidence intervals or repeated pairwise tests without simultaneous inference and multiplicity control.
- Invalid variants are treated as random noise. Systematic semantic drift is bias and construct failure; clustering cannot repair it.
- The study reports only score stability across ten generator runs, because DyCodeEval already does that.
- The study reports only paraphrase validity plus ranking changes, because FormInv already does that more directly.
- The study reports only a cross-method fidelity audit, because Sun et al. already cover 20 mitigation strategies.
- Generator repositories cannot be pinned and reproduced without undocumented paid services or changing proprietary models.

## Recommended revised framing

**Working title:** *How Much Evidence Is a Generated Benchmark Family? A Joint Bias-and-Coverage Audit of Dynamic LLM Benchmarks*

**One-sentence question:** Across established dynamic benchmark generators, how much do semantic-invalidity bias and within-seed dependence separately and jointly distort model gaps, interval coverage, and rank confidence sets?

**Contribution statement:** Evaluate several open dynamic benchmark generators under a shared repeated-generation design; independently validate variants; estimate the valid-variant, seed-population model gap; and measure how often naive item-wise inference versus family-aware inference covers that gap and supports the same rank decision. The reusable contribution is a generator audit protocol and bias–coverage profile, not the statistical fact that clustered observations require clustered inference.

## Verdict rationale

**Major revision**, bordering on rejection. The current F2 claim fails the program's literature-gap hard gate because FormInv is much closer than the shortlist states, and the dependence correction is already both classical statistics and an explicit subject of 2025–2026 LLM-evaluation papers. The candidate remains potentially worthwhile only as a cross-generator empirical calibration paper with the exact estimand and novelty conditions above. If the implementation cannot support repeated generator draws, independent validity adjudication, and family-aware rank coverage, reject F2 and promote another finalist.

## Search scope and evidence status

This audit searched primary papers and official artifacts through 2026-07-17 using combinations of: dynamic benchmark, paraphrase/semantic invariance, semantic preservation, generator validation, benchmark label error, prompt/item dependence, effective sample size, clustered/hierarchical inference, bootstrap, ranking uncertainty, contamination-resistant generation, DyVal, DyCodeEval, MathCheck, FormInv, and related citations. It inspected the full papers or official abstract/artifact pages for the load-bearing works above. No exact multi-generator joint validity-bias plus seed-cluster coverage paper was found, but absence from this search is not proof of absence; the novelty condition should be rerun immediately before preregistration or submission.
