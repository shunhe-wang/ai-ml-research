# Preliminary paired-design operating characteristics

**Generated:** 2026-07-17
**Source:** `analysis/design-operating-characteristics-v0.json`
**Status:** Plumbing/design diagnostic only; not a frozen power analysis.

## Purpose

The implementation audit used 120 targets as an illustrative minimum. This simulation tests whether that number is defensible for the primary positive-versus-negative paired risk difference before any model result is observed.

The simulator uses binary target decisions with baseline positive-decision probability 0.50 and injected directional risk differences of 0, 3, 5, or 10 percentage points. `pair_coupling` is a simple nuisance parameter: 1 means both conditions share the same latent draw, 0 means independent condition draws, and intermediate values mix the two. It is not a substitute for the final schema/history/model hierarchy.

Each cell uses 500 Monte Carlo replications. The reported intervals are simple paired Wald intervals. The confirmatory analysis must add schema/history clustering, fixed model effects and heterogeneity, invalid outputs, multiplicity, and the actual estimator.

## Key result

The illustrative 120-target design is not generally adequate for a five-point SESOI.

| Targets | Pair coupling | Power at 5 points | Power at 10 points | Null rejection rate |
| ---: | ---: | ---: | ---: | ---: |
| 120 | 0.0 | 0.114 | 0.358 | 0.056 |
| 120 | 0.5 | 0.166 | 0.544 | 0.054 |
| 120 | 0.9 | 0.476 | 0.898 | 0.054 |
| 240 | 0.0 | 0.204 | 0.608 | 0.058 |
| 240 | 0.5 | 0.320 | 0.798 | 0.054 |
| 240 | 0.9 | 0.736 | 0.992 | 0.042 |
| 400 | 0.0 | 0.306 | 0.820 | 0.042 |
| 400 | 0.5 | 0.482 | 0.966 | 0.044 |
| 400 | 0.9 | 0.918 | 1.000 | 0.056 |

Coverage was generally near the nominal 95% in this simplified grid, but 500 replications leave nontrivial Monte Carlo error. A larger final simulation is required.

## Decision impact

1. Do not freeze 120 targets merely because it appeared in the implementation audit.
2. Estimate baseline rates, within-target condition concordance, schema heterogeneity, and invalid-output rates from disjoint local calibration cases.
3. Choose the SESOI before confirmatory outcomes. A ten-point directional shift appears estimable at moderate sample sizes; a five-point shift may require substantially more independent targets unless within-target concordance is very high.
4. Do not replace target cases with repeated decoding calls. Repetitions estimate prompt-level stochasticity and do not solve the independent-target requirement.
5. Expand the final simulator to the staged Module A/Module B design and planned hierarchical/randomization estimator. If the resulting target count makes the call manifest infeasible, trigger the selection memo's kill gate.

## Reproduction

```bash
uv run carryover simulate-design \
  --targets 80 120 160 200 240 320 400 \
  --effects 0 0.03 0.05 0.10 \
  --couplings 0 0.5 0.9 \
  --baseline 0.5 \
  --replications 500 \
  --seed 20260717 \
  --output analysis/design-operating-characteristics-v0.json
```
