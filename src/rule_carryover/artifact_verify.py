from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast

from rule_carryover.case_set import load_case_set
from rule_carryover.domain import Decision
from rule_carryover.provenance import directory_file_hashes, git_source_snapshot
from rule_carryover.scoring import score_response


@dataclass(frozen=True)
class ArtifactVerificationSummary:
    case_sets_verified: int
    runs_verified: int
    failed_runs_verified: int
    executions_verified: int
    provider_prompts_verified: int
    model_artifact_sets_declared: int
    model_artifact_sets_verified: int
    model_artifact_sets_unavailable: int
    source_snapshots_declared: int
    source_snapshots_verified: int
    source_snapshots_unavailable: int


@dataclass(frozen=True)
class _RunVerification:
    executions_verified: int
    provider_prompts_verified: int
    model_artifact_sets_declared: int
    model_artifact_sets_verified: int
    model_artifact_sets_unavailable: int
    source_snapshots_declared: int
    source_snapshots_verified: int
    source_snapshots_unavailable: int
    failed_runs_verified: int


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _request_hash(payload: dict[str, Any], decoding: dict[str, Any]) -> str:
    record = cast(dict[str, Any], payload["record"])
    request = cast(dict[str, Any], payload["request"])
    canonical = {
        "provider": record["provider_name"],
        "model_id": record["model_id"],
        "request": {
            "system": request["system"],
            "messages": request["messages"],
        },
        "decoding": decoding,
    }
    text = json.dumps(canonical, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return _sha256(text)


def _gold(payload: dict[str, Any]) -> Decision:
    raw = cast(dict[str, Any], payload["gold"])
    return Decision(
        label=cast(Any, raw["label"]),
        rule_id=str(raw["rule_id"]),
        margin=int(raw["margin"]),
        trace=tuple(str(item) for item in cast(list[Any], raw["trace"])),
    )


def _git_commit_available(root: Path, commit: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=root,
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def _verify_run(
    run_dir: Path,
    root: Path,
    *,
    require_external_artifacts: bool,
) -> _RunVerification:
    manifest = cast(
        dict[str, Any], json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    )
    status = manifest.get("status")
    if status == "running":
        raise ValueError(f"run is incomplete: {run_dir}")
    failed = status == "failed"
    if failed:
        failure = manifest.get("failure")
        if not isinstance(failure, dict) or not all(
            isinstance(failure.get(key), str) and failure[key]
            for key in ("stage", "type", "message")
        ):
            raise ValueError(f"failed run has invalid failure metadata: {run_dir}")
        if not isinstance(manifest.get("failed_at"), str):
            raise ValueError(f"failed run has no failure timestamp: {run_dir}")

    model_artifact_sets_declared = 0
    model_artifact_sets_verified = 0
    model_artifact_sets_unavailable = 0
    artifact_hashes = manifest.get("model_artifact_sha256")
    if artifact_hashes is not None:
        model_artifact_sets_declared = 1
        model_path = root / str(manifest["model_path"])
        if not model_path.is_dir():
            if require_external_artifacts:
                raise ValueError(f"model artifacts unavailable for verification: {model_path}")
            model_artifact_sets_unavailable = 1
        else:
            if directory_file_hashes(model_path) != artifact_hashes:
                raise ValueError(f"model artifact hash mismatch: {run_dir}")
            model_artifact_sets_verified = 1

    source_snapshots_declared = 0
    source_snapshots_verified = 0
    source_snapshots_unavailable = 0
    source_dirty = manifest.get("source_dirty_at_start", manifest.get("git_dirty_at_start"))
    if source_dirty is False:
        source_snapshots_declared = 1
        paths = tuple(str(path) for path in manifest["source_snapshot_paths"])
        commit = str(manifest["git_commit"])
        if not _git_commit_available(root, commit):
            if require_external_artifacts:
                raise ValueError(f"source snapshot Git object unavailable: {commit}")
            source_snapshots_unavailable = 1
        else:
            snapshot = git_source_snapshot(root, commit, paths)
            if snapshot.sha256 != manifest["source_snapshot_sha256"]:
                raise ValueError(f"source snapshot hash mismatch: {run_dir}")
            source_snapshots_verified = 1

    execution_path = run_dir / "executions.jsonl"
    lines = (
        execution_path.read_text(encoding="utf-8").splitlines()
        if execution_path.is_file()
        else []
    )
    records = [cast(dict[str, Any], json.loads(line)) for line in lines if line.strip()]

    case_set_path = root / str(manifest["case_set_path"])
    case_set = load_case_set(case_set_path)
    if case_set.case_set_hash != manifest["case_set_hash"]:
        raise ValueError(f"manifest case-set hash mismatch: {run_dir}")

    if not records:
        if not failed:
            raise ValueError(f"run has no executions: {run_dir}")
        return _RunVerification(
            executions_verified=0,
            provider_prompts_verified=0,
            model_artifact_sets_declared=model_artifact_sets_declared,
            model_artifact_sets_verified=model_artifact_sets_verified,
            model_artifact_sets_unavailable=model_artifact_sets_unavailable,
            source_snapshots_declared=source_snapshots_declared,
            source_snapshots_verified=source_snapshots_verified,
            source_snapshots_unavailable=source_snapshots_unavailable,
            failed_runs_verified=1,
        )
    run_id = str(manifest["run_id"])
    if any(str(record["run_id"]) != run_id for record in records):
        raise ValueError(f"run ID mismatch: {run_dir}")
    attempt_ids = [str(record["attempt_id"]) for record in records]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise ValueError(f"duplicate attempt IDs: {run_dir}")

    decoding = cast(dict[str, Any], manifest["decoding"])
    counts = {
        "schema_valid": 0,
        "decision_correct": 0,
        "rule_correct": 0,
        "margin_correct": 0,
        "exact_correct": 0,
        "refusals": 0,
        "transport_errors": 0,
    }
    arms: dict[str, dict[str, str]] = {}
    provider_prompts_verified = 0
    by_cell: dict[str, list[dict[str, Any]]] = {}
    for payload in records:
        by_cell.setdefault(str(payload["cell_id"]), []).append(payload)
        stored = cast(dict[str, Any], payload["record"])
        if "latency_ms" in stored and (
            float(stored["latency_ms"]) < 0
            or str(stored["started_at"]) > str(stored["completed_at"])
        ):
            raise ValueError(f"invalid call timing in {run_dir}")
        if stored["request_hash"] != _request_hash(payload, decoding):
            raise ValueError(f"request hash mismatch in {run_dir}")
        provider_prompt = stored.get("provider_prompt")
        provider_prompt_hash = stored.get("provider_prompt_hash")
        if provider_prompt is not None:
            if provider_prompt_hash != _sha256(str(provider_prompt)):
                raise ValueError(f"provider prompt hash mismatch in {run_dir}")
            provider_prompts_verified += 1
        elif provider_prompt_hash is not None:
            raise ValueError(f"provider prompt bytes missing in {run_dir}")
        raw = stored["raw_response"]
        if raw is None:
            if stored["transport_error"] is None or stored["score"] is not None:
                raise ValueError(f"invalid transport record in {run_dir}")
            counts["transport_errors"] += 1
            continue
        if stored["response_hash"] != _sha256(str(raw)):
            raise ValueError(f"response hash mismatch in {run_dir}")
        score = score_response(str(raw), _gold(payload))
        if stored["score"] != asdict(score):
            raise ValueError(f"stored score mismatch in {run_dir}")
        counts["schema_valid"] += int(score.schema_valid)
        counts["decision_correct"] += int(score.decision_correct)
        counts["rule_correct"] += int(score.rule_correct)
        counts["margin_correct"] += int(score.margin_correct)
        counts["exact_correct"] += int(
            score.decision_correct and score.rule_correct and score.margin_correct
        )
        counts["refusals"] += int(score.refusal)
        parts = str(payload["cell_id"]).split("|")
        if (
            len(parts) >= 4
            and parts[-2] in {"positive", "negative"}
            and score.parsed_decision is not None
        ):
            arms.setdefault(parts[0], {})[parts[-2]] = score.parsed_decision

    unresolved_cells = 0
    max_retries = int(cast(dict[str, Any], manifest.get("retry_policy", {})).get("max_retries", 0))
    for cell_id, attempts in by_cell.items():
        if len(attempts) > max_retries + 1:
            raise ValueError(f"retry cap exceeded for {cell_id}: {run_dir}")
        for index, attempt in enumerate(attempts):
            parent = attempt["parent_attempt_id"]
            if index == 0:
                if parent is not None:
                    raise ValueError(f"first attempt has a parent for {cell_id}: {run_dir}")
                continue
            previous = attempts[index - 1]
            previous_record = cast(dict[str, Any], previous["record"])
            if parent != previous["attempt_id"]:
                raise ValueError(f"broken retry ancestry for {cell_id}: {run_dir}")
            if previous_record["transport_error"] is None:
                raise ValueError(f"retry follows a completed response for {cell_id}: {run_dir}")
            if cast(dict[str, Any], attempt["record"])["request_hash"] != previous_record[
                "request_hash"
            ]:
                raise ValueError(f"retry request changed for {cell_id}: {run_dir}")
        final_record = cast(dict[str, Any], attempts[-1]["record"])
        unresolved_cells += int(final_record["transport_error"] is not None)

    if failed:
        return _RunVerification(
            executions_verified=len(records),
            provider_prompts_verified=provider_prompts_verified,
            model_artifact_sets_declared=model_artifact_sets_declared,
            model_artifact_sets_verified=model_artifact_sets_verified,
            model_artifact_sets_unavailable=model_artifact_sets_unavailable,
            source_snapshots_declared=source_snapshots_declared,
            source_snapshots_verified=source_snapshots_verified,
            source_snapshots_unavailable=source_snapshots_unavailable,
            failed_runs_verified=1,
        )

    summary = cast(dict[str, Any], manifest["summary"])
    expected_size_key = "attempts" if "attempts" in summary else (
        "executions" if "executions" in summary else "total"
    )
    if int(summary[expected_size_key]) != len(records):
        raise ValueError(f"execution count mismatch: {run_dir}")
    if "executions" in summary:
        unique_cells = len({str(record["cell_id"]) for record in records})
        if int(summary["executions"]) != unique_cells:
            raise ValueError(f"treatment-cell count mismatch: {run_dir}")
    for key, value in counts.items():
        if key in summary and int(summary[key]) != value:
            raise ValueError(f"summary mismatch for {key}: {run_dir}")
    unresolved_key = (
        "unresolved_transport_executions"
        if "unresolved_transport_executions" in summary
        else "unresolved_transport_targets"
    )
    if unresolved_key in summary and int(summary[unresolved_key]) != unresolved_cells:
        raise ValueError(f"summary mismatch for {unresolved_key}: {run_dir}")

    if "targets" in summary:
        targets = len({str(record["cell_id"]).split("|")[0] for record in records})
        paired = [values for values in arms.values() if set(values) == {"positive", "negative"}]
        positive_approvals = sum(
            values.get("positive") == "APPROVE" for values in arms.values()
        )
        negative_approvals = sum(
            values.get("negative") == "APPROVE" for values in arms.values()
        )
        history_counts: dict[str, int | float] = {
            "targets": targets,
            "paired_valid": len(paired),
            "positive_approvals": positive_approvals,
            "negative_approvals": negative_approvals,
        }
        if paired:
            complete_case = sum(
                int(values["positive"] == "APPROVE")
                - int(values["negative"] == "APPROVE")
                for values in paired
            ) / len(paired)
            history_counts["directional_risk_difference"] = complete_case
            history_counts["directional_risk_difference_complete_case"] = complete_case
        positive_observed = sum("positive" in values for values in arms.values())
        negative_observed = sum("negative" in values for values in arms.values())
        history_counts["directional_risk_difference_lower_bound"] = (
            positive_approvals / targets
            - (negative_approvals + targets - negative_observed) / targets
        )
        history_counts["directional_risk_difference_upper_bound"] = (
            (positive_approvals + targets - positive_observed) / targets
            - negative_approvals / targets
        )
        for key, history_value in history_counts.items():
            if key in summary and summary[key] != history_value:
                raise ValueError(f"history summary mismatch for {key}: {run_dir}")
    return _RunVerification(
        executions_verified=len(records),
        provider_prompts_verified=provider_prompts_verified,
        model_artifact_sets_declared=model_artifact_sets_declared,
        model_artifact_sets_verified=model_artifact_sets_verified,
        model_artifact_sets_unavailable=model_artifact_sets_unavailable,
        source_snapshots_declared=source_snapshots_declared,
        source_snapshots_verified=source_snapshots_verified,
        source_snapshots_unavailable=source_snapshots_unavailable,
        failed_runs_verified=0,
    )


def verify_repository_artifacts(
    root: Path,
    *,
    require_external_artifacts: bool = False,
) -> ArtifactVerificationSummary:
    case_paths = sorted((root / "data" / "pilot").glob("*.json"))
    for path in case_paths:
        load_case_set(path)
    run_dirs = sorted(path for path in (root / "runs").iterdir() if path.is_dir())
    for run_dir in run_dirs:
        if not (run_dir / "manifest.json").is_file():
            raise ValueError(f"run directory has no manifest: {run_dir}")
    verified = [
        _verify_run(
            run_dir,
            root,
            require_external_artifacts=require_external_artifacts,
        )
        for run_dir in run_dirs
    ]
    return ArtifactVerificationSummary(
        case_sets_verified=len(case_paths),
        runs_verified=len(run_dirs),
        failed_runs_verified=sum(item.failed_runs_verified for item in verified),
        executions_verified=sum(item.executions_verified for item in verified),
        provider_prompts_verified=sum(item.provider_prompts_verified for item in verified),
        model_artifact_sets_declared=sum(
            item.model_artifact_sets_declared for item in verified
        ),
        model_artifact_sets_verified=sum(
            item.model_artifact_sets_verified for item in verified
        ),
        model_artifact_sets_unavailable=sum(
            item.model_artifact_sets_unavailable for item in verified
        ),
        source_snapshots_declared=sum(item.source_snapshots_declared for item in verified),
        source_snapshots_verified=sum(item.source_snapshots_verified for item in verified),
        source_snapshots_unavailable=sum(
            item.source_snapshots_unavailable for item in verified
        ),
    )
