# Appendix and replication-material index

**Checkpoint:** working-note v1, 2026-07-18

This repository-level appendix maps every quantitative or procedural claim in the working note to inspectable evidence. It is not an additional results section and does not expand the paper's claim boundary.

## A. Deterministic reproduction

From a Python 3.12 environment:

```bash
uv sync
make verify
make paper
```

The checkpoint runs the unit suite, Ruff, mypy, dual-solver and frozen-case checks, stored-run verification, prompt/response authentication, retry ancestry checks, causal-summary recomputation, and available local model/source hash verification. Missing external artifacts are counted and reported, not silently treated as verified. `make verify-external` requires those model folders and historical Git objects if they are restored. `make paper` rebuilds the PDF from the checked-in Markdown source using the declared ReportLab dependency. The optional MLX adapter tests are separate because model weights are not distributed.

## B. Artifact map

| Paper component | Primary repository evidence |
| --- | --- |
| Literature boundary and narrowed novelty posture | `audits/f1-literature-novelty.md`, `audits/methods-resource-novelty.md`, `research/sources.bib` |
| Frozen scope and excluded claims | `research/publication-scope-v1.md`, `audits/methods-note-red-team.md` |
| Rule worlds, cases, and two solvers | `data/pilot/`, `src/rule_carryover/case_set.py`, `src/rule_carryover/solvers.py`, `tests/` |
| Native-template rendering and exact matching | `src/rule_carryover/rendering.py`, `src/rule_carryover/histories.py`, tokenizer preflight tests |
| Response contract and failure handling | `src/rule_carryover/scoring.py`, `src/rule_carryover/runner.py`, `src/rule_carryover/manifest.py` |
| Failed and completed run registry | `runs/README.md`, immutable `runs/*/manifest.json`, append-only `runs/*/executions.jsonl` |
| Qwen and Llama descriptive summaries | `analysis/history-pilot-*.json`, `analysis/history-canary-llama31-*.json`, `analysis/family-canary-v1.md` |
| Panel illustration and its limitations | `analysis/panel-simulation-config-v1.json`, `analysis/panel-operating-characteristics-v1.json`, `analysis/panel-operating-characteristics-v1.md` |
| Independent recomputation | `audits/independent-reproduction.md` |
| AI assistance | `AI_ASSISTANCE.md` |
| Direct monetary cost | `COSTS.md` |

## C. Preserved exclusions

- Model weights are intentionally excluded and must not be redistributed from this repository.
- No private or restricted dataset, human-subject record, API credential, or paid-provider response is part of the artifact.
- The Llama targets overlap Qwen targets and are not an independent replication.
- Exact tests, target bootstraps, and the panel compound diagnostic are descriptive; they do not support population, interaction, equivalence, or sample-size inference.
- `tmp/` contains local render intermediates and is excluded from releases.

## D. Release-time verification

For every public tag, rerun `make verify`, rebuild and visually inspect the PDF, scan tracked files for credentials and oversized binaries, verify every external link and bibliographic field, confirm the repository URL in `CITATION.cff`, and record the exact release commit and artifact hashes.
