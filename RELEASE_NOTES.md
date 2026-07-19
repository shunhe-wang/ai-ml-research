# v0.1.0

**Status:** public working technical report; not peer reviewed

## What this release contains

- the 11-page working technical report *Before Measuring Context Carryover*;
- two executable synthetic rule worlds with structurally different deterministic solvers;
- native-template token-matching and strict response/task-validity checks;
- immutable local run manifests, exact prompts and raw responses, hashes, retry ancestry, and preserved failed runs;
- descriptive Qwen and Llama calibration artifacts plus the panel-simulation stop illustration;
- independent raw-log reproduction, hostile methods review, and a primary-source novelty/posture audit;
- the claim-to-evidence appendix, AI-assistance disclosure, actual-spend record, and follow-up research roadmap.

## Scientific claim boundary

This release is a methods/resource case study and transparent pre-confirmatory stop record. It does not establish a context-carryover effect, causal mechanism, model-by-world interaction, independent replication, null or equivalence result, model-family comparison, or confirmatory sample-size requirement. The Llama targets overlap a Qwen subset, and the executed positive-negative histories change multiple features together without same-target fresh and neutral controls.

## Verification checkpoint

- 59 tests passed; Ruff and mypy clean.
- Five frozen case sets and 29 runs, including one structured failed run, verified.
- At the private audited checkpoint, 292 executions, 160 provider prompts, 21 local model-artifact sets, and 20 historical source snapshots authenticated. The public one-commit export re-verifies all included cases, runs, prompts, responses, and summaries; it reports the excluded model folders and unavailable pre-import Git objects explicitly.
- Independent recomputation reproduced all six retained Qwen/Llama summaries and all audited prompt/response hashes.
- The release PDF was rebuilt from the public source, visually inspected page by page, and has SHA-256 `2087e1881cf976b0826fd916eb3c83116562b23cb8c8a138248cbe45f9fd839d`.
- A release-safety scan found no common credential/private-key pattern, personal home path, oversized release file, or model-weight symlink.

## Reproduction

```bash
uv sync
make verify
make paper
```

Python 3.12 is required. Model weights are intentionally excluded; the deterministic verification path and retained raw outputs do not require provider credentials.

## Release boundary

This GitHub release is the public v0.1.0 repository artifact. It does not create a DOI, preprint, venue submission, external outreach campaign, paid inference run, or human-subject activity.
