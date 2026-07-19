import json
from pathlib import Path

import pytest

from rule_carryover.case_set import load_case_set
from rule_carryover.cli import (
    _create_new_run_dir,
    _write_failed_manifest,
    _write_manifest,
    main,
)


def test_generate_command_writes_a_verified_balanced_case_set(tmp_path: Path) -> None:
    output = tmp_path / "benefit-cases.json"

    exit_code = main(
        [
            "generate",
            "--world",
            "benefit",
            "--schema-id",
            "cli-example",
            "--per-label",
            "3",
            "--seed",
            "17",
            "--output",
            str(output),
        ]
    )

    loaded = load_case_set(output)
    assert exit_code == 0
    assert len(loaded.items) == 6
    assert {item.decision.label for item in loaded.items} == {"APPROVE", "DENY"}

    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        main(
            [
                "generate",
                "--world",
                "benefit",
                "--schema-id",
                "cli-example",
                "--per-label",
                "3",
                "--seed",
                "17",
                "--output",
                str(output),
            ]
        )


def test_simulate_design_command_writes_operating_characteristics(tmp_path: Path) -> None:
    output = tmp_path / "design.json"

    exit_code = main(
        [
            "simulate-design",
            "--targets",
            "80",
            "120",
            "--effects",
            "0",
            "0.05",
            "--couplings",
            "0.5",
            "--replications",
            "20",
            "--seed",
            "19",
            "--output",
            str(output),
        ]
    )

    payload = json.loads(output.read_text())
    assert exit_code == 0
    assert len(payload["results"]) == 4
    assert payload["config"]["replications"] == 20


def test_simulate_panel_design_command_reads_named_scenarios(tmp_path: Path) -> None:
    config = tmp_path / "panel-config.json"
    output = tmp_path / "panel-results.json"
    config.write_text(
        json.dumps(
            {
                "targets_per_cell": [40, 80],
                "replications": 20,
                "seed": 29,
                "scenarios": [
                    {
                        "name": "homogeneous",
                        "discordance_probabilities": [0.1, 0.1],
                        "directional_risk_differences": [0.05, 0.05],
                    }
                ],
            }
        )
    )

    exit_code = main(
        [
            "simulate-panel-design",
            "--config",
            str(config),
            "--output",
            str(output),
        ]
    )

    payload = json.loads(output.read_text())
    assert exit_code == 0
    assert payload["config"] == json.loads(config.read_text())
    assert [result["targets_per_cell"] for result in payload["results"]] == [40, 80]
    assert {result["scenario"] for result in payload["results"]} == {"homogeneous"}


def test_generate_command_accepts_explicit_schema_parameters(tmp_path: Path) -> None:
    output = tmp_path / "permit-custom.json"

    main(
        [
            "generate",
            "--world",
            "permit",
            "--schema-id",
            "permit-custom",
            "--minimum-safety-score",
            "600",
            "--per-label",
            "2",
            "--seed",
            "29",
            "--output",
            str(output),
        ]
    )

    loaded = load_case_set(output)
    assert loaded.schema.parameters["minimum_safety_score"] == 600


def test_run_directory_creation_is_immutable(tmp_path: Path) -> None:
    run_dir = tmp_path / "run-1"

    _create_new_run_dir(run_dir)

    with pytest.raises(FileExistsError):
        _create_new_run_dir(run_dir)


def test_manifest_records_running_state_before_atomic_completion(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"

    _write_manifest(manifest_path, {"status": "running", "run_id": "run-1"})
    assert json.loads(manifest_path.read_text())["status"] == "running"

    _write_manifest(manifest_path, {"status": "completed", "run_id": "run-1"})
    assert json.loads(manifest_path.read_text())["status"] == "completed"
    assert not (tmp_path / ".manifest.json.tmp").exists()


def test_failed_manifest_preserves_base_and_structured_error(tmp_path: Path) -> None:
    manifest_path = tmp_path / "manifest.json"
    base = {"status": "running", "run_id": "run-1", "started_at": "earlier"}

    _write_failed_manifest(
        manifest_path,
        base,
        stage="baseline_execution",
        error=ValueError("adapter rejected roles"),
    )

    payload = json.loads(manifest_path.read_text())
    assert payload["status"] == "failed"
    assert payload["run_id"] == "run-1"
    assert payload["started_at"] == "earlier"
    assert payload["failed_at"]
    assert payload["failure"] == {
        "stage": "baseline_execution",
        "type": "ValueError",
        "message": "adapter rejected roles",
    }
