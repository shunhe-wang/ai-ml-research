import json
import shutil
from pathlib import Path

import pytest

from rule_carryover.artifact_verify import verify_repository_artifacts
from rule_carryover.case_set import load_case_set


def test_committed_case_sets_and_run_artifacts_verify() -> None:
    summary = verify_repository_artifacts(Path.cwd())

    assert summary.case_sets_verified == 5
    assert summary.runs_verified >= 7
    assert summary.executions_verified >= 120
    assert summary.model_artifact_sets_declared >= 1
    assert summary.model_artifact_sets_verified == 0
    assert summary.model_artifact_sets_unavailable == summary.model_artifact_sets_declared
    assert summary.source_snapshots_declared >= 1
    assert summary.source_snapshots_verified == 0
    assert summary.source_snapshots_unavailable == summary.source_snapshots_declared


def test_verifier_can_require_external_artifacts() -> None:
    with pytest.raises(ValueError, match="model artifacts unavailable"):
        verify_repository_artifacts(Path.cwd(), require_external_artifacts=True)


def _copy_run_fixture(tmp_path: Path, run_name: str) -> Path:
    shutil.copytree(Path.cwd() / "data", tmp_path / "data")
    (tmp_path / "runs").mkdir()
    run_dir = tmp_path / "runs" / run_name
    shutil.copytree(Path.cwd() / "runs" / run_name, run_dir)
    return run_dir


def test_verifier_rejects_tampered_provider_prompt_hash(tmp_path: Path) -> None:
    run_dir = _copy_run_fixture(tmp_path, "smoke-qwen35-4b-benefit-promptfix-20260717")
    records = [
        json.loads(line) for line in (run_dir / "executions.jsonl").read_text().splitlines()
    ]
    records[0]["record"]["provider_prompt"] = "tampered prompt"
    records[0]["record"]["provider_prompt_hash"] = "bad"
    (run_dir / "executions.jsonl").write_text(
        "\n".join(json.dumps(record) for record in records) + "\n"
    )

    with pytest.raises(ValueError, match="provider prompt hash mismatch"):
        verify_repository_artifacts(tmp_path)


def test_verifier_rejects_tampered_causal_summary_and_retry_parent(tmp_path: Path) -> None:
    run_dir = _copy_run_fixture(
        tmp_path,
        "history-canary-qwen35-4b-benefit-a-balanced-20260717",
    )
    manifest = json.loads((run_dir / "manifest.json").read_text())
    manifest["summary"]["directional_risk_difference_complete_case"] = 0.5
    (run_dir / "manifest.json").write_text(json.dumps(manifest))

    with pytest.raises(ValueError, match="history summary mismatch"):
        verify_repository_artifacts(tmp_path)

    manifest["summary"].pop("directional_risk_difference_complete_case")
    (run_dir / "manifest.json").write_text(json.dumps(manifest))
    records = [
        json.loads(line) for line in (run_dir / "executions.jsonl").read_text().splitlines()
    ]
    records[0]["parent_attempt_id"] = "invented-parent"
    (run_dir / "executions.jsonl").write_text(
        "\n".join(json.dumps(record) for record in records) + "\n"
    )

    with pytest.raises(ValueError, match="first attempt has a parent"):
        verify_repository_artifacts(tmp_path)


def test_verifier_rejects_manifestless_or_running_run_directories(tmp_path: Path) -> None:
    shutil.copytree(Path.cwd() / "data", tmp_path / "data")
    run_dir = tmp_path / "runs" / "interrupted"
    run_dir.mkdir(parents=True)

    with pytest.raises(ValueError, match="run directory has no manifest"):
        verify_repository_artifacts(tmp_path)

    (run_dir / "manifest.json").write_text('{"status":"running"}\n')
    with pytest.raises(ValueError, match="run is incomplete"):
        verify_repository_artifacts(tmp_path)


def test_verifier_accepts_explicit_failed_run_without_executions(tmp_path: Path) -> None:
    shutil.copytree(Path.cwd() / "data", tmp_path / "data")
    run_dir = tmp_path / "runs" / "adapter-failure"
    run_dir.mkdir(parents=True)
    case_set_path = Path("data/pilot/benefit-b.json")
    case_set = load_case_set(tmp_path / case_set_path)
    manifest = {
        "run_id": "adapter-failure",
        "status": "failed",
        "failed_at": "2026-07-17T00:00:01+00:00",
        "failure": {
            "stage": "baseline_execution",
            "type": "TemplateError",
            "message": "Conversation roles must alternate",
        },
        "case_set_path": str(case_set_path),
        "case_set_hash": case_set.case_set_hash,
        "git_dirty_at_start": True,
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest) + "\n")

    summary = verify_repository_artifacts(tmp_path)

    assert summary.runs_verified == 1
    assert summary.failed_runs_verified == 1
    assert summary.executions_verified == 0
