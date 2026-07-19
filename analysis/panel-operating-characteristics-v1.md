# Fixed-panel operating characteristics v1

**Generated:** 2026-07-17
**Inputs:** `panel-simulation-config-v1.json`
**Raw output:** `panel-operating-characteristics-v1.json`
**Status:** design decision, not model evidence

The simulation treats six fixed model × world cells as the minimum three-family, two-world panel. Within each cell, paired outcomes are generated from a discordance probability and a cell-specific risk difference. The displayed pooled test is the same exact one-sided test that would be tempting after concatenating all targets. “Sign-consistent rejection” is a descriptive compound rule: pooled `p <= 0.05` and every observed cell estimate strictly positive. It is not a simultaneous test of homogeneity, interaction, or cell-level positivity.

Each cell uses 5,000 replications. Targets below are per cell; total independent targets are six times larger and every target requires two history-arm responses before controls.

| Scenario | Targets/cell | Total targets | Pooled rejection | Sign-consistent rejection | Any negative observed cell |
| --- | ---: | ---: | ---: | ---: | ---: |
| Homogeneous null | 60 | 360 | 0.037 | 0.004 | 0.964 |
| Homogeneous null | 120 | 720 | 0.042 | 0.007 | 0.968 |
| Homogeneous null | 240 | 1,440 | 0.045 | 0.007 | 0.971 |
| Homogeneous +5 points | 60 | 360 | 0.897 | 0.387 | 0.340 |
| Homogeneous +5 points | 120 | 720 | 0.997 | 0.742 | 0.140 |
| Homogeneous +5 points | 240 | 1,440 | 1.000 | 0.959 | 0.024 |
| +5-point mean, one reversing cell | 60 | 360 | 0.763 | 0.062 | 0.859 |
| +5-point mean, one reversing cell | 120 | 720 | 0.962 | 0.047 | 0.917 |
| +5-point mean, one reversing cell | 240 | 1,440 | 1.000 | 0.018 | 0.974 |
| +5-point mean, one reversing cell | 400 | 2,400 | 1.000 | 0.003 | 0.996 |

The null exact test remains conservative in the pooled statistic. That does not solve the scientific problem: even under a homogeneous positive effect, 120 targets per cell provide only 74.2% probability that every cell point estimate is positive. Under a five-point positive mean with one true reversal, the pooled test approaches certainty while the diagnostic compound rule approaches zero. Increasing sample size reveals the negative point estimate more reliably; it does not validate a stable directional claim.

The balanced-sign and shrunk-pilot heterogeneity scenarios have approximately zero mean, pooled rejection near the nominal exact-test rate (`0.033`–`0.043`), and virtually certain negative cells. These scenarios reinforce that a pooled null would not establish absence of large opposing cell effects.

## Decision

Do not freeze or execute the current confirmatory causal-effect design. In this particular simulation, roughly 240 targets per cell are needed for the descriptive sign-consistency rule to exceed 95% under the homogeneous +5-point scenario: 1,440 targets and 2,880 H+/H− responses before neutral/channel controls. That number is a feasibility illustration, not an inferential sample-size recommendation. A defensible confirmatory design would first need a competent third family, a predeclared estimand for heterogeneity, and operating characteristics for a valid simultaneous or hierarchical procedure. The observed calibration pattern makes a pooled mean substantively risky regardless of nominal pooled power.

The completed contribution is therefore scoped as a methods and feasibility note: exact matching, response-validity gates, and cell-level sign diagnostics materially change what can be claimed from sequential-history experiments. No general assimilation, contrast, or null effect will be claimed.
