# Independent AI Research Program

This repository contains a reproducible AI/ML methods study about whether earlier, unrelated decisions can influence a language model's next rule-bound decision.

## In plain English

Imagine asking an AI to decide whether someone qualifies for a benefit or permit. The rules and the new case stay the same, but first the AI sees a short history in which earlier cases were mostly approved or mostly denied. Does that irrelevant history nudge the next answer?

This project built a small laboratory for asking that question carefully: two synthetic rule systems, independent programs that know the correct answer, matched prompt histories, strict output checks, immutable run logs, and tools that authenticate and reanalyze the evidence.

The important result is a **research stop, not an effect claim**. Small local-model calibration runs were inconsistent across rule systems, and review found that the executed comparison still bundled together several possible causes. Scaling it up would have produced a precise-looking but underidentified answer. The project therefore stopped before a confirmatory experiment and released the apparatus, failed iterations, and design lessons instead.

## Current status

- Phase: public methods/resource note after a pre-confirmatory stop
- Selected project: F1, narrowed from a causal-effect study to a reusable sequential-history evaluation harness and negative design case
- Completed evidence: literature/adversarial selection, dual-solver harness, fake-provider failure injection, local snapshot screens, Qwen/Llama calibration diagnostics, illustrative panel simulation, independent raw-log reproduction, hostile methods review, and an 11-page working note
- Failed iterations retained: the first paired-history canaries were invalidated by independent review because asymmetric permit margins, treatment-specific padding, and target/history fact overlap confounded interpretation
- Scientific status: no confirmatory result; no causal, interaction, null, equivalence, family-level, or sample-size claim
- Experiments authorized: deterministic implementation, simulation, and no-cost local calibration only; no paid model calls without approval
- Public release: v0.1.0 working technical report; not peer reviewed

## Repository map

- `research/` — publication landscape, literature notes, source registry, and candidate analyses
- `protocol/` — selection criteria and the current draft protocol
- `src/rule_carryover/` — generators, independent solvers, renderers, providers, runners, scoring, storage, and provenance controls
- `tests/` — deterministic unit and vertical pipeline tests
- `data/` — frozen, content-addressed pilot/calibration cases
- `runs/` — immutable local smoke/calibration manifests and append-only execution records
- `analysis/` — design-simulation outputs and later analysis artifacts
- `paper/` and `output/pdf/` — working-note source, artifact appendix, and rendered 11-page PDF
- `audits/` — finalist reviews, independent reproduction, hostile methods review, and novelty posture
- `AI_ASSISTANCE.md` and `COSTS.md` — material AI assistance and actual monetary-spend boundaries
- `RELEASE_NOTES.md` — reusable release description, verification record, and claim boundary

## Reproduce the current checkpoint

Python 3.12 is required. With `uv` installed:

```bash
uv sync
make verify
```

For the optional Apple Silicon local-model adapter:

```bash
UV_PROJECT_ENVIRONMENT=.venv-mlx uv sync --extra mlx
make verify-native
```

The model weights are deliberately excluded from the repository. Run manifests pin the model repository revision and weight SHA-256. The exact prompts and raw responses are retained in each execution JSONL. `make verify` checks every included artifact and reports the excluded model folders and pre-import Git objects as unavailable rather than pretending to re-authenticate them. If those external artifacts are restored at their manifest paths, `make verify-external` requires and hashes them.

Build the working-note PDF from its Markdown source with the same development environment:

```bash
make paper
```

Useful commands:

```bash
uv run carryover --help
uv run carryover generate --help
uv run carryover simulate-design --help
uv run carryover local-baseline --help
uv run carryover local-history-smoke --help
```

## Integrity rules

- Never invent citations, novelty, data, experiments, or results.
- Treat paper limitations and future-work statements as leads, not proof of novelty.
- Record all serious candidate projects, including rejections.
- Separate exploratory from confirmatory work.
- Do not contact, submit to a venue, purchase, or run paid inference without explicit approval.
- Keep claims narrower than the evidence.

The selection rationale and kill gates are in `audits/final-selection.md`. This repository release does not authorize confirmatory model execution, spending, outreach, preprint upload, or venue submission.
