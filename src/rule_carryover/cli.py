from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from rule_carryover.case_set import freeze_case_set, load_case_set, write_case_set
from rule_carryover.domain import RuleSchema, World
from rule_carryover.generation import generate_balanced_cases
from rule_carryover.histories import (
    build_directional_history_bank,
    history_bank_hash,
    pair_is_naturally_token_matched,
)
from rule_carryover.history_analysis import analyze_history_logs
from rule_carryover.history_smoke import run_directional_history_smoke
from rule_carryover.local_smoke import run_fresh_baseline
from rule_carryover.mlx_provider import MlxLmProvider
from rule_carryover.pairs import fact_signature, generate_counterfactual_pairs
from rule_carryover.provenance import (
    directory_file_hashes,
    git_is_dirty,
    git_paths_are_dirty,
    source_snapshot,
)
from rule_carryover.rendering import Channel
from rule_carryover.simulation import (
    evaluate_design,
    evaluate_discordance_design,
    evaluate_panel_design,
)


def _default_schema(world: World, schema_id: str) -> RuleSchema:
    if world == "benefit":
        return RuleSchema.benefit(
            schema_id=schema_id,
            income_ceiling=2_000,
            residency_months=12,
            caregiver_income_extension=300,
            caregiver_residency_reduction=2,
        )
    return RuleSchema.permit(schema_id=schema_id, minimum_safety_score=500)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="carryover")
    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="generate a dual-solver-verified case set")
    generate.add_argument("--world", choices=("benefit", "permit"), required=True)
    generate.add_argument("--schema-id", required=True)
    generate.add_argument("--per-label", type=int, required=True)
    generate.add_argument("--seed", type=int, required=True)
    generate.add_argument("--output", type=Path, required=True)
    generate.add_argument("--income-ceiling", type=int)
    generate.add_argument("--residency-months", type=int)
    generate.add_argument("--caregiver-income-extension", type=int)
    generate.add_argument("--caregiver-residency-reduction", type=int)
    generate.add_argument("--minimum-safety-score", type=int)

    simulate = subparsers.add_parser(
        "simulate-design", help="simulate paired-analysis operating characteristics"
    )
    simulate.add_argument("--targets", type=int, nargs="+", required=True)
    simulate.add_argument("--effects", type=float, nargs="+", required=True)
    simulate.add_argument("--couplings", type=float, nargs="+", required=True)
    simulate.add_argument("--baseline", type=float, default=0.50)
    simulate.add_argument("--replications", type=int, required=True)
    simulate.add_argument("--seed", type=int, required=True)
    simulate.add_argument("--output", type=Path, required=True)

    discordance = subparsers.add_parser(
        "simulate-discordance-design",
        help="simulate exact paired-test operating characteristics from discordance",
    )
    discordance.add_argument("--targets", type=int, nargs="+", required=True)
    discordance.add_argument("--discordances", type=float, nargs="+", required=True)
    discordance.add_argument("--effects", type=float, nargs="+", required=True)
    discordance.add_argument("--replications", type=int, required=True)
    discordance.add_argument("--seed", type=int, required=True)
    discordance.add_argument("--output", type=Path, required=True)

    panel = subparsers.add_parser(
        "simulate-panel-design",
        help="simulate pooled and sign-stable behavior across fixed model/world cells",
    )
    panel.add_argument("--config", type=Path, required=True)
    panel.add_argument("--output", type=Path, required=True)

    local = subparsers.add_parser(
        "local-baseline", help="run a non-confirmatory fresh-context MLX baseline"
    )
    local.add_argument("--case-set", type=Path, required=True)
    local.add_argument("--model-path", type=Path, required=True)
    local.add_argument("--model-id", required=True)
    local.add_argument("--model-revision", required=True)
    local.add_argument("--run-id", required=True)
    local.add_argument("--output-dir", type=Path, required=True)
    local.add_argument("--limit", type=int)
    local.add_argument("--max-tokens", type=int, default=128)
    local.add_argument("--max-transport-retries", type=int, default=1)

    history = subparsers.add_parser(
        "local-history-smoke",
        help="run a non-confirmatory token-matched directional-history smoke",
    )
    history.add_argument("--case-set", type=Path, required=True)
    history.add_argument("--model-path", type=Path, required=True)
    history.add_argument("--model-id", required=True)
    history.add_argument("--model-revision", required=True)
    history.add_argument("--run-id", required=True)
    history.add_argument("--output-dir", type=Path, required=True)
    history.add_argument("--pair-count", type=int, required=True)
    history.add_argument("--history-sets", type=int, required=True)
    history.add_argument("--horizon", type=int, required=True)
    history.add_argument("--pair-seed", type=int, required=True)
    history.add_argument("--history-seed", type=int, required=True)
    history.add_argument("--schedule-seed", type=int, required=True)
    history.add_argument(
        "--channel",
        choices=(Channel.GOLD_LABEL.value, Channel.OUTCOME_CODE.value),
        default=Channel.GOLD_LABEL.value,
    )
    history.add_argument("--limit", type=int)
    history.add_argument("--max-tokens", type=int, default=64)
    history.add_argument("--max-transport-retries", type=int, default=1)

    analyze = subparsers.add_parser(
        "analyze-history", help="analyze one paired directional-history execution log"
    )
    analyze.add_argument("--executions", type=Path, nargs="+", required=True)
    analyze.add_argument("--bootstrap-replications", type=int, required=True)
    analyze.add_argument("--seed", type=int, required=True)
    analyze.add_argument("--output", type=Path, required=True)
    return parser


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _git_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
    ).strip()


def _create_new_run_dir(path: Path) -> None:
    """Reserve one immutable run directory; never resume or overwrite implicitly."""
    path.mkdir(parents=True, exist_ok=False)


def _write_manifest(path: Path, payload: dict[str, object]) -> None:
    """Atomically publish either the running or completed state."""
    temporary = path.with_name(f".{path.name}.tmp")
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)


def _write_failed_manifest(
    path: Path,
    manifest_base: dict[str, object],
    *,
    stage: str,
    error: Exception,
) -> None:
    """Finalize a reserved run as failed without discarding its provenance."""
    failed = manifest_base | {
        "status": "failed",
        "failed_at": datetime.now(UTC).isoformat(),
        "failure": {
            "stage": stage,
            "type": type(error).__name__,
            "message": str(error),
        },
    }
    _write_manifest(path, failed)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "generate":
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite frozen case set: {args.output}")
        world: World = args.world
        default = _default_schema(world, args.schema_id)
        if world == "benefit":
            schema = RuleSchema.benefit(
                schema_id=args.schema_id,
                income_ceiling=args.income_ceiling
                if args.income_ceiling is not None
                else default.parameters["income_ceiling"],
                residency_months=args.residency_months
                if args.residency_months is not None
                else default.parameters["residency_months"],
                caregiver_income_extension=args.caregiver_income_extension
                if args.caregiver_income_extension is not None
                else default.parameters["caregiver_income_extension"],
                caregiver_residency_reduction=args.caregiver_residency_reduction
                if args.caregiver_residency_reduction is not None
                else default.parameters["caregiver_residency_reduction"],
            )
        else:
            schema = RuleSchema.permit(
                schema_id=args.schema_id,
                minimum_safety_score=args.minimum_safety_score
                if args.minimum_safety_score is not None
                else default.parameters["minimum_safety_score"],
            )
        cases = generate_balanced_cases(schema, per_label=args.per_label, seed=args.seed)
        frozen = freeze_case_set(schema, cases)
        write_case_set(args.output, frozen)
        print(f"wrote {len(frozen.items)} cases; sha256={frozen.case_set_hash}")
        return 0
    if args.command == "simulate-design":
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite design simulation: {args.output}")
        results = []
        index = 0
        for targets in args.targets:
            for effect in args.effects:
                for coupling in args.couplings:
                    result = evaluate_design(
                        targets=targets,
                        negative_history_probability=args.baseline,
                        directional_risk_difference=effect,
                        pair_coupling=coupling,
                        replications=args.replications,
                        seed=args.seed + index,
                    )
                    results.append(asdict(result))
                    index += 1
        payload = {
            "config": {
                "baseline": args.baseline,
                "replications": args.replications,
                "seed": args.seed,
            },
            "results": results,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"wrote {len(results)} design cells to {args.output}")
        return 0
    if args.command == "analyze-history":
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite history analysis: {args.output}")
        analysis_result = analyze_history_logs(
            args.executions,
            bootstrap_replications=args.bootstrap_replications,
            seed=args.seed,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(asdict(analysis_result), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(asdict(analysis_result), sort_keys=True))
        return 0
    if args.command == "simulate-discordance-design":
        if args.output.exists():
            raise FileExistsError(
                f"refusing to overwrite discordance simulation: {args.output}"
            )
        results = []
        index = 0
        for targets in args.targets:
            for discordance in args.discordances:
                for effect in args.effects:
                    if abs(effect) > discordance:
                        continue
                    discordance_result = evaluate_discordance_design(
                        targets=targets,
                        discordance_probability=discordance,
                        directional_risk_difference=effect,
                        replications=args.replications,
                        seed=args.seed + index,
                    )
                    results.append(asdict(discordance_result))
                    index += 1
        payload = {
            "config": {"replications": args.replications, "seed": args.seed},
            "results": results,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"wrote {len(results)} discordance design cells to {args.output}")
        return 0
    if args.command == "simulate-panel-design":
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite panel simulation: {args.output}")
        config = cast(
            dict[str, Any], json.loads(args.config.read_text(encoding="utf-8"))
        )
        targets_per_cell = cast(list[int], config["targets_per_cell"])
        scenarios = cast(list[dict[str, Any]], config["scenarios"])
        replications = int(config["replications"])
        seed = int(config["seed"])
        results = []
        index = 0
        for targets in targets_per_cell:
            for scenario in scenarios:
                panel_result = evaluate_panel_design(
                    targets_per_cell=int(targets),
                    discordance_probabilities=tuple(
                        float(value)
                        for value in cast(
                            list[float], scenario["discordance_probabilities"]
                        )
                    ),
                    directional_risk_differences=tuple(
                        float(value)
                        for value in cast(
                            list[float], scenario["directional_risk_differences"]
                        )
                    ),
                    replications=replications,
                    seed=seed + index,
                )
                results.append({"scenario": str(scenario["name"])} | asdict(panel_result))
                index += 1
        payload = {"config": config, "results": results}
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"wrote {len(results)} panel design cells to {args.output}")
        return 0
    if args.command == "local-baseline":
        started_at = datetime.now(UTC).isoformat()
        project_root = Path.cwd()
        source = source_snapshot(project_root)
        git_dirty_at_start = git_is_dirty(project_root)
        source_dirty_at_start = git_paths_are_dirty(project_root, source.paths)
        model_artifacts = directory_file_hashes(args.model_path)
        case_set = load_case_set(args.case_set)
        provider = MlxLmProvider.from_path(str(args.model_path))
        weights_path = args.model_path / "model.safetensors"
        manifest_base: dict[str, object] = {
            "run_id": args.run_id,
            "status": "running",
            "evidence_class": "local-smoke-not-confirmatory",
            "started_at": started_at,
            "git_commit": _git_commit(),
            "git_dirty_at_start": git_dirty_at_start,
            "source_dirty_at_start": source_dirty_at_start,
            "source_snapshot_sha256": source.sha256,
            "source_snapshot_paths": list(source.paths),
            "case_set_path": str(args.case_set),
            "case_set_hash": case_set.case_set_hash,
            "model_id": args.model_id,
            "model_revision": args.model_revision,
            "model_revision_provenance": "operator-supplied; artifact contents hashed below",
            "model_weight_sha256": _file_sha256(weights_path),
            "model_artifact_sha256": model_artifacts,
            "model_path": str(args.model_path),
            "runtime": {
                "machine": platform.machine(),
                "python": sys.version,
                "mlx": importlib.metadata.version("mlx"),
                "mlx_lm": importlib.metadata.version("mlx-lm"),
            },
            "decoding": {"temperature": 0, "max_tokens": args.max_tokens},
            "retry_policy": {
                "transport_only": True,
                "max_retries": args.max_transport_retries,
                "identical_request": True,
            },
            "limit": args.limit,
        }
        _create_new_run_dir(args.output_dir)
        _write_manifest(args.output_dir / "manifest.json", manifest_base)
        try:
            baseline_summary = run_fresh_baseline(
                case_set=case_set,
                provider=provider,
                provider_name="mlx-lm",
                model_id=args.model_id,
                run_id=args.run_id,
                log_path=args.output_dir / "executions.jsonl",
                max_tokens=args.max_tokens,
                limit=args.limit,
                max_transport_retries=args.max_transport_retries,
            )
        except Exception as error:
            _write_failed_manifest(
                args.output_dir / "manifest.json",
                manifest_base,
                stage="baseline_execution",
                error=error,
            )
            raise
        manifest = manifest_base | {
            "status": "completed",
            "completed_at": datetime.now(UTC).isoformat(),
            "summary": asdict(baseline_summary),
        }
        _write_manifest(args.output_dir / "manifest.json", manifest)
        print(json.dumps(asdict(baseline_summary), sort_keys=True))
        return 0
    if args.command == "local-history-smoke":
        started_at = datetime.now(UTC).isoformat()
        project_root = Path.cwd()
        source = source_snapshot(project_root)
        git_dirty_at_start = git_is_dirty(project_root)
        source_dirty_at_start = git_paths_are_dirty(project_root, source.paths)
        model_artifacts = directory_file_hashes(args.model_path)
        case_set = load_case_set(args.case_set)
        provider = MlxLmProvider.from_path(str(args.model_path))
        history_channel = Channel(args.channel)
        pairs = generate_counterfactual_pairs(
            case_set.schema,
            count=args.pair_count,
            seed=args.pair_seed,
            excluded_fact_signatures={
                fact_signature(item.case) for item in case_set.items
            },
            pair_filter=lambda pair: pair_is_naturally_token_matched(
                case_set.schema,
                pair,
                provider.token_count,
                provider.request_token_count,
                channel=history_channel,
            ),
        )
        histories = build_directional_history_bank(
            case_set.schema,
            pairs,
            sets=args.history_sets,
            horizon=args.horizon,
            seed=args.history_seed,
        )
        weights_path = args.model_path / "model.safetensors"
        manifest_base = {
            "run_id": args.run_id,
            "status": "running",
            "evidence_class": "local-history-smoke-not-confirmatory",
            "started_at": started_at,
            "git_commit": _git_commit(),
            "git_dirty_at_start": git_dirty_at_start,
            "source_dirty_at_start": source_dirty_at_start,
            "source_snapshot_sha256": source.sha256,
            "source_snapshot_paths": list(source.paths),
            "case_set_path": str(args.case_set),
            "case_set_hash": case_set.case_set_hash,
            "history_bank_hash": history_bank_hash(histories),
            "history_design": {
                "pair_count": args.pair_count,
                "history_sets": args.history_sets,
                "horizon": args.horizon,
                "pair_seed": args.pair_seed,
                "history_seed": args.history_seed,
                "schedule_seed": args.schedule_seed,
                "channel": history_channel.value,
                "boundary": "full",
                "token_matcher": (
                    "natural equality under per-message tokenizer counts and full "
                    "chat-template prompt tokens; no padding"
                ),
            },
            "model_id": args.model_id,
            "model_revision": args.model_revision,
            "model_revision_provenance": "operator-supplied; artifact contents hashed below",
            "model_weight_sha256": _file_sha256(weights_path),
            "model_artifact_sha256": model_artifacts,
            "model_path": str(args.model_path),
            "runtime": {
                "machine": platform.machine(),
                "python": sys.version,
                "mlx": importlib.metadata.version("mlx"),
                "mlx_lm": importlib.metadata.version("mlx-lm"),
            },
            "decoding": {"temperature": 0, "max_tokens": args.max_tokens},
            "retry_policy": {
                "transport_only": True,
                "max_retries": args.max_transport_retries,
                "identical_request": True,
            },
            "limit": args.limit,
        }
        _create_new_run_dir(args.output_dir)
        _write_manifest(args.output_dir / "manifest.json", manifest_base)
        try:
            history_summary = run_directional_history_smoke(
                case_set=case_set,
                histories=histories,
                provider=provider,
                provider_name="mlx-lm",
                model_id=args.model_id,
                run_id=args.run_id,
                log_path=args.output_dir / "executions.jsonl",
                max_tokens=args.max_tokens,
                token_counter=provider.token_count,
                request_token_counter=provider.request_token_count,
                schedule_seed=args.schedule_seed,
                channel=history_channel,
                limit=args.limit,
                max_transport_retries=args.max_transport_retries,
            )
        except Exception as error:
            _write_failed_manifest(
                args.output_dir / "manifest.json",
                manifest_base,
                stage="history_execution",
                error=error,
            )
            raise
        manifest = manifest_base | {
            "status": "completed",
            "completed_at": datetime.now(UTC).isoformat(),
            "summary": asdict(history_summary),
        }
        _write_manifest(args.output_dir / "manifest.json", manifest)
        print(json.dumps(asdict(history_summary), sort_keys=True))
        return 0
    raise AssertionError(f"unhandled command: {args.command}")


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
