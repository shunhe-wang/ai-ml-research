# Discordance-calibrated operating characteristics v1

**Generated:** 2026-07-17
**Source:** `analysis/discordance-operating-characteristics-v1.json`
**Status:** design calibration, not a confirmatory result

The disjoint Qwen pilot produced three discordant pairs among 32 targets (`q = 0.09375`), with sign heterogeneity by world: benefit-b had two negative-only discordances and permit-c had one positive-only discordance. Because 32 targets give a highly uncertain nuisance estimate, the simulation spans discordance probabilities `0.05`, `0.10`, and `0.20` rather than plugging in `0.09375` as known.

Each cell uses 5,000 Monte Carlo replications and the exact one-sided paired binomial test at alpha `0.05`. The effect is encoded as the imbalance between positive-only and negative-only discordances. The null rejection rate is conservative (`0.024`–`0.044` in the displayed grid), as expected from a discrete exact test.

## Selected power results

| Targets | Discordance | 3-point effect | 5-point effect | 10-point effect |
| ---: | ---: | ---: | ---: | ---: |
| 120 | 0.10 | 0.180 | 0.433 | 0.995 |
| 240 | 0.10 | 0.366 | 0.751 | 1.000 |
| 400 | 0.10 | 0.543 | 0.934 | 1.000 |
| 800 | 0.10 | 0.828 | 0.998 | 1.000 |
| 120 | 0.20 | 0.139 | 0.277 | 0.761 |
| 240 | 0.20 | 0.236 | 0.481 | 0.964 |
| 400 | 0.20 | 0.342 | 0.687 | 0.999 |
| 800 | 0.20 | 0.573 | 0.931 | 1.000 |

## Decision implication

A 120-target design is inadequate for a five-percentage-point SESOI. A pooled exact test needs roughly 400 targets when discordance is near 10%, but approximately 800 when discordance is 20%. A three-point SESOI needs at least 800 targets even in the favorable 10% regime and remains underpowered at 20% discordance.

These values are optimistic for the final fixed-panel claim because they omit model/world/schema heterogeneity, model-specific validity differences, and simultaneous secondary contrasts. The confirmatory manifest must not be frozen from this table alone. The next gate is a disjoint canary on two additional model families; if signs or task validity differ materially, the nested model must be simulated before scale-up.
