# Implementation and reproducibility audit of revised finalists

**Audit date:** 2026-07-17
**Scope:** Revised F1 and F2 questions in `selection-synthesis-v0.md`, plus the only surviving F3 pivot in `f3-literature-novelty.md`
**Constraint:** Design audit only. No paid model calls, cloud jobs, model/data artifact downloads, code implementation, spending, or external contacts were made.

## Executive decision

| Candidate | Practical verdict | Minimum calendar time | Confirmatory inference calls | Main implementation blocker |
| --- | --- | ---: | ---: | --- |
| F1 — cross-case carryover decomposition | **Major revision; conditionally feasible** | 8–12 full-time-equivalent weeks | about 18,240 | Preserving the novelty-defining controls without factorial explosion; reproducible self-history and API model drift |
| F2 — generated-family validity bias and coverage | **Reject as a one-researcher first project** | 14–22 weeks plus independent review | about 34,560 generation/evaluation calls | The surviving claim needs repeated generator replay and independent semantic-validity adjudication; neither is reproducibly available at the required scale |
| F3 pivot — temporal applicability decomposition | **Reject as a first project** | 14–20 weeks plus independent rule verification | about 28,000 under a plausible error rate | Dual rule executors, official historical-rule provenance, and independent effective-date verification dominate the work; novelty still depends on an interaction appearing |

F1 is the only candidate that passes basic buildability after revision, and it still does not earn an unqualified pass. A local smoke tier can validate its generator, transcript construction, scoring, and analysis on the available 16 GB M1 Pro. The approval-gated tier is large but bounded, uses synthetic public data, and does not require expert annotation. F1 should be selected only after freezing a fractional design with the exact call budget below and proving that at least one pinned open-weight model operates away from ceiling and floor.

F2 fails the program's practical independence gate. Its interesting target is validity *bias*, not merely deterministic execution failure. A code test suite or symbolic checker can reject obvious variants, but cannot by itself establish that a natural-language rewrite preserves the full construct. The closest open replay candidate, DyCodeEval, explicitly depends on commercial Claude generation and describes open-source generation as future work; DyVal is now housed in an archived Microsoft repository. Using only pre-generated outputs would remove repeated independent generator draws, while using only programmatic generators would make the semantic-invalidity half of the contribution largely artificial.

The F3 pivot is technically implementable, but not as the program's small first paper. Its minimum credible real-rule validation needs two independently checked executable representations of historical rules, verified effective dates and transition provisions, and a meaningful reproduction of the direct predecessor. That is a second project or a collaboration, not a bounded solo artifact.

## Common artifact architecture

Any promoted candidate should use the same small, boring, inspectable skeleton:

```text
project/
  pyproject.toml              # Python 3.12 lock, hashes, exact tool versions
  uv.lock
  CITATION.cff
  LICENSES/                   # upstream data/code/model licenses
  configs/                    # immutable YAML/JSON protocol cells
  schemas/                    # JSON Schemas for items, prompts, responses, scores
  src/
    generators/
    solvers/
    renderers/
    providers/
    scoring/
    analysis/
  tests/
    unit/
    property/
    golden/
    crosscheck/
  data/
    source/                   # checksummed upstream or official materials
    generated/                # immutable generated cases/families
    frozen/                   # preregistered confirmatory manifest
  runs/<run_id>/
    manifest.json             # git SHA, config hash, environment, timestamps
    requests.jsonl            # complete provider-neutral requests
    responses.jsonl           # raw responses and usage/error metadata
    scores.parquet
  analysis/                   # one-command tables, figures, and paper numbers
  containers/                 # only where an execution sandbox is required
  Makefile                    # smoke, freeze, run, score, analyze, verify
```

The runner must be resumable and content-addressed: a call key is the hash of the complete request, model identifier, decoding parameters, and provider adapter version. Retries are new records linked to the failed attempt, never silent overwrites. Every derived table must trace to raw response IDs. Secrets stay outside the artifact; request payloads, response bodies, token usage, finish reasons, provider request IDs, timestamps, and any system fingerprints are retained.

Use Python 3.12 through `uv`, not the installed Python 3.14, because statistical, ML, and execution-sandbox dependencies may lag the system interpreter. The analysis stack should be pinned and capable of running without provider credentials from released raw responses.

## F1 — causal decomposition of cross-case carryover

### Minimum publishable architecture

F1 needs six separable modules:

1. **Rule-world DSL and generator.** At least two non-mathematical rule families, each with typed facts, explicit precedence, deterministic thresholds/exceptions, and a seeded case generator. Every target and history case is complete independently.
2. **Two independent solvers.** One direct reference implementation and one structurally different checker—for example, imperative Python versus Datalog/Prolog or a truth-table compiler. They must agree on labels, threshold margins, and rule traces for every frozen item.
3. **History/transcript builder.** Produces neutral, case-text-only, gold-label, gold-rationale, and model-self-rationale histories. It freezes model-generated history transcripts once and reuses the exact bytes; otherwise history content changes across target conditions and destroys the paired contrast.
4. **Provider-aware matcher and renderer.** Keeps system rules and target bytes identical while matching history token count, position, role structure, and output schema within each model tokenizer. Matching cannot be assumed across providers because tokenizers differ. Record actual provider token counts and predeclare a tolerance, preferably no more than 1–2%.
5. **Stateless runner.** Uses direct request APIs, not provider-side assistant/thread products that may retain hidden state. “Hard reset” means a request containing only the frozen system/rule block and target. Soft-marker and assistant-deletion requests are separately materialized and hashed.
6. **Exact scorer and paired analysis.** Parses a minimal JSON response, scores label/threshold/rule/format outcomes separately, and estimates target-paired effects with uncertainty clustered over targets and history sets. Model-call replicates are not independent cases.

The analysis should include a simulator before any model call. Inject known assimilation, contrast, neutral-load, and missing-output effects into synthetic response matrices and verify that the preregistered model recovers them with correct sign and interval coverage.

### Open data and model dependencies

F1 can own its data completely: release the rule schemas, seeded generator, all generated cases, both solvers, and the frozen target/history assignment. No private corpus or human annotation is required.

The smoke tier needs one permissively licensed, pinned 3–4B instruct checkpoint in a quantized format plus a pinned `llama.cpp` or MLX runner. The confirmatory tier should include at least one pinned open-weight family and two dated API model snapshots from different families. If the open model is below 50% or above 95% on most frozen targets, it does not satisfy the cross-family novelty condition; retuning the benchmark after looking at confirmatory results is not allowed.

For API models, use immutable dated IDs where providers offer them, never aliases such as `latest`. Log provider, exact model string, API version, region/routing setting, tokenizer/count endpoint, decoding parameters, response fingerprint, and run window. Release all outputs because future callers may be unable to reproduce the model snapshot.

### Deterministic components and independent cross-checks

- Seeded generator with a published RNG algorithm and per-item provenance.
- Exhaustive enumeration of every small rule-world state to compare both solvers.
- Property tests that histories are normatively irrelevant to the target and never alter target bytes.
- Cross-version JSON Schema validation for every case, prompt, response, and score.
- Prompt-byte and token-count manifests for every condition/model pair.
- Independent reimplementation of the label and threshold scorer from the written rule specification.
- Blind spot-check of at least 10% of frozen cases against both rule traces before unblinding model results; this can be done by the researcher with the second solver, because no domain judgment is required.
- A negative-control fake provider that returns known labels and malformed outputs to exercise retry, parse, and missingness paths.

The self-rationale arm is the reproducibility trap. A transcript generated by model A must be shown only to model A in the primary self-history contrast, frozen before target calls, and identified by hash. A cross-model “foreign rationale” arm may be exploratory, but cannot silently substitute for self-history.

### Bottom-up confirmatory budget

The smallest defensible fractional design I could construct without dropping a novelty-defining factor is:

- 2 rule worlds × 60 frozen target cases = **120 targets**;
- **24 unique cells per target**, comprising a fixed-horizon channel decomposition, positive/negative/balanced verdict-streak contrasts, selected congruent/conflicting semantic contrasts, horizon checks at 1/4/8, and soft/deletion/hard boundary checks;
- 3 model families;
- 2 decoding replicates, analyzed as within-target model variability rather than new items.

The 24 cells must be enumerated before power analysis; one coherent allocation is:

| Block | Cells | Count |
| --- | --- | ---: |
| Channel decomposition at horizon 4, congruent/balanced history | fresh baseline; neutral; case text only; gold labels; gold rationales; self rationales | 6 |
| Direction at horizon 4 | positive and negative histories for each of gold labels, gold rationales, and self rationales; balanced counterparts are in the first block | 6 |
| Semantic conflict at horizon 4, balanced outcomes | conflicting counterparts for case text, gold labels, gold rationales, and self rationales | 4 |
| Horizon extension | neutral at horizons 1 and 8; balanced self rationales at horizons 1 and 8; horizon 4 is in the first block | 4 |
| Boundary extension | soft marker and assistant-deletion for positive and negative self-rationale histories; the unmodified histories are in the direction block and the common literal hard reset is the fresh baseline | 4 |
| **Total** |  | **24** |

“Positive” and “negative” identify the solver-labeled prior case sets. Do not rejection-sample model transcripts until they display the desired streak; that would select histories differently by model. Record the labels actually displayed by the model and estimate both assignment-to-history and displayed-streak effects.

Target calls:

\[
120\ \text{targets} \times 24\ \text{cells} \times 3\ \text{models} \times 2\ \text{replicates}
=17{,}280.
\]

Create 20 independent maximum-horizon history sets per world and model, each with eight prior cases:

\[
20\ \text{sets} \times 2\ \text{worlds} \times 3\ \text{models} \times 8\ \text{prior turns}
=960
\]

self-history generation calls. Total: **18,240 inference calls**, excluding free/offline token counting and local deterministic work.

Budget approximately 62 million input tokens and 3.4 million output tokens: about 60.5M/3.1M for target calls at a 3,500-token mean input and 180-token mean output, plus 1.15M/0.24M for transcript generation. A 20% operational reserve for retries and provider errors should be authorized but not automatically spent.

Raw request/response text is roughly 300 MB by character count; JSON, trace, and retry overhead make **0.5–1.0 GB uncompressed** a safer allowance, or about 100–300 MB compressed. The local checkpoint adds roughly 2.5–5 GB. This fits the current disk, but only one or two local checkpoints should be retained at once.

As a cost sanity check—not a purchase recommendation—the 2026-07-17 public list prices include OpenAI `gpt-5.4-mini` at $0.75/M input and $4.50/M output on short context ([official pricing](https://developers.openai.com/api/docs/pricing)), Claude Sonnet 4.6 at $3/M and $15/M ([official pricing](https://platform.claude.com/docs/en/about-claude/pricing)), and Gemini 3.1 Flash-Lite at $0.25/M and $1.50/M ([official pricing](https://ai.google.dev/gemini-api/docs/pricing)). Splitting the estimated token load evenly across those example tiers is about $110 before failures. A realistic approval envelope is **$100–$600**, because a scientifically appropriate model matrix may use more capable tiers, providers may tokenize differently, reasoning tokens can be billed as output, and prices may change. Recalculate from a frozen 1% pilot immediately before approval.

### Local M1 Pro 16 GB smoke tier

The smoke tier is deliberately incapable of supporting the paper's claim:

- 2 rule worlds × 12 targets = 24 targets;
- 8 plumbing cells: fresh, neutral, text-only, gold label, gold rationale, self rationale, assistant deletion, hard reset;
- one pinned 3–4B quantized instruct model;
- two decoding replicates;
- 48 or fewer prior-turn generations.

This is **384 target calls plus at most 48 history calls = 432 local calls**, approximately 1.0–1.3M input tokens and under 0.1M output tokens. Allow 3–8 wall-clock hours, 3–6 GB for the runtime/checkpoint, and under 50 MB for run artifacts. The tier passes only if both solvers agree, all prompts validate, resets differ only in declared history, malformed outputs are handled, the paired analysis reproduces injected effects, and the local model is not uniformly invalid. It says nothing about the substantive hypothesis.

### Approval-gated confirmatory tier

Approval should cover a staged execution, not one open-ended budget:

1. **One-percent canary:** 120–180 calls across all providers; verify model IDs, token accounting, schemas, refusals, latency, and actual cost.
2. **Frozen-model calibration:** no more than 10% of targets, used only to confirm the preregistered ceiling/floor and operational assumptions. Stop if any required family is outside the admissible accuracy band.
3. **Full run:** execute the frozen 18,240-call manifest in randomized blocks. No prompt edits after unblinding.
4. **Predeclared retry reserve:** retry only transient provider failures and schema-invalid responses under a written policy; keep the original response.

Expected elapsed provider-run time is 2–7 days with conservative concurrency and rate limits; analysis and artifact verification take 2–3 additional weeks. Total solo project time is **8–12 weeks** if the rule worlds are kept synthetic and the fractional design is frozen early.

### Artifact and version risks

- API providers can silently update snapshots, safety layers, tokenizer behavior, or routing. Raw output release mitigates but does not eliminate this.
- Provider-side prompt caching may change cost/latency and possibly routing; either disable it or log it as infrastructure, never treat cached and uncached requests as experimental conditions.
- Exact token matching is provider-specific; a single “same length” history file is not enough.
- Quantized open-model results can depend on runtime, quantization, chat template, and sampling implementation. Pin weights, quantization file hash, runner commit, and template.
- Generated self-rationales can leak target structure if history assignment is not constructed before targets. Freeze disjoint case pools.
- Reusing too few history sets makes results specific to a handful of histories. History-set ID belongs in the analysis hierarchy.
- Requiring free-form rationales inflates cost and parse failures. Use a short structured rationale field with a hard output cap.

### Scope reductions that invalidate F1's novelty

Any of these changes converts F1 into an incremental replication and should trigger rejection:

- one rule world or fewer than three model families;
- no byte-identical intact-target control;
- neutral history matched only by rough character count with no provider-token check;
- no distinction among case text, label, gold rationale, and self rationale;
- no directional prior-verdict streak test;
- only one horizon;
- calling an instruction marker or recap a “reset” without a literal fresh request;
- regenerating histories independently in each condition instead of freezing paired transcripts;
- aggregate call-level inference rather than target-paired analysis;
- dropping the open-weight checkpoint and releasing only proprietary-model summaries.

### F1 verdict

**Major revision; conditionally feasible.** F1 fits one researcher and the machine only under the fractional 24-cell design, frozen transcript bank, two solver implementations, and staged API approval. It should become the leading candidate if a no-cost smoke implementation demonstrates those seams and an a priori paired-power simulation shows that 120 targets can detect the minimum meaningful directional effect. Do not promote it yet if the design is still described as a full factorial; that version is not budget-controlled.

## F2 — joint validity-bias and coverage audit of generated benchmark families

### Minimum publishable architecture

The surviving F2 requires substantially more than a cluster bootstrap:

1. **Upstream adapters for two established generators** with different sampling regimes: one seed-rewrite system and one programmatic generator. Each adapter must map generator run → seed family → variant and record prompts, random seeds, model IDs, validator outputs, and upstream commit.
2. **Repeated independent generation**, not repeated subsampling from one released benchmark. Generator draws are a sampling level.
3. **Validity pipeline** with deterministic execution/formal checks where possible, followed by blinded independent review of residual semantic-equivalence questions. The generating model and its validator cannot define ground truth.
4. **Model-evaluation sandbox** with language-specific isolation, CPU/memory/time limits, hidden tests, and complete logs for code tasks.
5. **Statistical calibration harness** that defines a large reference population or repeated draws, computes the valid-variant paired gap, and evaluates naive item bootstrap, seed-cluster bootstrap, and a paired multilevel model for coverage, width, sign, and simultaneous rank-set decisions.
6. **Simulation layer** whose true ICC, invalidity process, family-size imbalance, model gap, and invalidity-by-model interaction are known. Coverage code must pass here before empirical use.

### Open dependencies and their practical state

- [DyCodeEval's repository](https://github.com/SeekingDream/DyCodeEval) exposes pre-generated HumanEval/MBPP variants and generation/evaluation scripts, but its README requires commercial LLM accounts, maps generation to Claude 3.5 Haiku/Sonnet, and lists open-source generation as a future feature. The README still contains placeholder links and describes evaluation scripts as fragmented. This is an artifact, not a stable generator service.
- [DyVal](https://github.com/microsoftarchive/promptbench/tree/main/promptbench/dyval) is programmatic and its paper points to PromptBench, but GitHub now redirects the project under `microsoftarchive`. It should be vendored at a commit after license review, not installed from a moving package.
- HumanEval/MBPP source data, hidden tests, language runtimes, and licenses must be pinned. Generated code is untrusted and needs an offline sandbox; do not run it directly on the host.
- At least four evaluation models are needed for meaningful simultaneous rank sets. One local open model can smoke-test the path, but a publishable cross-model result will require dated APIs or approved compute for stronger open models.

The dependency mismatch is fatal to the clean one-researcher story. Pre-generated DyCodeEval data support a *fixed-dataset reanalysis*, not repeated independent generator draws. Fresh DyCodeEval draws depend on retired or changing commercial models and their multi-agent prompts. DyVal provides a reproducible contrast but not naturally occurring semantic-invalidity bias.

### Deterministic components and independent cross-checks

- Vendor exact upstream commits and preserve their licenses and original metadata.
- Recompute every programmatic label with a clean-room solver or exhaustive graph algorithm.
- Run generated code against both the upstream tests and an independently generated mutation/metamorphic test suite.
- Hash container images and block network, filesystem escape, and subprocess abuse.
- Double-code the seed/family/run identifiers and verify that family bootstrap samples whole seeds.
- Validate interval coverage on simulated data with known truth and on a finite generated census before model inference.
- Reproduce at least one published upstream table from each generator; failure blocks the audit.
- Resolve validity disagreements without access to model identities or ranks.

Execution is deterministic evidence of behavior on tests, not proof of semantic equivalence. Any claim that “all passing rewrites are valid” recreates the validity problem F2 is supposed to measure.

### Bottom-up confirmatory budget

A small but credible empirical calibration would require:

- 2 generators;
- 60 seed families per generator;
- 4 variants per seed;
- 12 independent complete generator draws;
- 4 evaluation models.

Generated variants:

\[
2 \times 60 \times 4 \times 12 = 5{,}760.
\]

Evaluation calls:

\[
5{,}760 \times 4 = 23{,}040.
\]

If one generator is LLM-based and uses a conservative four generation/critique/validation calls per accepted variant, its half of the dataset adds:

\[
2{,}880 \times 4 = 11{,}520
\]

calls, for approximately **34,560 generation and evaluation calls** before retries.

A plausible token budget is **about 69M input and 18M output tokens**: roughly 46M/11.5M for multi-agent generation and 23M/6.9M for four-model evaluation. Code and sandbox logs make storage larger than token text: allow **5–10 GB**, plus container images and any local checkpoint. This fits the disk only with disciplined cleanup; the current 34 GiB free space leaves little margin for several model weights and language images.

At current public API rates, a heterogeneous matrix could cost roughly **$300–$1,500** after generation, evaluation, retries, and reasoning output. The more important cost is adjudication. Double review of all 2,880 residual LLM-generated rewrites at only three minutes per item is 288 person-hours. A 25% double-reviewed audit is still 72 person-hours and cannot produce an item-level valid-only model gap without an additional two-phase sampling/measurement-error model. No reviewer labor has been authorized or sourced.

### Local M1 Pro 16 GB smoke tier

Use frozen public outputs only:

- 10 seeds × 3 variants × 2 nominal draws × 2 generator adapters = 120 variants;
- one local 3–4B model = 120 evaluation calls;
- all deterministic generator/solver and bootstrap simulations;
- a small offline code sandbox.

Allow 2–5 hours, under 0.5M inference tokens, and 1–3 GB beyond the checkpoint depending on container images. This can verify ingestion, family IDs, execution, scoring, cluster resampling, and one-command reproduction. It **cannot** verify fresh DyCodeEval generation, repeated-draw coverage, or independent semantic validity, so success does not de-risk the central contribution.

### Approval-gated confirmatory tier

The tier would require three separate approvals:

1. commercial generator replay with exact model availability and a frozen per-draw cap;
2. four-model evaluation calls; and
3. independent blinded validity review or a formally justified validation-subsampling design.

Even with approval, first reproduce upstream generators, then run three independent draws as a feasibility gate. Stop if acceptance rates, variant counts, token costs, or model IDs differ materially from the paper. Only after the adjudication protocol reaches acceptable inter-reviewer agreement should the 12-draw run begin.

Engineering and statistics require 10–14 weeks; generator archaeology, sandbox hardening, and validity review add 4–8 weeks. Total: **14–22 weeks plus reviewer scheduling**.

### Artifact and version risks

- DyCodeEval's original Claude generation models may be retired or behaviorally changed; replaying prompts on a new model is a new generator.
- PromptBench/DyVal is archived; transitive dependencies may not support Python 3.12 or arm64.
- Pre-generated datasets may omit rejected attempts, agent traces, or randomness needed to model generator selection.
- Hidden tests are not semantic proofs; test leakage and weak tests create correlated validity errors.
- Code execution is a host-security risk and may be nondeterministic across language/runtime versions.
- Generator acceptance filters make observed variants a selected sample; coverage claims must target the accepted-generator distribution explicitly.
- Four model ranks are weakly informative for simultaneous rank calibration, while more models multiply cost.
- Human adjudication decisions and expertise are themselves a dependence layer and must be released with reasons.
- API-based generation makes the benchmark impossible to exactly regenerate after model retirement; releasing all attempts is essential.

### Scope reductions that invalidate F2's novelty

- one generator, one seed benchmark, or one task domain;
- released variants only, with no independent generator draws;
- fewer than enough complete draws to evaluate empirical coverage;
- an LLM judge or generating-model validator as final semantic ground truth;
- execution tests treated as exhaustive equivalence certification;
- no item-level or sampling-design correction for unreviewed validity;
- only ICC, design effect, cluster bootstrap, or score stability;
- point ranks or pairwise intervals instead of simultaneous rank confidence sets;
- validity and dependence reported in separate tables with no joint distortion/interaction analysis;
- no raw rejected generations and generator-run metadata.

### F2 verdict

**Reject as a one-researcher first project.** The minimum design that preserves novelty violates the program's requirement that the work not depend on external expert annotation or unstable paid services. Replacing the LLM rewrite generator with only deterministic formal generators would make the pipeline reproducible, but would also remove the naturally occurring semantic-invalidity process that gives the joint bias-and-coverage question its point. F2 could become a collaboration or a later methods paper after a generator consortium releases complete draws and validity labels; it should not be selected now.

## F3 pivot — causal decomposition of temporal applicability errors

### Minimum publishable architecture

The only surviving F3 is a mechanism study, not a benchmark release. It needs:

1. **Versioned rule DSL.** Explicit version IDs, half-open effective intervals, transition rules, precedence, and five substantive migration types: threshold, exception, scope, deadline, and priority/precedence.
2. **Cross-version executor.** Runs every fact pattern under every version and retains the full label matrix. Generation accepts an item only when at least two versions produce different labels.
3. **Observable task decomposition.** Separate exact schemas for version selection, oracle-version application, end-to-end selection plus decision, and predeclared repair signals.
4. **Counterbalanced renderer.** Uses a Latin-square/fractional design for applicable-version position, chronological order, neutral versus `old/current/latest` labels, event-date-derived versus explicitly requested applicability, and matched non-temporal conflicts.
5. **Error classifier.** Deterministically identifies wrong selection, execution failure under a correct version, version-consistent substitution, and malformed output. It never infers selection from free-form rationale.
6. **Real-rule validation.** A small official historical rule family, version-specific executable modules, official source snapshots, effective-date/transition provenance, and the same presentation controls as the synthetic DSL.
7. **Direct-predecessor bridge.** Reproduce a meaningful released subset/protocol from [Asking For An Old Friend](https://github.com/TUMLegalTech/temporal_bias) and state what cannot be reproduced from its available data/prompts.

### Open data and model dependencies

The synthetic core is fully ownable. The real-rule tier would likely use a small SARA/DeonticBench-style U.S. federal tax family and official archived statute/IRS materials. [DeonticBench](https://github.com/guangyaodou/DeonticBench) provides executable-rule precedent, while the direct predecessor's repository exposes its QA set and prompts but not a turnkey complete harness.

US federal statutory text is generally public domain, but the artifact must record exact official URLs, retrieval dates, archived copies/hashes where redistribution is lawful, and the legal basis for every effective interval and transition rule. Commentary, commercial tax services, or unofficial summaries cannot serve as the oracle.

The model matrix has the same minimum as F1: one pinned open-weight model plus two dated API families. The real-rule module additionally needs SWI-Prolog or another pinned logic engine if a declarative second implementation is used.

### Deterministic components and independent cross-checks

- Two independent version-interval and rule-execution implementations.
- Exhaustive boundary tests one day before/on/after every effective date.
- Counterfactual generation invariant: at least two version labels differ for every primary item.
- Published item × version label matrix and rule trace.
- Latin-square balance tests for applicable position, order, label wording, regime, and migration type.
- Exact forced-choice version IDs and outcomes; rationales remain secondary qualitative data.
- Manual source-provenance table mapping each executable clause to official text and effective dates.
- Two-person verification of all effective intervals/transition rules and a sample of executions. The author cannot supply both “independent” checks.
- Reproduction test for the predecessor subset and a no-temporal matched-conflict negative control.

The two-person provenance check is not optional. A single incorrect transition rule can create the apparent temporal effect, and two software implementations copied from the same mistaken legal interpretation are not independent validation.

### Bottom-up confirmatory budget

A minimally balanced synthetic core:

- 90 base items across five migration types and three applicable regimes;
- 6 counterbalanced presentation cells;
- temporal plus matched non-temporal conflict = 2 conditions;
- selection, oracle application, and end-to-end = 3 task modes;
- 3 model families;
- 2 decoding replicates.

Calls:

\[
90 \times 6 \times 2 \times 3 \times 3 \times 2 = 19{,}440.
\]

Real-rule validation with 36 discriminating cases spanning at least six substantive rule changes and three effective-date regimes, six presentation cells, three task modes, three models, and two replicates adds:

\[
36 \times 6 \times 3 \times 3 \times 2 = 3{,}888.
\]

A 30-item, two-condition predecessor bridge adds 360 calls. If 20% of the 7,776 synthetic-plus-real end-to-end responses are wrong and each receives three predeclared repair signals, repair adds about 4,666 calls. Total expected workload: **about 28,350 calls**; authorize a cap, because error-triggered repair otherwise makes cost depend on the result.

Allow **about 55M input and 2.5M output tokens**, **0.5–1 GB** of run artifacts, and another 1–3 GB for official sources, containers, and logic runtimes. At current API rates, a mixed model tier is plausibly **$100–$600**, before any external verification labor. The primary cost is 4–8 weeks of careful rule provenance and independent checking, not tokens.

### Local M1 Pro 16 GB smoke tier

- 12 synthetic discriminating items;
- six presentation cells;
- temporal and matched non-temporal versions;
- three task modes;
- one local 3–4B model;
- one replicate.

This is **432 local calls**, roughly 0.8–1.2M input tokens and less than 0.1M output tokens. Allow 3–8 hours and the same 3–6 GB local model footprint as F1. The smoke tier exercises only the synthetic DSL, cross-version solver, balancing, parser, and decomposition. It omits the real-law module and therefore cannot validate F3's most failure-prone component.

### Approval-gated confirmatory tier

Before model-call approval:

1. freeze all synthetic items and the full cross-version matrix;
2. obtain the independent real-rule provenance check;
3. reproduce the predecessor subset offline from released materials;
4. pass simulation-based power and error-decomposition tests;
5. freeze the repair-call cap and sampling rule.

Then run a 1% provider canary, a 10% ceiling/floor check, and the frozen manifest. Expected implementation time is 6–8 weeks for the DSL, solvers, and renderer; 4–8 weeks for real-rule construction and verification; and 3–4 weeks for preregistration, calls, analysis, and artifact release: **14–20 weeks** with overlap.

### Artifact and version risks

- Official web pages can be updated or removed; provenance needs archived, hashed source snapshots where lawful.
- “Effective date” is not always enough: transition, grandfathering, tax-year, filing-date, and retroactivity clauses may control.
- Prolog modules can agree with a Python solver while sharing the same mistaken source interpretation.
- Neutral IDs versus `current/latest` labels must not change layout length or position unintentionally.
- A fractional design can alias the temporal interaction with order unless the design matrix is published and checked for estimability.
- The direct predecessor's public artifact is not a turnkey reproduction harness, so the bridge may be limited to data/prompt re-evaluation.
- Closed API drift threatens the small interaction on which novelty depends.
- Error-triggered repair creates post-treatment selection; the repair estimand and denominator must be declared.

### Scope reductions that invalidate F3's pivot

- synthetic rules only, with no official real-rule validation;
- one executable implementation or no independent effective-date verification;
- cases whose labels do not differ across versions;
- free-form rationale used to infer selected version;
- only ascending versus descending order, with no position/label/non-temporal controls;
- no oracle-version application task;
- no version-consistent substitution metric;
- no direct-predecessor comparison;
- one domain or fewer than three model families;
- headline claims about discovering stale-law, recency, or historical-version failure.

### F3 verdict

**Reject as a first project.** The pivot is implementable but fails scope discipline and solo reproducibility. Its scientific novelty depends on a counterbalanced temporal-specific interaction, while its validity depends on external, independently checked historical-rule interpretation. Removing the real-rule tier makes the work a synthetic factorial assembled from occupied components; keeping it makes the project 14–20 weeks and collaboration-dependent. Preserve it as a later project if a domain expert and a second implementer join.

## Reproducibility checklist for any selected project

### Before data generation

- [ ] One-sentence estimand and falsification condition frozen.
- [ ] Full design matrix and call-count formula checked for duplicates and aliasing.
- [ ] Minimum meaningful effect and simulation-based power/coverage recorded.
- [ ] Separate exploratory, calibration, and confirmatory item IDs.
- [ ] All upstream licenses, data terms, and redistribution rights recorded.
- [ ] Python/runtime/container/model versions pinned by hash, not mutable tag.
- [ ] Independent solver/checker agrees on every frozen primary item.
- [ ] No confirmatory prompt edited after model outputs are visible.

### For each model run

- [ ] Exact request JSON, model ID, provider/API version, parameters, and request hash saved.
- [ ] Prompt byte hash and actual input/output token counts saved.
- [ ] Timestamp, provider request ID, region/routing, latency, finish reason, and fingerprint saved where available.
- [ ] Original failures and schema-invalid outputs retained; retries linked, not overwritten.
- [ ] Rate-limit/concurrency schedule and retry policy fixed.
- [ ] Provider aliases and UI chat products prohibited.
- [ ] Model-generated histories or generator traces frozen and released.

### Scoring and analysis

- [ ] Scoring requires no API access and runs from raw released responses.
- [ ] Format errors, refusals, missing responses, and substantive errors are separate outcomes.
- [ ] Unit of analysis matches the estimand; repeated calls are not treated as new items.
- [ ] All multiplicity, stopping, exclusion, and missingness rules predeclared.
- [ ] Analysis reproduces known simulated effects and null coverage.
- [ ] Every paper number traces to a table cell and raw response IDs.
- [ ] A clean environment can rebuild every table and figure in one command.

### Release and independent reproduction

- [ ] Frozen data manifest, all prompts, raw responses, scores, and analysis code released.
- [ ] Upstream repositories vendored or pinned; no branch-only dependency.
- [ ] Local smoke tier runs without paid credentials on an arm64 16 GB machine.
- [ ] Confirmatory analysis reruns without provider access.
- [ ] At least one independent clean-room execution follows the README.
- [ ] Known non-reproducible components—especially retired API models—are named explicitly.
- [ ] Cost, tokens, wall time, hardware, and carbon-relevant compute metadata reported.

## Final practical ranking

1. **F1 — retain, major revision.** It has a fully synthetic, solver-checkable path; the main challenge is disciplined fractional design and immutable transcript/model provenance.
2. **F3 pivot — reject now, preserve for later collaboration.** Technically clean synthetic core, but the real-rule validity tier is too large and independent verification is load-bearing.
3. **F2 — reject now.** The exact combination that preserves novelty also depends on the least reproducible assets: proprietary stochastic generator replay and independent semantic adjudication at scale.

No candidate earns a full implementation/reproducibility pass today. F1 is the only one for which a no-cost smoke implementation could realistically convert the verdict to pass without changing the scientific question.
