# Analysis status

The current analysis artifacts are design-simulation outputs, not experimental findings. `design-operating-characteristics-v0.*` evaluates a simplified paired binary design and demonstrates that 120 targets is generally underpowered for a five-percentage-point effect unless within-target coupling is very high.

The final simulation must incorporate pilot-derived baseline rates, schema and history clustering, model heterogeneity, invalid output, missingness, and the exact staged design before protocol freeze.

`history-canary-v2-*.json` contains deterministic paired analyses of the four-target remediated canaries. The benefit interval is deliberately wide and the exact test is non-significant; the permit run has no discordant pairs. These files are diagnostics, not paper results.

`history-pilot-*.json` contains the 16-target-per-world disjoint Qwen pilot analyses and a combined 32-target view. `discordance-operating-characteristics-v1.*` uses the pilot's low observed discordance only as a nuisance-range anchor and shows that the original 120-target planning example is underpowered for a five-point SESOI.

`history-canary-llama31-*.json` contains the four-target-per-world Llama 3.1 literal-history analyses. `family-canary-v1.md` consolidates the predeclared fresh/task/tokenizer gates and explains why the local panel does not justify scale-up.

`panel-simulation-config-v1.json`, `panel-operating-characteristics-v1.json`, and the matching Markdown note evaluate pooled exact-test behavior over six fixed model × world cells. The simulation supports the documented stop decision by showing that high pooled rejection probability can coexist with a reversing cell. Its all-positive-point-estimate rule is descriptive, not a valid simultaneous stability test or a confirmatory sample-size procedure.
