# Local compute feasibility snapshot

Captured: 2026-07-17

## Available machine

- MacBook Pro (MacBookPro18,1)
- Apple M1 Pro, 10 CPU cores
- 16 GB unified memory
- macOS 15.7.7, arm64
- Approximately 34 GiB free disk space at capture time
- Python 3.14.6 and `uv` installed
- Ollama not installed

## Implications

- Data generation, exact solvers, statistical analysis, tests, and most benchmark infrastructure are comfortably feasible locally.
- Small quantized open models are feasible, but a broad modern-model comparison is not realistically supported by this machine alone.
- Disk space is a binding constraint for multiple local checkpoints; model downloads should be minimal and documented.
- The final protocol should separate a no-cost smoke-test tier from the confirmatory model matrix.
- Any paid API or cloud-compute plan remains approval-gated. Until approval, implementation should use fixtures, deterministic mock providers, and at most lawful no-cost public models.
- Python 3.14 may be ahead of support for some ML packages; the selected project should pin a compatible interpreter (likely 3.11 or 3.12) through `uv` rather than assume the system Python.
