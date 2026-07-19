# Finalist selection synthesis

**Status:** Working document; no project selected.
**Cutoff:** 2026-07-17 literature and local feasibility checks.
**Rule:** Score only the contribution that survives adversarial review, not the attractive broad proposal that entered the shortlist.

## Surviving questions

### F1 — causal decomposition of cross-case carryover

With governing rules and the target case held byte-identical and fully intact, does a history of independently adjudicated same-rule cases change the target decision beyond token-, position-, and format-matched neutral history? If so, how much is attributable to prior case text, outcome labels, gold rationales, or the model's own rationales, and which literal boundary operation removes it?

This is not a claim to discover sequential interference, context pollution, non-mathematical multi-turn degradation, legal order effects, or reset mitigation. Those broad claims are occupied.

### F2 — joint validity-bias and coverage audit of generated benchmark families

Across established open dynamic-benchmark generators, how much do invalid variants and within-seed dependence separately and jointly distort paired model gaps, interval coverage, and simultaneous rank confidence sets over repeated independent generator draws?

This is not a claim that generated variants may be invalid, that related prompts are dependent, that clustering narrows effective sample size, or that invalid labels can change rankings. Those broad claims are occupied.

### F3 — rejected; causal temporal-applicability pivot under audit

The original “temporal rule-version fidelity beyond code” candidate fails the literature-gap hard gate because *Asking For An Old Friend* (ICAIL 2026) directly studies historical-version selection, stale statutory knowledge, recency bias, and retrieval mitigation. The only plausible replacement asks: when all competing versions and a decisive event date are present, how much error comes from mapping the date to the wrong version versus executing a correctly selected rule, and is selection error amplified by temporal salience beyond matched position and non-temporal conflict controls?

This pivot is a new candidate, not a cosmetic rewrite of F3. It must directly score the selected version ID, use an oracle-version application arm, require items whose labels differ across versions, and publish the version-by-item execution matrix.

## Decision tests

Each surviving candidate receives a fresh 0–4 score under the promotion standard and a written answer to the following tests.

| Test | Pass condition |
| --- | --- |
| Novelty | The closest-paper matrix leaves a joint, testable gap; the contribution is more than a domain transfer or standard method application. |
| Identification | The primary estimand is defined; the planned contrasts identify it without relying on post hoc interpretation. |
| Statistical validity | Unit of analysis, dependence, uncertainty, multiplicity, missingness, invalid outputs, and stopping rules are predeclared. |
| Task validity | Generators and solvers agree; cases measure the target construct; no benchmark leakage or semantic drift is required. |
| Feasibility | The minimum publishable design fits one researcher, a 16 GB M1 Pro, public artifacts, and an approval-gated model-call budget. |
| Reproducibility | An independent person can rebuild data, rerun the smoke tier, inspect raw responses, and reproduce every table and figure. |
| Null value | A well-powered null or failed replication would resolve a live uncertainty rather than merely report no effect. |
| Audience and venue | Specific researchers and a realistic venue path exist; the artifact is more than a blog post or product demo. |
| Identity fit | The work demonstrates ML research skill through design, code, statistics, and evidence, with institutional reasoning as an advantage rather than a credential substitute. |
| Scope discipline | The confirmatory protocol can be frozen without a factorial explosion, private data, human-subject recruitment, or frontier-scale training. |

## Automatic rejection rules

Reject a finalist if any one is true after revision:

1. the literature gap requires claiming novelty for a bundle of ordinary controls rather than a scientific question;
2. the minimum publishable design cannot be completed without unapproved paid services or external expert annotation;
3. the causal or inferential claim depends on treating repeated model calls, variants, or prompts as independent experimental units;
4. the task generator or solver cannot be independently cross-checked;
5. the proposed finding is already a direct result in the closest work and only the application domain changes;
6. a null result would be uninterpretable because of ceiling/floor performance, insufficient power, or task invalidity;
7. the study cannot expose raw data, prompts, outputs, version information, and analysis decisions; or
8. completing the credible version would require more than one first project before any bounded contribution exists.

## Evidence still required before selection

- F3 literature and novelty audit. **Completed: reject as stated; only the causal pivot advances to comparative audit.**
- Independent experimental-design and statistical review of all revised questions. **Completed: F1's paired directional effect is identifiable after staged narrowing; F2 needs an outer truth/sampling design; F3's proposed selection/application rates are not an additive causal decomposition.**
- Independent implementation and reproducibility review, including a bottom-up call-count and storage estimate. **Completed: F1 conditionally feasible at about 18,240 confirmatory calls; F2 rejected as a solo first project; F3 pivot rejected as a first project.**
- Independent venue-fit and hostile-review pass. **Completed: F2 ranked first on venue-native contribution but only behind a two-generator feasibility gate; F1 is the fallback; F3 should retire.**
- Rescored promotion table using only the minimum design that would earn the surviving claim.
- Explicit selection memo that responds to every unresolved objection and names the runner-up and rejection reason.
